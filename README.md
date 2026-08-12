# Learning Under Hardware Shift: Neural Decoding Across Superconducting Quantum Processors

This repository accompanies the AusDM 2026 Research Track study of neural and hybrid quantum-error-correction decoders under temporal and cross-device distribution shift.

## Research question

Can a learned decoder improve on an exact-circuit MWPM baseline on untouched hardware blocks, and does that improvement transfer to a different superconducting processor without retuning?

## Core idea

The study represents syndrome detection events as structured spatio-temporal `(x, y, t)` tokens and uses a graph-biased residual transformer with multi-head attention to learn when the MWPM correction should be changed. A label-free drift guard detects changes in the hardware distribution. Frozen XGBoost benefit selectors route uncertain cases to complementary analytical decoders rather than forcing one learned model to handle every device.

## Evaluation design

- Models and policies are frozen before confirmation testing.
- Training and validation use whole calibration domains, not random shot-level splits.
- Confirmation uses untouched execution blocks collected later or on different IBM processors.
- The baseline is an exact-circuit MWPM decoder whose weights are derived from the submitted circuit and calibration snapshot.
- The study compares neural, tree-based, recurrent, convolutional, classical and quantum-assisted alternatives.
- Results report positive, negative and null outcomes under the same pre-registered evaluation discipline.

## Main confirmed results

| Evaluation | Result |
|---|---|
| Pooled untouched confirmation blocks | 1.34 percentage-point logical-error reduction, 4.0% relative improvement over MWPM across 259,200 shots |
| Fourth independent block | 1.53 percentage-point reduction |
| Within-backend generalisation | Improvement reproduced on later blocks from the training backend |
| Cross-backend transfer | Benefit shrank on one backend and disappeared on another without retuning |
| Hardware-specific fallback | Classical experts recovered the gain where the transferred learned policy failed |
| Quantum-assisted screen | Did not clear the pre-registered confirmation bar and is reported as a negative result |

## Interpretation

The evidence supports hardware-domain-aware model selection and selective fallback rather than one universally deployed neural decoder. A model can be useful on the hardware distribution it has learned while becoming unreliable after calibration or processor changes.

## Scope and limitations

This repository documents a real-hardware IBM surface-code study. It does not claim a universal cross-device decoder, a live qLDPC/BB144 result, or hardware-independent logical-error improvement. The work is a reproducible study of distribution shift, model selection and risk-controlled decoder deployment.

## Citation

*Learning Under Hardware Shift: Neural Decoding Across Superconducting Quantum Processors.* AusDM 2026 Research Track submission.

## Repository status

The landing page contains the paper description only. Experimental data, code and supplementary materials can be added later as separate, versioned releases.
