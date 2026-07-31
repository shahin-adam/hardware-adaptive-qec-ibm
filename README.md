# Hardware-adaptive QEC decoder benchmark

Sanitized, versioned results from the IBM-QEC decoder project. The canonical registry is [`ALL_VERSIONS.md`](ALL_VERSIONS.md); this page is intentionally a short status view.

## How to read the table

- **Gain** is an absolute reduction in logical-error percentage points versus the stated baseline.
- **X/Z** means the basis-specific result; **both** means pooled across bases.
- A result is **promoted** only if held-out X, Z, distance, round and domain gates pass. Diagnostic results are not claims of universal QPU performance.

## Validated baseline

| Version | Distance | Basis | Baseline ? candidate | Gain | Evidence |
|---|---:|---|---:|---:|---|
| V12 | d=3 | X | 39.21682% ? 38.42284% | +0.79398 pp | repeated real IBM hardware |
| V12 | d=3 | Z | 28.14275% ? 26.25077% | +1.89198 pp | repeated real IBM hardware |
| V12 | d=3 | both | 33.67978% ? 32.33681% | +1.34298 pp | 259,200 shots |

## Latest controlled experiments

| Version | Distance | Basis / rounds | Baseline | Candidate | Gain | Status |
|---|---:|---|---:|---:|---:|---|
| V410 | d=3 | both; r=3,5,7 | V12 | temporal residual router | ?3.556 pp | rejected |
| V411 | d=3 | X/Z; specialist only r=7 | V12 | guarded specialist | +0.117 pp | diagnostic; CI ?0.161 to +0.407 pp |
| V412 | source d=5 rows | X/Z; selected manifest | stored Transformer | stored-output gate | ?15.152 pp | audit only; 100-row subset |
| V413 | recovered tensor block | leave-job-out; X/Z metadata | majority proxy | calibration + 3D statistics | job gains -2.205 to +1.333 pp; diagnostic; V12 vector unavailable |
| V414 | recovered tensor block | leave-job-out; round sequence | majority proxy | sequence fallback | Wolffe gains -0.583 to +0.564 pp; diagnostic; V12 vector unavailable |
| V416 | d=3 | X/Z; r=3,5,7 | majority proxy | 3D CNN + FiLM | -2.667 pp | rejected diagnostic; local CPU; Wolffe PyTorch blocked |
| V417 | d=3/5 | X/Z; r=3,5,7 | calibrated MWPM | locked confirmation audit | MWPM 42.6442% | measured audit; analytical baseline wins |
| V418 | d=3/5 | all 12 slices | frozen predictions | reproduction audit | exact source metrics reproduced | verified audit |
| V419 | d=3 | X/Z; r=3,5,7 | V12 | empirical lookup | +0.340 pp pooled | rejected; basis-1 -3.718 pp; 3.75% coverage |
| V420 | d=3 | X/Z; r=3,5,7 | exact calibrated MWPM | residual router | +0.1245 pp vs selected MWPM | diagnostic; seven-round regressions; Wolffe 64814 matched |

## Recovered IBM 3D evidence

The 15 July handoff contains 127,200 numerical shots with 3D volumes, detector masks, 27 calibration features and job identifiers. A separate frozen source report covers 192,000 IBM Kingston shots and reports +0.124 pp versus selected single-MWPM (95% CI +0.024 to +0.223 pp), but documents seven-round regressions and incomplete historical calibration information. It is retained as diagnostic until replayed against paired V12 predictions with full gates.

## Public cross-vendor checks

Google Willow d3/d5 raw detector shots and supplied DEMs are benchmarked separately. They establish DEM/MWPM portability, not IBM transfer or universal-vendor performance.

## Open implementations reviewed

- [BP+OSD / LDPC](https://github.com/quantumgizmos/bp_osd)
- [Google Tesseract decoder](https://github.com/quantumlib/tesseract-decoder)
- [qLDPC toolkit](https://github.com/qLDPCOrg/qLDPC)
- [NVIDIA Ising surface-code pre-decoder](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Accurate)
- [PyMatching](https://github.com/quantumlib/PyMatching)

## Audit boundary

`Z:\\Meetings\\Complete\\15-7-2026` yielded 14,983 files, including 6,322 broad QEC candidates. `Z:\\Meetings\\Complete\\22-7-2026` yielded 17,590 files, including 8,872 broad QEC candidates. The literal `Z:\\Meetings\\22-7-2026` path is unavailable. Source files were not deleted.

Last update: 31 July 2026 (Australia/Sydney).
