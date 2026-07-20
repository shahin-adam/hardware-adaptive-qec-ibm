# Hardware-Adaptive QEC Progress

Public, sanitized progress record for a Western Sydney University quantum-error-correction research programme.

## Project team

- Principal Investigator and academic supervisor: [Dr Weisheng Si](https://researchers.westernsydney.edu.au/en/persons/weisheng-si/), Senior Lecturer in Networking & Mobile Computing, Western Sydney University.
- Lead student researcher and technical implementer: Shahin Adam, Western Sydney University student ID 22228049.

## Funding context

This repository is the public preliminary-work link supporting an application to the IBM Quantum Credits Program. Dr Weisheng Si is the proposed Principal Investigator and applicant; Shahin Adam is the collaborating lead student researcher. The application remains subject to Dr Si's review and approval.

Only experiment identifiers, aggregate percentages, evidence level, and target status are published here. Current methods, model designs, private datasets, credentials, checkpoints, next-step hypotheses, and internal research documents are intentionally excluded while manuscript preparation is in progress.

## Best current development result

| Version | Basis | Baseline error | Candidate error | Relative reduction | Evidence |
|---|---:|---:|---:|---:|---|
| V81 | X | 3.545% | 1.980% | 44.15% | Synthetic development; confirmation running |
| V81 | Z | 3.805% | 2.760% | 27.46% | Synthetic development; confirmation running |

The below-1% two-basis target has not yet been achieved. These V81 figures are not IBM-hardware confirmation results.

## Confirmed and repeated historical improvements

| Version | Baseline error | Candidate error | Absolute improvement | Relative reduction | Evidence |
|---|---:|---:|---:|---:|---|
| V12 | 33.67978% | 32.33681% | 1.34298 percentage points | 3.9875% | Repeated across 259,200 untouched IBM shots |
| V38 | 35.7153% | 34.4201% | 1.29514 percentage points | 3.6265% | Independent 86,400-shot IBM block |
| V39 | 46.512731% | 45.708333% | 0.804398 percentage points | 1.7294% | Independent 86,400-shot IBM block |

Results use different datasets and comparators and must not be added together.

## Current version status

| Version | Public status |
|---|---|
| V81 | Untouched synthetic confirmation running |
| V97 | Development failed; sealed |
| V102 | Structural gate failed; sealed |
| V103 | Structural gate failed; sealed |
| V104 | Frozen synthetic development running |
| V105 | Pre-registered and dormant; not launched |

The complete method-free version and percentage index is available in [ALL_VERSIONS.md](ALL_VERSIONS.md).

Last public update: 20 July 2026, Australia/Sydney.

## Disclosure boundary

This repository does not publish current research ideas or implementation details. Full reproducibility material will be considered after manuscript preparation, institutional review, and security review.
