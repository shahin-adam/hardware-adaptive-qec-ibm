"""V498: multi-seed Relay consensus as a routing-stability diagnostic.

The correction algorithm and fallback are unchanged. A shot takes the fast path
only when every independently seeded Relay run converges, closes H e = s, and
agrees on the observable logical effect O e. Reused shots make this diagnostic,
not independent confirmation.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import cudaq_qec as qec
import numpy as np

HERE = Path(__file__).resolve().parent
SEEDS = [4981, 4982, 4983, 4984, 4985]
CFG = {"pre_iter": 5, "num_sets": 3, "gamma0": .3}


def make_relay(H, p, batch_size, seed):
    return qec.get_decoder(
        "nv-qldpc-decoder", H, error_rate_vec=p, max_iterations=100,
        use_sparsity=True, bp_batch_size=batch_size, use_osd=False,
        bp_method=3, composition=1, gamma0=CFG["gamma0"], gamma_dist=[.1, .5],
        srelay_config={"pre_iter": CFG["pre_iter"], "num_sets": CFG["num_sets"],
                       "stopping_criterion": "FirstConv"}, bp_seed=seed,
    )


rows = []
for path in sorted((HERE / "contracts").glob("*.npz")):
    x = np.load(path); H = np.ascontiguousarray(x["H"], np.uint8); O = np.ascontiguousarray(x["O"], np.uint8)
    p = np.asarray(x["error_rate_vec"], float); S = np.asarray(x["syndromes"], np.float32)
    raw = np.asarray(x["logical_failure"], np.uint8); n = len(S)
    start = time.perf_counter()
    seed_errors, seed_valid, seed_logical = [], [], []
    for seed in SEEDS:
        results = make_relay(H, p, n, seed).decode_batch([s for s in S])
        errors = [(np.asarray(z.result) >= .5).astype(np.uint8) for z in results]
        valid = np.asarray([bool(z.converged) and np.array_equal((H @ e) % 2, s.astype(np.uint8))
                            for z, e, s in zip(results, errors, S)])
        logical = np.asarray([int(((O @ e) % 2)[0]) if O.shape[0] else 0 for e in errors], np.uint8)
        seed_errors.append(errors); seed_valid.append(valid); seed_logical.append(logical)
    valid_stack, logical_stack = np.vstack(seed_valid), np.vstack(seed_logical)
    consensus = np.all(valid_stack, axis=0) & np.all(logical_stack == logical_stack[0], axis=0)
    final_errors = [None] * n
    for i in np.flatnonzero(consensus):
        final_errors[i] = seed_errors[0][i]
    fallback_idx = np.flatnonzero(~consensus)
    if len(fallback_idx):
        fallback = qec.get_decoder(
            "nv-qldpc-decoder", H, error_rate_vec=p, max_iterations=100,
            use_sparsity=True, bp_batch_size=len(fallback_idx), use_osd=True, bp_method=0,
        )
        results = fallback.decode_batch([S[i] for i in fallback_idx])
        for i, z in zip(fallback_idx, results):
            final_errors[i] = (np.asarray(z.result) >= .5).astype(np.uint8)
    elapsed = time.perf_counter() - start
    closure = np.asarray([np.array_equal((H @ e) % 2, s.astype(np.uint8))
                          for e, s in zip(final_errors, S)])
    if not np.all(closure):
        raise RuntimeError(f"closure failure in {path.name}")
    prediction = np.asarray([int(((O @ e) % 2)[0]) if O.shape[0] else 0 for e in final_errors], np.uint8)
    decoded = raw ^ prediction
    # Agreement conditional on all seeds returning an algebraically valid answer.
    all_valid = np.all(valid_stack, axis=0)
    disagreement = all_valid & ~np.all(logical_stack == logical_stack[0], axis=0)
    rows.append({
        "tag": path.stem, "shots": n, "seed_count": len(SEEDS),
        "consensus_fast_bits": consensus.astype(int).tolist(),
        "all_seed_valid_bits": all_valid.astype(int).tolist(),
        "valid_but_logically_disagree_bits": disagreement.astype(int).tolist(),
        "per_seed_valid_fractions": valid_stack.mean(axis=1).tolist(),
        "consensus_fast_fraction": float(consensus.mean()),
        "valid_but_logically_disagree_fraction": float(disagreement.mean()),
        "raw_failure_bits": raw.astype(int).tolist(),
        "decoded_failure_bits": decoded.astype(int).tolist(),
        "syndrome_closure_fraction": float(closure.mean()),
        "ms_per_shot": 1000 * elapsed / n,
    })

payload = {
    "experiment": "V498_MULTISEED_RELAY_CONSENSUS_ROUTING_REAL_IBM_REPLAY",
    "seeds": SEEDS, "relay_config": CFG, "rows": rows,
    "gate": "Diagnostic on reused shots. Require 100% closure and separate X/Z/distance/backend intervals; no independent accuracy claim.",
}
(HERE / "V498_RESULTS.json").write_text(json.dumps(payload, indent=2) + "\n")
print(json.dumps({"rows": [{k:r[k] for k in ("tag", "shots", "consensus_fast_fraction",
      "valid_but_logically_disagree_fraction", "syndrome_closure_fraction", "ms_per_shot")} for r in rows]}, indent=2), flush=True)
