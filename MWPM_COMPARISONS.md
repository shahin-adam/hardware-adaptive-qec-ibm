# Matched MWPM comparisons

This register includes only comparisons explicitly identified as MWPM/PyMatching in authoritative project records and evaluated on a matched block. Improvement is `MWPM LER - candidate LER`, in percentage points: positive means the candidate has lower LER than MWPM; negative means the candidate is worse. Values measured against CNN, Transformer, V12, raw readout, or another candidate are not silently relabeled as MWPM comparisons.

| Version | Candidate/method | Evaluation block | Candidate LER | Matched MWPM LER | Improvement vs MWPM (pp) | Evidence status | Notes/source provenance |
|---|---|---|---:|---:|---:|---|---|
| V1 | Four-model ensemble | Independent IBM confirmation, 120,000 shots | 44.0908% | 42.6442% | -1.4466 pp | Confirmed AI-vs-AI result; MWPM comparison is matched | Recovered master ledger E03/E04 and results/statistics record. The separate +1.2180 pp and +0.8383 pp values are not MWPM gains. |
| V20 | Selective overlay | Historical diagnostic scope | not recorded | not recorded | +1.24074 pp | Historical numeric record | The authoritative registry explicitly labels this value `vs MWPM`; component LERs were not defensibly recovered. |
| V21 | Selective overlay | Historical diagnostic/null scope | not recorded | not recorded | +1.53125 pp | Historical numeric record | The authoritative registry explicitly labels this value `vs MWPM`; component LERs were not defensibly recovered. |
| V38 | Historical candidate | Independent 86,400-shot evaluation block | 34.4201% | 35.7153% | +1.29514 pp | Confirmed | Detailed registry explicitly labels the comparison `vs MWPM`; the separate +0.17245 pp versus V12 and transfer result are different comparators. |
| V501 | Default DEM-based PyMatching/MWPM | Corrected-observable offline replay, 1,536 preserved real-IBM detector-event shots | 49.934896% | not applicable | not applicable | Accuracy null | MWPM is the evaluated decoder, not the comparator. Its benefit versus raw/no correction was +0.455729 pp, with paired-bootstrap 95% CI [-2.929688, +3.906250] pp. |

## Withdrawn range

V490–V500 are marked `withdrawn`, not assigned an MWPM gain. V501 found that the archived logical observable map was defective. Algebraic closure, timing, routing, and reproducibility facts unaffected by that map remain reported separately.

## Coverage

- Candidate-over-MWPM comparisons established: 4 versions.
- MWPM evaluated against raw/no correction, so candidate-over-MWPM delta is not applicable: 1 version (V501).
- Withdrawn logical-accuracy comparisons: 11 versions (V490–V500).
- MWPM comparison not established: 485 versions.

V487 reports a matched synthetic MWPM control across distance/basis slices, but it does not report a separate candidate-versus-MWPM improvement; its `MWPM Δ` therefore remains `not established`.
