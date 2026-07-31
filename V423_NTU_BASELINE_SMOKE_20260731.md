# V423 NTU baseline compatibility smoke

The recovered NTU surface-code baseline was executed locally on synthetic Stim circuits. It is not an IBM hardware result.

| distance | standard PyMatching | correlated PyMatching |
|---:|---:|---:|
| d=3 | 0.6000% | 0.7300% |
| d=5 | 0.3350% | 0.2750% |

Wolffe job 64849 was blocked by a Slurm Python environment missing NumPy; no performance interpretation is made.