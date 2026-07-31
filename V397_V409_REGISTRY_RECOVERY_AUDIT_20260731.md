# V397â€“V409 registry recovery audit

The synchronized OneDrive mirror contains version-folder artifacts for V397â€“V404, V407, V408, and V409, while the master registry previously stopped around this range and reported these IDs as missing. V405 and V406 have no readable artifact in either Complete15 or Complete22 mirror, so they are recorded as explicit missing-artifact placeholders rather than inferred experiments.

Recovered results:

- V397: basis-only policy produced no pooled or held-out gain.
- V398: basis/distance/round policy has no independent test shots; diagnostic only.
- V399: matching-cost/V151 screen +0.075 pp pooled and +0.106 pp held-out; UF and DQEC proxies regressed.
- V400: four-tier router regressed âˆ’0.014 pp pooled and âˆ’0.061 pp held-out; rejected.
- V401: temporal-risk router +0.067 pp pooled and +0.069 pp held-out, but r3/r5 subgroups regressed; not promoted.
- V402: Google Willow 3D-CNN smoke lost to majority; not comparable to IBM V12.
- V403: distance-3 specialist +0.074 pp pooled, with +0.722 pp on 7-round shots but a subgroup regression; prospective validation required.
- V404: nested guard has no independent held-out confirmation; diagnostic protocol only.
- V407: public Google distance-conditioned smoke regressed against majority in all d3/d5 X/Z slices.
- V408: public DEM residual adapter regressed against matched MWPM in all four slices.
- V409: public DEM confidence gate had tiny d3 X gain but d3 Z and both d5 slices regressed; rejected.

No version is promoted from this recovery alone. The registry now contains 425 rows for V1â€“V425, with V405/V406 explicitly marked missing rather than fabricated.
