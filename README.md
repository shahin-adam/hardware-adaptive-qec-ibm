# Hardware-Adaptive Quantum Error Correction on IBM Systems

[![Status](https://img.shields.io/badge/status-offline%20validated-blue)](#validated-results)
[![IBM QPU](https://img.shields.io/badge/IBM%20QPU-submissions%20gated-orange)](#execution-safety)
[![Accuracy](https://img.shields.io/badge/logical%20accuracy-statistically%20null-lightgrey)](#scientific-boundary)

A fail-closed research programme for reliable, reproducible quantum-error-correction decoding on preserved IBM hardware data. The project combines algebraic decoder validation, reproducible GPU batching, independent decoder controls, and guarded preparation for future matched hardware acquisition.

## Project team

- Researcher: Shahin Adam
- Academic supervisors: A/Prof Quang Vinh Nguyen, A/Prof Weisheng Si, and Prof Simeon J. Simoff, Western Sydney University.

## Full results registry

See **[QEC results by distance and basis](RESULTS_BY_DISTANCE.md)** for all V1–V501 entries, including a compact comparator-safe `MWPM delta` column. Positive means the candidate has lower LER than matched MWPM; negative means it is worse. The dedicated **[matched MWPM comparison register](MWPM_COMPARISONS.md)** gives the supported candidate and matched-control details. Values against CNN, Transformer, V12, raw readout, or other candidates are not presented as MWPM gains; V501 is explicitly not applicable because MWPM itself is the evaluated decoder.

## Why this work matters

Real-time QEC requires more than a decoder with a favorable point estimate. A trustworthy system must preserve the syndrome equation, reproduce its decisions, meet latency constraints, and demonstrate logical improvement with uncertainty that excludes a null result. This repository separates those claims so that systems performance is not mistaken for physical error suppression.

```mermaid
flowchart LR
    A[Preserved IBM syndrome data] --> B[Contract and observable validation]
    B --> C[Deterministic decoder controls]
    C --> D[Algebraic closure: H e = s]
    D --> E[Matched offline latency benchmark]
    E --> F[Statistical logical-accuracy audit]
    F -->|Current result| G[Accuracy remains null]
    F -->|Future, separately authorized| H[Matched IBM acquisition]
```

## Validated results

| Result | Measured outcome | Scope |
|---|---:|---|
| Algebraic syndrome closure | **100%** | 1,536 preserved real-IBM replay shots |
| Batched replay speedup | **2.252x** | 95% CI **[2.135, 2.362]x** |
| Batched latency | **1.461 ms/shot** | Offline matched replay |
| Sequential latency | **3.435 ms/shot** | Offline matched replay |
| V501 corrected logical gain | **+0.455729 percentage points** | 95% CI **[-2.929688, +3.906250] pp**; statistically null |
| V501 raw versus decoded LER | **50.390625% → 49.934896%** | Corrected observable contract; offline replay |

The closure and latency results are defensible systems findings. They do **not** establish below-threshold QEC, physical error suppression, or quantum advantage.

## Independent decoder and representation controls

The corrected V501 PyMatching control provides an independent offline comparison against the project decoder stack. It confirms deterministic replay and graph closure, while the corrected logical-accuracy interval still crosses zero.

A separate sparse 3D space-time GCN experiment found a modest **1.45 percentage-point** improvement over logistic regression, with its confidence interval excluding zero. Its logical error rate was **12.12%**, compared with **12.97%** for an always-zero control and **2.95%** for PyMatching. This shows that space-time structure contains learnable information, but the tested GCN was not competitive with MWPM/PyMatching. The GCN did not produce the closure or GPU-speedup results above.

## Scientific boundary

- Historical V490–V500 logical-accuracy values were withdrawn after V501 identified incorrect observable maps in all 24 audited contracts.
- V501 recomputed accuracy on corrected contracts; the result remains statistically null.
- Relay routing did not meet the **95%** cross-seed production gate. Five-seed consensus retained only **2.864583%** fast-path coverage, and valid seeds disagreed logically on **23.632812%** of shots.
- No claim of physical error suppression, `Lambda > 1`, real-time feedback latency, or accuracy breakthrough is made.

## Execution safety

Live IBM submissions are gated. The repository's preparation and validation work does not authorize a hardware job.

Planned hardware controls, subject to a separate signed go/no-go review, include:

- matched compilation, layout, and dynamical-decoupling provenance across approved backends;
- logical `0`, `1`, `+`, and `-` preparations;
- an `N=0` SPAM calibration baseline;
- variable syndrome-round acquisition;
- backend-measured dynamic-feedforward latency.

These controls are **planned, not yet reported as executed**. In particular, this project does not claim completed `N=0` SPAM inversion or sub-microsecond IBM feedforward.

## Funding objectives

Support would enable four bounded objectives:

1. **Reproducible real-time systems benchmarking** — characterize decoder throughput and end-to-end latency on controlled CPU/GPU environments.
2. **Matched hardware acquisition** — acquire statistically powered, calibration-matched IBM datasets only after protocol and budget authorization.
3. **Robust decoding research** — benchmark deterministic graph decoders and carefully scoped space-time learning methods against strong PyMatching controls.
4. **Open validation infrastructure** — release sanitized schemas, audit checks, and reproducibility artifacts after institutional and security review.

Success will be assessed with preregistered gates: 100% algebraic closure, at least 95% routing agreement where routing is used, matched uncertainty intervals, and no physical-suppression claim unless its confidence bound clears the declared threshold.

## Governance and disclosure

The work is led at Western Sydney University under academic supervision. Results are reported as offline, historical, synthetic, or live-hardware evidence according to their actual provenance.

Public material intentionally excludes:

- API keys, credentials, account identifiers, job-access secrets, and private endpoints;
- private datasets and shot-level records;
- unpublished model weights, proprietary decoder internals, and exploit-ready infrastructure details;
- internal filesystem paths, cluster account details, and unsigned hardware-submission instructions.

No software license is asserted because this repository does not currently contain a license file.

## Current status

The project has a validated offline systems result and a corrected, statistically null logical-accuracy result. IBM hardware acquisition remains gated pending a separate explicit authorization and a frozen matched protocol.

## Complete Version Percentage Ledger

This registry preserves every public percentage string from V1 through V501 verbatim in the final column. Structured fields are populated only when their mapping is explicit in authoritative records; ambiguous basis, distance, baseline, or candidate fields remain `not recorded`. Improvement entries name their comparator explicitly when the source supports it; a positive value must not be read as an MWPM gain unless MWPM is named.

| Version | Scope / basis / distance | Baseline | Candidate / result | Improvement | Evidence status | Interpretation / notes | Source percentage string |
|---|---|---:|---:|---:|---|---|---|
| V1 | two scopes: real IBM held-out test; independent IBM confirmation; basis/distance not consistently recorded | CNN 46.4231%; frozen Transformer 44.9292% | Transformer 45.2051%; four-model ensemble 44.0908% | +1.2180 pp Transformer vs CNN; +0.8383 pp ensemble vs frozen Transformer | development: 31,200 held-out shots; confirmed: 120,000 independent-confirmation shots | Neither gain is versus MWPM. On the ensemble confirmation, phenomenological MWPM was 42.6442%, beating the 44.0908% ensemble by 1.4466 pp. Pre-versioned foundation, not a uniquely reconstructable V1 checkpoint. | 1.2180 pp; 0.8383 pp |
| V2 | not recorded | not recorded | not recorded | +0.4750 pp; 0.1531 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.4750 pp; 0.1531 pp |
| V3 | not recorded | not recorded | not recorded | +0.3281 pp; 1.9688 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.3281 pp; 1.9688 pp |
| V4 | not recorded | not recorded | not recorded | +1.7396 pp development; +0.6505 pp confirmed pooled | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.7396 pp development; +0.6505 pp confirmed pooled |
| V5 | not recorded | not recorded | not recorded | +1.5167 pp; 0.0000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.5167 pp; 0.0000 pp |
| V6 | not recorded | not recorded | not recorded | +1.5906 pp development; +0.0740 pp confirmation | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.5906 pp development; +0.0740 pp confirmation |
| V7 | not recorded | not recorded | not recorded | +1.7313 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.7313 pp |
| V8 | not recorded | not recorded | not recorded | +1.7443 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.7443 pp |
| V9 | not recorded | not recorded | not recorded | +1.8125 pp; 0.6493 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.8125 pp; 0.6493 pp |
| V10 | not recorded | not recorded | not recorded | +1.3600 pp first independent block; +0.7697 pp second block | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.3600 pp first independent block; +0.7697 pp second block |
| V11 | not recorded | not recorded | not recorded | 1.0918 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 1.0918 pp |
| V12 | not recorded | not recorded | not recorded | +1.34298 pp pooled | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.34298 pp pooled |
| V13 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V14 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V15 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V16 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V17 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V18 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V19 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V20 | not recorded | not recorded | not recorded | +0.05093 pp incremental; +1.24074 pp vs MWPM | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.05093 pp incremental; +1.24074 pp vs MWPM |
| V21 | not recorded | not recorded | not recorded | +0.00347 pp incremental; +1.53125 pp vs MWPM | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.00347 pp incremental; +1.53125 pp vs MWPM |
| V22 | not recorded | not recorded | 0.16204% conditional error at 5% retained coverage | not recorded | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 0.16204% conditional error at 5% retained coverage |
| V23 | not recorded | not recorded | not recorded | +0.021219 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.021219 pp |
| V24 | not recorded | not recorded | not recorded | +0.001157 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.001157 pp |
| V25 | not recorded | not recorded | not recorded | +0.128472 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.128472 pp |
| V26 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V27 | not recorded | not recorded | not recorded | 1.7222 pp; 0.9667 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 1.7222 pp; 0.9667 pp |
| V28 | not recorded | not recorded | not recorded | +0.2847 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.2847 pp |
| V29 | not recorded | not recorded | not recorded | +0.9741 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.9741 pp |
| V30 | not recorded | not recorded | not recorded | +0.07639 pp; +0.03241 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.07639 pp; +0.03241 pp |
| V31 | not recorded | not recorded | not recorded | +0.05440 pp; +0.00347 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.05440 pp; +0.00347 pp |
| V32 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V33 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V34 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V35 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V36 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V37 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V38 | not recorded | not recorded | not recorded | +1.29514 pp vs MWPM; +0.17245 pp vs V12; +0.016204 pp Fez transfer | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.29514 pp vs MWPM; +0.17245 pp vs V12; +0.016204 pp Fez transfer |
| V39 | not recorded | not recorded | not recorded | +0.804398 pp pooled | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.804398 pp pooled |
| V40 | not recorded | not recorded | not recorded | +1.223380 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.223380 pp |
| V41 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V42 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V43 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V44 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V45 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V46 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V47 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V48 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V49 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V50 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V51 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V52 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V53 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V54 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V55 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V56 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V57 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V58 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V59 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V60 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V61 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V62 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V63 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V64 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V65 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V66 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V67 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V68 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V69 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V70 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V71 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V72 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V73 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V74 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V75 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V76 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V77 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V78 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V79 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V80 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V81 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V82 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V83 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V84 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V85 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V86 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V87 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V88 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V89 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V90 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V91 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V92 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V93 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V94 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V95 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V96 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V97 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V98 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V99 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V100 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V101 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V102 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V103 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V104 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V105 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V106 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V107 | not recorded | not recorded | not recorded | +0.053755 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.053755 pp |
| V108 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V109 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V110 | not recorded | not recorded | not recorded | +0.00077 pp; +0.00154 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.00077 pp; +0.00154 pp |
| V111 | not recorded | not recorded | not recorded | +0.02816 pp; +0.05633 pp; 0.01505 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.02816 pp; +0.05633 pp; 0.01505 pp |
| V112 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V113 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V114 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V115 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V116 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V117 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V118 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V119 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V120 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V121 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V122 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V123 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V124 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V125 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V126 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V127 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V128 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V129 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V130 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V131 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V132 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V133 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V134 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V135 | not recorded | not recorded | not recorded | +0.37252 pp; +0.32424 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.37252 pp; +0.32424 pp |
| V136 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V137 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V138 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V139 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V140 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V141 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V142 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V143 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V144 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V145 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V146 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V147 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V148 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V149 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V150 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V151 | not recorded | not recorded | not recorded | 0.85818 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 0.85818 pp |
| V152 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V153 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V154 | not recorded | not recorded | not recorded | 1.2180 pp; 0.8383 pp; +0.4750 pp; 0.1531 pp; +0.3281 pp; 1.9688 pp; +1.7396 pp; +0.6505 pp; +1.5167 pp; 0.0000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 1.2180 pp; 0.8383 pp; +0.4750 pp; 0.1531 pp; +0.3281 pp; 1.9688 pp; +1.7396 pp; +0.6505 pp; +1.5167 pp; 0.0000 pp |
| V155 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V156 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V157 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V158 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V159 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V160 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V161 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V162 | not recorded | not recorded | not recorded | +0.72487 pp; +0.00066 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.72487 pp; +0.00066 pp |
| V163 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V164 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V165 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V166 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V167 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V168 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V169 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V170 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V171 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V172 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V173 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V174 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V175 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V176 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V177 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V178 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V179 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V180 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V181 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V182 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V183 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V184 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V185 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V186 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V187 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V188 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V189 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V190 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V191 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V192 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V193 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V194 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V195 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V196 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V197 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V198 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V199 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V200 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V201 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V202 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V203 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V204 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V205 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V206 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V207 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V208 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V209 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V210 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V211 | not recorded | not recorded | not recorded | 0.10 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 0.10 pp |
| V212 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V213 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V214 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V215 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V216 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V217 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V218 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V219 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V220 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V221 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V222 | not recorded | not recorded | not recorded | +0.01862 pp; 0.00000 pp; +0.03724 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.01862 pp; 0.00000 pp; +0.03724 pp |
| V223 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V224 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V225 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V226 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V227 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V228 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V229 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V230 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V231 | not recorded | not recorded | not recorded | +0.00231 pp; +0.00000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.00231 pp; +0.00000 pp |
| V232 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V233 | not recorded | not recorded | not recorded | -0.03704 pp; 0.00000 pp; -0.07407 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.03704 pp; 0.00000 pp; -0.07407 pp |
| V234 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V235 | not recorded | not recorded | not recorded | +0.03931 pp; -0.16509 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.03931 pp; -0.16509 pp |
| V236 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V237 | not recorded | not recorded | not recorded | +0.00000 pp; -0.08648 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.00000 pp; -0.08648 pp |
| V238 | not recorded | not recorded | not recorded | +0.00786 pp; -0.28302 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.00786 pp; -0.28302 pp |
| V239 | not recorded | not recorded | not recorded | -0.36164 pp; -0.79403 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.36164 pp; -0.79403 pp |
| V240 | not recorded | not recorded | not recorded | +0.44811 pp; -3.23899 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.44811 pp; -3.23899 pp |
| V241 | not recorded | not recorded | not recorded | +0.44811 pp; 0.00000 pp; +0.22406 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.44811 pp; 0.00000 pp; +0.22406 pp |
| V242 | not recorded | not recorded | not recorded | +0.18868 pp; 0.00000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.18868 pp; 0.00000 pp |
| V243 | not recorded | not recorded | not recorded | +0.44811 pp; -3.23899 pp; 0.00000 pp; +0.18868 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.44811 pp; -3.23899 pp; 0.00000 pp; +0.18868 pp |
| V244 | not recorded | not recorded | not recorded | +0.22799 pp; -0.52673 pp; -0.14937 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.22799 pp; -0.52673 pp; -0.14937 pp |
| V245 | not recorded | not recorded | not recorded | -0.53459 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.53459 pp |
| V246 | not recorded | not recorded | not recorded | 0.00000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 0.00000 pp |
| V247 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V248 | not recorded | not recorded | not recorded | -0.57390 pp; -1.17925 pp; -0.87657 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.57390 pp; -1.17925 pp; -0.87657 pp |
| V249 | not recorded | not recorded | not recorded | +0.22799 pp; -0.52673 pp; -0.14937 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.22799 pp; -0.52673 pp; -0.14937 pp |
| V250 | not recorded | not recorded | not recorded | 0.00000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 0.00000 pp |
| V251 | not recorded | not recorded | not recorded | +0.02083 pp; -0.18056 pp; -0.07986 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.02083 pp; -0.18056 pp; -0.07986 pp |
| V252 | not recorded | not recorded | not recorded | +0.00000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.00000 pp |
| V253 | not recorded | not recorded | not recorded | +0.04630 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.04630 pp |
| V254 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V255 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V256 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V257 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V258 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V259 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V260 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V261 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V262 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V263 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V264 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V265 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V266 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V267 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V268 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V269 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V270 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V271 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V272 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V273 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V274 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V275 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V276 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V277 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V278 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V279 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V280 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V281 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V282 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V283 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V284 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V285 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V286 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V287 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V288 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V289 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V290 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V291 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V292 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V293 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V294 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V295 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V296 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V297 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V298 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V299 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V300 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V301 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V302 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V303 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V304 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V305 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V306 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V307 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V308 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V309 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V310 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V311 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V312 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V313 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V314 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V315 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V316 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V317 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V318 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V319 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V320 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V321 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V322 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V323 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V324 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V325 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V326 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V327 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V328 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V329 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V330 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V331 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V332 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V333 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V334 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V335 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V336 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V337 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V338 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V339 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V340 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V341 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V342 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V343 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V344 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V345 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V346 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V347 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V348 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V349 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V350 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V351 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V352 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V353 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V354 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V355 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V356 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V357 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V358 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V359 | not recorded | not recorded | not recorded | +0.15972pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.15972pp |
| V360 | not recorded | not recorded | not recorded | -0.0637pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.0637pp |
| V361 | not recorded | not recorded | not recorded | +0.06996pp; -0.0104pp; +0.1470pp; -0.0266pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.06996pp; -0.0104pp; +0.1470pp; -0.0266pp |
| V362 | not recorded | not recorded | not recorded | +0.05298pp; +0.1238pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.05298pp; +0.1238pp |
| V363 | not recorded | not recorded | not recorded | +0.05298pp; -0.0255pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.05298pp; -0.0255pp |
| V364 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V365 | not recorded | not recorded | not recorded | +0.06713pp; -0.05556pp; +0.01736pp; +0.11921pp; +0.07986pp; +0.18403pp; +0.09144pp; +0.00116pp; +0.14352pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.06713pp; -0.05556pp; +0.01736pp; +0.11921pp; +0.07986pp; +0.18403pp; +0.09144pp; +0.00116pp; +0.14352pp |
| V366 | not recorded | not recorded | not recorded | +0.07305pp; +0.14236pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.07305pp; +0.14236pp |
| V367 | not recorded | not recorded | not recorded | +0.06237pp; +0.14352pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.06237pp; +0.14352pp |
| V368 | not recorded | not recorded | not recorded | +0.07677pp; +0.21644pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.07677pp; +0.21644pp |
| V369 | not recorded | not recorded | not recorded | -0.01402pp; -0.08681pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.01402pp; -0.08681pp |
| V370 | not recorded | not recorded | not recorded | +0.00836pp; -0.16898pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.00836pp; -0.16898pp |
| V371 | not recorded | not recorded | not recorded | +0.01196pp; +0.03472pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.01196pp; +0.03472pp |
| V372 | not recorded | not recorded | not recorded | +0.05337pp; +0.17361pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.05337pp; +0.17361pp |
| V373 | not recorded | not recorded | not recorded | +0.01800pp; +0.04282pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.01800pp; +0.04282pp |
| V374 | not recorded | not recorded | not recorded | +0.06970pp; +0.19213pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.06970pp; +0.19213pp |
| V375 | not recorded | not recorded | not recorded | +0.02739pp; +0.18634pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.02739pp; +0.18634pp |
| V376 | not recorded | not recorded | not recorded | +0.02739pp; +0.18634pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.02739pp; +0.18634pp |
| V377 | not recorded | not recorded | not recorded | +0.01595pp; +0.18634pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.01595pp; +0.18634pp |
| V378 | not recorded | not recorded | not recorded | +0.01453pp; +0.03356pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.01453pp; +0.03356pp |
| V379 | not recorded | not recorded | not recorded | +0.01723pp; +0.09722pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.01723pp; +0.09722pp |
| V380 | not recorded | not recorded | not recorded | +0.01698pp; -0.00463pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.01698pp; -0.00463pp |
| V381 | not recorded | not recorded | not recorded | +0.02276pp; +0.06366pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.02276pp; +0.06366pp |
| V382 | not recorded | not recorded | not recorded | +0.02251pp; +0.06366pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.02251pp; +0.06366pp |
| V383 | not recorded | not recorded | not recorded | +0.00694pp; +0.03588pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.00694pp; +0.03588pp |
| V384 | not recorded | not recorded | not recorded | +0.02238pp; -0.02431pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.02238pp; -0.02431pp |
| V385 | not recorded | not recorded | not recorded | -0.00694pp; -0.09606pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.00694pp; -0.09606pp |
| V386 | not recorded | not recorded | not recorded | +0.00180pp; +0.04167pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.00180pp; +0.04167pp |
| V387 | not recorded | not recorded | not recorded | +0.01608pp; +0.06250pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.01608pp; +0.06250pp |
| V388 | not recorded | not recorded | not recorded | -0.00360pp; +0.09606pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.00360pp; +0.09606pp |
| V389 | not recorded | not recorded | not recorded | +1.7111pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.7111pp |
| V390 | not recorded | not recorded | not recorded | +0.9657pp; +0.9648pp; +0.9639pp; +0.9694pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.9657pp; +0.9648pp; +0.9639pp; +0.9694pp |
| V391 | not recorded | not recorded | not recorded | +0.9648pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.9648pp |
| V392 | not recorded | not recorded | not recorded | +0.8806pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.8806pp |
| V393 | not recorded | not recorded | not recorded | +0.662963 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.662963 pp |
| V394 | not recorded | not recorded | not recorded | +0.662963 pp; -0.124074 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.662963 pp; -0.124074 pp |
| V395 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V396 | not recorded | not recorded | not recorded | +0.005556 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.005556 pp |
| V397 | not recorded | not recorded | not recorded | +0.000000 pp; +0.000000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.000000 pp; +0.000000 pp |
| V398 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V399 | not recorded | not recorded | not recorded | +0.075000 pp; +0.105556 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.075000 pp; +0.105556 pp |
| V400 | not recorded | not recorded | not recorded | -0.013889 pp; -0.061111 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.013889 pp; -0.061111 pp |
| V401 | not recorded | not recorded | not recorded | +0.066667 pp; +0.068519 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.066667 pp; +0.068519 pp |
| V402 | not recorded | not recorded | not recorded | -3.740000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -3.740000 pp |
| V403 | not recorded | not recorded | not recorded | +0.022222 pp; +0.074074 pp; +0.722222 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.022222 pp; +0.074074 pp; +0.722222 pp |
| V404 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V405 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V406 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V407 | not recorded | not recorded | not recorded | 12.553333 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 12.553333 pp |
| V408 | not recorded | not recorded | not recorded | 15.653333 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 15.653333 pp |
| V409 | not recorded | not recorded | not recorded | +0.006667 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.006667 pp |
| V410 | not recorded | not recorded | not recorded | +0.000000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.000000 pp |
| V411 | not recorded | not recorded | not recorded | +0.117284 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.117284 pp |
| V412 | not recorded | not recorded | not recorded | -15.151515 pp; +0.124 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -15.151515 pp; +0.124 pp |
| V413 | not recorded | not recorded | not recorded | +1.333333 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.333333 pp |
| V414 | not recorded | not recorded | not recorded | +0.262821 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.262821 pp |
| V415 | not recorded | not recorded | not recorded | -0.186111 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.186111 pp |
| V416 | not recorded | not recorded | not recorded | -2.6667 pp; +0.7692 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -2.6667 pp; +0.7692 pp |
| V417 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V418 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V419 | not recorded | not recorded | not recorded | +0.3395 pp; +0.457 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.3395 pp; +0.457 pp |
| V420 | not recorded | not recorded | not recorded | +0.1245 pp; +0.2865 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.1245 pp; +0.2865 pp |
| V421 | not recorded | not recorded | not recorded | +0.162500 pp; +0.164583 pp; +0.155208 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.162500 pp; +0.164583 pp; +0.155208 pp |
| V422 | not recorded | not recorded | not recorded | +0.659259 pp; +0.782407 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.659259 pp; +0.782407 pp |
| V423 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V424 | not recorded | not recorded | not recorded | +1.0768519 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +1.0768519 pp |
| V425 | not recorded | not recorded | not recorded | -0.1531250 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.1531250 pp |
| V426 | not recorded | not recorded | not recorded | +0.2212963 pp; +0.0740741 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.2212963 pp; +0.0740741 pp |
| V427 | not recorded | not recorded | not recorded | +0.1018519 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.1018519 pp |
| V428 | not recorded | not recorded | not recorded | 0.000000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 0.000000 pp |
| V429 | not recorded | not recorded | not recorded | -0.0005556 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.0005556 pp |
| V430 | not recorded | not recorded | not recorded | -0.2062500 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.2062500 pp |
| V431 | not recorded | not recorded | not recorded | +0.2650463 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.2650463 pp |
| V432 | not recorded | not recorded | not recorded | +0.1203704 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.1203704 pp |
| V433 | not recorded | not recorded | not recorded | +0.1828704 pp; -0.0031250 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.1828704 pp; -0.0031250 pp |
| V434 | not recorded | not recorded | not recorded | +0.0729167 pp; -0.1885417 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.0729167 pp; -0.1885417 pp |
| V435 | not recorded | not recorded | not recorded | +0.0405093 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.0405093 pp |
| V436 | not recorded | not recorded | not recorded | -0.0949074 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.0949074 pp |
| V437 | not recorded | not recorded | not recorded | -0.0768519 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.0768519 pp |
| V438 | not recorded | not recorded | not recorded | -0.0192308 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -0.0192308 pp |
| V439 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V440 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V441 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V442 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V443 | not recorded | not recorded | not recorded | +0.038462 pp; +1.256410 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.038462 pp; +1.256410 pp |
| V444 | not recorded | not recorded | not recorded | +0.696296 pp; +0.459259 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.696296 pp; +0.459259 pp |
| V445 | not recorded | not recorded | not recorded | +0.227778 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.227778 pp |
| V446 | not recorded | not recorded | not recorded | +0.090667 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.090667 pp |
| V447 | not recorded | not recorded | not recorded | +0.313667 pp sweep maximum; +0.090667 pp at fixed 0.80 | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.313667 pp sweep maximum; +0.090667 pp at fixed 0.80 |
| V448 | not recorded | not recorded | not recorded | +0.007292 pp; +0.019792 pp; +0.649074 pp held-out blocks | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.007292 pp; +0.019792 pp; +0.649074 pp held-out blocks |
| V449 | not recorded | not recorded | not recorded | +0.043750 pp; +0.056250 pp; +0.649074 pp held-out blocks | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.043750 pp; +0.056250 pp; +0.649074 pp held-out blocks |
| V450 | not recorded | not recorded | not recorded | +0.043750 pp; +0.056250 pp; +0.649074 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.043750 pp; +0.056250 pp; +0.649074 pp |
| V451 | not recorded | not recorded | not recorded | +0.128125 pp; +0.151042 pp; +0.649074 pp held-out blocks | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.128125 pp; +0.151042 pp; +0.649074 pp held-out blocks |
| V452 | not recorded | not recorded | not recorded | +0.010417 pp; +0.016667 pp; +0.227778 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.010417 pp; +0.016667 pp; +0.227778 pp |
| V453 | not recorded | not recorded | 35.4600%/46.5000%/48.9500%; 17.4000%/32.7700%/42.5800% | not recorded | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 35.4600%/46.5000%/48.9500%; 17.4000%/32.7700%/42.5800% |
| V454 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V455 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V456 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V457 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V458 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V459 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V460 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V461 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V462 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V463 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V464 | not recorded | not recorded | not recorded | +0.003205 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.003205 pp |
| V465 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V466 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V467 | not recorded | not recorded | not recorded | +0.100000 pp; -0.150000 pp; +0.000000 pp; +0.250000 pp; +0.100000 pp; +0.000000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.100000 pp; -0.150000 pp; +0.000000 pp; +0.250000 pp; +0.100000 pp; +0.000000 pp |
| V468 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V469 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V470 | not recorded | not recorded | not recorded | +0.130000 pp; +0.080000 pp; +0.090000 pp; +0.050000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.130000 pp; +0.080000 pp; +0.090000 pp; +0.050000 pp |
| V471 | not recorded | not recorded | not recorded | +0.015000 pp; -0.070000 pp; +0.120000 pp; +0.075000 pp; +0.090000 pp; +0.045000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.015000 pp; -0.070000 pp; +0.120000 pp; +0.075000 pp; +0.090000 pp; +0.045000 pp |
| V472 | not recorded | not recorded | not recorded | +0.000000 pp; +0.109000 pp; +0.102000 pp; +0.088000 pp; +0.086000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.000000 pp; +0.109000 pp; +0.102000 pp; +0.088000 pp; +0.086000 pp |
| V473 | not recorded | not recorded | not recorded | +0.103000 pp; +0.000000 pp; +0.109000 pp; +0.102000 pp; +0.088000 pp; +0.086000 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.103000 pp; +0.000000 pp; +0.109000 pp; +0.102000 pp; +0.088000 pp; +0.086000 pp |
| V474 | not recorded | not recorded | not recorded | +0.025157 pp; +0.000000 pp; +0.358491 pp; -1.191824 pp; -0.202044 pp pooled | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.025157 pp; +0.000000 pp; +0.358491 pp; -1.191824 pp; -0.202044 pp pooled |
| V475 | not recorded | not recorded | not recorded | +0.256667 pp; +0.000000 pp; -0.426667 pp; +0.000000 pp; -0.042500 pp pooled | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.256667 pp; +0.000000 pp; -0.426667 pp; +0.000000 pp; -0.042500 pp pooled |
| V476 | not recorded | not recorded | not recorded | +0.176667 pp; +0.000000 pp; +0.088333 pp pooled | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.176667 pp; +0.000000 pp; +0.088333 pp pooled |
| V477 | not recorded | not recorded | not recorded | +0.000000 pp pooled | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.000000 pp pooled |
| V478 | not recorded | not recorded | not recorded | +0.433333 pp; -0.113333 pp; -0.300000 pp; +0.046667 pp; +0.016667 pp pooled | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.433333 pp; -0.113333 pp; -0.300000 pp; +0.046667 pp; +0.016667 pp pooled |
| V479 | not recorded | not recorded | not recorded | +0.305000 pp selected slice | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.305000 pp selected slice |
| V480 | not recorded | not recorded | not recorded | +0.442000 pp selected slice | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | +0.442000 pp selected slice |
| V481 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V482 | not recorded | not recorded | 51.822917% raw; 42.187500% raw | not recorded | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 51.822917% raw; 42.187500% raw |
| V483 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V484 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V485 | not recorded | not recorded | not recorded | -3.190 pp | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | -3.190 pp |
| V486 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V487 | not recorded | not recorded | 0.700000%/1.230000%/1.600000%; 0.700000%/1.060000%/1.410000%; 0.190000%/0.270000%/0.650000%; 0.300000%/0.380000%/0.460000%; 0.070000%/0.140000%/0.190000%; 0.030000%/0.070000%/0.210000% | not recorded | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 0.700000%/1.230000%/1.600000%; 0.700000%/1.060000%/1.410000%; 0.190000%/0.270000%/0.650000%; 0.300000%/0.380000%/0.460000%; 0.070000%/0.140000%/0.190000%; 0.030000%/0.070000%/0.210000% |
| V488 | not recorded | not recorded | 48.697917%/51.822917%; 41.927083%/42.187500%; 51.041667%/45.833333%; 50.520833%/48.437500%; 51.041667%/54.166667%; 51.562500%/50.520833% | not recorded | historical numeric record | Exact source percentage retained; ambiguous mapping not inferred. | 48.697917%/51.822917%; 41.927083%/42.187500%; 51.041667%/45.833333%; 50.520833%/48.437500%; 51.041667%/54.166667%; 51.562500%/50.520833% |
| V489 | not recorded | not recorded | not recorded | not recorded | no numeric evidence | No value or X/Z/d mapping inferred. | not recorded |
| V490 | preserved IBM replay; d=5/d=7 | not recorded | 100% syndrome closure | not recorded | closure retained; accuracy withdrawn | Observable-map defect affects accuracy, not algebraic closure. | 100% syndrome closure; accuracy withdrawn |
| V491 | not recorded | not recorded | not recorded | not recorded | no recoverable numeric result | No value inferred. | not recorded |
| V492 | preserved IBM replay; d=5/d=7 | not recorded | 100% syndrome closure | not recorded | closure retained; accuracy withdrawn | Observable-map defect affects accuracy, not algebraic closure. | 100% syndrome closure; accuracy withdrawn |
| V493 | not recorded | not recorded | not recorded | not recorded | no recoverable numeric result | No value inferred. | not recorded |
| V494 | 1,536 preserved IBM replay shots; d=5/d=7 | not recorded | 100% syndrome closure | not recorded | closure retained; accuracy withdrawn | Historical logical-accuracy value withdrawn after V501 observable audit. | 100% syndrome closure; accuracy withdrawn |
| V495 | preserved IBM replay; d=5/d=7 | not recorded | 100% syndrome closure | not recorded | closure retained; accuracy withdrawn | Historical logical-accuracy value withdrawn after V501 observable audit. | 100% syndrome closure; accuracy withdrawn |
| V496 | protocol/power audit | not recorded | not recorded | not recorded | no canonical result recovered | No result reconstructed from the surviving analysis script. | not recorded |
| V497 | 1,536 preserved IBM replay shots; offline matched timing | 3.435 ms/shot sequential | 1.461 ms/shot batched | 2.252x; 95% CI [2.135, 2.362]x | systems result retained; accuracy withdrawn | 100% closure retained. Speedup is offline replay, not QPU feedback latency. | 100% syndrome closure; accuracy withdrawn |
| V498 | 1,536 preserved IBM replay shots; five-seed routing audit | not recorded | 2.864583% fast-path coverage; 23.632812% logical disagreement | not recorded | routing gate failed; accuracy withdrawn | Below 95% cross-seed production requirement. | 2.864583% fast-path coverage; 23.632812% logical disagreement; accuracy withdrawn |
| V499 | preserved IBM replay; route determinism audit | not recorded | 90.234375% same-seed route agreement; 92.708333% reverse-order route agreement | not recorded | routing unresolved | Relay nondeterminism remained below the production gate. | 90.234375% same-seed route agreement; 92.708333% reverse-order route agreement |
| V500 | preserved IBM replay; offline reproducibility | not recorded | 99.821% correction-bit reproducibility | not recorded | offline reproducibility only; accuracy withdrawn | Does not establish logical improvement or live-hardware performance. | 99.821% correction-bit reproducibility; accuracy withdrawn |
| V501 | Corrected observable contract; offline replay | 50.390625% raw LER | 49.934896% decoded LER | +0.455729 pp; 95% CI [-2.929688, +3.906250] pp | corrected accuracy statistically null | Independent PyMatching control; CI crosses zero. | 50.390625% raw; 49.934896% decoded; +0.455729 pp |
