# Hardware-Adaptive Quantum Error Correction on IBM Systems

[![Status](https://img.shields.io/badge/status-offline%20validated-blue)](#validated-results)
[![IBM QPU](https://img.shields.io/badge/IBM%20QPU-submissions%20gated-orange)](#execution-safety)
[![Accuracy](https://img.shields.io/badge/logical%20accuracy-statistically%20null-lightgrey)](#scientific-boundary)

A fail-closed research programme for reliable, reproducible quantum-error-correction decoding on preserved IBM hardware data. The project combines algebraic decoder validation, reproducible GPU batching, independent decoder controls, and guarded preparation for future matched hardware acquisition.

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

The table below preserves the complete percentage-only public ledger through V501. `not recorded` means no defensible numeric value was recoverable; no value was inferred.

| Version | Percentage |
|---|---:|
| V1 | 1.2180 pp; 0.8383 pp |
| V2 | +0.4750 pp; 0.1531 pp |
| V3 | +0.3281 pp; 1.9688 pp |
| V4 | +1.7396 pp development; +0.6505 pp confirmed pooled |
| V5 | +1.5167 pp; 0.0000 pp |
| V6 | +1.5906 pp development; +0.0740 pp confirmation |
| V7 | +1.7313 pp |
| V8 | +1.7443 pp |
| V9 | +1.8125 pp; 0.6493 pp |
| V10 | +1.3600 pp first independent block; +0.7697 pp second block |
| V11 | 1.0918 pp |
| V12 | +1.34298 pp pooled |
| V13 | not recorded |
| V14 | not recorded |
| V15 | not recorded |
| V16 | not recorded |
| V17 | not recorded |
| V18 | not recorded |
| V19 | not recorded |
| V20 | +0.05093 pp incremental; +1.24074 pp vs MWPM |
| V21 | +0.00347 pp incremental; +1.53125 pp vs MWPM |
| V22 | 0.16204% conditional error at 5% retained coverage |
| V23 | +0.021219 pp |
| V24 | +0.001157 pp |
| V25 | +0.128472 pp |
| V26 | not recorded |
| V27 | 1.7222 pp; 0.9667 pp |
| V28 | +0.2847 pp |
| V29 | +0.9741 pp |
| V30 | +0.07639 pp; +0.03241 pp |
| V31 | +0.05440 pp; +0.00347 pp |
| V32 | not recorded |
| V33 | not recorded |
| V34 | not recorded |
| V35 | not recorded |
| V36 | not recorded |
| V37 | not recorded |
| V38 | +1.29514 pp vs MWPM; +0.17245 pp vs V12; +0.016204 pp Fez transfer |
| V39 | +0.804398 pp pooled |
| V40 | +1.223380 pp |
| V41 | not recorded |
| V42 | not recorded |
| V43 | not recorded |
| V44 | not recorded |
| V45 | not recorded |
| V46 | not recorded |
| V47 | not recorded |
| V48 | not recorded |
| V49 | not recorded |
| V50 | not recorded |
| V51 | not recorded |
| V52 | not recorded |
| V53 | not recorded |
| V54 | not recorded |
| V55 | not recorded |
| V56 | not recorded |
| V57 | not recorded |
| V58 | not recorded |
| V59 | not recorded |
| V60 | not recorded |
| V61 | not recorded |
| V62 | not recorded |
| V63 | not recorded |
| V64 | not recorded |
| V65 | not recorded |
| V66 | not recorded |
| V67 | not recorded |
| V68 | not recorded |
| V69 | not recorded |
| V70 | not recorded |
| V71 | not recorded |
| V72 | not recorded |
| V73 | not recorded |
| V74 | not recorded |
| V75 | not recorded |
| V76 | not recorded |
| V77 | not recorded |
| V78 | not recorded |
| V79 | not recorded |
| V80 | not recorded |
| V81 | not recorded |
| V82 | not recorded |
| V83 | not recorded |
| V84 | not recorded |
| V85 | not recorded |
| V86 | not recorded |
| V87 | not recorded |
| V88 | not recorded |
| V89 | not recorded |
| V90 | not recorded |
| V91 | not recorded |
| V92 | not recorded |
| V93 | not recorded |
| V94 | not recorded |
| V95 | not recorded |
| V96 | not recorded |
| V97 | not recorded |
| V98 | not recorded |
| V99 | not recorded |
| V100 | not recorded |
| V101 | not recorded |
| V102 | not recorded |
| V103 | not recorded |
| V104 | not recorded |
| V105 | not recorded |
| V106 | not recorded |
| V107 | +0.053755 pp |
| V108 | not recorded |
| V109 | not recorded |
| V110 | +0.00077 pp; +0.00154 pp |
| V111 | +0.02816 pp; +0.05633 pp; 0.01505 pp |
| V112 | not recorded |
| V113 | not recorded |
| V114 | not recorded |
| V115 | not recorded |
| V116 | not recorded |
| V117 | not recorded |
| V118 | not recorded |
| V119 | not recorded |
| V120 | not recorded |
| V121 | not recorded |
| V122 | not recorded |
| V123 | not recorded |
| V124 | not recorded |
| V125 | not recorded |
| V126 | not recorded |
| V127 | not recorded |
| V128 | not recorded |
| V129 | not recorded |
| V130 | not recorded |
| V131 | not recorded |
| V132 | not recorded |
| V133 | not recorded |
| V134 | not recorded |
| V135 | +0.37252 pp; +0.32424 pp |
| V136 | not recorded |
| V137 | not recorded |
| V138 | not recorded |
| V139 | not recorded |
| V140 | not recorded |
| V141 | not recorded |
| V142 | not recorded |
| V143 | not recorded |
| V144 | not recorded |
| V145 | not recorded |
| V146 | not recorded |
| V147 | not recorded |
| V148 | not recorded |
| V149 | not recorded |
| V150 | not recorded |
| V151 | 0.85818 pp |
| V152 | not recorded |
| V153 | not recorded |
| V154 | 1.2180 pp; 0.8383 pp; +0.4750 pp; 0.1531 pp; +0.3281 pp; 1.9688 pp; +1.7396 pp; +0.6505 pp; +1.5167 pp; 0.0000 pp |
| V155 | not recorded |
| V156 | not recorded |
| V157 | not recorded |
| V158 | not recorded |
| V159 | not recorded |
| V160 | not recorded |
| V161 | not recorded |
| V162 | +0.72487 pp; +0.00066 pp |
| V163 | not recorded |
| V164 | not recorded |
| V165 | not recorded |
| V166 | not recorded |
| V167 | not recorded |
| V168 | not recorded |
| V169 | not recorded |
| V170 | not recorded |
| V171 | not recorded |
| V172 | not recorded |
| V173 | not recorded |
| V174 | not recorded |
| V175 | not recorded |
| V176 | not recorded |
| V177 | not recorded |
| V178 | not recorded |
| V179 | not recorded |
| V180 | not recorded |
| V181 | not recorded |
| V182 | not recorded |
| V183 | not recorded |
| V184 | not recorded |
| V185 | not recorded |
| V186 | not recorded |
| V187 | not recorded |
| V188 | not recorded |
| V189 | not recorded |
| V190 | not recorded |
| V191 | not recorded |
| V192 | not recorded |
| V193 | not recorded |
| V194 | not recorded |
| V195 | not recorded |
| V196 | not recorded |
| V197 | not recorded |
| V198 | not recorded |
| V199 | not recorded |
| V200 | not recorded |
| V201 | not recorded |
| V202 | not recorded |
| V203 | not recorded |
| V204 | not recorded |
| V205 | not recorded |
| V206 | not recorded |
| V207 | not recorded |
| V208 | not recorded |
| V209 | not recorded |
| V210 | not recorded |
| V211 | 0.10 pp |
| V212 | not recorded |
| V213 | not recorded |
| V214 | not recorded |
| V215 | not recorded |
| V216 | not recorded |
| V217 | not recorded |
| V218 | not recorded |
| V219 | not recorded |
| V220 | not recorded |
| V221 | not recorded |
| V222 | +0.01862 pp; 0.00000 pp; +0.03724 pp |
| V223 | not recorded |
| V224 | not recorded |
| V225 | not recorded |
| V226 | not recorded |
| V227 | not recorded |
| V228 | not recorded |
| V229 | not recorded |
| V230 | not recorded |
| V231 | +0.00231 pp; +0.00000 pp |
| V232 | not recorded |
| V233 | -0.03704 pp; 0.00000 pp; -0.07407 pp |
| V234 | not recorded |
| V235 | +0.03931 pp; -0.16509 pp |
| V236 | not recorded |
| V237 | +0.00000 pp; -0.08648 pp |
| V238 | +0.00786 pp; -0.28302 pp |
| V239 | -0.36164 pp; -0.79403 pp |
| V240 | +0.44811 pp; -3.23899 pp |
| V241 | +0.44811 pp; 0.00000 pp; +0.22406 pp |
| V242 | +0.18868 pp; 0.00000 pp |
| V243 | +0.44811 pp; -3.23899 pp; 0.00000 pp; +0.18868 pp |
| V244 | +0.22799 pp; -0.52673 pp; -0.14937 pp |
| V245 | -0.53459 pp |
| V246 | 0.00000 pp |
| V247 | not recorded |
| V248 | -0.57390 pp; -1.17925 pp; -0.87657 pp |
| V249 | +0.22799 pp; -0.52673 pp; -0.14937 pp |
| V250 | 0.00000 pp |
| V251 | +0.02083 pp; -0.18056 pp; -0.07986 pp |
| V252 | +0.00000 pp |
| V253 | +0.04630 pp |
| V254 | not recorded |
| V255 | not recorded |
| V256 | not recorded |
| V257 | not recorded |
| V258 | not recorded |
| V259 | not recorded |
| V260 | not recorded |
| V261 | not recorded |
| V262 | not recorded |
| V263 | not recorded |
| V264 | not recorded |
| V265 | not recorded |
| V266 | not recorded |
| V267 | not recorded |
| V268 | not recorded |
| V269 | not recorded |
| V270 | not recorded |
| V271 | not recorded |
| V272 | not recorded |
| V273 | not recorded |
| V274 | not recorded |
| V275 | not recorded |
| V276 | not recorded |
| V277 | not recorded |
| V278 | not recorded |
| V279 | not recorded |
| V280 | not recorded |
| V281 | not recorded |
| V282 | not recorded |
| V283 | not recorded |
| V284 | not recorded |
| V285 | not recorded |
| V286 | not recorded |
| V287 | not recorded |
| V288 | not recorded |
| V289 | not recorded |
| V290 | not recorded |
| V291 | not recorded |
| V292 | not recorded |
| V293 | not recorded |
| V294 | not recorded |
| V295 | not recorded |
| V296 | not recorded |
| V297 | not recorded |
| V298 | not recorded |
| V299 | not recorded |
| V300 | not recorded |
| V301 | not recorded |
| V302 | not recorded |
| V303 | not recorded |
| V304 | not recorded |
| V305 | not recorded |
| V306 | not recorded |
| V307 | not recorded |
| V308 | not recorded |
| V309 | not recorded |
| V310 | not recorded |
| V311 | not recorded |
| V312 | not recorded |
| V313 | not recorded |
| V314 | not recorded |
| V315 | not recorded |
| V316 | not recorded |
| V317 | not recorded |
| V318 | not recorded |
| V319 | not recorded |
| V320 | not recorded |
| V321 | not recorded |
| V322 | not recorded |
| V323 | not recorded |
| V324 | not recorded |
| V325 | not recorded |
| V326 | not recorded |
| V327 | not recorded |
| V328 | not recorded |
| V329 | not recorded |
| V330 | not recorded |
| V331 | not recorded |
| V332 | not recorded |
| V333 | not recorded |
| V334 | not recorded |
| V335 | not recorded |
| V336 | not recorded |
| V337 | not recorded |
| V338 | not recorded |
| V339 | not recorded |
| V340 | not recorded |
| V341 | not recorded |
| V342 | not recorded |
| V343 | not recorded |
| V344 | not recorded |
| V345 | not recorded |
| V346 | not recorded |
| V347 | not recorded |
| V348 | not recorded |
| V349 | not recorded |
| V350 | not recorded |
| V351 | not recorded |
| V352 | not recorded |
| V353 | not recorded |
| V354 | not recorded |
| V355 | not recorded |
| V356 | not recorded |
| V357 | not recorded |
| V358 | not recorded |
| V359 | +0.15972pp |
| V360 | -0.0637pp |
| V361 | +0.06996pp; -0.0104pp; +0.1470pp; -0.0266pp |
| V362 | +0.05298pp; +0.1238pp |
| V363 | +0.05298pp; -0.0255pp |
| V364 | not recorded |
| V365 | +0.06713pp; -0.05556pp; +0.01736pp; +0.11921pp; +0.07986pp; +0.18403pp; +0.09144pp; +0.00116pp; +0.14352pp |
| V366 | +0.07305pp; +0.14236pp |
| V367 | +0.06237pp; +0.14352pp |
| V368 | +0.07677pp; +0.21644pp |
| V369 | -0.01402pp; -0.08681pp |
| V370 | +0.00836pp; -0.16898pp |
| V371 | +0.01196pp; +0.03472pp |
| V372 | +0.05337pp; +0.17361pp |
| V373 | +0.01800pp; +0.04282pp |
| V374 | +0.06970pp; +0.19213pp |
| V375 | +0.02739pp; +0.18634pp |
| V376 | +0.02739pp; +0.18634pp |
| V377 | +0.01595pp; +0.18634pp |
| V378 | +0.01453pp; +0.03356pp |
| V379 | +0.01723pp; +0.09722pp |
| V380 | +0.01698pp; -0.00463pp |
| V381 | +0.02276pp; +0.06366pp |
| V382 | +0.02251pp; +0.06366pp |
| V383 | +0.00694pp; +0.03588pp |
| V384 | +0.02238pp; -0.02431pp |
| V385 | -0.00694pp; -0.09606pp |
| V386 | +0.00180pp; +0.04167pp |
| V387 | +0.01608pp; +0.06250pp |
| V388 | -0.00360pp; +0.09606pp |
| V389 | +1.7111pp |
| V390 | +0.9657pp; +0.9648pp; +0.9639pp; +0.9694pp |
| V391 | +0.9648pp |
| V392 | +0.8806pp |
| V393 | +0.662963 pp |
| V394 | +0.662963 pp; -0.124074 pp |
| V395 | not recorded |
| V396 | +0.005556 pp |
| V410 | +0.000000 pp |
| V411 | +0.117284 pp |
| V412 | -15.151515 pp; +0.124 pp |
| V413 | +1.333333 pp |
| V414 | +0.262821 pp |
| V415 | -0.186111 pp |
| V416 | -2.6667 pp; +0.7692 pp |
| V417 | not recorded |
| V418 | not recorded |
| V419 | +0.3395 pp; +0.457 pp |
| V420 | +0.1245 pp; +0.2865 pp |
| V421 | +0.162500 pp; +0.164583 pp; +0.155208 pp |
| V422 | +0.659259 pp; +0.782407 pp |
| V423 | not recorded |
| V424 | +1.0768519 pp |
| V425 | -0.1531250 pp |
| V397 | +0.000000 pp; +0.000000 pp |
| V398 | not recorded |
| V399 | +0.075000 pp; +0.105556 pp |
| V400 | -0.013889 pp; -0.061111 pp |
| V401 | +0.066667 pp; +0.068519 pp |
| V402 | -3.740000 pp |
| V403 | +0.022222 pp; +0.074074 pp; +0.722222 pp |
| V404 | not recorded |
| V405 | not recorded |
| V406 | not recorded |
| V407 | 12.553333 pp |
| V408 | 15.653333 pp |
| V409 | +0.006667 pp |
| V426 | +0.2212963 pp; +0.0740741 pp |
| V427 | +0.1018519 pp |
| V428 | 0.000000 pp |
| V429 | -0.0005556 pp |
| V430 | -0.2062500 pp |
| V431 | +0.2650463 pp |
| V432 | +0.1203704 pp |
| V433 | +0.1828704 pp; -0.0031250 pp |
| V434 | +0.0729167 pp; -0.1885417 pp |
| V435 | +0.0405093 pp |
| V436 | -0.0949074 pp |
| V437 | -0.0768519 pp |
| V438 | -0.0192308 pp |
| V439 | not recorded |
| V440 | not recorded |
| V441 | not recorded |
| V442 | not recorded |
| V446 | +0.090667 pp |
| V443 | +0.038462 pp; +1.256410 pp |
| V444 | +0.696296 pp; +0.459259 pp |
| V445 | +0.227778 pp |
| V447 | +0.313667 pp sweep maximum; +0.090667 pp at fixed 0.80 |
| V448 | +0.007292 pp; +0.019792 pp; +0.649074 pp held-out blocks |
| V449 | +0.043750 pp; +0.056250 pp; +0.649074 pp held-out blocks |
| V450 | +0.043750 pp; +0.056250 pp; +0.649074 pp |
| V451 | +0.128125 pp; +0.151042 pp; +0.649074 pp held-out blocks |
| V452 | +0.010417 pp; +0.016667 pp; +0.227778 pp |
| V453 | 35.4600%/46.5000%/48.9500%; 17.4000%/32.7700%/42.5800% |
| V454 | not recorded |
| V455 | not recorded |
| V456 | not recorded |
| V457 | not recorded |
| V458 | not recorded |
| V459 | not recorded |
| V460 | not recorded |
| V461 | not recorded |
| V462 | not recorded |
| V463 | not recorded |
| V464 | +0.003205 pp |
| V465 | not recorded |
| V466 | not recorded |
| V467 | +0.100000 pp; -0.150000 pp; +0.000000 pp; +0.250000 pp; +0.100000 pp; +0.000000 pp |
| V468 | not recorded |
| V469 | not recorded |
| V470 | +0.130000 pp; +0.080000 pp; +0.090000 pp; +0.050000 pp |
| V471 | +0.015000 pp; -0.070000 pp; +0.120000 pp; +0.075000 pp; +0.090000 pp; +0.045000 pp |
| V472 | +0.000000 pp; +0.109000 pp; +0.102000 pp; +0.088000 pp; +0.086000 pp |
| V473 | +0.103000 pp; +0.000000 pp; +0.109000 pp; +0.102000 pp; +0.088000 pp; +0.086000 pp |
| V474 | +0.025157 pp; +0.000000 pp; +0.358491 pp; -1.191824 pp; -0.202044 pp pooled |
| V475 | +0.256667 pp; +0.000000 pp; -0.426667 pp; +0.000000 pp; -0.042500 pp pooled |
| V476 | +0.176667 pp; +0.000000 pp; +0.088333 pp pooled |
| V477 | +0.000000 pp pooled |
| V478 | +0.433333 pp; -0.113333 pp; -0.300000 pp; +0.046667 pp; +0.016667 pp pooled |
| V479 | +0.305000 pp selected slice |
| V480 | +0.442000 pp selected slice |
| V481 | not recorded |
| V482 | 51.822917% raw; 42.187500% raw |
| V483 | not recorded |
| V484 | not recorded |
| V485 | -3.190 pp |
| V486 | not recorded |
| V487 | 0.700000%/1.230000%/1.600000%; 0.700000%/1.060000%/1.410000%; 0.190000%/0.270000%/0.650000%; 0.300000%/0.380000%/0.460000%; 0.070000%/0.140000%/0.190000%; 0.030000%/0.070000%/0.210000% |
| V488 | 48.697917%/51.822917%; 41.927083%/42.187500%; 51.041667%/45.833333%; 50.520833%/48.437500%; 51.041667%/54.166667%; 51.562500%/50.520833% |
| V489 | not recorded |
| V490 | 100% syndrome closure; accuracy withdrawn |
| V491 | not recorded |
| V492 | 100% syndrome closure; accuracy withdrawn |
| V493 | not recorded |
| V494 | 100% syndrome closure; accuracy withdrawn |
| V495 | 100% syndrome closure; accuracy withdrawn |
| V496 | not recorded |
| V497 | 100% syndrome closure; accuracy withdrawn |
| V498 | 2.864583% fast-path coverage; 23.632812% logical disagreement; accuracy withdrawn |
| V499 | 90.234375% same-seed route agreement; 92.708333% reverse-order route agreement |
| V500 | 99.821% correction-bit reproducibility; accuracy withdrawn |
| V501 | 50.390625% raw; 49.934896% decoded; +0.455729 pp |

