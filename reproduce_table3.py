#!/usr/bin/env python3
"""Reproduce Table 3 of the paper from the per-shot scored data.

Run with no arguments:

    python reproduce_table3.py

It reads each data/scored_<job>.npz, recomputes the logical error rate of the
minimum-weight perfect matching baseline and of the relational decoder, runs the
paired McNemar test over the same shots, and checks the result against the
committed results/<job>.json. Nothing is refit and no model is loaded -- these
are the frozen per-shot predictions, so the numbers are reproduced arithmetically
rather than retrained.

Requires only numpy.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
# Job -> (per-shot file stem, backend). "F1" in an earlier release of this
# repository pointed at the V25 cross-backend transfer confirmation, which is
# a different ibm_fez block from the paper's job F1 (the hard-syndrome expert,
# MWPM 46.01%). That file is now named transfer_fez_V25 after the frozen
# record it came from, and job F2 -- which Table 5 of the paper reports -- is
# released alongside it.
JOBS = [
    ("K1", "scored_K1", "ibm_kingston"),
    ("K2", "scored_K2", "ibm_kingston"),
    ("K3", "scored_K3", "ibm_kingston"),
    ("K4", "scored_K4", "ibm_kingston"),
    ("K5", "scored_K5", "ibm_kingston"),
    ("V25", "transfer_fez_V25", "ibm_fez"),
    ("M1", "scored_M1", "ibm_marrakesh"),
]


def mcnemar_p(better: int, worse: int) -> float:
    """Two-sided McNemar. Only discordant pairs carry information.

    Exact binomial for small discordant counts; the normal approximation with
    continuity correction above that, which is the standard form of the test and
    is accurate to many digits at the counts seen here (thousands per job).
    """
    n = better + worse
    if n == 0:
        return 1.0
    if n <= 1000:
        k = min(better, worse)
        tail = sum(math.comb(n, i) for i in range(k + 1)) / (2.0 ** n)
        return min(1.0, 2.0 * tail)
    z = (abs(better - worse) - 1) / math.sqrt(n)
    return math.erfc(z / math.sqrt(2.0))


def wilson_diff_ci(labels, base, cand):
    """95% CI on the paired difference in error rate, in percentage points.

    Paired data, so the variance comes from the discordant pairs alone; the
    shots where both decoders agree contribute nothing to the difference.
    """
    b = int(np.sum((base != labels) & (cand == labels)))
    w = int(np.sum((base == labels) & (cand != labels)))
    n = len(labels)
    diff = (b - w) / n
    se = np.sqrt((b + w) - (b - w) ** 2 / n) / n
    return 100 * (diff - 1.96 * se), 100 * (diff + 1.96 * se), b, w


def main() -> None:
    print(f"{'job':<4} {'backend':<15} {'shots':>7} {'MWPM':>8} {'model':>8} "
          f"{'gain pp':>8} {'95% CI':>16} {'McNemar p':>11}   check")
    print("-" * 96)

    for job, stem, backend in JOBS:
        npz = ROOT / "data" / f"{stem}.npz"
        ref_path = ROOT / "results" / f"{stem.replace('scored_', '')}.json"
        if not ref_path.exists():
            ref_path = ROOT / "results" / f"{stem}.json"
        ref = json.loads(ref_path.read_text())["overall"]

        if not npz.exists():
            # K1's per-shot arrays were not retained; its committed confirmation
            # is still reported so the table is complete.
            print(f"{job:<4} {backend:<15} {ref['shots']:>7} "
                  f"{ref['base_ler']:>8.4f} {ref['candidate_ler']:>8.4f} "
                  f"{ref['gain_percentage_points']:>8.2f} "
                  f"{'(from results/)':>16} {ref['mcnemar_p']:>11.2e}   "
                  "json only")
            continue

        d = np.load(npz)
        labels, base, cand = d["labels"], d["mwpm"], d["candidate"]

        base_ler = float(np.mean(base != labels))
        cand_ler = float(np.mean(cand != labels))
        gain = 100 * (base_ler - cand_ler)
        lo, hi, better, worse = wilson_diff_ci(labels, base, cand)
        p = mcnemar_p(better, worse)

        ok = (abs(base_ler - ref["base_ler"]) < 1e-6
              and abs(cand_ler - ref["candidate_ler"]) < 1e-6)

        print(f"{job:<4} {backend:<15} {len(labels):>7} "
              f"{base_ler:>8.4f} {cand_ler:>8.4f} {gain:>8.2f} "
              f"{f'[{lo:+.2f},{hi:+.2f}]':>16} {p:>11.2e}   "
              f"{'MATCH' if ok else 'MISMATCH'}")

    # The paper's primary within-backend claim pools three same-backend jobs.
    pooled = [j for j in ("K3", "K4", "K5")
              if (ROOT / "data" / f"scored_{j}.npz").exists()]
    if len(pooled) == 3:
        L = np.concatenate([np.load(ROOT / "data" / f"scored_{j}.npz")["labels"] for j in pooled])
        B = np.concatenate([np.load(ROOT / "data" / f"scored_{j}.npz")["mwpm"] for j in pooled])
        C = np.concatenate([np.load(ROOT / "data" / f"scored_{j}.npz")["candidate"] for j in pooled])
        bl, cl = float(np.mean(B != L)), float(np.mean(C != L))
        lo, hi, better, worse = wilson_diff_ci(L, B, C)
        print("-" * 96)
        print(f"pooled K3-K5 ({len(L):,} shots): MWPM {bl:.4f} -> model {cl:.4f}  "
              f"= {100*(bl-cl):.2f} pp  [{lo:+.2f},{hi:+.2f}]  "
              f"relative {100*(bl-cl)/bl:.1f}%  p={mcnemar_p(better, worse):.2e}")
        print("This is the paper's primary within-backend result.")


if __name__ == "__main__":
    main()

