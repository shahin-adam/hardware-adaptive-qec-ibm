# Learning Under Hardware Shift: Neural Decoding Across Superconducting Quantum Processors

Code and data for the paper of the same name, accepted to the **Australasian
Data Mining Conference (AusDM) 2026, Application Track**.

**Shahin Adam · Rani Adam · Weisheng Si · Simeon J. Simoff · Quang Vinh Nguyen**
Western Sydney University

This repository contains the artefacts behind the paper and nothing else: the
decoder implementations it evaluates, the per-shot scored predictions for the
confirmation jobs, and scripts that regenerate the paper's tables and ablations
from that data.

---

## Reproduce the headline number

```bash
git clone https://github.com/shahin-adam/hardware-adaptive-qec-ibm
cd hardware-adaptive-qec-ibm
pip install -r requirements.txt
python reproduce_table3.py
```

Runs in a few seconds. Expected output:

```
job  backend           shots     MWPM    model  gain pp           95% CI   McNemar p   check
------------------------------------------------------------------------------------------------
K1   ibm_kingston      86400   0.3500   0.3364     1.36  (from results/)    8.85e-46   json only
K2   ibm_kingston      86400   0.3641   0.3553     0.88    [+0.70,+1.07]    5.23e-21   MATCH
K3   ibm_kingston      86400   0.3458   0.3339     1.19    [+1.00,+1.38]    2.56e-34   MATCH
K4   ibm_kingston      86400   0.3468   0.3315     1.53    [+1.34,+1.72]    1.77e-56   MATCH
K5   ibm_kingston      86400   0.3178   0.3047     1.31    [+1.13,+1.49]    1.10e-44   MATCH
V25  ibm_fez           86400   0.4595   0.4583     0.13    [-0.02,+0.28]    1.00e-01   MATCH
M1   ibm_marrakesh     86400   0.4554   0.4525     0.28    [+0.10,+0.47]    2.50e-03   MATCH
------------------------------------------------------------------------------------------------
pooled K3-K5 (259,200 shots): MWPM 0.3368 -> model 0.3234  = 1.34 pp  [+1.23,+1.45]
relative 4.0%  p=2.33e-130
```

`MATCH` means the logical error rate recomputed from the per-shot arrays agrees
with the committed confirmation JSON to within 1e-6. The script refits nothing
and loads no model — the predictions were frozen before scoring, so the table is
reproduced arithmetically.

### Reproduce the ablations

```bash
python reproduce_selector_ablation.py   # paper §4.3.1
python reproduce_guard_ablation.py      # paper §5.1.6
```

---

## Note on a corrected file name

An earlier release of this repository shipped a file called `scored_F1.npz` and
labelled it job **F1**. That was wrong, and it is corrected here.

That file is the **V25 cross-backend transfer confirmation** — the Kingston-trained
decoder applied to `ibm_fez` without retuning, frozen 2026-07-17, MWPM 45.955% →
45.826%. The paper's job **F1** is a different `ibm_fez` block: the hard-syndrome
expert confirmation, MWPM 46.01% → 45.04%.

Both are now released under names that match their frozen records:

| File | What it is | MWPM → model |
|---|---|---|
| `data/transfer_fez_V25.npz` | V25 cross-backend transfer (was mislabelled `scored_F1.npz`) | 45.955% → 45.826% |
| `data/expert_F1.npz` | paper job **F1**, hard-syndrome expert, 108,000 shots | 46.015% → 45.041% |
| `data/scored_F2.npz` | paper job **F2**, reproduces Table 5 | 46.513% → 46.369% |

Anyone who cited or scripted against the old `scored_F1.npz` should switch to
`transfer_fez_V25.npz`; the contents are unchanged, only the name is.

---

## Three results on `ibm_fez`, and how to tell them apart

The paper reports more than one decoder on Fez. They are different experiments
and the distinction is the point of §4.5:

| | model | shots | MWPM → model | gain |
|---|---|---:|---|---|
| **V25 transfer** | relational decoder, **transferred from Kingston without retuning** | 86,400 | 45.955% → 45.826% | +0.13 pp, **not significant** (p = 0.10) |
| **F2** (Table 5) | same transferred decoder, second Fez block | 86,400 | 46.513% → 46.385% | +0.13 pp, **not significant** (p = 0.10) |
| **F1** (§4.5.1) | hard-syndrome XGBoost expert, **fitted against Fez statistics** | 108,000 | 46.015% → 45.041% | **+0.97 pp**, p < 0.001 |
| **F2, BP-OSD** (Table 5) | classical expert, priors rebuilt for Fez | 86,400 | 46.513% → 45.708% | **+0.80 pp**, p < 0.001 |

