# Hardware-Adaptive QEC Progress

Public, sanitized progress record for a Western Sydney University quantum-error-correction research programme.

## Project team

- Principal Investigator and academic supervisor: Dr Weisheng, Western Sydney University.
- Lead student researcher and technical implementer: Shahin Adam, Western Sydney University.

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
contains an explicit row for every version from V1 through V174, including
archive gaps, null results, failed/sealed experiments, active development,
and confirmed evidence. README tables are intentionally summaries and must
not be interpreted as the complete version list.

## Current development status

V12 remains the best validated full-coverage model on its tested validation
scope. Recent opened-domain development results and active experiments are:

| Version | Best aggregate observation | Status |
| --- | --- | --- |
| V125 | 0.3327 pp pooled development gain | Not promoted; basis/domain gates failed |
| V128 | 0.3725 pp pooled development gain | Not promoted; basis/domain gates failed |
| V129 | 0.0749 pp pooled development gain | Not promoted; transfer safety gates failed |
| V130 | 0.3242 pp pooled development gain | X +0.6485 pp, Z unchanged; worst-fold gate failed |
| V131 | Best arm 0.00000 pp; fine-tuned arm -0.01141 pp | Foundation-model transfer completed; no arm was promoted |
| V132 | 0.00000 pp in all four fusion/control arms | Fusion completed; no arm was promoted |
| V133 | Best arm +0.44015 pp; X +0.87500 pp, Z +0.00529 pp | Opened-domain development only; negative held cells prevented promotion |
| V134 | Not a decoder metric | Research audit; no performance claim |
| V135 | Best arm +0.37550 pp; X +0.75099 pp, Z unchanged | Opened-domain development only; negative held cells prevented promotion |
| V136 | Best arm +0.27993 pp; X +0.55985 pp, Z unchanged | Full evaluation completed; zero-gain cells prevented promotion |
| V137 | Best arm +0.15476 pp; X +0.30952 pp, Z unchanged | Full evaluation completed; zero-gain cells prevented promotion |
| V138 | 0.00000 pp in all asymmetric-risk arms | Full evaluation completed; no arm was promoted |
| V139 | Completed metric audit | No decoder-improvement claim |
| V140 | Best zero-shot +0.17342 pp; corresponding few-shot +0.16750 pp | MMD/EWC transfer development completed; no arm was promoted |
| V141 | Best arm +0.23472 pp; X +0.46944 pp, Z unchanged | Unlabelled-target MMD development completed; negative held cells prevented promotion |
| V142 | 0.00000 pp for original and spectral variants | Spectral audit and matched decoder comparison completed; no promotion |
| V143 | Completed drift audit | No decoder-improvement claim |
| V144 | Completed algebraic audit | No decoder-improvement claim |
| V145 | Best arm 0.00000 pp; strongest adversarial arm -0.07434 pp | Domain-adversarial evaluation completed; no arm was promoted |
| V146 | 0.00000 pp for all four importance-weight caps | Covariate-shift evaluation completed; no arm was promoted |
| V147 | No decoder percentage | Exact mechanism-graph recovery and validation |
| V148 | No decoder percentage | Mathematical implementation/conformance audit |
| V149 | 46.38542% to 45.53588%; +0.84954 pp | Historical Fez development; X +1.69907 pp, Z unchanged; fresh 120,000-shot full-coverage Fez confirmation submitted and pending |
| V150 | Best arm 46.38542% to 45.65509%; +0.73032 pp | Historical Fez development; multiscale arm failed Z safety and did not beat V149 |
| V151 | 46.38542% to 45.65509%; +0.73032 pp | 3.68171%-intervention Pareto cascade; strong concentration but 0.11921 pp worse than V149 |
| V152 | 46.38542% to 45.53588%; +0.84954 pp | 100%-coverage population/criticality extension made no safe Z changes and reduced exactly to V149; no incremental gain |
| V153 | 46.38542% to 45.53588%; +0.84954 pp | 100%-coverage symbolic island-GP extension found no safe Z rule and reduced exactly to V149; no incremental gain |
| V154 | 46.38542% to 45.53588%; +0.84954 pp | Eight exact-graph CUDA-Q BP/prior Z variants were tested across three Fez blocks; none passed the two-development-block safety rule, so V154 reduced exactly to V149 |
| V155 | Z-only 35.49206% to 35.47388%; +0.01819 pp | Seven held-domain neural population-router test; confidence interval crossed zero |
| V156 | Z-only 35.49206% to 35.50033%; -0.00827 pp | Configuration-specific neural router regressed; not promoted |
| V157 | V39 Z-only 43.32407% to 43.47685%; -0.15278 pp | Deep Transformer regression; not promoted |
| V158 | Best arm V39 Z-only 43.32407% to 43.24769%; +0.07639 pp | Scratch recurrent-Transformer result; confidence interval crossed zero |
| V159 | Best arm V39 Z-only 43.32407% to 43.31019%; +0.01389 pp | Six-architecture comparison; no arm passed confidence gating |
| V160 | V39 46.38542% to 45.57060%; +0.81481 pp; seven-domain pooled 40.34706% to 39.98429%; +0.36276 pp | Cross-domain evaluation completed on 604,800 shots: X +0.72487 pp, Z +0.00066 pp; Marrakesh regressed and Z CI crossed zero, so not promoted |
| V161 | Seven-domain 40.34706% to 39.90427%; +0.44279 pp; X +0.89153 pp, Z -0.00595 pp | Cross-domain development result; domain regressions prevented promotion |
| V162 | Seven-domain 40.34706% to 39.89269%; +0.45437 pp; X +0.90873 pp, Z unchanged | Cross-domain development result with no negative domain point estimate; positive Z evidence absent |
| V163 | 40.34706% to 39.99223%; +0.35483 pp; X +1.28704 pp, Z -0.57738 pp | Full-coverage development comparator; Z and two Kingston domains regressed |
| V164 | 40.34706% to 39.84210%; +0.50496 pp; X +1.00992 pp, Z unchanged | Nested seven-domain development result with no negative domain point estimate; fresh confirmation still required |
| V165 | Six exact-graph domains 39.52951% to 39.25868%; +0.27083 pp | Nested cost-margin development result; X +0.54167 pp, Z unchanged; not promoted |
| V166 | Six exact-graph domains +0.40374 pp | Configuration-specific syndrome selector; X +0.80748 pp, Z unchanged; not promoted |
| V167 | Seven-domain full coverage 40.34706% to 39.70354%; +0.64352 pp | Strongest retrospective candidate in this audit; X +1.10516 pp and Z +0.18188 pp, but fresh confirmation is required |
| V168 | Repeated-seed range +0.59904 to +0.64352 pp | Positive X and Z gains persisted across five seeds; matched exact-only and syndrome-only ablations were weaker |
| V169 | No new performance percentage | Fez X/Z selectors and thresholds frozen before fresh-outcome retrieval |
| V170 | 40.34706% to 39.79167%; +0.55539 pp | Source-only top-20% feature model; retained positive X/Z gains but was weaker than V167 |
| V171 | Marrakesh 45.25231% to 45.25231%; +0.00000 pp | No source-only X/Z rule passed all safety gates; V12 retained |
| V172 | No decoder percentage | All 12 multi-beam extraction tasks completed successfully; outputs feed V174 |
| V173 | Full coverage +0.06052 pp; X +0.12103 pp, Z unchanged | Neural exact-coset router completed; one Kingston block regressed, so no promotion |
| V174 | Running; no result yet | Six nested multi-beam selector arms are being evaluated; no performance claim |

These opened retrospective results are not independent confirmation evidence and do not replace V12.

The V149 confirmation uses one shared untouched block for exact MWPM, V12,
full BP-OSD and V149. All models will be scored on the same 12 circuits,
120,000 shots and 100% denominator. No confirmation outcome or external job
identifier is published while execution is pending.

Last public update: 24 July 2026, Australia/Sydney.

## Disclosure boundary

This repository does not publish current research ideas or implementation details. Full reproducibility material will be considered after manuscript preparation, institutional review, and security review.
