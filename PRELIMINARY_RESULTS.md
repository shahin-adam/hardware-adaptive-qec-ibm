# Preliminary real-hardware results

Updated 24 July 2026.

Project team: Dr Weisheng, academic supervisor; Shahin Adam, lead student researcher and technical implementer. Western Sydney University.

This page reports sanitized aggregate evidence from a study of reducing logical quantum-error-correction error rates across two complementary bases. Results remain subject to academic review. Private methods, datasets, credentials, models, and current research ideas are intentionally excluded.

## How to read these results

An apples-to-apples comparison must use the same hardware block, scored shots, circuit cohort, bases, denominator, and baseline. For that reason:

- Each table below contains only results evaluated on identical shots within that table.
- Results in different tables must not be directly ranked or combined.
- All main tables use the full scored denominator with 100% coverage.
- A percentage-point (pp) improvement is baseline error minus candidate error; larger positive values are better.
- Conditional/postselected results are reported separately and are not full-decoder error rates.
- The complete experiment history is an audit index, not a leaderboard; see [ALL_VERSIONS.md](ALL_VERSIONS.md).

The canonical registry now contains an explicit row for every version from
V1 through V173. This preliminary-results page contains only comparable
headline tables; absence from this page does not mean that a version is
missing from the project record.

## Current post-V12 development

| Version | Pooled development observation | Decision/status |
| --- | ---: | --- |
| V125 | +0.33267 pp over V12 | Not promoted; basis/domain safety failed |
| V128 | +0.37252 pp over V12 | Not promoted; strict held-cell confidence requirement failed |
| V129 | +0.07490 pp over V12 | Not promoted; external-backbone transfer gate failed |
| V130 | +0.32424 pp over V12 | Not promoted; X-only gain and negative worst-fold bound |
| V131 | Best +0.00000 pp; fine-tuned -0.01141 pp | Not promoted |
| V132 | +0.00000 pp in all arms | Not promoted |
| V133 | Best +0.44015 pp; X +0.87500 pp, Z +0.00529 pp | Not promoted; negative held cells |
| V134 | Not a decoder metric | No decoder-performance claim |
| V135 | Best +0.37550 pp; X +0.75099 pp, Z unchanged | Not promoted; negative held cells |
| V136 | Best +0.27993 pp; X +0.55985 pp, Z unchanged | Not promoted |
| V137 | Best +0.15476 pp; X +0.30952 pp, Z unchanged | Not promoted |
| V138 | +0.00000 pp in all arms | Not promoted |
| V139 | Completed metric audit | No decoder-improvement claim |
| V140 | Best zero-shot +0.17342 pp; few-shot +0.16750 pp | Not promoted |
| V141 | Best +0.23472 pp; X +0.46944 pp, Z unchanged | Not promoted; negative held cells |
| V142 | +0.00000 pp in both matched variants | Not promoted |
| V143 | Completed drift audit | No decoder-improvement claim |
| V144 | Completed algebraic audit | No decoder-improvement claim |
| V145 | Best +0.00000 pp; adversarial arm -0.07434 pp | Not promoted |
| V146 | +0.00000 pp in all four arms | Not promoted |

These are opened-domain development experiments. They demonstrate continued
model progress but do not replace V12 without a complete X/Z/backend safety
pass and a new untouched IBM confirmation block.

## Metric-definition note

The percentages reported on this page are full-circuit logical-error fractions over the stated scored shots. They are **not** logical error per error-correction round (LER/round) and must not be compared directly with per-round results from studies such as AlphaQubit.

An AlphaQubit-compatible LER requires the logical-error fraction at known syndrome-round counts and either (i) inversion of the repeated-round fidelity model at a fixed round count, or (ii) a fit of log fidelity across several round counts with fit-quality diagnostics. The private audit now additionally tracks round count, code distance, fitted LER, fit quality, detection-event density, distance-suppression factor, probability calibration, decoder throughput and final latency. Blank fields mean that the preserved evidence does not support that measurement. No validated LER/round or distance-suppression claim is currently made for V12.

## Primary repeated result

This is the strongest repeated full-denominator result. It pools three post-freeze real-hardware blocks using the same frozen V12 candidate and matched baseline on every scored shot.

| Candidate | Blocks | Scored shots | Coverage | Baseline error | Candidate error | Improvement | Relative reduction | Evidence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| V12 | 3 | 259,200 | 100% | 33.67978% | 32.33681% | 1.34298 pp | 3.9875% | Repeated full-denominator evaluation |