The transferred policy is deliberately null on both Fez blocks: a policy learned
on Kingston does not transfer. The backend-specific experts do help. That
contrast — classical decoder diversity transfers where a learned routing policy
does not — is the paper's cross-device finding.

### Why job F1 is scored on 108,000 shots

Every other job withholds a 21,600-shot context prefix. F1 does not, and the
reason is a property of that expert rather than an exception to the protocol: the
prefix is withheld only for policies that estimate drift statistics *from the job
they are then scored on*. The hard-syndrome expert estimates nothing from its
confirmation job — it was frozen against a separate 9,000-shot Fez development
block beforehand — so all 108,000 shots are untouched test data.

The result does not depend on this. Restricting the same frozen predictions to
the 86,400-shot per-configuration suffix used elsewhere gives **+0.98 pp
(95% CI 0.71–1.24)** against **+0.97 pp (95% CI 0.74–1.21)** on the full job.

---

## The result

The task is decoding quantum error-correction syndromes, treated as structured
spatio-temporal data under distribution shift. The baseline is minimum-weight
perfect matching (MWPM), the standard decoder. The models are a relational
decoder over detection-event tokens and an extended variant adding dynamic
event-coactivity attention.

**Within-backend** (`ibm_kingston`), pooling K3–K5 for 259,200 scored shots, the
relational decoder reduces logical error by **1.34 percentage points**, a 4.0%
relative reduction, p = 2.3e-130. This is the paper's primary claim.

**Across backends** the gain largely disappears: both Fez blocks give +0.13 pp
(not significant) and `ibm_marrakesh` +0.28 pp. That gap is the hardware shift
the paper is about, and it is reported here rather than smoothed over.

### The two deployment safeguards came out differently

`reproduce_selector_ablation.py` and `reproduce_guard_ablation.py` print the
evidence for both. In short:

**The selector works.** On K6 it routes 1.97% of shots to BP-OSD. BP-OSD applied
to *every* shot is worse than the neural decoder (35.00% vs 34.59%), yet routing
that 1.97% improves on the decoder alone by **+0.17 pp [0.08, 0.27]**. It manages
this by discrimination: BP-OSD is **8.74 pp better** on the shots the selector
routes and **0.60 pp worse** on the shots it declines — a separation of 9.33 pp.
That skill degrades across backends (9.33 → 6.92 → 0.51 pp) rather than
transferring.

**The guard does not.** Ablated against an always-apply baseline it *reduces*
mean gain on all six jobs — 0.18–0.71 pp within backend — and on no job does it
prevent a statistically significant loss. Its frozen allow-list rejects the (Z,7)
cohort. Across the six jobs in that ablation the decoder's Z7 advantage reaches +0.75 to +3.46 pp on the four `ibm_kingston` blocks, and on the separate selector job K6 it is larger still at +4.44 pp
and which the selector routes most heavily. We report this rather than the
favourable guard-versus-MWPM comparison, which does not isolate the guard's
contribution.

---

## Protocol

Every job is 108,000 shots from a single IBM Quantum backend, spanning **twelve
configurations** — two bases × three round counts × two logical operators — of
9,000 shots each. The split is a **per-configuration suffix**: within every
configuration the first 1,800 shots are held out as label-free context and the
final 7,200 are scored, giving 21,600 context and 86,400 scored.

Splitting is by whole execution block, never at random shot level — random splits
leak calibration-block characteristics across the boundary and inflate apparent
gains. The scored set was examined only after the decoding policy was frozen;
`results/*.json` record the freeze timestamp and the model hashes.

The split is recomputable from the released arrays rather than asserted:

```python
z = np.load("data/scored_K3.npz"); md, si = z["metadata"], z["sample_index"]
for cell in np.unique(md, axis=0):          # 12 configurations
    s = si[(md == cell).all(1)]             # 7200 shots each,
    assert len(s) == 7200 and (np.diff(s) == 1).all()   # contiguous
```

---

## Layout

```
reproduce_table3.py             regenerates Table 3 and checks it against results/
reproduce_selector_ablation.py  selector factorial, discrimination, routing (§4.3.1)
reproduce_guard_ablation.py     drift-guard ablation vs always-apply (§5.1.6)
data/scored_K2-K5.npz           per-shot arrays, ibm_kingston
data/scored_M1.npz              per-shot arrays, ibm_marrakesh
data/transfer_fez_V25.npz       V25 cross-backend transfer, ibm_fez
data/scored_F2.npz              job F2, ibm_fez, with BP-OSD + route (Table 5)
data/selector_K6.npz            job K6, ibm_kingston, with BP-OSD + route (Table 4)
data/selector_fez_V25.npz       V25 block with BP-OSD + route
data/expert_F1.npz              job F1 hard-syndrome expert, 108,000 shots
results/<job>.json              frozen confirmation: LER, gain, CI, McNemar p,
                                per-configuration breakdown, freeze time, hashes
decoders/                       relational_decoder.py, extended_relational_decoder.py
training/                       training entry point and IBM circuit-graph tensor builder
requirements.txt                runtime dependency for the scripts (numpy)
```

