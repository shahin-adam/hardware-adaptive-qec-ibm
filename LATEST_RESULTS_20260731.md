# Latest controlled QEC results ? 31 July 2026

These are IBM-specific diagnostic experiments. No universal-vendor performance claim is made. All gains are percentage-point reductions in held-out logical error relative to the stated baseline.

| Version | Data / method | Held-out result | Status |
|---|---|---:|---|
| V410 | IBM V29 space-time residual router | -3.556 pp vs V12 | Rejected; temporal summaries alone regressed |
| V411 | IBM V29 strict seven-round specialist | +0.117 pp vs V12; 95% CI -0.161 to +0.407 pp | Diagnostic; not promoted |
| V412 | Recovered IBM 3D handoff, fresh gate on 100 selected rows | -15.152 pp vs stored Transformer reference; 95% CI -42.424 to +12.121 pp | Audit only; subset is not a benchmark |
| V413 | Full 127,200-shot 3D/calibration tensor block | Job gains -2.205 to +1.333 pp vs majority proxy | Diagnostic; V12 vector absent |
| V414 | Full tensor block, round-sequence fallback | Job gains -2.667 to +0.263 pp vs majority proxy | Diagnostic; Wolffe replay pending |

## Recovered source evidence

The 15 July IBM 3D handoff contains 127,200 numerical shots with detector masks, 3D volumes, 27 calibration features and job identifiers. Its separate frozen report covers 192,000 scored IBM Kingston shots and reports +0.124 pp versus selected single-MWPM (95% CI +0.024 to +0.223 pp), but it also documents seven-round regressions and incomplete historical calibration information. That source result remains diagnostic until reproduced against the frozen V12 vector with basis and domain gates.

## Audit boundary

`Z:\Meetings\22-7-2026` was unavailable at audit time. `Z:\Meetings\Complete\15-7-2026` yielded 14,983 files, including 5,472 readable QEC-related candidates. Source files were not deleted.
