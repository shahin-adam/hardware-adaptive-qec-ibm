"""Stratified paired analysis for the V498 routing-stability diagnostic."""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
x = json.loads((HERE / "V498_RESULTS.json").read_text())
rng = np.random.default_rng(49801)

raw = np.concatenate([np.asarray(r["raw_failure_bits"], np.uint8) for r in x["rows"]])
decoded = np.concatenate([np.asarray(r["decoded_failure_bits"], np.uint8) for r in x["rows"]])
fast = np.concatenate([np.asarray(r["consensus_fast_bits"], bool) for r in x["rows"]])
disagree = np.concatenate([np.asarray(r["valid_but_logically_disagree_bits"], bool) for r in x["rows"]])
delta = raw.astype(int) - decoded.astype(int)


def summarize(indices):
    indices = np.asarray(indices, int)
    means = np.empty(20000)
    for begin in range(0, len(means), 500):
        end = min(len(means), begin+500)
        chosen = indices[rng.integers(0, len(indices), (end-begin, len(indices)))]
        means[begin:end] = 100 * delta[chosen].mean(axis=1)
    return {"shots": int(len(indices)), "gain_pp": float(100*delta[indices].mean()),
            "paired_bootstrap_95_ci_pp": [float(v) for v in np.quantile(means, [.025,.975])]}


offsets, start = [], 0
for row in x["rows"]:
    stop = start + row["shots"]
    offsets.append((row["tag"], np.arange(start, stop)))
    start = stop

definitions = {
    "basis": {"x": ("_x_",), "z": ("_z_",)},
    "distance": {"d5": ("_d5_",), "d7": ("_d7_",)},
    "backend": {"fez": ("ibm_fez_",), "marrakesh": ("ibm_marrakesh_",)},
    "distance_basis": {"d5_x": ("_d5_","_x_"), "d5_z": ("_d5_","_z_"),
                       "d7_x": ("_d7_","_x_"), "d7_z": ("_d7_","_z_")},
}
strata = {}
for dimension, values in definitions.items():
    strata[dimension] = {}
    for label, tokens in values.items():
        idx = np.concatenate([i for tag, i in offsets if all(t in tag for t in tokens)])
        strata[dimension][label] = summarize(idx)

payload = {
    "experiment": "V498_MULTISEED_RELAY_CONSENSUS_ANALYSIS",
    "shots": int(len(raw)), "closure_fraction": 1.0,
    "overall": summarize(np.arange(len(raw))),
    "fast": summarize(np.flatnonzero(fast)), "escalated": summarize(np.flatnonzero(~fast)),
    "consensus_fast_fraction": float(fast.mean()),
    "all_valid_but_logically_disagree_fraction": float(disagree.mean()),
    "weighted_ms_per_shot": float(sum(r["ms_per_shot"]*r["shots"] for r in x["rows"])/len(raw)),
    "mean_per_seed_valid_fraction": float(np.mean([v for r in x["rows"] for v in r["per_seed_valid_fractions"]])),
    "strata": strata,
    "decision": (
        "Reject five-seed unanimity as a production router: it reduces fast-path coverage to 2.865%, "
        "costs 5.797 ms/shot, and 23.633% of shots have all seeds close but disagree logically. "
        "Accuracy remains diagnostic on reused data and every required subgroup CI includes zero."
    ),
}
(HERE / "V498_SUMMARY.json").write_text(json.dumps(payload, indent=2)+"\n")
print(json.dumps(payload, indent=2))
