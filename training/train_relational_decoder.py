#!/usr/bin/env python3
"""Reference architecture as evaluated in the manuscript.

This file is provided for inspection of the model as it was run. It is NOT a
standalone entry point: it imports development modules that are not
redistributed, and training additionally requires the context-split syndromes
and per-job calibration snapshots described in the README. Running it directly
will raise ModuleNotFoundError, which is expected.

Every published number is reproduced instead from the frozen per-shot arrays by
the reproduce_*.py scripts in the repository root, which need only numpy.
"""

"""Controlled rendered-snapshot versus long-range snapshot-relation QEC screen.

The rendered representation is a differentiable numerical raster, not a saved RGB
picture.  Both variants receive exactly the same per-round 7x7 three-channel
images, exact-circuit MWPM summaries, metadata, and label-free detector-rate
context.  The only architectural difference is whether snapshots are pooled
independently or related through explicit all-to-all temporal attention.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader

from train_crossblock_v3 import CrossBlockData, infer as _unused_infer
from train_graph_biased_residual_attention import load_coordinates
from train_harmony_spacetime_v2 import config_id


VARIANTS = ("rendered_image", "rendered_3d_views", "longrange_snapshots", "local_global_memory", "all_pair_relations", "shift_robust_relations")


class SnapshotRasterizer(nn.Module):
    """Rasterize detector events into round x y tensors without image artefacts."""

    def forward(self, bits, mask, xyz, rates):
        batch = bits.shape[0]
        xi = (xyz[..., 0] * 6).round().long().clamp(0, 6)
        yi = (xyz[..., 1] * 6).round().long().clamp(0, 6)
        ti = (xyz[..., 2] * 7).round().long().clamp(0, 7)
        flat = ti * 49 + yi * 7 + xi
        image = torch.zeros((batch, 3, 8 * 7 * 7), device=bits.device)
        features = torch.stack((bits.float(), rates, bits.float() - rates), 1)
        features = features * mask[:, None]
        image.scatter_add_(2, flat[:, None].expand(-1, 3, -1), features)
        occupancy = torch.zeros((batch, 8 * 7 * 7), device=bits.device)
        occupancy.scatter_add_(1, flat, mask.float())
        round_valid = occupancy.view(batch, 8, 7, 7).sum((2, 3)) > 0
        return image.view(batch, 3, 8, 7, 7).permute(0, 2, 1, 3, 4), round_valid


class SnapshotEncoder(nn.Module):
    def __init__(self, width=96):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.GroupNorm(4, 32), nn.GELU(),
            nn.Conv2d(32, 48, 3, padding=1), nn.GroupNorm(6, 48), nn.GELU(),
            nn.Conv2d(48, width, 3, padding=1), nn.GroupNorm(8, width), nn.GELU(),
        )
        self.project = nn.Sequential(nn.Linear(width * 2 + 3, width), nn.GELU())

    def forward(self, images):
        batch, rounds, channels, height, width = images.shape
        h = self.net(images.reshape(batch * rounds, channels, height, width))
        mean = h.mean((2, 3))
        maximum = h.amax((2, 3))
        raw = images.reshape(batch * rounds, channels, -1).mean(2)
        return self.project(torch.cat((mean, maximum, raw), 1)).view(batch, rounds, -1)


class LongRangeBlock(nn.Module):
    """Direct all-to-all snapshot attention with learned lag-dependent bias."""

    def __init__(self, width=96, heads=6, max_rounds=8, dropout=0.10):
        super().__init__()
        if width % heads:
            raise ValueError("width must be divisible by heads")
        self.heads, self.head_width = heads, width // heads
        self.norm1 = nn.LayerNorm(width)
        self.qkv = nn.Linear(width, width * 3)
        self.out = nn.Linear(width, width)
        self.lag_bias = nn.Parameter(torch.zeros(heads, max_rounds))
        self.dropout = nn.Dropout(dropout)
        self.norm2 = nn.LayerNorm(width)
        self.ffn = nn.Sequential(nn.Linear(width, width * 4), nn.GELU(), nn.Dropout(dropout), nn.Linear(width * 4, width))

    def forward(self, x, valid, film):
        batch, rounds, width = x.shape
        h = self.norm1(x)
        q, k, v = self.qkv(h).chunk(3, -1)
        q = q.view(batch, rounds, self.heads, self.head_width).transpose(1, 2)
        k = k.view(batch, rounds, self.heads, self.head_width).transpose(1, 2)
        v = v.view(batch, rounds, self.heads, self.head_width).transpose(1, 2)
        score = torch.matmul(q, k.transpose(-1, -2)) / math.sqrt(self.head_width)
        index = torch.arange(rounds, device=x.device)
        lag = (index[:, None] - index[None, :]).abs().clamp_max(self.lag_bias.shape[1] - 1)
        score = score + self.lag_bias[:, lag][None]
        score = score.masked_fill(~valid[:, None, None, :], -1e4)
        attention = score.softmax(-1)
        attended = torch.matmul(attention, v).transpose(1, 2).reshape(batch, rounds, width)
        x = x + self.dropout(self.out(attended))
        gamma, beta = film.chunk(2, -1)
        x = x * (1 + 0.1 * torch.tanh(gamma[:, None])) + 0.1 * beta[:, None]
        x = x + self.dropout(self.ffn(self.norm2(x)))
        return x.masked_fill(~valid[..., None], 0)


class SnapshotRelationshipDecoder(nn.Module):
    def __init__(self, members, variant, width=96, layers=3, heads=6):
        super().__init__()
        if variant not in VARIANTS:
            raise ValueError(variant)
        self.variant, self.width, self.layers = variant, width, layers
        self.rasterizer = SnapshotRasterizer()
        self.encoder = SnapshotEncoder(width)
        self.round_embedding = nn.Embedding(8, width)
        self.basis = nn.Embedding(2, width)
        self.round_count = nn.Embedding(3, width)
        self.logical = nn.Embedding(2, width)
        self.base = nn.Embedding(2, width)
        self.matching = nn.Sequential(nn.Linear(2 * members + 6, 160), nn.GELU(), nn.Linear(160, width))
        self.calibration = nn.Sequential(nn.Linear(56, 160), nn.GELU(), nn.Linear(160, width + layers * 2 * width))
        self.blocks = nn.ModuleList(LongRangeBlock(width, heads) for _ in range(layers))
        self.local_3d = nn.Sequential(
            nn.Conv3d(3, 32, 3, padding=1), nn.GroupNorm(4, 32), nn.GELU(),
            nn.Conv3d(32, 48, 3, padding=(2, 1, 1), dilation=(2, 1, 1)), nn.GroupNorm(6, 48), nn.GELU(),
            nn.Conv3d(48, width, 3, padding=1), nn.GroupNorm(8, width), nn.GELU(),
        )
        self.memory = nn.GRU(width, width // 2, batch_first=True, bidirectional=True)
        # Explicit long-lag relationship descriptors: activity correlation,
        # agreement, and absolute difference for every lag 1..7.
        self.pair_project = nn.Sequential(nn.Linear(21, 96), nn.GELU(), nn.Linear(96, width))
        # Explicit relationship tokens retain every valid (snapshot_i, snapshot_j)
        # pair instead of reducing each temporal lag to a single activity scalar.
        self.pair_lag = nn.Embedding(8, 16)
        self.all_pair_project = nn.Sequential(
            nn.Linear(width * 4 + 16, width * 2), nn.GELU(), nn.Dropout(0.10), nn.Linear(width * 2, width)
        )
        self.relation_map = nn.Sequential(
            nn.Conv2d(21, 48, 3, padding=1), nn.GroupNorm(6, 48), nn.GELU(),
            nn.Conv2d(48, width, 3, padding=1), nn.GroupNorm(8, width), nn.GELU(),
        )
        head_width = width * (6 if variant in {"local_global_memory", "all_pair_relations", "shift_robust_relations"} else 4)
        self.head = nn.Sequential(nn.Linear(head_width, 192), nn.GELU(), nn.Dropout(0.12))
        self.residual = nn.Linear(192, 1)
        self.direct = nn.Linear(192, 1)
        self.risk = nn.Linear(192, 1)

    @staticmethod
    def _pair_features(images, valid):
        activity = images[:, :, 0].mean((2, 3))
        features = []
        for lag in range(1, 8):
            pair_valid = valid[:, lag:] & valid[:, :-lag]
            left, right = activity[:, lag:], activity[:, :-lag]
            denominator = pair_valid.sum(1).clamp_min(1)
            features.extend((
                ((left * right) * pair_valid).sum(1) / denominator,
                ((left - right).abs() * pair_valid).sum(1) / denominator,
                ((1 - (left - right).abs()) * pair_valid).sum(1) / denominator,
            ))
        return torch.stack(features, 1)

    @staticmethod
    def _render_3d_views(images, valid):
        """Render XY, X-time, and Y-time orthographic views of the volume."""
        weight = valid.float()[:, :, None, None, None]
        normalizer = valid.sum(1).clamp_min(1).float()[:, None, None, None]
        xy = (images * weight).sum(1) / normalizer
        # Retain the full time axis in side views; interpolate only to give every
        # camera view the same 8x8 raster size consumed by the shared encoder.
        xt = (images * weight).mean(3).permute(0, 2, 1, 3)
        yt = (images * weight).mean(4).permute(0, 2, 1, 3)
        xy = nn.functional.interpolate(xy, size=(8, 8), mode="bilinear", align_corners=False)
        xt = nn.functional.interpolate(xt, size=(8, 8), mode="bilinear", align_corners=False)
        yt = nn.functional.interpolate(yt, size=(8, 8), mode="bilinear", align_corners=False)
        return torch.stack((xy, xt, yt), 1)

    def _all_pair_features(self, snapshots, images, valid):
        """Encode every snapshot pair plus detector-level multi-lag relation maps."""
        batch, rounds, width = snapshots.shape
        left = snapshots[:, :, None, :].expand(-1, -1, rounds, -1)
        right = snapshots[:, None, :, :].expand(-1, rounds, -1, -1)
        index = torch.arange(rounds, device=snapshots.device)
        lag = (index[:, None] - index[None, :]).abs().clamp_max(7)
        lag_feature = self.pair_lag(lag)[None].expand(batch, -1, -1, -1)
        tokens = self.all_pair_project(torch.cat((left, right, (left - right).abs(), left * right, lag_feature), -1))
        pair_valid = valid[:, :, None] & valid[:, None, :]
        # Exclude diagonal self-pairs: the branch is specifically relational.
        pair_valid = pair_valid & (~torch.eye(rounds, dtype=torch.bool, device=snapshots.device)[None])
        count = pair_valid.sum((1, 2)).clamp_min(1)[:, None]
        token_mean = (tokens * pair_valid[..., None]).sum((1, 2)) / count
        token_max = tokens.masked_fill(~pair_valid[..., None], -1e4).amax((1, 2))

        maps = []
        for temporal_lag in range(1, 8):
            left_image = images[:, temporal_lag:, 0]
            right_image = images[:, :-temporal_lag, 0]
            lag_valid = (valid[:, temporal_lag:] & valid[:, :-temporal_lag]).float()[..., None, None]
            denominator = lag_valid.sum(1).clamp_min(1)
            maps.extend((
                (left_image * right_image * lag_valid).sum(1) / denominator,
                ((left_image - right_image).abs() * lag_valid).sum(1) / denominator,
                (torch.maximum(left_image, right_image) * lag_valid).sum(1) / denominator,
            ))
        relation_volume = self.relation_map(torch.stack(maps, 1))
        map_feature = 0.5 * relation_volume.mean((2, 3)) + 0.5 * relation_volume.amax((2, 3))
        return token_mean + 0.5 * token_max, map_feature

    def forward(self, bits, mask, xyz, rates, hardware, meta, members, scores, consensus, base):
        del hardware
        batch = bits.shape[0]
        valid_detector = mask.float()
        denominator = valid_detector.sum(1).clamp_min(1)
        active = (bits.float() * valid_detector).sum(1) / denominator
        model_rates = rates
        if self.variant == "shift_robust_relations":
            # Remove global calibration-day scale while retaining the spatial
            # ranking of detector rates. Training-only jitter forces FiLM and
            # the relation branch to tolerate unseen label-free rate profiles.
            logits = torch.logit(rates.clamp(1e-4, 1 - 1e-4))
            centre = (logits * valid_detector).sum(1, keepdim=True) / denominator[:, None]
            variance = (((logits - centre) ** 2) * valid_detector).sum(1, keepdim=True) / denominator[:, None]
            standardized = (logits - centre) / variance.sqrt().clamp_min(0.25)
            if self.training:
                standardized = standardized + 0.20 * torch.randn_like(standardized)
            model_rates = torch.sigmoid(standardized) * valid_detector
        mean_rate = (model_rates * valid_detector).sum(1) / denominator
        vote = members.mean(1)
        entropy = -(vote.clamp(1e-5, 1 - 1e-5) * vote.clamp(1e-5, 1 - 1e-5).log() +
                    (1 - vote).clamp(1e-5, 1 - 1e-5) * (1 - vote).clamp(1e-5, 1 - 1e-5).log())
        matching_summary = torch.cat((
            members, scores.clamp(-8, 8), vote[:, None], consensus[:, None], entropy[:, None],
            active[:, None], mean_rate[:, None], (active - mean_rate).abs()[:, None]
        ), 1)
        rid = torch.where(meta[:, 2] == 3, 0, torch.where(meta[:, 2] == 5, 1, 2))
        calibration = self.calibration(model_rates * valid_detector)
        calibration_context = calibration[:, :self.width]
        films = calibration[:, self.width:].view(batch, self.layers, 2 * self.width)
        context = (self.matching(matching_summary) + calibration_context + self.basis(meta[:, 1]) +
                   self.round_count(rid) + self.logical(meta[:, 3]) + self.base(base))

        images, round_valid = self.rasterizer(bits, mask, xyz, model_rates)
        if self.variant == "rendered_3d_views":
            views = self._render_3d_views(images, round_valid)
            view_features = self.encoder(views) + context[:, None]
            mean, maximum = view_features.mean(1), view_features.amax(1)
        else:
            snapshots = self.encoder(images)
            time_index = torch.arange(8, device=bits.device)[None]
            snapshots = snapshots + self.round_embedding(time_index) + context[:, None]
            if self.variant in {"longrange_snapshots", "local_global_memory", "all_pair_relations", "shift_robust_relations"}:
                for layer, block in enumerate(self.blocks):
                    snapshots = block(snapshots, round_valid, films[:, layer])
            count = round_valid.sum(1).clamp_min(1)[:, None]
            mean = (snapshots * round_valid[..., None]).sum(1) / count
            maximum = snapshots.masked_fill(~round_valid[..., None], -1e4).amax(1)
        pair = self.pair_project(self._pair_features(images, round_valid))
        features = [mean, maximum, pair, context]
        if self.variant == "local_global_memory":
            volume = self.local_3d(images.permute(0, 2, 1, 3, 4))
            local = 0.5 * volume.mean((2, 3, 4)) + 0.5 * volume.amax((2, 3, 4))
            lengths = round_valid.sum(1).clamp_min(1).cpu()
            packed = nn.utils.rnn.pack_padded_sequence(snapshots, lengths, batch_first=True, enforce_sorted=False)
            _, hidden = self.memory(packed)
            persistent_memory = torch.cat((hidden[-2], hidden[-1]), 1)
            features.extend((local, persistent_memory))
        elif self.variant in {"all_pair_relations", "shift_robust_relations"}:
            pair_tokens, relation_maps = self._all_pair_features(snapshots, images, round_valid)
            features.extend((pair_tokens, relation_maps))
        h = self.head(torch.cat(features, 1))
        return self.residual(h).squeeze(1), self.direct(h).squeeze(1), self.risk(h).squeeze(1)


@torch.no_grad()
def infer(model, loader, device):
    model.eval()
    output = [[] for _ in range(8)]
    for batch in loader:
        bits, mask, xyz, rates, hardware, meta, members, scores, consensus, base, _, labels, index = batch
        inputs = [x.to(device, non_blocking=True) for x in (bits, mask, xyz, rates, hardware, meta, members, scores, consensus, base)]
        logits = model(*inputs)
        values = (torch.sigmoid(logits[0]).cpu().numpy(), torch.sigmoid(logits[1]).cpu().numpy(),
                  torch.sigmoid(logits[2]).cpu().numpy(), labels.numpy(), base.numpy(), consensus.numpy(),
                  index.numpy(), meta.numpy())
        for target, value in zip(output, values):
            target.append(value)
    return tuple(np.concatenate(value) for value in output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--coordinates", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--variant", choices=VARIANTS, required=True)
    parser.add_argument("--train-domain", type=int)
    parser.add_argument("--train-domains", help="Comma-separated domains for multi-day training")
    parser.add_argument("--validation-domain", type=int, required=True)
    parser.add_argument("--diagnostic-domain", type=int, default=2)
    parser.add_argument("--seed", type=int, default=2718)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--patience", type=int, default=6)
    parser.add_argument("--batch-size", type=int, default=256)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    random.seed(args.seed); np.random.seed(args.seed); torch.manual_seed(args.seed); torch.cuda.manual_seed_all(args.seed)

    with np.load(args.data, allow_pickle=False) as archive:
        arrays = {key: archive[key] for key in archive.files}
    scored = arrays["split"] != 2
    if args.train_domains:
        train_domains = np.asarray([int(value) for value in args.train_domains.split(",")], dtype=int)
    elif args.train_domain is not None:
        train_domains = np.asarray([args.train_domain], dtype=int)
    else:
        raise RuntimeError("Provide --train-domain or --train-domains")
    indices = {
        "train": np.flatnonzero(scored & np.isin(arrays["domain_id"], train_domains)),
        "validation": np.flatnonzero(scored & (arrays["domain_id"] == args.validation_domain)),
        "diagnostic": np.flatnonzero(scored & (arrays["domain_id"] == args.diagnostic_domain)),
    }
    if any(len(value) == 0 for value in indices.values()):
        raise RuntimeError({key: len(value) for key, value in indices.items()})
    coordinates = load_coordinates(args.coordinates, arrays["detectors"].shape[1])
    loaders = {
        name: DataLoader(CrossBlockData(arrays, ids, coordinates, "nominal"), batch_size=args.batch_size,
                         shuffle=name == "train", num_workers=3, pin_memory=True, persistent_workers=True)
        for name, ids in indices.items()
    }
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SnapshotRelationshipDecoder(arrays["member_predictions"].shape[1], args.variant).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=3e-3)
    scaler = torch.amp.GradScaler("cuda", enabled=device.type == "cuda")
    best, stale, history = math.inf, 0, []
    checkpoint = args.output / "checkpoint_best.pt"
    for epoch in range(1, args.epochs + 1):
        model.train(); total = 0; loss_sum = 0.0
        for batch in loaders["train"]:
            bits, mask, xyz, rates, hardware, meta, members, scores, consensus, base, residual_y, labels, _ = [x.to(device, non_blocking=True) for x in batch]
            optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast("cuda", enabled=device.type == "cuda"):
                residual, direct, risk = model(bits, mask, xyz, rates, hardware, meta, members, scores, consensus, base)
                loss = (nn.functional.binary_cross_entropy_with_logits(residual, residual_y) +
                        0.20 * nn.functional.binary_cross_entropy_with_logits(direct, labels) +
                        0.35 * nn.functional.binary_cross_entropy_with_logits(risk, residual_y))
            scaler.scale(loss).backward(); scaler.unscale_(optimizer)
            nn.utils.clip_grad_norm_(model.parameters(), 1.5)
            scaler.step(optimizer); scaler.update()
            loss_sum += float(loss.detach()) * len(labels); total += len(labels)

        values = infer(model, loaders["validation"], device)
        residual_probability, _, _, labels, base, *_ = values
        target = labels.astype(np.uint8) ^ base.astype(np.uint8)
        val_bce = float(nn.functional.binary_cross_entropy(torch.from_numpy(residual_probability).clamp(1e-6, 1 - 1e-6), torch.from_numpy(target).float()))
        row = {"epoch": epoch, "train_loss": loss_sum / total, "validation_bce": val_bce}
        history.append(row); print(json.dumps(row), flush=True)
        if val_bce < best - 1e-5:
            best, stale = val_bce, 0
            torch.save({"state": model.state_dict(), "variant": args.variant, "seed": args.seed}, checkpoint)
        else:
            stale += 1
        if stale >= args.patience:
            break

    model.load_state_dict(torch.load(checkpoint, map_location=device, weights_only=False)["state"])
    names = ("residual_probability", "direct_probability", "risk_probability", "labels", "base", "consensus", "sample_index", "metadata")
    for name in ("validation", "diagnostic"):
        np.savez_compressed(args.output / f"{name}_predictions.npz", **dict(zip(names, infer(model, loaders[name], device))))
    report = {
        "experiment": "rendered_snapshot_vs_longrange_snapshot_relationships_v5",
        "variant": args.variant, "seed": args.seed, "train_domain": args.train_domain,
        "train_domains": train_domains.tolist(),
        "validation_domain": args.validation_domain, "diagnostic_domain": args.diagnostic_domain,
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "best_validation_bce": best, "history": history,
        "rendering": "differentiable 7x7 numerical detector raster per syndrome round; no RGB or screenshot input",
        "longrange": "direct all-to-all round attention with learned lag bias and explicit lag-1..7 pair descriptors",
        "warning": "Diagnostic domain is historical development data and is not independent confirmation.",
    }
    (args.output / "training_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
