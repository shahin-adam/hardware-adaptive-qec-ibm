#!/usr/bin/env python3
"""Regenerate the drift-guard ablation tables from the released per-shot arrays.

Refits nothing. The decoder predictions and the guard allow-list were frozen
before scoring; this script is arithmetic over `data/scored_*.npz`.

The comparison that matters is guard vs *always-neural*, not guard vs MWPM.
Guard-vs-MWPM is favourable but does not isolate the guard's contribution: the
neural decoder is doing that work. Both are printed.
"""

import json
import os
from math import sqrt

import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
JOBS = ("K2", "K3", "K4", "K5", "transfer_fez_V25", "M1")
BACKEND = {"K2": "kingston", "K3": "kingston", "K4": "kingston",
           "K5": "kingston", "transfer_fez_V25": "fez",
           "M1": "marrakesh"}

# short display label so the table columns line up
LABEL = {"transfer_fez_V25": "V25"}

# Frozen per-cohort allow-list (V422, 31 Jul 2026). Applied unchanged to every
# job -- it is not re-selected per job.
ALLOW = {("X", 3), ("Z", 3), ("Z", 5)}

# metadata columns: [code distance, basis, rounds, logical index]
BASIS = {0: "X", 1: "Z"}
COHORTS = [(b, r) for b in ("X", "Z") for r in (3, 5, 7)]


def paired_gain(baseline, variant, labels):
    """Mean reduction in logical error, in percentage points, with 95% CI.

    Paired over shots: both decoders see the same syndromes, so the paired SE is
    the correct one and is much tighter than treating the two rates as
    independent.
    """
    diff = (baseline != labels).astype(np.int8) - (variant != labels).astype(np.int8)
    gain = diff.mean() * 100
    se = diff.std(ddof=1) / sqrt(len(diff)) * 100
    return gain, gain - 1.96 * se, gain + 1.96 * se


def load(job):
    z = np.load(os.path.join(DATA, f"scored_{job}.npz" if job.startswith("K") or job.startswith("M")
                 else f"{job}.npz"))
    md = z["metadata"]
    return {
        "labels": z["labels"],
        "mwpm": z["mwpm"],
        "neural": z["candidate"],
        "basis": np.array([BASIS[b] for b in md[:, 1]]),
        "rounds": md[:, 2],
    }


def guarded_output(d):
    """Guard on: neural where the cohort is allow-listed, MWPM everywhere else."""
    routed = np.zeros(len(d["labels"]), dtype=bool)
    for b, r in ALLOW:
        routed |= (d["basis"] == b) & (d["rounds"] == r)
    return np.where(routed, d["neural"], d["mwpm"]), routed


def main():
    results = {}

    print("=" * 100)
    print("Table 9  Drift guard: MWPM vs guard-on vs always-neural")
    print(f"         allow-list {sorted(ALLOW)}, applied unchanged to every job")
    print("=" * 100)
    print(f"{'job':<5}{'backend':<11}{'MWPM':>9}{'guard':>9}{'neural':>9}"
          f"{'guard-MWPM':>22}{'neural-MWPM':>13}{'guard-neural':>14}")
    print("-" * 100)

    for job in JOBS:
        d = load(job)
        guard, _ = guarded_output(d)
        lab, mwpm, neural = d["labels"], d["mwpm"], d["neural"]

        g, lo, hi = paired_gain(mwpm, guard, lab)
        n, _, _ = paired_gain(mwpm, neural, lab)

        print(f"{LABEL.get(job, job):<5}{BACKEND[job]:<11}"
              f"{(mwpm != lab).mean() * 100:>8.3f}%"
              f"{(guard != lab).mean() * 100:>8.3f}%"
              f"{(neural != lab).mean() * 100:>8.3f}%"
              f"{g:>10.3f} [{lo:+.3f},{hi:+.3f}]"
              f"{n:>13.3f}{g - n:>14.3f}")

        results[job] = {"guard_vs_mwpm": g, "ci": [lo, hi],
                        "neural_vs_mwpm": n, "guard_vs_neural": g - n}

    print("-" * 100)
    print("guard-neural is negative on every job: gating cohorts off costs gain.")

    print()
    print("=" * 100)
    print("Table 10  Always-neural gain by cohort -- what the guard accepted and rejected")
    print("          R = routed, . = rejected;  * = 95% CI excludes zero")
    print("=" * 100)
    header = f"{'cohort':<9}" + "".join(f"{LABEL.get(j, j):>13}" for j in JOBS)
    print(header)
    print("-" * len(header))

    per_cohort = {}
    for b, r in COHORTS:
        mark = "R" if (b, r) in ALLOW else "."
        line = f"{b}{r} {mark:<6}"
        row = {}
        for job in JOBS:
            d = load(job)
            m = (d["basis"] == b) & (d["rounds"] == r)
            g, lo, hi = paired_gain(d["mwpm"][m], d["neural"][m], d["labels"][m])
            star = "*" if lo > 0 else ("!" if hi < 0 else " ")
            line += f"{g:>12.3f}{star}"
            row[job] = {"gain": g, "ci": [lo, hi]}
        per_cohort[f"{b}{r}"] = {"decision": "route" if mark == "R" else "reject",
                                 "jobs": row}
        print(line)

    print("-" * len(header))
    print("(Z,7) is rejected by the frozen allow-list but is the strongest cohort")
    print("on Kingston (+0.75 to +3.46 pp, all CIs excluding zero). (X,7) is zero")
    print("everywhere because that configuration is gated off in the decoder.")

    out = {"table9": results, "table10": per_cohort}
    with open("guard_ablation_results.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote guard_ablation_results.json")


if __name__ == "__main__":
    main()