The same preserved predictions support an exact basis split:

| Basis | Scored shots | Coverage | Baseline error | V12 error | Improvement | Paired 95% CI | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| X | 129,600 | 100% | 39.21682% | 38.42284% | 0.79398 pp | 0.65881 to 0.92916 pp | Confirmed positive |
| Z | 129,600 | 100% | 28.14275% | 26.25077% | 1.89198 pp | 1.72304 to 2.06091 pp | Confirmed positive |

Both bases improve, but the full-denominator below-1% two-basis target has not been achieved.

## Same-shot comparison A: V20 block

All rows use the same 86,400 scored shots and the same matched baseline.

| Candidate | Coverage | Baseline error | Candidate error | Improvement vs baseline | Increment beyond V12 | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| V12 | 100% | 34.5845% | 33.3947% | 1.1898 pp | — | Confirmed |
| V12 + V20 | 100% | 34.5845% | 33.3438% | 1.2407 pp | 0.0509 pp | Confirmed positive increment |

## Same-shot comparison B: V21 block

All rows use the same 86,400 scored shots and the same matched baseline.

| Candidate | Coverage | Baseline error | Candidate error | Improvement vs baseline | Increment beyond V12 | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| V12 | 100% | 34.6771% | 33.1493% | 1.5278 pp | — | Confirmed |
| V12 + V21 | 100% | 34.6771% | 33.1458% | 1.5313 pp | 0.0035 pp | Null increment |

## Same-shot comparison C: V22 block

The full-denominator row uses all 86,400 scored shots.

| Candidate | Coverage | Baseline error | Candidate error | Improvement vs baseline | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| V12 | 100% | 31.7778% | 30.4664% | 1.3113 pp | Confirmed |

The V22 conditional result is intentionally excluded from this table because it retained only 5% of shots.

## Same-shot comparison D: V38 confirmation block

All rows use the same 86,400 scored shots and the same matched baseline.

| Candidate | Coverage | Baseline error | Candidate error | Improvement vs baseline | Increment beyond V12 | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Mathematical comparator | 100% | 35.7153% | 35.0035% | 0.7118 pp | — | Confirmed |
| V12 | 100% | 35.7153% | 34.5926% | 1.1227 pp | — | Confirmed |
| V12 + V38 | 100% | 35.7153% | 34.4201% | 1.2951 pp | 0.1725 pp | Confirmed positive increment |

This is the strongest independently confirmed same-block hybrid result in the public evidence.

## Same-shot comparison E: cross-hardware transfer block

All rows use the same 86,400 scored shots and the same matched baseline. This block shows why results must be compared on identical data rather than ranked across blocks.

| Candidate | Coverage | Baseline error | Candidate error | Improvement vs baseline | Increment beyond V12 | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| V39 | 100% | 46.5127% | 45.7083% | 0.8044 pp | — | Confirmed on this block |
| V12 | 100% | 46.5127% | 46.3854% | 0.1273 pp | — | Null transfer result |
| V12 + V38 | 100% | 46.5127% | 46.3692% | 0.1435 pp | 0.0162 pp | Null hybrid increment |

## Same-shot comparison F: V68 block

All rows use the same 86,400 scored shots and the same matched baseline.

