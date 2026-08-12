# Learning Under Hardware Shift: Neural Decoding Across Superconducting Quantum Processors



## Paper summary

The paper studies supervised quantum-error-correction decoding under temporal and cross-device distribution shift. It compares a graph-biased residual transformer, classical analytical decoders, recurrent and convolutional alternatives, tree-based selectors, and a small quantum-assisted screen against an exact-circuit MWPM baseline.

The proposed residual decoder represents syndrome detection events as `(x, y, t)` tokens and uses graph-biased multi-head attention to learn when MWPM's correction should be changed. A label-free drift guard and XGBoost benefit selectors route uncertain cases to analytical experts.

## Main confirmed findings

- On untouched confirmation blocks from the training backend, the frozen neural decoder reduced logical error by **1.34 percentage points**, or **4.0% relative**, over the exact-circuit MWPM baseline across **259,200 shots**.
- A fourth independent block produced a **1.53-point** reduction.
- Transfer without retuning was conditional: the gain shrank on one additional backend and disappeared on another.
- Backend-specific classical experts recovered the gain where the transferred learned policy failed.
- The paper reports negative and null outcomes, including the quantum-assisted/QAOA screen, rather than selecting only favorable experiments.

## Interpretation

The result supports hardware-domain-aware model selection and selective fallback rather than one universally deployed neural decoder. The paperâ€™s contribution is the frozen, block-level evaluation of neural and hybrid decoders under real hardware distribution shift.

## Scope and limitations


## Citation

