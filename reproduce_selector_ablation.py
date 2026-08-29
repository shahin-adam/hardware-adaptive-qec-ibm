#!/usr/bin/env python3
"""Selector ablation -- the half of W3 that was blocked on locating K6.

Refits nothing. The selector was frozen before these jobs were scored; this is
arithmetic over the per-shot arrays.

Files:
  data/selector_K6.npz       job K6, ibm_kingston  (reproduces Table 4)
  data/selector_fez_V25.npz  V25 ibm_fez transfer block
  data/scored_F2.npz         job F2, ibm_fez       (reproduces Table 5)
"""

import os
from math import sqrt

import numpy as np

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
JOBS = [
    ("K6  kingston", "selector_K6.npz"),
    ("V25 fez     ", "selector_fez_V25.npz"),
    ("F2  fez     ", "scored_F2.npz"),
]


def gain(base, var, lab):
    """Paired reduction in logical error, percentage points, with 95% CI."""
    d = (base != lab).astype(np.int8) - (var != lab).astype(np.int8)
    g = d.mean() * 100
    se = d.std(ddof=1) / sqrt(len(d)) * 100 if len(d) > 1 else 0.0
    return g, g - 1.96 * se, g + 1.96 * se


def load(fn):
    z = np.load(os.path.join(D, fn))
    return {k: z[k] for k in z.files}


print("=" * 96)
print("Check: is `candidate` exactly the routed combination of v12 and osd?")
print("=" * 96)
for name, fn in JOBS:
    d = load(fn)
    recon = np.where(d["route"], d["osd"], d["v12"])
    bad = int((recon != d["candidate"]).sum())
    print(f"  {name}: candidate == where(route, osd, v12) -> "
          f"{'EXACT' if bad == 0 else f'{bad} mismatches'}")

print()
print("=" * 96)
print("Table B  Selector factorial: what each component contributes")
print("=" * 96)
print(f"{'job':<14}{'MWPM':>9}{'v12 only':>10}{'OSD only':>10}{'routed':>9}"
      f"{'route %':>9}{'routed-vs-v12 (95% CI)':>28}")
print("-" * 96)
for name, fn in JOBS:
    d = load(fn)
    lab = d["labels"]
    g, lo, hi = gain(d["v12"], d["candidate"], lab)
    print(f"{name:<14}"
          f"{(d['mwpm'] != lab).mean() * 100:>8.3f}%"
          f"{(d['v12'] != lab).mean() * 100:>9.3f}%"
          f"{(d['osd'] != lab).mean() * 100:>9.3f}%"
          f"{(d['candidate'] != lab).mean() * 100:>8.3f}%"
          f"{d['route'].mean() * 100:>8.2f}%"
          f"{g:>16.3f} [{lo:+.3f},{hi:+.3f}]")

print()
print("=" * 96)
print("Table C  Selector discrimination -- does it route the shots OSD actually helps?")
print("=" * 96)
print("If the selector has skill, OSD's advantage over v12 must be LARGE on the")
print("routed shots and ~zero or negative on the rest. A selector with no skill")
print("shows the same advantage in both columns.")
print()
print(f"{'job':<14}{'routed n':>9}{'OSD-v12 | routed':>22}"
      f"{'OSD-v12 | not routed':>24}{'discrimination':>16}")
print("-" * 96)
for name, fn in JOBS:
    d = load(fn)
    lab, r = d["labels"], d["route"].astype(bool)
    gr, lor, hir = gain(d["v12"][r], d["osd"][r], lab[r])
    gn, _, _ = gain(d["v12"][~r], d["osd"][~r], lab[~r])
    print(f"{name:<14}{r.sum():>9}"
          f"{gr:>10.3f} [{lor:+.2f},{hir:+.2f}]"
          f"{gn:>24.3f}{gr - gn:>16.3f}")

print()
print("=" * 96)
print("Table D  Where the selector routes -- by basis/round cohort")
print("=" * 96)
BN = {0: "X", 1: "Z"}
hdr = f"{'cohort':<9}" + "".join(f"{n.strip():>18}" for n, _ in JOBS)
print(hdr)
print("-" * len(hdr))
for b in (0, 1):
    for rd in (3, 5, 7):
        line = f"{BN[b]}{rd:<8}"
        for name, fn in JOBS:
            d = load(fn)
            md = d["metadata"]
            m = (md[:, 1] == b) & (md[:, 2] == rd)
            line += f"{d['route'][m].mean() * 100:>17.2f}%"
        print(line)
print("-" * len(hdr))
print("percentage of each cohort's shots routed to BP-OSD")