| Candidate | Coverage | Baseline error | Candidate error | Improvement vs baseline | Increment beyond V12 | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| V12 | 100% | 32.7581% | 31.2303% | 1.5278 pp | — | Confirmed |
| V12 + V68 | 100% | 32.7581% | 31.2072% | 1.5509 pp | 0.0231 pp | Null increment; improvement is principally attributable to V12 |

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
| V107 | 9 | 777,600 | 100% | 39.28987% baseline to 39.23611% candidate; 0.05376 pp improvement; sealed null | Retrospective leave-one-domain-out development |
| V149 | 1 | 86,400 | 100% | 46.38542% V12 to 45.53588% candidate; 0.84954 pp improvement; X +1.69907 pp and Z unchanged | Historical Fez configuration-routing development; not promoted |
| V150 | 1 | 86,400 | 100% | Best arm 46.38542% V12 to 45.65509% candidate; 0.73032 pp improvement; multiscale arm regressed Z | Historical Fez development; not promoted |
| V151 | 1 | 86,400 | 100% | 46.38542% V12 to 45.65509% candidate; +0.73032 pp while intervening on 3.68171% of shots | Historical Fez Pareto-concentration development; 0.11921 pp worse than V149 |
| V152 | 1 | 86,400 | 100% | 46.38542% V12 to 45.53588% candidate; +0.84954 pp; X +1.69907 pp and Z unchanged | Historical Fez population/criticality extension; no safe Z intervention, therefore identical to V149 |
| V153 | 1 | 86,400 | 100% | 46.38542% V12 to 45.53588% candidate; +0.84954 pp; X +1.69907 pp and Z unchanged | Historical Fez symbolic island-GP extension; no evolved Z program passed the safety gate, therefore identical to V149 |
| V154 | 3 | 86,400 evaluation | 100% | 46.38542% V12 to 45.53588% candidate; +0.84954 pp; X +1.69907 pp and Z unchanged | Exact-graph CUDA-Q Z sweep selected on two Fez blocks and evaluated on a third opened block; no Z variant passed, therefore identical to V149 |
| V155 | 7 | 302,400 Z shots | 100% | 35.49206% V12 to 35.47388% candidate; +0.01819 pp; 95% CI crossed zero | Held-domain neural population-router development null |
| V156 | 7 | 302,400 Z shots | 100% | 35.49206% V12 to 35.50033% candidate; -0.00827 pp | Configuration-specific neural-router development null |
| V157 | 1 | 43,200 Z shots | 100% | 43.32407% V12 to 43.47685% candidate; -0.15278 pp | Held V39 deep-Transformer regression |
| V158 | 1 | 43,200 Z shots | 100% | Best arm 43.32407% V12 to 43.24769% candidate; +0.07639 pp; 95% CI crossed zero | Recurrent-Transformer scratch/pretrained transfer controls; no promotion |
| V159 | 1 | 43,200 Z shots | 100% | Best arm 43.32407% V12 to 43.31019% candidate; +0.01389 pp; 95% CI crossed zero | Six neural architecture families; no promotion |
| V160 | 7 | 604,800 X/Z shots | 100% | 40.34706% V12 to 39.98429% candidate; +0.36276 pp pooled; X +0.72487 pp (95% CI +0.56248 to +0.88725), Z +0.00066 pp (95% CI -0.00392 to +0.00524) | Cross-domain development completed; Marrakesh regressed and the Z interval crossed zero, so no promotion |
| V161 | 7 | 604,800 X/Z shots | 100% | 40.34706% V12 to 39.90427% candidate; +0.44279 pp pooled; X +0.89153 pp, Z -0.00595 pp | Cross-domain development result; Marrakesh and one Kingston block regressed, so no promotion |
| V162 | 7 | 604,800 X/Z shots | 100% | 40.34706% V12 to 39.89269% candidate; +0.45437 pp pooled; X +0.90873 pp, Z +0.00000 pp | Cross-domain development result with no negative domain point estimate; positive Z and all-domain lower bounds were absent |
| V163 | 7 | 604,800 X/Z shots | 100% | 40.34706% V12 to 39.99223% candidate; +0.35483 pp pooled; X +1.28704 pp, Z -0.57738 pp | Full-support development comparator; Z and two Kingston domains regressed, so no promotion |
| V164 | 7 | 604,800 X/Z shots | 100% | 40.34706% V12 to 39.84210% candidate; +0.50496 pp pooled (95% CI +0.45936 to +0.55056); X +1.00992 pp, Z +0.00000 pp | Nested cross-domain development result with no negative domain point estimate; fresh confirmation and positive Z evidence remain absent |
| V165 | 39.52951% | 39.25868% | +0.27083 pp | X +0.54167 pp; Z unchanged | Six exact-graph domains; retrospective development, not promoted |
| V166 | 39.52951% | 39.12577% | +0.40374 pp | X +0.80748 pp; Z unchanged | Six exact-graph domains; retrospective development, not promoted |
| V167 | 40.34706% | 39.70354% | +0.64352 pp | X +1.10516 pp; Z +0.18188 pp | Seven-domain 100%-coverage retrospective development; fresh confirmation required |
| V168 | 40.34706% | 39.70354% best repeated seed | +0.59904 to +0.64352 pp | Positive X and Z gains across five seeds | Robustness development; no independent confirmation claim |
| V169 | — | — | — | Frozen X/Z deployment package | No new percentage; frozen before fresh-outcome retrieval |
| V170 | 40.34706% | 39.79167% | +0.55539 pp | X +1.08366 pp; Z +0.02712 pp | Top-20% feature development result; weaker than V167 |
| V171 | 45.25231% | 45.25231% | +0.00000 pp | No X/Z intervention | Source-only safety null on Marrakesh |
| V172 | — | — | — | Performance pending | Multi-beam exact-coset extraction running |
| V173 | 40.34706% | 40.28654% | +0.06052 pp | X +0.12103 pp; Z unchanged | Neural router completed; Kingston regression prevented promotion |
| V174 | 40.34706% | 39.73132% | +0.61574 pp | X +1.06019 pp; Z +0.17130 pp | Multi-beam exact-coset development; weaker than V167 |
| V175 | 40.34706% | 39.73099% | +0.61607 pp | X +1.06713 pp; Z +0.16501 pp | Exact-coset refinement; weaker than V167 |
| V176 | 40.34706% | 39.70470% | +0.64236 pp | X +1.10350 pp; Z +0.18122 pp | Authoritative V167 reproduction; second-stage residual was null |
| V177 | 40.34706% | 39.91898% | +0.42808 pp | X +0.85615 pp; Z unchanged | Exact-IBM graph pretraining; incremental CI over scratch crossed zero |
| V178 | 40.34706% | 39.72239% | +0.62467 pp | X +1.06812 pp; Z +0.18122 pp | Label-sealed stack; weaker than V167 |
| V179 | 40.34706% | 39.86194% | +0.48512 pp | X +0.97024 pp; Z unchanged | Scaled basis-separated graph pretraining; weaker than V167 |
| V181 | 40.34706% | 39.93882% | +0.40823 pp | X +0.81647 pp; Z unchanged | IBM-adapted recurrent graph-attention core; Marrakesh regressed |
| V182 | 40.34706% | 39.64897% | +0.69808 pp | X +1.21495 pp; Z +0.18122 pp | Label-sealed V167/V179 cascade; retrospective development only |
| V184 | 40.34706% | 39.89633% | +0.45073 pp | X +0.90146 pp; Z unchanged | Causal temporal decoder; Marrakesh regressed |
| V185 | 40.34706% | 39.69907% | +0.64798 pp | X +1.11475 pp; Z +0.18122 pp | Holland classifier-system router; below V182 |
| V186 | 40.34706% | 39.70370% | +0.64335 pp | X +1.10549 pp; Z +0.18122 pp | Best hierarchical partial-pooling arm; negligible increment over V167 reproduction |
| V187 | 40.34706% | 39.63624% | +0.71081 pp | X +1.23512 pp; Z +0.18651 pp | Strongest retrospective point estimate; +0.01273 pp versus V182 with CI crossing zero |
| V188 | 40.34706% | 39.63029% | +0.71677 pp | X +1.25231 pp; Z +0.18122 pp | Temporal delayed-credit router; strongest retrospective point estimate, not independent confirmation |

