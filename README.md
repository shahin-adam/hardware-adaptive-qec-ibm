# Learning Under Hardware Shift: Neural Decoding Across Superconducting Quantum Processors

This repository is the paper landing page for the AusDM 2026 Research Track study of neural and hybrid quantum-error-correction decoders under temporal and cross-device distribution shift.

## Abstract

We study whether learned decoders improve on a strong exact-circuit minimum-weight perfect matching (MWPM) baseline when quantum-hardware calibration changes over time or across processors. The proposed residual decoder represents detection events as numerical `(x, y, t)` tokens and uses graph-biased multi-head attention to learn when the MWPM correction should be changed. A label-free drift guard and frozen XGBoost benefit selectors route uncertain cases to complementary analytical experts.

The central finding is conditional generalisation: the frozen learned policy repeatedly improves on untouched blocks from its training processor, but the gain shrinks or disappears after transfer to other processors without retuning. Backend-specific classical experts recover gains where the transferred policy fails. The study therefore supports domain-aware model selection and selective fallback rather than one universal decoder.

## Research questions

1. Can a learned residual decoder improve on exact-circuit MWPM on untouched hardware blocks?
2. Does the improvement survive temporal calibration drift on the same processor?
3. Does a frozen policy transfer to a different processor without retuning?
4. Can label-free drift detection and analytical fallback reduce deployment risk?
5. Do alternative neural architectures or a small quantum-assisted screen improve the confirmed result?

## Decoder framework

The pipeline contains four components:

- **Exact-circuit MWPM baseline:** edge weights are derived from the submitted transpiled circuit and its calibration snapshot.
- **Residual transformer:** graph-biased attention processes detector coordinates and syndrome time, predicting when the MWPM correction should be changed.
- **Label-free drift guard:** an unlabeled context prefix estimates whether the current hardware distribution remains within the validated training domain.
- **Frozen benefit selectors:** XGBoost models route shots to the learned decoder or complementary analytical experts such as BP-OSD/MWPM.

All learned components, thresholds and routing policies are frozen before confirmation testing.

## Evaluation protocol

- Whole calibration domains are used for training and validation; random shot-level splits are avoided because they leak block-specific hardware information.
- Confirmation blocks are collected later or on different IBM processors and are evaluated once after the policy is frozen.
- Each primary block contains 108,000 shots: 21,600 for label-free context estimation and 86,400 untouched scored shots.
- The study covers X/Z memory and 3-, 5- and 7-round syndrome cohorts at distance 3.
- Outcomes include positive, negative and null results; no method is promoted only because it performed well during development.

## Confirmed results

| Test | Result | Interpretation |
|---|---:|---|
| Kingston K3â€“K5 pooled confirmation | **1.34 percentage-point** reduction; **4.0% relative** improvement over MWPM across **259,200 shots** | Primary within-backend result |
| Independent Kingston K7 block | **1.53 percentage-point** reduction | Repeated confirmation on a later block |
| Kingston cross-domain selector | **1.09â€“1.50 percentage-point** paired 95% interval; p = 3.60Ã—10â»â¶ | Frozen selector improved on untouched K6 |
| Fez backend-specific expert | **0.97 percentage-point** improvement on F1 | Hardware-specific expert recovered a gain |
| Fez transferred Kingston policy | Small/conditional benefit | Transfer is not uniformly reliable |
| Marrakesh transferred policy | **0.28 percentage-point** reduction on M1 | Smaller but significant transfer |
| Quantum-assisted/QAOA screen | Did not clear confirmation bar | Reported as a negative result |

The paperâ€™s headline within-backend result is the 1.34-point reduction over 259,200 untouched Kingston shots. Cross-backend numbers are intentionally reported separately because they answer a different generalisation question.

## What the results show

The strongest evidence is not that one neural model wins everywhere. It is that deployment must account for hardware domain shift. A model trained on one calibration distribution can be useful there and become miscalibrated elsewhere. A label-free guard plus domain-specific analytical fallback provides a more defensible deployment strategy than unconditional neural decoding.

## Negative and null results retained

- A rendered 3D representation did not establish a stronger primary result than numerical detector tokens.
- Several architecture and routing searches did not produce a confirmed improvement.
- A local-hypergraph subsolver and hypergraph-benefit router were not promoted as universal gains.
- The quantum-assisted/QAOA screen did not pass its pre-registered confirmation criterion.
- No universal cross-processor decoder claim is made.

## Limitations and future work

The study does not claim a hardware-independent decoder, a live qLDPC/BB144 result, or a universal logical-error improvement. Complete pulse-level idle, crosstalk and leakage characterisation is unavailable from the measured interface. No external independent reproduction has yet been completed.

Priority follow-up directions are backend-aware expert selection using label-free processor fingerprints, calibration-conditioned models tested on a fourth processor, more complete noise characterisation, and independent reproduction.

## Citation

*Learning Under Hardware Shift: Neural Decoding Across Superconducting Quantum Processors.* AusDM 2026 Research Track submission.

## Repository contents

This repository intentionally contains the paper landing page only. Code, data and supplementary artifacts can be released separately with versioned provenance and the appropriate review status.
