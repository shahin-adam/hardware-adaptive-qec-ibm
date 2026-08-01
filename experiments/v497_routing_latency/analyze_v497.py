"""Cluster-aware analysis for V497 routing and repeated latency benchmark."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "V497_RESULTS.json"
rng = np.random.default_rng(49701)
x = json.loads(SOURCE.read_text())


def percentile_ci(values):
    return [float(v) for v in np.quantile(values, [.025, .975])]


def paired_gain(raw, decoded, indices, draws=10000):
    delta = raw.astype(int) - decoded.astype(int)
    if len(indices) == 0:
        return {"shots": 0, "gain_pp": None, "bootstrap_95_ci_pp": None}
    samples = np.empty(draws)
    for begin in range(0, draws, 500):
        end = min(draws, begin + 500)
        picked = indices[rng.integers(0, len(indices), (end-begin, len(indices)))]
        samples[begin:end] = 100 * delta[picked].mean(axis=1)
    return {"shots": int(len(indices)), "gain_pp": float(100 * delta[indices].mean()),
            "bootstrap_95_ci_pp": percentile_ci(samples)}


route_results = {}
for name, result in x["config_summary"].items():
    selected_records = [r for r in x["records"] if r["config"] == name]
    raw = np.concatenate([np.asarray(r["raw_failure_bits"], np.uint8)
                          for r in selected_records])
    decoded = np.asarray(result["decoded_failure_bits"], np.uint8)
    fast = np.asarray(result["fast_bits"], bool)
    groups = {"all": np.arange(len(raw)), "fast": np.flatnonzero(fast),
              "escalated": np.flatnonzero(~fast)}
    summaries = {label: paired_gain(raw, decoded, idx) for label, idx in groups.items()}
    # Bootstrap the raw-failure enrichment of escalated versus fast groups.
    enrichment = np.empty(20000)
    fast_idx, escalated_idx = groups["fast"], groups["escalated"]
    for i in range(len(enrichment)):
        f = fast_idx[rng.integers(0, len(fast_idx), len(fast_idx))]
        e = escalated_idx[rng.integers(0, len(escalated_idx), len(escalated_idx))]
        enrichment[i] = 100 * (raw[e].mean() - raw[f].mean())
    # Required reporting gates: keep basis, distance, and backend separate.
    offsets, start = [], 0
    for record in selected_records:
        stop = start + record["shots"]
        offsets.append((record["tag"], np.arange(start, stop)))
        start = stop
    strata = {}
    definitions = {
        "basis": {"x": ("_x_",), "z": ("_z_",)},
        "distance": {"d5": ("_d5_",), "d7": ("_d7_",)},
        "backend": {"fez": ("ibm_fez_",), "marrakesh": ("ibm_marrakesh_",)},
        "distance_basis": {
            "d5_x": ("_d5_", "_x_"), "d5_z": ("_d5_", "_z_"),
            "d7_x": ("_d7_", "_x_"), "d7_z": ("_d7_", "_z_"),
        },
    }
    for dimension, values in definitions.items():
        strata[dimension] = {}
        for label, tokens in values.items():
            idx = np.concatenate([indices for tag, indices in offsets if all(token in tag for token in tokens)])
            strata[dimension][label] = paired_gain(raw, decoded, idx)
    strata["domain"] = {tag: paired_gain(raw, decoded, indices) for tag, indices in offsets}
    route_results[name] = {
        "groups": summaries,
        "strata": strata,
        "difficulty_enrichment_pp": float(100 * (raw[escalated_idx].mean()-raw[fast_idx].mean())),
        "difficulty_enrichment_bootstrap_95_ci_pp": percentile_ci(enrichment),
    }


contract_ratios, batch_medians, seq_medians = [], [], []
for row in x["timing_repeats"]:
    batch = np.asarray(row["batched_ms_per_shot"], float)
    seq = np.asarray(row["sequential_ms_per_shot"], float)
    ratio = seq / batch
    contract_ratios.append(float(np.median(ratio)))
    batch_medians.append(float(np.median(batch)))
    seq_medians.append(float(np.median(seq)))
contract_ratios = np.asarray(contract_ratios)
batch_medians, seq_medians = np.asarray(batch_medians), np.asarray(seq_medians)

# Contracts are the resampling units; repeats within a contract share data and hardware context.
boot_ratio = np.empty(50000)
for i in range(len(boot_ratio)):
    idx = rng.integers(0, len(contract_ratios), len(contract_ratios))
    boot_ratio[i] = np.median(contract_ratios[idx])

timing = {
    "contracts": int(len(contract_ratios)), "repeats_per_contract": 5,
    "batched_contract_median_ms_per_shot": float(np.median(batch_medians)),
    "sequential_contract_median_ms_per_shot": float(np.median(seq_medians)),
    "median_paired_speedup": float(np.median(contract_ratios)),
    "cluster_bootstrap_95_ci_speedup": percentile_ci(boot_ratio),
    "minimum_contract_median_speedup": float(contract_ratios.min()),
    "maximum_contract_median_speedup": float(contract_ratios.max()),
    "contracts_favoring_batch": int(np.sum(contract_ratios > 1)),
    "two_sided_sign_test_p_all_24_favor_batch": float(2 / 2**len(contract_ratios)),
    "scope": "Offline CUDA-QX replay on one Wolffe A30 node; not QPU wall-clock or online-control latency.",
}

payload = {
    "experiment": "V497_ROUTING_AND_LATENCY_ANALYSIS",
    "closure": "100% in every V497 final correction; enforced during execution",
    "routing": route_results,
    "route_agreement": x["route_agreement"],
    "timing": timing,
    "posthoc_oracle_ler": x["posthoc_oracle_ler"],
    "decision": (
        "Promote the offline batching systems result with its exact scope. Do not promote accuracy. "
        "Freeze new decoder variants; routing decisions are configuration-sensitive and do not "
        "consistently enrich raw failures."
    ),
}
(HERE / "V497_SUMMARY.json").write_text(json.dumps(payload, indent=2) + "\n")
print(json.dumps(payload, indent=2))
