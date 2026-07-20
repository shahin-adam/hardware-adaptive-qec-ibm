# Preliminary real-hardware results

Updated 20 July 2026.

Project team: Dr Weisheng, academic supervisor; Shahin Adam, lead student researcher and technical implementer. Western Sydney University.

This page reports sanitized aggregate evidence from a study of reducing logical quantum-error-correction error rates across two complementary bases. Results remain subject to academic review. Private methods, datasets, credentials, models, and current research ideas are intentionally excluded.

## How to read these results

An apples-to-apples comparison must use the same hardware block, scored shots, circuit cohort, bases, denominator, and baseline. For that reason:

- Each table below contains only results evaluated on identical shots within that table.
- Results in different tables must not be directly ranked or combined.
- All main tables use the full scored denominator with 100% coverage.
- A percentage-point (pp) improvement is baseline error minus candidate error; larger positive values are better.
- Conditional/postselected results are reported separately and are not full-decoder error rates.
- `LER/cycle` is populated only after a stable round-resolved fit on a matched circuit cohort. `Not validated` means the aggregate percentage cannot safely be converted into a per-cycle rate.
- The complete experiment history is an audit index, not a leaderboard; see [ALL_VERSIONS.md](ALL_VERSIONS.md).

## Primary repeated result

This is the strongest repeated full-denominator result. It pools three post-freeze real-hardware blocks using the same frozen V12 candidate and matched baseline on every scored shot.

| Candidate | Blocks | Scored shots | Coverage | Baseline error | Candidate error | Improvement | Relative reduction | LER/cycle | Evidence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| V12 | 3 | 259,200 | 100% | 33.67978% | 32.33681% | 1.34298 pp | 3.9875% | Not validated | Repeated full-denominator evaluation |

The same preserved predictions support an exact basis split:

| Basis | Scored shots | Coverage | Baseline error | V12 error | Improvement | Paired 95% CI | LER/cycle | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| X | 129,600 | 100% | 39.21682% | 38.42284% | 0.79398 pp | 0.65881 to 0.92916 pp | Not validated | Confirmed positive |
| Z | 129,600 | 100% | 28.14275% | 26.25077% | 1.89198 pp | 1.72304 to 2.06091 pp | Not validated | Confirmed positive |

Both bases improve, but the full-denominator below-1% two-basis target has not been achieved.

The current 3-, 5-, and 7-round records are suitable for retrospective per-cycle analysis, but the pooled preliminary fit is not stable enough to publish as one rate. Aggregate error is not divided by round count.

A matched-method audit used the published log-fidelity slope definition separately for every preserved domain, basis, and logical configuration. All 14 Z fits passed the declared quality gate, but 0 of 14 X fits passed. Therefore no combined two-basis LER/cycle value is published.

## Same-shot comparison A: V20 block

All rows use the same 86,400 scored shots and the same matched baseline.

| Candidate | Coverage | Baseline error | Candidate error | Improvement vs baseline | Increment beyond V12 | LER/cycle | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| V12 | 100% | 34.5845% | 33.3947% | 1.1898 pp | — | Not validated | Confirmed |
| V12 + V20 | 100% | 34.5845% | 33.3438% | 1.2407 pp | 0.0509 pp | Not validated | Confirmed positive increment |

## Same-shot comparison B: V21 block

All rows use the same 86,400 scored shots and the same matched baseline.

| Candidate | Coverage | Baseline error | Candidate error | Improvement vs baseline | Increment beyond V12 | LER/cycle | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| V12 | 100% | 34.6771% | 33.1493% | 1.5278 pp | — | Not validated | Confirmed |
| V12 + V21 | 100% | 34.6771% | 33.1458% | 1.5313 pp | 0.0035 pp | Not validated | Null increment |

## Same-shot comparison C: V22 block

The full-denominator row uses all 86,400 scored shots.

| Candidate | Coverage | Baseline error | Candidate error | Improvement vs baseline | LER/cycle | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| V12 | 100% | 31.7778% | 30.4664% | 1.3113 pp | Not validated | Confirmed |

The V22 conditional result is intentionally excluded from this table because it retained only 5% of shots.

## Same-shot comparison D: V38 confirmation block

All rows use the same 86,400 scored shots and the same matched baseline.

| Candidate | Coverage | Baseline error | Candidate error | Improvement vs baseline | Increment beyond V12 | LER/cycle | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Mathematical comparator | 100% | 35.7153% | 35.0035% | 0.7118 pp | — | Not validated | Confirmed |
| V12 | 100% | 35.7153% | 34.5926% | 1.1227 pp | — | Not validated | Confirmed |
| V12 + V38 | 100% | 35.7153% | 34.4201% | 1.2951 pp | 0.1725 pp | Not validated | Confirmed positive increment |

This is the strongest independently confirmed same-block hybrid result in the public evidence.

## Same-shot comparison E: cross-hardware transfer block

All rows use the same 86,400 scored shots and the same matched baseline. This block shows why results must be compared on identical data rather than ranked across blocks.

| Candidate | Coverage | Baseline error | Candidate error | Improvement vs baseline | Increment beyond V12 | LER/cycle | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| V39 | 100% | 46.5127% | 45.7083% | 0.8044 pp | — | Not validated | Confirmed on this block |
| V12 | 100% | 46.5127% | 46.3854% | 0.1273 pp | — | Not validated | Null transfer result |
| V12 + V38 | 100% | 46.5127% | 46.3692% | 0.1435 pp | 0.0162 pp | Not validated | Null hybrid increment |

## Same-shot comparison F: V68 block

All rows use the same 86,400 scored shots and the same matched baseline.

| Candidate | Coverage | Baseline error | Candidate error | Improvement vs baseline | Increment beyond V12 | LER/cycle | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| V12 | 100% | 32.7581% | 31.2303% | 1.5278 pp | — | Not validated | Confirmed |
| V12 + V68 | 100% | 32.7581% | 31.2072% | 1.5509 pp | 0.0231 pp | Not validated | Null increment; improvement is principally attributable to V12 |

## Conditional result — not comparable with full-denominator tables

| Version | Retained shots | Coverage | Conditional error | Matched retained-set advantage | Status |
|---|---:|---:|---:|---:|---|
| V22 | 4,320 of 86,400 | 5% | 0.16204% | 0.00000 pp | Confirmed postselection only |

The matched baseline made the same predictions and the same seven errors on the retained shots. Therefore, 0.16204% is evidence of identifying an easy subset, not an AI correction improvement and not a below-1% full-dataset result.

## What is deliberately excluded from the leaderboard

- Conventional decoding versus no correction, because it is not a novel AI contribution.
- Selected-cohort gains, because their denominators differ from the full dataset.
- Development and cross-validation results, because they are not independent confirmation.
- Small pilot screens, because they are not sufficiently powered for a headline claim.
- Simulation results, because this public page reports real-hardware evidence only.
- Blank, structural, operational, failed, or non-comparable ledger entries.

Results from different tables must not be added together. Complete version status and negative-result history remain available in [ALL_VERSIONS.md](ALL_VERSIONS.md).

## Latest real-hardware development test

| Version | Domains | Scored shots | Coverage | Outcome | Evidence |
|---|---:|---:|---:|---|---|
| V106 | 7 | 604,800 | 100% | No universally transferable X/Z improvement; sealed null | Retrospective leave-one-domain-out development |

V106 tested a target-label-free calibrated fallback policy. No candidate achieved a positive paired 95% lower improvement bound in every training domain separately for X and Z. No new hardware confirmation was requested.
