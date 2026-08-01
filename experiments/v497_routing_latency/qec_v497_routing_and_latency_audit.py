"""V497: diagnose cascade routing and repeat latency on unchanged real IBM contracts.

No new decoder candidate is introduced. The experiment replays the V495 Relay
operating points, records per-shot route masks, and benchmarks sequential versus
batched execution on the same node after warm-up. Every accepted correction is
checked against H e = s.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import cudaq_qec as qec
import numpy as np

HERE = Path(__file__).resolve().parent
CONFIGS = [
    {"name": "relay_3x_pre3", "pre_iter": 3, "num_sets": 3, "gamma0": .3},
    {"name": "relay_3x_pre5", "pre_iter": 5, "num_sets": 3, "gamma0": .3},
    {"name": "relay_5x_pre5", "pre_iter": 5, "num_sets": 5, "gamma0": .3},
    {"name": "relay_5x_pre8", "pre_iter": 8, "num_sets": 5, "gamma0": .5},
]


def decoders(H, p, batch_size, cfg, seed):
    common = {"error_rate_vec": p, "max_iterations": 100,
              "use_sparsity": True, "bp_batch_size": batch_size}
    relay = qec.get_decoder(
        "nv-qldpc-decoder", H, **common, use_osd=False, bp_method=3,
        composition=1, gamma0=cfg["gamma0"], gamma_dist=[.1, .5],
        srelay_config={"pre_iter": cfg["pre_iter"], "num_sets": cfg["num_sets"],
                       "stopping_criterion": "FirstConv"}, bp_seed=seed,
    )
    fallback = qec.get_decoder("nv-qldpc-decoder", H, **common, use_osd=True, bp_method=0)
    return relay, fallback


def run_batch(H, O, p, S, raw, cfg, seed):
    relay, fallback = decoders(H, p, len(S), cfg, seed)
    rz = relay.decode_batch([s for s in S])
    errors, fast, bad = [None] * len(S), np.zeros(len(S), bool), []
    for i, (s, z) in enumerate(zip(S, rz)):
        e = (np.asarray(z.result) >= .5).astype(np.uint8)
        valid = bool(z.converged) and np.array_equal((H @ e) % 2, s.astype(np.uint8))
        if valid:
            errors[i], fast[i] = e, True
        else:
            bad.append(i)
    if bad:
        fz = fallback.decode_batch([S[i] for i in bad])
        for i, z in zip(bad, fz):
            errors[i] = (np.asarray(z.result) >= .5).astype(np.uint8)
    closure = np.asarray([np.array_equal((H @ e) % 2, s.astype(np.uint8))
                          for e, s in zip(errors, S)])
    predicted = np.asarray([int(((O @ e) % 2)[0]) if O.shape[0] else 0 for e in errors], np.uint8)
    decoded = predicted ^ raw
    return fast, decoded, closure


def timed_selected(H, O, p, S, raw, cfg, repeats=5):
    # Fresh decoder objects each repeat match realistic job setup; one unscored
    # warm-up removes first-launch/JIT effects from both execution modes.
    timings = {"batched_ms_per_shot": [], "sequential_ms_per_shot": []}
    run_batch(H, O, p, S[:min(8, len(S))], raw[:min(8, len(S))], cfg, 49700)
    for repeat in range(repeats):
        start = time.perf_counter()
        _, _, closure = run_batch(H, O, p, S, raw, cfg, 49800 + repeat)
        timings["batched_ms_per_shot"].append(1000 * (time.perf_counter()-start) / len(S))
        if not np.all(closure):
            raise RuntimeError("batched closure failure")

        relay, fallback = decoders(H, p, 1, cfg, 49900 + repeat)
        start = time.perf_counter()
        for s in S:
            z = relay.decode(s); e = (np.asarray(z.result) >= .5).astype(np.uint8)
            if not (bool(z.converged) and np.array_equal((H @ e) % 2, s.astype(np.uint8))):
                z = fallback.decode(s); e = (np.asarray(z.result) >= .5).astype(np.uint8)
            if not np.array_equal((H @ e) % 2, s.astype(np.uint8)):
                raise RuntimeError("sequential closure failure")
        timings["sequential_ms_per_shot"].append(1000 * (time.perf_counter()-start) / len(S))
    return timings


def conditional(raw, decoded, fast):
    delta = raw.astype(int) - decoded.astype(int)
    escalated = ~fast
    def group(mask):
        return {"shots": int(mask.sum()), "raw_ler": float(raw[mask].mean()),
                "decoded_ler": float(decoded[mask].mean()),
                "gain_pp": float(100 * delta[mask].mean())}
    return {
        "fast": group(fast), "escalated": group(escalated),
        "p_escalated_given_raw_failure": float(escalated[raw == 1].mean()),
        "p_escalated_given_raw_success": float(escalated[raw == 0].mean()),
        "difficulty_enrichment_pp": float(100 * (raw[escalated].mean() - raw[fast].mean())),
    }


contracts = sorted((HERE / "contracts").glob("*.npz"))
if not contracts:
    raise FileNotFoundError("contracts/*.npz missing")
records, masks_by_config, outcomes_by_config = [], {c["name"]: [] for c in CONFIGS}, {c["name"]: [] for c in CONFIGS}
timing_rows = []
for path_index, path in enumerate(contracts):
    x = np.load(path); H = np.ascontiguousarray(x["H"], np.uint8); O = np.ascontiguousarray(x["O"], np.uint8)
    p = np.asarray(x["error_rate_vec"], float); S = np.asarray(x["syndromes"], np.float32)
    raw = np.asarray(x["logical_failure"], np.uint8)
    for cfg_index, cfg in enumerate(CONFIGS):
        fast, decoded, closure = run_batch(H, O, p, S, raw, cfg, 497 + cfg_index)
        if not np.all(closure):
            raise RuntimeError(f"closure failed for {path.name} {cfg['name']}")
        masks_by_config[cfg["name"]].append(fast)
        outcomes_by_config[cfg["name"]].append(decoded)
        records.append({"tag": path.stem, "config": cfg["name"], "shots": len(raw),
                        "fast_bits": fast.astype(int).tolist(),
                        "raw_failure_bits": raw.astype(int).tolist(),
                        "decoded_failure_bits": decoded.astype(int).tolist(),
                        "conditional": conditional(raw, decoded, fast)})
    # Repeat timing on the unchanged V494 operating point for every contract.
    timing_rows.append({"tag": path.stem, **timed_selected(H, O, p, S, raw, CONFIGS[1])})

config_summary = {}
raw_all = np.concatenate([np.asarray(np.load(p)["logical_failure"], np.uint8) for p in contracts])
for cfg in CONFIGS:
    name = cfg["name"]; fast = np.concatenate(masks_by_config[name]); decoded = np.concatenate(outcomes_by_config[name])
    config_summary[name] = {"config": cfg, "conditional": conditional(raw_all, decoded, fast),
                            "fast_bits": fast.astype(int).tolist(),
                            "decoded_failure_bits": decoded.astype(int).tolist()}

route_agreement = []
for i, left in enumerate(CONFIGS):
    for right in CONFIGS[i+1:]:
        a = np.concatenate(masks_by_config[left["name"]]); b = np.concatenate(masks_by_config[right["name"]])
        union = np.logical_or(a, b).sum()
        route_agreement.append({"left": left["name"], "right": right["name"],
                                "identical_route_fraction": float(np.mean(a == b)),
                                "fast_set_jaccard": float(np.logical_and(a, b).sum()/union) if union else 1.0})

# Post-hoc diagnostic ceiling only: success if any tested unchanged operating
# point succeeds. It is not an implementable router and cannot be promoted.
outcome_stack = np.vstack([np.concatenate(outcomes_by_config[c["name"]]) for c in CONFIGS])
oracle_ler = float(np.min(outcome_stack, axis=0).mean())
payload = {"experiment": "V497_ROUTING_AND_LATENCY_AUDIT_REAL_IBM_REPLAY",
           "new_decoder_candidate": False, "all_final_corrections_closed": True,
           "records": records, "config_summary": config_summary,
           "route_agreement": route_agreement, "timing_repeats": timing_rows,
           "posthoc_oracle_ler": oracle_ler,
           "interpretation_gate": "Routing diagnosis only. No accuracy promotion, equivalence, or speed claim before paired CIs and repeated-timing summary."}
(HERE / "V497_RESULTS.json").write_text(json.dumps(payload, indent=2) + "\n")
print(json.dumps({"config_summary": {k:v["conditional"] for k,v in config_summary.items()},
                  "route_agreement": route_agreement, "timing_repeats": timing_rows,
                  "posthoc_oracle_ler": oracle_ler}, indent=2), flush=True)
