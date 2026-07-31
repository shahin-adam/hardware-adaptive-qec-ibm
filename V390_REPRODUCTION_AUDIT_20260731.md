# V390 reproduction audit

V390 was rerun locally from the archived paired IBM Fez NPZ inputs:

- `soft_decoder_confirmation_data.npz`
- `V29_CONFIRMATION.npz`
- source implementation `v390_v29_soft_abstention.py`

All four fixed thresholds reproduced the archived candidate logical-error rates exactly:

| Ï„ | Candidate LER | Archived LER | Difference |
|---:|---:|---:|---:|
| 0.05 | 45.0490741% | 45.0490741% | 0 |
| 0.10 | 45.0500000% | 45.0500000% | 0 |
| 0.15 | 45.0509259% | 45.0509259% | 0 |
| 0.20 | 45.0453704% | 45.0453704% | 0 |

This verifies the V390 artifact and implementation, but does not change its scientific decision: it remains diagnostic/not promoted because distance-5 and other subgroup regressions violate the project safety gate.