V106 tested a target-label-free calibrated fallback policy. No candidate achieved a positive paired 95% lower improvement bound in every training domain separately for X and Z. No new hardware confirmation was requested.

V107's pooled paired 95% interval for the 0.05376-point estimate was -0.04517 to +0.15268 percentage points, and no held domain had a positive lower bound. It is therefore not a confirmed improvement and is excluded from the leaderboard.

V149 recovered configuration-specific value by retaining V12 except on two
preselected Fez X-basis configurations. Its pooled paired 95% interval was
0.66018 to 1.03890 percentage points. V150 tested an exponentially spaced
multiscale representation; it remained positive in aggregate but did not beat
V149 and failed the separate Z safety requirement. Both blocks had previously
been opened, so neither result replaces the validated V12 claim.

V151 tested whether V149's useful minority could be narrowed further. It
retained 100% prediction coverage through V12 fallback and achieved a positive
aggregate result, but the additional selectivity discarded useful corrections
and did not beat V149.

V152 tested a covariance-aware population decoder and a detector-cascade
criticality gate as a separate Z extension to V149. Neither OSD-guided changes
nor direct V12 flips passed the multiplicity-adjusted tuning safety bound.
V152 therefore retained 100% coverage but made zero Z changes and produced no
incremental improvement beyond V149. This is a sealed development null, not a
new performance claim.

