# Latest controlled QEC results ? 31 July 2026

These are IBM-specific diagnostic experiments. No universal-vendor performance claim is made. All gains are percentage-point reductions in held-out logical error relative to the stated baseline.

| Version | Data / method | Held-out result | Status |
|---|---|---:|---|
| V410 | IBM V29 space-time residual router | -3.556 pp vs V12 | Rejected; temporal summaries alone regressed |
| V411 | IBM V29 strict seven-round specialist | +0.117 pp vs V12; 95% CI -0.161 to +0.407 pp | Diagnostic; not promoted |
| V412 | Recovered IBM 3D handoff, fresh gate on 100 selected rows | -15.152 pp vs stored Transformer reference; 95% CI -42.424 to +12.121 pp | Audit only; subset is not a benchmark |
| V413 | Full 127,200-shot 3D/calibration tensor block | Job gains -2.205 to +1.333 pp vs majority proxy | Diagnostic; V12 vector absent |
| V414 | Full tensor block, round-sequence NumPy fallback | Wolffe job gains -0.583 to +0.564 pp vs majority proxy | Diagnostic; job 64788 completed; V12 vector absent |
| V415 | IBM V29 conformal-style member gate | -0.186 pp vs V12 on held-out test; 5/6 X/Z/round slices regressed | Rejected; Wolffe job 64799 matched local |
| V416 | Full IBM tensor block, true 3D CNN + calibration FiLM | 51.0641% vs 48.3974% majority proxy (-2.667 pp); only basis-0/r7 slice positive | Rejected diagnostic; no paired V12 vector; Wolffe replay 64804 blocked by PyTorch import |
| V420 | Exact-transpiled IBM Kingston MWPM ensemble + residual router, two untouched blocks | 36.1604% vs selected MWPM 36.2849% (+0.1245 pp; CI +0.0203 to +0.2292); +0.2865 pp vs majority | Diagnostic promising; seven-round subgroup regressions; Kingston-only; Wolffe 64814 matched |
| V419 | IBM V29 empirical distance-3 lookup with basis/round/domain safety gates | +0.340 pp overall vs V12; paired 95% CI +0.213 to +0.457 pp; basis-1 −3.718 pp; 3.75% coverage | Rejected; pooled gain fails basis/coverage gates; Wolffe job 64811 matched local |
| V418 | Deterministic reproduction of locked IBM confirmation predictions | Reproduced Transformer 44.9292%, FiLM 44.5450%, UNet 44.7658%, sparse 44.1275%, four-model 44.0908% across 120,000 shots and 12 d/basis/round slices | Verified audit; no fitting; no per-shot V12 vector |
| V417 | Recovered locked IBM Kingston confirmation (120,000 shots, d=3/5, rounds 3/5/7) | MWPM 42.6442%; BP-OSD 43.2592%; four-model ensemble 44.0908%; Transformer 44.9292% | Measured audit; MWPM wins; phenomenological DEM limitation; no universal claim |
## Recovered source evidence

The 15 July IBM 3D handoff contains 127,200 numerical shots with detector masks, 3D volumes, 27 calibration features and job identifiers. Its separate frozen report covers 192,000 scored IBM Kingston shots and reports +0.124 pp versus selected single-MWPM (95% CI +0.024 to +0.223 pp), but it also documents seven-round regressions and incomplete historical calibration information. That source result remains diagnostic until reproduced against the frozen V12 vector with basis and domain gates.

## Audit boundary

`Z:\Meetings\22-7-2026` was unavailable at audit time. `Z:\Meetings\Complete\15-7-2026` yielded 14,983 files, including 5,472 readable QEC-related candidates. Complete/22 source audit found 17,590 entries (8,872 QEC candidates); source files were not deleted.


### V421 — cross-block basis/round guard (31 July 2026)
- IBM Kingston exact-router replay on two untouched blocks; local and Wolffe job 64816 matched exactly.
- Retrospective common allow-list: +0.162500 pp (fresh) and +0.164583 pp (later) versus selected exact-circuit MWPM base.
- Leave-one-block-out transfer: +0.052083 pp and +0.155208 pp.
- Status: diagnostic only. The common allow-list is retrospective, only two blocks exist, and a third independent IBM block is required before promotion. Seven-round slices remain protected by the base decoder.

### V422 â€” independent third-block guard (31 July 2026)
- Frozen V421 policy evaluated without retuning on IBM Kingston D02 future block (108,000 shots).
- Selected MWPM base 33.662963% -> guard 33.003704%; gain +0.659259 pp.
- Paired bootstrap 95% CI: [+0.535185, +0.782407] pp. All six X/Z Ã— round slices are non-regressing; Wolffe job 64819 matches local.
- Status: promoted only for IBM Kingston d=3 under the frozen guard. Distance-5, independent-backend, latency and cross-vendor tests remain open.
### V423 - NTU baseline compatibility smoke
- Recovered NTU standard/correlated PyMatching path ran locally on synthetic Stim d=3/d=5 controls.
- d=3: standard 0.6000%, correlated 0.7300%; d=5: standard 0.3350%, correlated 0.2750% (20,000 shots/mode).
- Wolffe job 64849 is an environment blocker (Slurm Python lacked NumPy); this is not an IBM result and is not promoted.