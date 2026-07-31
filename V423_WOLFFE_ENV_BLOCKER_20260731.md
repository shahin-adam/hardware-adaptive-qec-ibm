# V423 Wolffe environment diagnosis (2026-07-31)

V423 is a synthetic NTU/PyMatching smoke benchmark, not an IBM result. The local run completed successfully. Wolffe Slurm jobs 64848, 64849, 64858, 64860, and 64861 failed before the experiment because the non-interactive compute-node Python environment did not provide a compatible NumPy installation.

The final diagnostic job was 64867. On `a30-003`, `/usr/bin/python` is Python 3.14.6. The available v67 NumPy binary is built for Python 3.13; adding its site-packages to Python 3.14 produces the expected missing `_multiarray_umath` ABI error. The login-shell v67 environment works with Python 3.13, but that interpreter is not present at `/usr/bin/python3.13` on the tested compute node.

Therefore no Wolffe performance number is reported for V423, and no decoder conclusion is drawn from the failed jobs. The local smoke numbers remain the only V423 measurements:

- d=3 standard PyMatching: 0.6000% logical error rate
- d=3 correlated PyMatching: 0.7300%
- d=5 standard PyMatching: 0.3350%
- d=5 correlated PyMatching: 0.2750%

Next valid rerun condition: use a Slurm node/module exposing Python 3.13 with the v67 packages, or install a native Python 3.14 NumPy build in a controlled environment. Do not mix Python 3.13 binary wheels with Python 3.14.