V153 evolved strongly typed symbolic routing rules in four migrating island
populations. Neither OSD-selection nor direct-flip rules passed the
multiplicity-adjusted per-cell safety gate. V153 therefore also retained 100%
coverage but reduced exactly to V149, with zero incremental improvement.

V154 tested eight exact-circuit CUDA-Q BP-OSD and physical-prior variants.
Selection used two Fez development blocks and required a positive paired lower
confidence bound in both. No configuration-level or pooled-Z variant passed.
The third opened Fez block was evaluated only after selection; V154 retained
V12 for every Z shot and reduced exactly to V149.

V160's complete seven-domain evaluation confirmed that its useful effect is
concentrated in X/Fez. Across 604,800 opened real-IBM shots it improved the
pooled error by 0.36276 percentage points, but Z was statistically null, three
Kingston domains were inactive, and Marrakesh regressed by 0.18171 points.
It therefore remains development evidence and does not replace V12.

V161 and V162 each improved the opened V39 Fez development block by about
0.90 percentage points relative to V12, entirely through X-basis changes.
Across all seven domains, V161 retained +0.44279 pp but introduced small
Marrakesh, Kingston and Z regressions. V162 retained +0.45437 pp with no
negative domain point estimate, but Z remained unchanged. Neither result is a
validated replacement for V12.

V163's full-support comparator improved X but significantly damaged Z. V164
used a nested same-backend evidence gate and retained V12 outside the
consistently useful Fez X cells. It improved the seven-domain pooled error by
0.50496 percentage points with no negative domain point estimate. Z remained
unchanged, and all domains were already opened, so V164 remains development
evidence pending a frozen fresh confirmation.

V149 has now been frozen for a new 120,000-shot Fez confirmation covering all
12 X/Z, 3/5/7-round and logical-state cells. Exact MWPM, V12, full BP-OSD and
V149 will decode the identical outcomes, giving a paired 100%-coverage
comparison. Execution is pending; no new improvement is claimed.

V172 completed 12 larger-beam exact-coset extraction tasks without errors.
V174 and V175 converted those outputs into positive X/Z development signals
of +0.61574 and +0.61607 percentage points respectively, but neither exceeded
V167. V176 reproduced the V167 pipeline at +0.64236 pp (within 0.00116 pp of
the archived result); eight compatible second-stage residual arms then added
exactly 0.00000 pp.

V177 adapted the synthetic-pretraining principle to recovered exact IBM fault
graphs. Its best arm improved V12 by +0.42808 pp, concentrated in X. The
increment over an architecture-identical scratch control was only +0.02563 pp
and its paired confidence interval crossed zero; Z was unchanged and
Marrakesh regressed. V178 then stacked the independent V167 and V177 experts
using other-domain evidence only. It achieved +0.62467 pp with positive X and
Z development gains but remained below V167. V179 increased synthetic exposure
with independent basis experts and reached +0.48512 pp, concentrated entirely
in X, so it did not replace V167.

V182 combined V167's exact-coset Z evidence with V179's Fez-X expert using
source-only routing and reached +0.69808 pp. V185's book-derived classifier
system and V186's hierarchical partial pooling remained below V182. V187 added
an exact-coset MAP residual and produced the largest retrospective point
estimate, +0.71081 pp. Its +0.01273 pp increment over V182 had a paired 95%
interval of -0.02686 to +0.05233 pp, so superiority over V182 is not
statistically established. V188 then used source-only temporal delayed credit
to reach +0.71677 pp. Its increment over V182 was +0.01868 pp with a paired
95% interval of +0.00047 to +0.03690 pp, while its +0.00595 pp increment over
V187 had an interval crossing zero. None of V182-V188 is fresh independent
confirmation.

V180 records a future IBM circuit-level detector-rate optimization protocol.
It has no decoder percentage and cannot run retrospectively because the
historical shots do not contain randomized policy assignments. It is listed
to distinguish a pre-registered hardware experiment from a completed result.

V189 completed with +0.84537 pp on one held historical block, concentrated in
X (+1.69074 pp) while Z remained unchanged. It is therefore a specialist
development result rather than a universal replacement. V190 remains a
running comparison of no alignment against class-conditional covariance and
third-moment alignment.

## External real-IBM repetition-code transfer

