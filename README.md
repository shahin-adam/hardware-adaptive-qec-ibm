# Hardware-Adaptive QEC Progress

Public, sanitized progress record for a Western Sydney University quantum-error-correction research programme.

## Project team

- Principal Investigator and academic supervisor: Dr Weisheng, Western Sydney University.
- Lead student researcher and technical implementer: Shahin Adam, Western Sydney University student ID 22228049.

## Research context

This repository records a sanitized preliminary study of approaches for reducing logical quantum-error-correction error rates across two complementary bases. We report aggregate baseline and candidate error percentages from controlled development evaluations. Dr Weisheng is the academic supervisor and Shahin Adam is the lead student researcher; all work remains subject to academic review.

Only experiment identifiers, aggregate percentages, evidence level, and target status are published here. Current methods, model designs, private datasets, credentials, checkpoints, next-step hypotheses, and internal research documents are intentionally excluded while manuscript preparation is in progress.

## Leading full-denominator real-hardware result

| Version | X error | Z error | Pooled baseline | Pooled candidate | Improvement | Relative reduction | Coverage | LER/cycle | Evidence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| V12 | 38.42284% (baseline 39.21682%) | 26.25077% (baseline 28.14275%) | 33.67978% | 32.33681% | 1.34298 pp | 3.9875% | 100% (259,200 shots) | Not validated | Repeated real-hardware evaluation |

The X and Z columns each contain 129,600 scored shots from the same three blocks. V12 improved X by 0.79398 percentage points and Z by 1.89198 points. The below-1% full-denominator target has not been achieved.

`LER/cycle` remains `Not validated` because these aggregate failure percentages cannot be divided by round count. A publishable per-cycle metric requires a stable fit across matched circuit cohorts and round counts.

Using the published log-fidelity slope method on the available 3-, 5-, and 7-round records, all 14 Z fits passed the declared quality gate but none of the 14 X fits passed. A combined two-basis per-cycle number is therefore not reported.

## Conditional real-hardware result requiring separate interpretation

| Version | Result | Coverage | Interpretation |
|---|---:|---:|---|
| V22 | 0.16204% conditional error | 5% selected coverage | Real-hardware postselection result; not below 1% on the full dataset |

This row is not ranked against the full-denominator table.

## Confirmed and repeated historical improvements

| Version | Baseline error | Candidate error | Absolute improvement | Relative reduction | LER/cycle | Evidence |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| V12 | 33.67978% | 32.33681% | 1.34298 percentage points | 3.9875% | Not validated | Repeated across 259,200 untouched evaluation shots |
| V38 | 35.7153% | 34.4201% | 1.29514 percentage points | 3.6265% | Not validated | Independent 86,400-shot evaluation block |
| V39 | 46.512731% | 45.708333% | 0.804398 percentage points | 1.7294% | Not validated | Independent 86,400-shot evaluation block |

Results use different datasets and comparators and must not be added together.

## Standard comparison fields

Every new result is reported with data source, dataset/block role, full or selected denominator, coverage, X error, Z error, pooled error, matched baseline, absolute improvement, relative reduction, statistical evidence, evidence level, and below-1% status. Versions are ranked only when dataset, circuit cohort, basis, denominator, and split role match. Cross-block percentages are contextual rather than direct head-to-head comparisons.

The complete method-free index contains only versions evaluated using real-hardware data and is available in [ALL_VERSIONS.md](ALL_VERSIONS.md).

Last public update: 20 July 2026, Australia/Sydney.

## Disclosure boundary

This repository does not publish current research ideas or implementation details. Full reproducibility material will be considered after manuscript preparation, institutional review, and security review.
