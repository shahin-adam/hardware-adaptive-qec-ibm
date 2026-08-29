"""Reference architecture as evaluated in the manuscript.

This file is provided for inspection of the model as it was run. It is NOT a
standalone entry point: it imports development modules that are not
redistributed, and training additionally requires the context-split syndromes
and per-job calibration snapshots described in the README. Running it directly
will raise ModuleNotFoundError, which is expected.

Every published number is reproduced instead from the frozen per-shot arrays by
the reproduce_*.py scripts in the repository root, which need only numpy.
"""

"""V125: manuscript-derived relational V12 residual decoder on real IBM shots.

This is a retrospective development experiment. It combines all-pair detector
attention, operation-graph and temporal biases, shot-level coactivity/change
biases, optional label-free domain drift context, multi-task supervision and
cohort-specific safety routing. No simulated labels are used.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler

from v120_neural_ensemble_selector import Domain, paired_stats, seed_all


def config_index(meta: np.ndarray) -> np.ndarray:
    basis = np.clip(np.rint(meta[:, 1]).astype(int), 0, 1)
    rounds = np.rint(meta[:, 2]).astype(int)
    ridx = np.where(rounds <= 3, 0, np.where(rounds <= 5, 1, 2))
    logical = np.clip(np.rint(meta[:, 3]).astype(int), 0, 1)
    return basis * 6 + ridx * 2 + logical


def domain_context(domain: Domain) -> np.ndarray:
    """Label-free prefix/current detector fingerprint, fixed per domain."""
    n = len(domain.x)
    cut = max(1, n // 10)
    observed = domain.x.astype(np.float32) * domain.mask
    prefix = observed[:cut].sum(0) / domain.mask[:cut].sum(0).clip(1)
    current = observed[cut:].sum(0) / domain.mask[cut:].sum(0).clip(1)
    return np.concatenate((prefix, current, current - prefix)).astype(np.float32)


class Rows(Dataset):
    def __init__(self, domains: list[Domain], basis: int, context: str):
        rows = []
        for domain in domains:
            q = domain.basis == basis
            ctx = domain_context(domain)
            if context in {"none", "zero"}:
                ctx = np.zeros_like(ctx)
            rows.append((domain.x[q], domain.mask[q], domain.meta[q], domain.y[q],
                         domain.v12[q], np.repeat(ctx[None], int(q.sum()), axis=0),
                         np.full(int(q.sum()), domain.name)))
        self.x = np.concatenate([r[0] for r in rows])
        self.mask = np.concatenate([r[1] for r in rows])
        self.meta = np.concatenate([r[2] for r in rows])
        self.y = np.concatenate([r[3] for r in rows]).astype(np.float32)
        self.v12 = np.concatenate([r[4] for r in rows]).astype(np.float32)
        self.context = np.concatenate([r[5] for r in rows])
        self.domain = np.concatenate([r[6] for r in rows])

    def __len__(self):
        return len(self.y)

    def __getitem__(self, i):
        return self.x[i], self.mask[i], self.meta[i], self.context[i], self.y[i], self.v12[i]


class RelationalBlock(nn.Module):
    def __init__(self, width=96, heads=6, dropout=.10):
        super().__init__()
        self.heads, self.dim = heads, width // heads
        self.norm1, self.norm2 = nn.LayerNorm(width), nn.LayerNorm(width)
        self.qkv = nn.Linear(width, width * 3)
        self.out = nn.Linear(width, width)
        self.ff = nn.Sequential(nn.Linear(width, width * 3), nn.GELU(), nn.Dropout(dropout),
                                nn.Linear(width * 3, width))
        self.dropout = nn.Dropout(dropout)
        self.lag_bias = nn.Embedding(8, heads)
        self.graph_weight = nn.Parameter(torch.zeros(heads))
        self.coactivity_weight = nn.Parameter(torch.zeros(heads))
        self.change_weight = nn.Parameter(torch.zeros(heads))

    def forward(self, h, mask, lag, graph, events):
        z = self.norm1(h)
        batch, nodes, width = z.shape
        q, k, v = self.qkv(z).chunk(3, -1)
        q = q.view(batch, nodes, self.heads, self.dim).transpose(1, 2)
        k = k.view(batch, nodes, self.heads, self.dim).transpose(1, 2)
        v = v.view(batch, nodes, self.heads, self.dim).transpose(1, 2)
        score = torch.matmul(q, k.transpose(-1, -2)) / math.sqrt(self.dim)
        score = score + self.lag_bias(lag).permute(0, 3, 1, 2)
        score = score + graph.unsqueeze(1) * self.graph_weight.view(1, -1, 1, 1)
        coactivity = events[:, None, :, None] * events[:, None, None, :]
        change = (events[:, None, :, None] - events[:, None, None, :]).abs()
        score = score + coactivity * self.coactivity_weight.view(1, -1, 1, 1)
        score = score + change * self.change_weight.view(1, -1, 1, 1)
        valid = mask[:, None, None, :] > .5
        score = score.masked_fill(~valid, -1e4)
        attention = torch.softmax(score, -1)
        attended = torch.matmul(attention, v).transpose(1, 2).reshape(batch, nodes, width)
        h = h + self.dropout(self.out(attended))
        h = h + self.dropout(self.ff(self.norm2(h)))
        return h * mask.unsqueeze(-1)


class ManuscriptRelationalDecoder(nn.Module):
    def __init__(self, graph_path: Path, context: str, multitask: bool, width=96, heads=6, layers=3):
        super().__init__()
        graph_data = np.load(graph_path)
        for name, key in (("incidence", "incidence"), ("dcoord", "detector_coordinates"),
                          ("opfeat", "detector_operation_features")):
            self.register_buffer(name, torch.from_numpy(graph_data[key].astype(np.float32)))
        self.context_kind, self.multitask = context, multitask
        self.token = nn.Embedding(4, width)
        self.detector_in = nn.Linear(4 + self.opfeat.shape[-1], width)
        self.meta = nn.Sequential(nn.Linear(4, width), nn.GELU(), nn.Linear(width, width))
        self.blocks = nn.ModuleList([RelationalBlock(width, heads) for _ in range(layers)])
        if context != "none":
            self.context = nn.Sequential(nn.Linear(168, 192), nn.GELU(), nn.Dropout(.10),
                                         nn.Linear(192, width * 2))
        self.final = nn.LayerNorm(width)
        self.residual_head = nn.Linear(width, 1)
        self.direct_head = nn.Linear(width, 1)
        self.risk_head = nn.Linear(width, 1)

    def forward(self, x, mask, meta, context):
        basis = meta[:, 1].round().long().clamp(0, 1)
        rounds = meta[:, 2].round().long()
        ridx = torch.where(rounds <= 3, 0, torch.where(rounds <= 5, 1, 2))
        logical = meta[:, 3].round().long().clamp(0, 1)
        cfg = basis * 6 + ridx * 2 + logical
        coords, opfeat, incidence = self.dcoord[cfg], self.opfeat[cfg], self.incidence[cfg]
        token_id = x.long() + 2 * (mask < .5).long()
        h = self.token(token_id) + self.detector_in(torch.cat((coords, opfeat), -1))
        scaled_meta = meta.clone(); scaled_meta[:, 0] /= 7; scaled_meta[:, 2] /= 7
        h = h + self.meta(scaled_meta).unsqueeze(1)
        graph = (torch.bmm(incidence, incidence.transpose(1, 2)) > 0).float()
        times = coords[:, :, 2].round().long()
        lag = (times[:, :, None] - times[:, None, :]).abs().clamp_max(7)
        for block in self.blocks:
            h = block(h, mask, lag, graph, x.float() * mask)
        pooled = (h * mask.unsqueeze(-1)).sum(1) / mask.sum(1, keepdim=True).clamp_min(1)
        if self.context_kind != "none":
            gamma, beta = self.context(context).chunk(2, 1)
            pooled = pooled * (1 + .10 * torch.tanh(gamma)) + .10 * beta
        pooled = self.final(pooled)
        return self.residual_head(pooled).squeeze(1), self.direct_head(pooled).squeeze(1), self.risk_head(pooled).squeeze(1)


def train_model(domains, basis, graph, context, multitask, device, epochs, batch):
    data = Rows(domains, basis, context)
    counts = {d: int(np.sum(data.domain == d)) for d in np.unique(data.domain)}
    sampler = WeightedRandomSampler(np.asarray([1 / counts[d] for d in data.domain]), len(data), replacement=True)
    loader = DataLoader(data, batch_size=batch, sampler=sampler, num_workers=3, pin_memory=True)
    model = ManuscriptRelationalDecoder(graph, context, multitask).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), 2e-4, weight_decay=3e-4)
    residual = data.v12 != data.y
    positive = float(residual.mean())
    pos_weight = torch.tensor([(1 - positive) / max(positive, 1e-4)], device=device)
    best = (float("inf"), None)
    check = np.random.default_rng(125).choice(len(data), min(20000, len(data)), replace=False)
    for epoch in range(1, epochs + 1):
        model.train()
        for x, mask, meta, ctx, y, v12 in loader:
            x, mask, meta, ctx = x.to(device), mask.to(device), meta.to(device), ctx.to(device)
            y, v12 = y.to(device), v12.to(device); target = (y != v12).float()
            residual_logit, direct_logit, risk_logit = model(x, mask, meta, ctx)
            loss = nn.functional.binary_cross_entropy_with_logits(residual_logit, target, pos_weight=pos_weight)
            if multitask:
                direct = nn.functional.binary_cross_entropy_with_logits(direct_logit, y)
                risk = nn.functional.binary_cross_entropy_with_logits(risk_logit, target, pos_weight=pos_weight)
                direct_flip = torch.where(v12 < .5, torch.sigmoid(direct_logit), 1 - torch.sigmoid(direct_logit))
                consistency = nn.functional.mse_loss(torch.sigmoid(residual_logit), direct_flip)
                loss = loss + .30 * direct + .15 * risk + .10 * consistency
            optimizer.zero_grad(set_to_none=True); loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 2); optimizer.step()
        if epoch % 2 == 0:
            model.eval(); losses = []
            with torch.no_grad():
                for start in range(0, len(check), batch):
                    z = check[start:start + batch]
                    logits = model(torch.as_tensor(data.x[z], device=device),
                                   torch.as_tensor(data.mask[z], device=device),
                                   torch.as_tensor(data.meta[z], device=device),
                                   torch.as_tensor(data.context[z], device=device))[0]
                    target = torch.as_tensor((data.v12[z] != data.y[z]).astype(np.float32), device=device)
                    losses.append(float(nn.functional.binary_cross_entropy_with_logits(logits, target).cpu()))
            value = float(np.mean(losses))
            if value < best[0]: best = (value, copy.deepcopy(model.state_dict()))
    if best[1] is not None: model.load_state_dict(best[1])
    return model


@torch.no_grad()
def predict(model, domain, basis, context, multitask, device, batch):
    idx = np.flatnonzero(domain.basis == basis); output = []
    ctx = domain_context(domain)
    if context in {"none", "zero"}: ctx[:] = 0
    model.eval()
    for start in range(0, len(idx), batch):
        z = idx[start:start + batch]
        c = torch.as_tensor(np.repeat(ctx[None], len(z), axis=0), device=device)
        residual, direct, risk = model(torch.as_tensor(domain.x[z], device=device),
                                       torch.as_tensor(domain.mask[z], device=device),
                                       torch.as_tensor(domain.meta[z], device=device), c)
        score = torch.sigmoid(residual)
        if multitask:
            direct_flip = torch.where(torch.as_tensor(domain.v12[z], device=device) < .5,
                                      torch.sigmoid(direct), 1 - torch.sigmoid(direct))
            score = (score + direct_flip + torch.sigmoid(risk)) / 3
        output.append(score.cpu().numpy())
    return idx, np.concatenate(output)


def apply(domain, basis, idx, prob, thresholds):
    selected = domain.basis == basis; result = domain.v12[selected].copy()
    local = np.flatnonzero(selected); lookup = {g: i for i, g in enumerate(local)}
    rounds = np.rint(domain.meta[:, 2]).astype(int)
    for g, p in zip(idx, prob):
        cohort = int(rounds[g])
        if cohort in thresholds and p >= thresholds[cohort]: result[lookup[int(g)]] ^= 1
    return selected, result


def choose(model, domains, basis, context, multitask, device, batch, gate):
    cached = [(d, *predict(model, d, basis, context, multitask, device, batch)) for d in domains]
    cohorts = [0] if gate == "basis" else [3, 5, 7]
    thresholds, safe_map, diagnostics = {}, {}, {}
    for cohort in cohorts:
        values = []
        for d, idx, p in cached:
            keep = np.ones(len(idx), dtype=bool) if cohort == 0 else np.rint(d.meta[idx, 2]).astype(int) == cohort
            values.append(p[keep])
        allp = np.concatenate(values) if values else np.empty(0)
        best = None
        for threshold in (np.unique(np.quantile(allp, np.linspace(.60, .999, 140))) if len(allp) else [1.1]):
            stats, ys, bases, candidates = [], [], [], []
            for d, idx, p in cached:
                q = d.basis == basis
                if cohort != 0: q &= np.rint(d.meta[:, 2]).astype(int) == cohort
                candidate = d.v12[q].copy(); local = np.flatnonzero(q); lookup = {g: i for i, g in enumerate(local)}
                for g, probability in zip(idx, p):
                    if g in lookup and probability >= threshold: candidate[lookup[int(g)]] ^= 1
                stats.append(paired_stats(d.y[q], d.v12[q], candidate))
                ys.append(d.y[q]); bases.append(d.v12[q]); candidates.append(candidate)
            pooled = paired_stats(np.concatenate(ys), np.concatenate(bases), np.concatenate(candidates))
            key = (pooled["ci_low_pp"], min(s["gain_pp"] for s in stats), pooled["gain_pp"])
            if best is None or key > best[0]: best = (key, float(threshold), stats, pooled)
        safe = best[0][0] > 0 and best[0][1] >= 0
        thresholds[cohort] = best[1]; safe_map[cohort] = safe
        diagnostics[str(cohort)] = {"safe": safe, "threshold": best[1], "validation": best[2], "pooled": best[3]}
    if gate == "basis":
        thresholds = {r: thresholds[0] for r in (3, 5, 7)} if safe_map[0] else {}
    else:
        thresholds = {r: thresholds[r] for r in (3, 5, 7) if safe_map[r]}
    return thresholds, diagnostics


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True); ap.add_argument("--graph", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True); ap.add_argument("--context", choices=["none", "prefix", "zero"], required=True)
    ap.add_argument("--heads", choices=["single", "multitask"], required=True); ap.add_argument("--gate", choices=["basis", "cohort"], required=True)
    ap.add_argument("--epochs", type=int, default=12); ap.add_argument("--batch", type=int, default=256); ap.add_argument("--seed", type=int, default=1250)
    ap.add_argument("--max-folds", type=int, default=0)
    a = ap.parse_args(); seed_all(a.seed); device = torch.device("cuda")
    domains = {p.stem: Domain(p) for p in sorted(a.data.glob("*.npz"))}; rows = []
    held_names = list(domains)[:a.max_folds] if a.max_folds else list(domains)
    for held in held_names:
        others = [n for n in domains if n != held]; validation = []
        for backend in ("kingston", "fez", "marrakesh"):
            choices = [n for n in others if backend in n]
            if choices and choices[-1] not in validation: validation.append(choices[-1])
        validation = validation[:2]; training = [n for n in others if n not in validation]
        for basis in (0, 1):
            model = train_model([domains[n] for n in training], basis, a.graph, a.context,
                                a.heads == "multitask", device, a.epochs, a.batch)
            thresholds, validation_info = choose(model, [domains[n] for n in validation], basis,
                                                 a.context, a.heads == "multitask", device, a.batch, a.gate)
            d = domains[held]; idx, prob = predict(model, d, basis, a.context, a.heads == "multitask", device, a.batch)
            selected, candidate = apply(d, basis, idx, prob, thresholds)
            row = {"held_domain": held, "basis": "XZ"[basis], "thresholds": thresholds,
                   "validation_domains": validation, "validation": validation_info,
                   **paired_stats(d.y[selected], d.v12[selected], candidate)}
            rows.append(row); print(json.dumps(row), flush=True)
    shots = sum(r["shots"] for r in rows)
    summary = {"version": "V125", "method": "manuscript all-pair relational V12 residual decoder",
               "context": a.context, "heads": a.heads, "gate": a.gate, "real_ibm_only": True,
               "domains": len(held_names), "shots": shots,
               "pooled_gain_pp": sum(r["gain_pp"] * r["shots"] for r in rows) / shots,
               "promotion_allowed": all(r["ci_low_pp"] > 0 for r in rows), "rows": rows,
               "limitations": ["Opened retrospective development domains", "No fresh IBM confirmation block",
                               "Fez/Marrakesh operation graphs remain structural proxies"]}
    a.output.mkdir(parents=True, exist_ok=True)
    name = f"V125_{a.context}_{a.heads}_{a.gate}_RESULT.json"
    (a.output / name).write_text(json.dumps(summary, indent=2)); print(json.dumps(summary, indent=2))


if __name__ == "__main__": main()