V199 performs three leave-one-backend-out tests on an independently published
real-IBM repetition-code dataset. Its primary calibration-conditioned model
improved Fez by +1.10986 pp, Kingston by +0.91347 pp, and Pittsburgh by
+0.70499 pp. The X and Z lower 95% confidence bounds were positive in all
three held-backend folds.

This is strong cross-device transfer evidence, but it is deliberately
separated from the surface-code ranking: the code family, labels, circuits,
and baseline differ, and the data are retrospective rather than a fresh IBM
execution. It does not replace V12.

V203 then tested ERM, IRMv1, and MMD under a balanced synthetic heterogeneous
noise protocol. The best held-environment gain was only +0.00167 pp with a
lower 95% confidence bound of -0.00160 pp. V204 subsequently completed its
bounded invariant-plus-calibration-residual follow-up; its results are reported below.
## Correlation-aware retrospective routing

V205 evaluated a full-coverage source-only router on 604,800 opened real-IBM
shots. It reduced the matched V12 error from 40.34706% to 39.62930%, a
+0.71776 percentage-point development gain. X improved by +1.25430 points
and Z by +0.18122 points. All domain point estimates were non-negative, but
Marrakesh retained V12 exactly. The incremental gain over V187 was only
+0.00694 points and was not statistically established.

This is retrospective development evidence, not fresh confirmation, and it
does not replace V12 as the validated full-coverage winner.
## Historical-data diversity ablation

V206 held the residual architecture, seeds, source/validation splits and V12
fallback fixed while adding one opened historical Kingston block to training.
The augmentation improved its matched current-data-only student by +0.05192
percentage points (95% CI +0.01013 to +0.09370), but the augmented student
still regressed by -0.06763 points versus V12. The benefit was concentrated
in Kingston and did not improve Fez or Marrakesh transfer.

This is useful data-ablation evidence, not a promoted decoder.
## Leakage-safe level-1 IQ ablation

V207 evaluated frozen V12 on a historical real-IBM level-1 IQ block. V12
improved the pooled error by +1.18958 percentage points, but X regressed by
-0.06250 points while Z improved by +2.44167 points. A matched residual model
using only intermediate-measurement analog confidence improved over its
hard-only control by +0.08333 points; its 95% interval crossed zero and a
permuted-IQ control was statistically indistinguishable.

V207 is historical single-backend development evidence and was not promoted.
## Pre-registered decoder switching

V208 selected between exact-circuit MWPM and frozen V12 separately for X3, X5,
X7, Z3, Z5, and Z7 using a validation time segment only. Only Z7 passed the
positive-lower-confidence-bound rule. On the held final time segment, the
switched decoder improved over MWPM by +1.25000 percentage points: X was
unchanged and Z improved by +2.50000 points.

This eliminated the X regression observed when applying V12 broadly, but it did
not outperform frozen V12 overall. The result is historical single-backend
development evidence and was not promoted.
## Completed bounded calibration adapter

The completed V204 campaign used an external real-IBM repetition-code dataset
with complete leave-one-backend-out evaluation over Fez, Kingston and
Pittsburgh. Under one shared perturbation bound, the invariant backbone
improved the benchmark baseline by +0.76971 percentage points, and the bounded
calibration adapter added a further +0.01512 points (95% CI +0.01291 to
+0.01732). The complete model improved X by +0.75498 points and Z by +0.80668
points over the external baseline.

This is strong external repetition-code development evidence, but it is not a
surface-code experiment and is not directly comparable with V12.
## Completed moment-alignment ablation

V190 completed five real-IBM development arms. Its unaligned control had the
largest pooled gain, +0.41245 percentage points, with X +0.82491 points and Z
unchanged. The best covariance-aligned arm reached +0.40040 points, while
stronger covariance and third-moment penalties progressively reduced the gain.

The control regressed one Marrakesh X domain, and no arm activated Z. V190 was
therefore rejected as a V12 successor.
## Uncertainty-filtered pseudo-label test

V209 tested transductive semi-supervised adaptation across seven opened
real-IBM domains. The best uncertainty-filtered arm changed V12 by -0.07093
percentage points overall: X -0.14484 points and Z +0.00298 points. Its small
+0.01521-point increment over a matched weak source-only student was not
significant and was reproduced by a random-position control.

The experiment therefore found no useful pseudo-label signal and was rejected.
Target labels were opened only by a separate evaluator after prediction
artifacts were frozen.