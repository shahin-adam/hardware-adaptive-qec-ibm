#!/usr/bin/env python3
"""V161: IBM-native dynamic event-coactivity attention decoder.

This controlled extension of V160 implements the event-pair attention features
described for the original AlphaQubit architecture: current-current,
current-previous, previous-current, and previous-previous detector products.
The features only modulate IBM circuit-graph attention; no Google data or
weights are used.

IBM-specific structure comes from the recovered detector/error-mechanism
graphs. The learned model proposes residual flips relative to frozen V12.
Thresholds are selected on a separate validation domain, independently for X
and Z; the held evaluation labels are never used for training or routing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


DOMAINS = [
    "v21_kingston",
    "v25_fez",
    "v28_marrakesh",
    "v29_fez",
    "v38_kingston",
    "v39_fez",
    "v68_kingston",
]

ARMS = {
    "static_control": {
        "use_graph": True,
        "pretrain": False,
        "input_mask": True,
        "dynamic_mode": "none",
    },
    "dynamic_spatial": {
        "use_graph": True,
        "pretrain": False,
        "input_mask": True,
        "dynamic_mode": "spatial",
    },
    "dynamic_fourway": {
        "use_graph": True,
        "pretrain": False,
        "input_mask": True,
        "dynamic_mode": "fourway",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def paired(y: np.ndarray, base: np.ndarray, candidate: np.ndarray) -> dict:
    base_error = base != y
    candidate_error = candidate != y
    corrected = int(np.sum(base_error & ~candidate_error))
    damaged = int(np.sum(~base_error & candidate_error))
    n = int(y.size)
    gain = 100.0 * (corrected - damaged) / n if n else 0.0
    discordant = corrected + damaged
    variance = (
        (discordant / n - ((corrected - damaged) / n) ** 2) / n
        if n
        else 0.0
    )
    half = 1.96 * 100.0 * math.sqrt(max(0.0, variance))
    return {
        "shots": n,
        "baseline_error_pct": 100.0 * float(np.mean(base_error)) if n else 0.0,
        "candidate_error_pct": (
            100.0 * float(np.mean(candidate_error)) if n else 0.0
        ),
        "improvement_pp": gain,
        "ci95_lower_pp": gain - half,
        "ci95_upper_pp": gain + half,
        "corrected": corrected,
        "damaged": damaged,
        "interventions": int(np.sum(base != candidate)),
    }


@dataclass
class GraphTables:
    matrices: np.ndarray
    degrees: np.ndarray
    exact: np.ndarray
    lookup: dict[tuple[str, str], int]
    provenance: list[dict]


def mechanism_graph(path: Path) -> np.ndarray:
    """Project a detector-mechanism hypergraph onto eight stabilizer tracks."""
    with np.load(path, allow_pickle=False) as data:
        probability = data["mechanism_probability"].astype(np.float64)
        mechanism = data["edge_mechanism_index"].astype(np.int64)
        detector = data["edge_detector_index"].astype(np.int64)
    adjacency = np.zeros((8, 8), dtype=np.float64)
    order = np.argsort(mechanism, kind="stable")
    mechanism, detector = mechanism[order], detector[order]
    boundaries = np.flatnonzero(np.diff(mechanism)) + 1
    for indices in np.split(np.arange(mechanism.size), boundaries):
        if not len(indices):
            continue
        mechanism_id = mechanism[indices[0]]
        tracks = np.unique(detector[indices] % 8)
        weight = -math.log1p(-float(probability[mechanism_id]))
        adjacency[np.ix_(tracks, tracks)] += weight
    adjacency = 0.5 * (adjacency + adjacency.T)
    np.fill_diagonal(adjacency, np.diag(adjacency) + adjacency.mean())
    maximum = float(adjacency.max())
    return (adjacency / maximum if maximum > 0 else adjacency).astype(np.float32)


def build_graph_tables(graph_root: Path) -> GraphTables:
    matrices: list[np.ndarray] = [np.zeros((8, 8), dtype=np.float32)]
    exact: list[float] = [0.0]
    lookup: dict[tuple[str, str], int] = {}
    provenance: list[dict] = []
    for backend in ("ibm_kingston", "ibm_fez"):
        directory = graph_root / backend
        for path in sorted(directory.glob("*.v149_graph.npz")):
            config = path.name.split(".")[0]
            graph_id = len(matrices)
            matrices.append(mechanism_graph(path))
            exact.append(1.0)
            lookup[(backend, config)] = graph_id
            provenance.append(
                {
                    "backend": backend,
                    "configuration": config,
                    "file": path.name,
                    "sha256": sha256(path),
                }
            )
    matrix = np.stack(matrices)
    degree = matrix.sum(axis=2, keepdims=True)
    degree /= np.maximum(degree.max(axis=1, keepdims=True), 1e-8)
    return GraphTables(
        matrices=matrix,
        degrees=degree.astype(np.float32),
        exact=np.asarray(exact, dtype=np.float32)[:, None],
        lookup=lookup,
        provenance=provenance,
    )


def backend_for(domain: str) -> str:
    if "kingston" in domain:
        return "ibm_kingston"
    if "fez" in domain:
        return "ibm_fez"
    return "ibm_marrakesh"


def config_name(basis: int, rounds: int, logical: int) -> str:
    return f"{'Z' if int(basis) else 'X'}{int(rounds)}_L{int(logical)}"


def load_domain(root: Path, name: str, tables: GraphTables) -> dict:
    with np.load(root / f"{name}.npz", allow_pickle=False) as data:
        metadata = data["metadata"].astype(np.int16)
        basis = metadata[:, 1].astype(np.int64)
        rounds = metadata[:, 2].astype(np.int64)
        logical = metadata[:, 3].astype(np.int64)
        backend = backend_for(name)
        graph_id = np.asarray(
            [
                tables.lookup.get(
                    (backend, config_name(b, r, l)),
                    0,
                )
                for b, r, l in zip(basis, rounds, logical)
            ],
            dtype=np.int64,
        )
        return {
            "x": data["detectors"].astype(np.float32),
            "rounds": rounds,
            "basis": basis,
            "logical": logical,
            "y": data["labels"].astype(np.uint8),
            "v12": data["v12"].astype(np.uint8),
            "graph_id": graph_id,
            "domain": np.full(len(basis), DOMAINS.index(name), dtype=np.int64),
            "source_index": data["source_index"].astype(np.int64),
        }


def combine(parts: list[dict]) -> dict:
    return {
        key: np.concatenate([part[key] for part in parts])
        for key in (
            "x",
            "rounds",
            "basis",
            "logical",
            "y",
            "v12",
            "graph_id",
            "domain",
        )
    }


def dataset(data: dict, include_label: bool = True) -> TensorDataset:
    tensors = [
        torch.from_numpy(data["x"]),
        torch.from_numpy(data["rounds"]),
        torch.from_numpy(data["basis"]),
        torch.from_numpy(data["logical"]),
        torch.from_numpy(data["v12"].astype(np.int64)),
        torch.from_numpy(data["graph_id"]),
    ]
    if include_label:
        tensors.append(torch.from_numpy(data["y"].astype(np.int64)))
    return TensorDataset(*tensors)


class RecurrentLayer(nn.Module):
    def __init__(self, width: int):
        super().__init__()
        self.project = nn.Linear(width * 2, width)
        self.norm = RMSNorm(width)
        nn.init.orthogonal_(self.project.weight[:, :width])

    def forward(self, state: torch.Tensor, value: torch.Tensor) -> torch.Tensor:
        return self.norm(torch.nn.functional.gelu(self.project(torch.cat([state, value], -1))))


class GatedDense(nn.Module):
    def __init__(self, width: int, widening: int = 3):
        super().__init__()
        self.value = nn.Linear(width, width * widening)
        self.gate = nn.Linear(width, width * widening)
        self.output = nn.Linear(width * widening, width)

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        return self.output(
            torch.nn.functional.gelu(self.value(value))
            * torch.sigmoid(self.gate(value))
        )


class RMSNorm(nn.Module):
    """RMSNorm compatible with older PyTorch installations."""

    def __init__(self, width: int, epsilon: float = 1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(width))
        self.epsilon = epsilon

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        scale = torch.rsqrt(value.pow(2).mean(dim=-1, keepdim=True) + self.epsilon)
        return value * scale * self.weight


class GraphSpatialAttention(nn.Module):
    def __init__(self, width: int, heads: int):
        super().__init__()
        if width % heads:
            raise ValueError("width must be divisible by heads")
        self.heads = heads
        self.depth = width // heads
        self.norm1 = RMSNorm(width)
        self.qkv = nn.Linear(width, width * 3, bias=False)
        self.output = nn.Linear(width, width, bias=False)
        self.norm2 = RMSNorm(width)
        self.dense = GatedDense(width)
        self.graph_scale_raw = nn.Parameter(torch.tensor(0.0))
        self.event_bias = nn.Linear(4, heads, bias=False)
        nn.init.zeros_(self.event_bias.weight)

    def forward(
        self,
        value: torch.Tensor,
        graph: torch.Tensor,
        use_graph: bool,
        current_event: torch.Tensor,
        previous_event: torch.Tensor,
        dynamic_mode: str,
    ) -> torch.Tensor:
        batch, stabilizers, width = value.shape
        normalized = self.norm1(value)
        q, k, v = self.qkv(normalized).chunk(3, dim=-1)
        q = q.view(batch, stabilizers, self.heads, self.depth).transpose(1, 2)
        k = k.view(batch, stabilizers, self.heads, self.depth).transpose(1, 2)
        v = v.view(batch, stabilizers, self.heads, self.depth).transpose(1, 2)
        score = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.depth)
        if use_graph:
            bias = torch.log1p(50.0 * graph).unsqueeze(1)
            scale = torch.nn.functional.softplus(self.graph_scale_raw)
            score = score + scale * bias
        if dynamic_mode != "none":
            current_current = current_event[:, :, None] * current_event[:, None, :]
            previous_previous = (
                previous_event[:, :, None] * previous_event[:, None, :]
            )
            if dynamic_mode == "spatial":
                zero = torch.zeros_like(current_current)
                event_features = torch.stack(
                    [current_current, zero, zero, previous_previous], dim=-1
                )
            elif dynamic_mode == "fourway":
                current_previous = (
                    current_event[:, :, None] * previous_event[:, None, :]
                )
                previous_current = (
                    previous_event[:, :, None] * current_event[:, None, :]
                )
                event_features = torch.stack(
                    [
                        current_current,
                        current_previous,
                        previous_current,
                        previous_previous,
                    ],
                    dim=-1,
                )
            else:
                raise ValueError(f"unknown dynamic mode: {dynamic_mode}")
            dynamic_bias = self.event_bias(event_features).permute(0, 3, 1, 2)
            score = score + dynamic_bias
        attention = torch.softmax(score, dim=-1)
        update = torch.matmul(attention, v).transpose(1, 2).reshape(batch, stabilizers, width)
        value = value + self.output(update)
        return value + self.dense(self.norm2(value))


class CrossReadout(nn.Module):
    def __init__(self, width: int, heads: int):
        super().__init__()
        self.heads = heads
        self.depth = width // heads
        self.query = nn.Linear(width, width, bias=False)
        self.key = nn.Linear(width, width, bias=False)
        self.value = nn.Linear(width, width, bias=False)
        self.output = nn.Linear(width, width, bias=False)

    def forward(self, query: torch.Tensor, memory: torch.Tensor) -> torch.Tensor:
        batch, stabilizers, width = memory.shape
        q = self.query(query).view(batch, self.heads, 1, self.depth)
        k = (
            self.key(memory)
            .view(batch, stabilizers, self.heads, self.depth)
            .transpose(1, 2)
        )
        v = (
            self.value(memory)
            .view(batch, stabilizers, self.heads, self.depth)
            .transpose(1, 2)
        )
        attention = torch.softmax(
            torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.depth),
            dim=-1,
        )
        pooled = torch.matmul(attention, v).reshape(batch, width)
        return self.output(pooled)


class IBMAQDecoder(nn.Module):
    def __init__(self, tables: GraphTables, width: int = 128, heads: int = 8):
        super().__init__()
        self.width = width
        self.input = nn.Linear(2, width)
        self.stabilizer = nn.Embedding(8, width)
        self.round_position = nn.Embedding(7, width)
        self.basis = nn.Embedding(2, width)
        self.logical_state = nn.Embedding(2, width)
        self.round_count = nn.Embedding(8, width)
        self.graph_degree = nn.Linear(2, width)
        self.recurrent1 = RecurrentLayer(width)
        self.spatial1 = GraphSpatialAttention(width, heads)
        self.recurrent2 = RecurrentLayer(width)
        self.spatial2 = GraphSpatialAttention(width, heads)
        self.recurrent3 = RecurrentLayer(width)
        self.readout_attention = CrossReadout(width, heads)
        self.readout_norm = RMSNorm(width)
        self.residual_heads = nn.ModuleList(
            [
                nn.Sequential(
                    nn.Linear(width, width),
                    nn.GELU(),
                    nn.Linear(width, 1),
                )
                for _ in range(2)
            ]
        )
        self.logical_heads = nn.ModuleList(
            [nn.Linear(width, 1) for _ in range(2)]
        )
        self.reconstruct = nn.Linear(width, 1)
        self.register_buffer(
            "graph_table", torch.from_numpy(tables.matrices), persistent=True
        )
        self.register_buffer(
            "degree_table", torch.from_numpy(tables.degrees), persistent=True
        )
        self.register_buffer(
            "exact_table", torch.from_numpy(tables.exact), persistent=True
        )

    def forward(
        self,
        x: torch.Tensor,
        rounds: torch.Tensor,
        basis: torch.Tensor,
        logical: torch.Tensor,
        graph_id: torch.Tensor,
        use_graph: bool,
        dynamic_mode: str,
        mask_probability: float = 0.0,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        batch = x.shape[0]
        x = x.reshape(batch, 7, 8)
        active = (
            torch.arange(7, device=x.device)[None, :, None] < rounds[:, None, None]
        ).expand(-1, -1, 8)
        observed = active.clone()
        if self.training and mask_probability > 0:
            observed &= torch.rand_like(x) >= mask_probability
        pair = torch.stack([x * observed, observed.float()], dim=-1)
        graph = self.graph_table[graph_id]
        degree = self.degree_table[graph_id]
        exact = self.exact_table[graph_id].unsqueeze(1).expand(-1, 8, -1)
        graph_feature = self.graph_degree(torch.cat([degree, exact], dim=-1))
        stabilizer = self.stabilizer(torch.arange(8, device=x.device))[None]
        state1 = torch.zeros(batch, 8, self.width, device=x.device)
        state2 = torch.zeros_like(state1)
        state3 = torch.zeros_like(state1)
        reconstruction: list[torch.Tensor] = []
        previous_event = torch.zeros(batch, 8, device=x.device)
        for time in range(7):
            current_event = pair[:, time, :, 0]
            value = (
                self.input(pair[:, time])
                + stabilizer
                + self.round_position.weight[time][None, None]
                + self.basis(basis)[:, None]
                + graph_feature
            )
            active_time = active[:, time, 0][:, None, None]
            update1 = self.recurrent1(state1, value)
            state1 = torch.where(active_time, update1, state1)
            value = self.spatial1(
                state1,
                graph,
                use_graph,
                current_event,
                previous_event,
                dynamic_mode,
            )
            update2 = self.recurrent2(state2, value)
            state2 = torch.where(active_time, update2, state2)
            value = self.spatial2(
                state2,
                graph,
                use_graph,
                current_event,
                previous_event,
                dynamic_mode,
            )
            update3 = self.recurrent3(state3, value)
            state3 = torch.where(active_time, update3, state3)
            reconstruction.append(self.reconstruct(state3).squeeze(-1))
            previous_event = current_event
        query = (
            state3.mean(dim=1)
            + self.basis(basis)
            + self.logical_state(logical)
            + self.round_count(rounds)
        )
        pooled = self.readout_norm(self.readout_attention(query, state3) + query)
        residual_all = torch.cat(
            [head(pooled) for head in self.residual_heads], dim=1
        )
        logical_all = torch.cat(
            [head(pooled) for head in self.logical_heads], dim=1
        )
        index = basis[:, None]
        residual = residual_all.gather(1, index).squeeze(1)
        direct = logical_all.gather(1, index).squeeze(1)
        return residual, direct, torch.stack(reconstruction, dim=1), observed


def move(batch: tuple[torch.Tensor, ...], device: torch.device):
    return tuple(item.to(device, non_blocking=True) for item in batch)


@torch.no_grad()
def predict(
    model: IBMAQDecoder,
    data: dict,
    device: torch.device,
    batch_size: int,
    use_graph: bool,
    dynamic_mode: str,
) -> np.ndarray:
    loader = DataLoader(dataset(data), batch_size=batch_size, shuffle=False)
    model.eval()
    values: list[np.ndarray] = []
    for batch in loader:
        x, rounds, basis, logical, _, graph_id, _ = move(batch, device)
        residual, _, _, _ = model(
            x, rounds, basis, logical, graph_id, use_graph, dynamic_mode, 0.0
        )
        values.append(torch.sigmoid(residual).cpu().numpy())
    return np.concatenate(values)


def select_threshold(probability: np.ndarray, data: dict, basis_value: int):
    take = data["basis"] == basis_value
    probability = probability[take]
    y = data["y"][take]
    v12 = data["v12"][take]
    candidates = np.unique(
        np.concatenate(
            [
                np.linspace(0.5, 0.9995, 500),
                np.quantile(probability, np.linspace(0.5, 0.9995, 300)),
            ]
        )
    )
    accepted, best = [], None
    for threshold in candidates:
        route = probability >= threshold
        if int(route.sum()) < 30:
            continue
        candidate = v12.copy()
        candidate[route] = 1 - candidate[route]
        result = paired(y, v12, candidate)
        row = {"threshold": float(threshold), "validation": result}
        if best is None or result["improvement_pp"] > best["validation"]["improvement_pp"]:
            best = row
        if result["ci95_lower_pp"] > 0:
            accepted.append(row)
    if not accepted:
        return None, {"accepted": 0, "best_nominal": best}
    accepted.sort(
        key=lambda row: (
            row["validation"]["ci95_lower_pp"],
            row["validation"]["improvement_pp"],
        ),
        reverse=True,
    )
    return accepted[0]["threshold"], {
        "accepted": len(accepted),
        "selected": accepted[0],
        "best_nominal": best,
    }


def evaluate(
    probability: np.ndarray,
    data: dict,
    thresholds: dict[int, float | None],
) -> tuple[np.ndarray, dict]:
    candidate = data["v12"].copy()
    route = np.zeros(len(candidate), dtype=bool)
    for basis_value in (0, 1):
        threshold = thresholds[basis_value]
        take = data["basis"] == basis_value
        if threshold is not None:
            route[take] = probability[take] >= threshold
    candidate[route] = 1 - candidate[route]
    report = {
        "X": paired(
            data["y"][data["basis"] == 0],
            data["v12"][data["basis"] == 0],
            candidate[data["basis"] == 0],
        ),
        "Z": paired(
            data["y"][data["basis"] == 1],
            data["v12"][data["basis"] == 1],
            candidate[data["basis"] == 1],
        ),
        "pooled": paired(data["y"], data["v12"], candidate),
        "coverage": 1.0,
        "route_count": int(route.sum()),
    }
    return candidate, report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arm", choices=ARMS, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--graph-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evaluation-domain", default="v39_fez")
    parser.add_argument("--validation-domain", default="v29_fez")
    parser.add_argument("--pretrain-epochs", type=int, default=3)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=768)
    parser.add_argument("--width", type=int, default=128)
    args = parser.parse_args()
    if args.evaluation_domain == args.validation_domain:
        raise ValueError("evaluation and validation domains must differ")
    arm = ARMS[args.arm]
    seed = 16100 + list(ARMS).index(args.arm)
    torch.manual_seed(seed)
    np.random.seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tables = build_graph_tables(args.graph_root)
    loaded = {name: load_domain(args.data_root, name, tables) for name in DOMAINS}
    train_names = [
        name
        for name in DOMAINS
        if name not in (args.evaluation_domain, args.validation_domain)
    ]
    training = combine([loaded[name] for name in train_names])
    validation = loaded[args.validation_domain]
    evaluation = loaded[args.evaluation_domain]
    model = IBMAQDecoder(tables, width=args.width).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=2e-4)
    generator = torch.Generator().manual_seed(seed)
    loader = DataLoader(
        dataset(training),
        batch_size=args.batch_size,
        shuffle=True,
        generator=generator,
        num_workers=0,
        pin_memory=device.type == "cuda",
    )
    history: list[dict] = []
    if arm["pretrain"]:
        for epoch in range(args.pretrain_epochs):
            model.train()
            total, count = 0.0, 0
            for batch in loader:
                x, rounds, basis, logical, _, graph_id, _ = move(batch, device)
                _, _, reconstruction, observed = model(
                    x,
                    rounds,
                    basis,
                    logical,
                    graph_id,
                    arm["use_graph"],
                    arm["dynamic_mode"],
                    0.5,
                )
                active = (
                    torch.arange(7, device=device)[None, :, None]
                    < rounds[:, None, None]
                ).expand(-1, -1, 8)
                masked = active & ~observed
                loss = nn.functional.binary_cross_entropy_with_logits(
                    reconstruction[masked], x.reshape(-1, 7, 8)[masked]
                )
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                nn.utils.clip_grad_norm_(model.parameters(), 1.5)
                optimizer.step()
                total += float(loss.detach()) * int(masked.sum())
                count += int(masked.sum())
            history.append(
                {
                    "stage": "ibm_masked_pretraining",
                    "epoch": epoch + 1,
                    "loss": total / max(count, 1),
                }
            )
    best_state, best_loss, patience = None, float("inf"), 0
    for epoch in range(args.epochs):
        model.train()
        total, count = 0.0, 0
        for batch in loader:
            x, rounds, basis, logical, v12, graph_id, y = move(batch, device)
            mask_probability = 0.2 if arm["input_mask"] else 0.0
            residual, direct, reconstruction, observed = model(
                x,
                rounds,
                basis,
                logical,
                graph_id,
                arm["use_graph"],
                arm["dynamic_mode"],
                mask_probability,
            )
            residual_target = (y != v12).float()
            loss = nn.functional.binary_cross_entropy_with_logits(
                residual, residual_target
            )
            loss = loss + 0.2 * nn.functional.binary_cross_entropy_with_logits(
                direct, y.float()
            )
            if mask_probability:
                active = (
                    torch.arange(7, device=device)[None, :, None]
                    < rounds[:, None, None]
                ).expand(-1, -1, 8)
                masked = active & ~observed
                if masked.any():
                    loss = loss + 0.1 * nn.functional.binary_cross_entropy_with_logits(
                        reconstruction[masked], x.reshape(-1, 7, 8)[masked]
                    )
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.5)
            optimizer.step()
            total += float(loss.detach()) * len(y)
            count += len(y)
        validation_probability = predict(
            model,
            validation,
            device,
            args.batch_size * 2,
            arm["use_graph"],
            arm["dynamic_mode"],
        )
        residual_target = (validation["y"] != validation["v12"]).astype(np.float32)
        clipped = np.clip(validation_probability, 1e-6, 1 - 1e-6)
        validation_loss = float(
            -np.mean(
                residual_target * np.log(clipped)
                + (1 - residual_target) * np.log(1 - clipped)
            )
        )
        history.append(
            {
                "stage": "ibm_supervised_residual",
                "epoch": epoch + 1,
                "training_loss": total / count,
                "validation_residual_bce": validation_loss,
            }
        )
        if validation_loss < best_loss - 1e-5:
            best_loss = validation_loss
            best_state = {
                key: value.detach().cpu().clone()
                for key, value in model.state_dict().items()
            }
            patience = 0
        else:
            patience += 1
            if patience >= 3:
                break
    if best_state is None:
        raise RuntimeError("training did not produce a checkpoint")
    model.load_state_dict(best_state)
    validation_probability = predict(
        model,
        validation,
        device,
        args.batch_size * 2,
        arm["use_graph"],
        arm["dynamic_mode"],
    )
    evaluation_probability = predict(
        model,
        evaluation,
        device,
        args.batch_size * 2,
        arm["use_graph"],
        arm["dynamic_mode"],
    )
    thresholds, threshold_audit = {}, {}
    for basis_value, basis_name in ((0, "X"), (1, "Z")):
        thresholds[basis_value], threshold_audit[basis_name] = select_threshold(
            validation_probability, validation, basis_value
        )
    candidate, result = evaluate(evaluation_probability, evaluation, thresholds)
    report = {
        "version": "V161",
        "description": "IBM-native dynamic detector-event coactivity attention V12 residual decoder",
        "arm": args.arm,
        "external_training_data_or_weights": False,
        "training_evidence": "preserved real IBM hardware shots only",
        "dynamic_event_mode": arm["dynamic_mode"],
        "parameter_count": sum(p.numel() for p in model.parameters()),
        "training_domains": train_names,
        "validation_domain": args.validation_domain,
        "evaluation_domain": args.evaluation_domain,
        "held_evaluation_labels_used_for_training_or_threshold": False,
        "graph_records": len(tables.provenance),
        "exact_graph_fraction": {
            name: float(np.mean(loaded[name]["graph_id"] != 0)) for name in DOMAINS
        },
        "thresholds": {"X": thresholds[0], "Z": thresholds[1]},
        "threshold_audit": threshold_audit,
        "evaluation": result,
        "promotion_candidate": (
            result["X"]["ci95_lower_pp"] > 0
            and result["Z"]["ci95_lower_pp"] > 0
        ),
        "history": history,
        "graph_provenance": tables.provenance,
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "result.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    np.savez_compressed(
        args.output / "held_predictions.npz",
        probability=evaluation_probability.astype(np.float32),
        candidate=candidate,
        v12=evaluation["v12"],
        labels=evaluation["y"],
        basis=evaluation["basis"],
        source_index=evaluation["source_index"],
    )
    torch.save(
        {
            "model_state_dict": best_state,
            "arm": args.arm,
            "width": args.width,
            "graph_file_hashes": [
                row["sha256"] for row in tables.provenance
            ],
        },
        args.output / "model.pt",
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
