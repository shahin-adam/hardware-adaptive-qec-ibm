# Hardware-Adaptive QEC Progress

Public, sanitized progress record for a Western Sydney University quantum-error-correction research programme.

## Project team

- Principal Investigator and academic supervisor: Dr Weisheng, Western Sydney University.
- Lead student researcher and technical implementer: Shahin Adam, Western Sydney University student ID 22228049.

## Research context

This repository records a sanitized preliminary study of approaches for reducing logical quantum-error-correction error rates across two complementary bases. We report aggregate baseline and candidate error percentages from controlled development evaluations. Dr Weisheng is the academic supervisor and Shahin Adam is the lead student researcher; all work remains subject to academic review.

Only experiment identifiers, aggregate percentages, evidence level, and target status are published here. Current methods, model designs, private datasets, credentials, checkpoints, next-step hypotheses, and internal research documents are intentionally excluded while manuscript preparation is in progress.

## Leading full-denominator real-hardware result

| Version | X error | Z error | Pooled baseline | Pooled candidate | Improvement | Relative reduction | Coverage | Evidence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| V12 | 38.42284% (baseline 39.21682%) | 26.25077% (baseline 28.14275%) | 33.67978% | 32.33681% | 1.34298 pp | 3.9875% | 100% (259,200 shots) | Repeated real-hardware evaluation |

The X and Z columns each contain 129,600 scored shots from the same three blocks. V12 improved X by 0.79398 percentage points and Z by 1.89198 points. The below-1% full-denominator target has not been achieved.

## Conditional real-hardware result requiring separate interpretation

| Version | Result | Coverage | Interpretation |
|---|---:|---:|---|
| V22 | 0.16204% conditional error | 5% selected coverage | Real-hardware postselection result; not below 1% on the full dataset |

This row is not ranked against the full-denominator table.

## Confirmed and repeated historical improvements

| Version | Baseline error | Candidate error | Absolute improvement | Relative reduction | Evidence |
| --- | ---: | ---: | ---: | ---: | --- |
| V12 | 33.67978% | 32.33681% | 1.34298 percentage points | 3.9875% | Repeated across 259,200 untouched evaluation shots |
| V38 | 35.7153% | 34.4201% | 1.29514 percentage points | 3.6265% | Independent 86,400-shot evaluation block |
| V39 | 46.512731% | 45.708333% | 0.804398 percentage points | 1.7294% | Independent 86,400-shot evaluation block |

Results use different datasets and comparators and must not be added together.

## Standard comparison fields

Every new result is reported with data source, dataset/block role, full or selected denominator, coverage, X error, Z error, pooled error, matched baseline, absolute improvement, relative reduction, statistical evidence, evidence level, and below-1% status. Versions are ranked only when dataset, circuit cohort, basis, denominator, and split role match. Cross-block percentages are contextual rather than direct head-to-head comparisons.

The canonical, complete registry is [ALL_VERSIONS.md](ALL_VERSIONS.md). It
contains an explicit row for every version from V1 through V135, including
archive gaps, null results, failed/sealed experiments, active development,
and confirmed evidence. README tables are intentionally summaries and must
not be interpreted as the complete version list.

## Current development status

V12 remains the validated winner. Recent opened-domain development results and active experiments are:

| Version | Best aggregate observation | Status |
| --- | --- | --- |
| V125 | 0.3327 pp pooled development gain | Not promoted; basis/domain gates failed |
| V128 | 0.3725 pp pooled development gain | Not promoted; basis/domain gates failed |
| V129 | 0.0749 pp pooled development gain | Not promoted; transfer safety gates failed |
| V130 | 0.3242 pp pooled development gain | X +0.6485 pp, Z unchanged; worst-fold gate failed |
| V131 | Corrected full transfer job running | Official NTU checkpoint transfer with matched scratch/frozen/fine-tuned controls |
| V132 | Smoke/full jobs running | V128 structural + V129 directional-Pathfinder gated fusion |
| V133 | Full 12-arm sweep running | Amplifies V130 metric auxiliaries with multitask and routing controls |
| V134 | Qwen result-audit job queued | Open-model research analyst; not a syndrome decoder or performance claim |
| V135 | Corrected smoke/full jobs queued | Direct V12 + V128 + V130 merged decoder |

These opened retrospective results are not independent confirmation evidence and do not replace V12.

Last public update: 24 July 2026, Australia/Sydney.

## Disclosure boundary

This repository does not publish current research ideas or implementation details. Full reproducibility material will be considered after manuscript preparation, institutional review, and security review.