### Array reference

| Array | Meaning | Present in |
|---|---|---|
| `labels` | ground-truth logical outcome | all |
| `mwpm` | MWPM baseline prediction | all |
| `candidate` | released decoder output for that job | all except `expert_F1` |
| `v12` | extended relational decoder prediction | selector files, `scored_F2` |
| `osd` | BP-OSD prediction | selector files, `scored_F2` |
| `route` | per-shot selector route flag | selector files, `scored_F2` |
| `p_left`, `p_right` | the two benefit selectors' scores | selector files, `scored_F2` |
| `residual_probability` | model's residual-flip probability | `scored_K*`, `transfer_fez_V25`, `scored_M1` |
| `v10_probability`, `v12_probability` | component decision probabilities | `scored_K*`, `transfer_fez_V25`, `scored_M1` |
| `prediction_hard_only` and three soft variants | expert predictions | `expert_F1` |
| `metadata` | `[code distance, basis, rounds, logical index]` | all |
| `sample_index` | index into the original 108,000-shot job | `scored_K*`, `transfer_fez_V25`, `scored_M1` |

`metadata` columns are `distance` (always 3), `basis` (0 = X, 1 = Z), `rounds`
(3, 5 or 7) and `logical index` (0 or 1) — **12 configurations of 7,200 shots
each**. Marginalising over the logical index gives the six basis/round cohorts of
14,400 shots used for the per-cohort breakdowns in `results/*.json`.

The decoder's decision rule is recoverable from these arrays alone:

```
candidate = mwpm XOR (residual_probability >= 0.5075)
```

reproducing every released prediction bit-exactly, with one documented exception:
the **(X, 7) configuration returns unmodified MWPM** regardless of
`residual_probability`. Its MWPM error rate is 48.8–49.6%, indistinguishable from
chance; the paper assigns that cohort an exact-MWPM fallback (§3.4.2).

Likewise, for the selector files:

```
candidate = where(route, osd, v12)
```

holds exactly on all three.

---

## Scope and limits

- **K1 and K7 have no per-shot file.** Their arrays were not retained; the
  committed confirmation JSON is reported instead. Neither is part of the pooled
  headline (K3–K5), so no reported number depends on them, but they cannot be
  independently recomputed from this repository.
- **The drift guard is a per-cohort policy, not a per-shot classifier.** It makes
  six decisions per job, one per basis/round cohort. Cohorts the guard rejects
  show a gain of exactly 0.00 pp by construction, because rejection means the
  output *is* unmodified MWPM.
- **Raw IBM job payloads are not included.** What ships is the processed
  per-shot representation, which is what the tables are computed from. The raw
  payloads add hardware account metadata and roughly two orders of magnitude in
  size without changing any reported number.
- **Training is not reproducible from this repository alone** — it needs the
  context-split syndromes and calibration snapshots, which are not included.
  The frozen predictions are, so every result released as a per-shot file is checkable; K1 and K7 are the exceptions noted above and are reported from their confirmation records.
- **`decoders/` and `training/` are reference implementations, not
  runnable entry points.** They are the model code as run, carrying internal
  version numbers (V125, V161) from the development history, but they import
  PyTorch and several development modules that are not redistributed, so
  executing them directly raises `ModuleNotFoundError`. That is expected.
  `requirements.txt` therefore lists only what the `reproduce_*.py` scripts
  need, which is numpy alone; every published number is regenerated from the
  frozen per-shot arrays without loading a model.
- All confirmations use code distance 3. Distance 5 approached 50% logical
  failure from routing overhead and is excluded, as stated in the paper.

---

## Related work in progress

This paper is one result from a broader programme on decoders that adapt to the
hardware they run on. Other strands are active and unpublished; they are not part
of this paper and are not included in this repository. Enquiries to the
corresponding author.

---

## Citation

```bibtex
@inproceedings{adam2026hardwareshift,
  title     = {Learning Under Hardware Shift: Neural Decoding Across
               Superconducting Quantum Processors},
  author    = {Adam, Shahin and Adam, Rani and Si, Weisheng and
               Simoff, Simeon J. and Nguyen, Quang Vinh},
  booktitle = {Proceedings of the Australasian Data Mining Conference (AusDM)},
  year      = {2026},
  note      = {Application Track}
}
```

Hardware access was provided through IBM Quantum. The results are the authors'
own and do not represent IBM.
