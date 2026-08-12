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

## Public evaluation summary

The study compares learned, hybrid and analytical decoding approaches under calibration and processor changes. Only aggregate outcomes are shown here; implementation details, raw data and internal experiment metadata are intentionally omitted.

## Confirmed results

| Test | Result | Interpretation |
|---|---:|---|
| Kingston K3-K5 pooled confirmation | **1.34 percentage-point** reduction; **4.0% relative** improvement over MWPM | Primary within-backend result |
| Independent Kingston K7 block | **1.53 percentage-point** reduction | Repeated confirmation on a later block |
| Kingston cross-domain selector | **1.09-1.50 percentage-point** paired 95% interval | Frozen selector improved on untouched K6 |
| Fez backend-specific expert | **0.97 percentage-point** improvement on F1 | Hardware-specific expert recovered a gain |
| Fez transferred Kingston policy | Small/conditional benefit | Transfer is not uniformly reliable |
| Marrakesh transferred policy | **0.28 percentage-point** reduction on M1 | Smaller but significant transfer |
| Quantum-assisted/QAOA screen | Did not clear confirmation bar | Reported as a negative result |

The headline result is a **1.34 percentage-point** within-processor improvement. Cross-processor results are reported separately because transfer performance depends on the hardware domain.

## What the results show

The strongest evidence is not that one neural model wins everywhere. It is that deployment must account for hardware domain shift. A model trained on one calibration distribution can be useful there and become miscalibrated elsewhere. A label-free guard plus domain-specific analytical fallback provides a more defensible deployment strategy than unconditional neural decoding.

## What this QEC study achieved

- **Machine learning:** a residual neural decoder and hardware-aware selectors improved the exact-circuit baseline on confirmed within-processor data, with a **1.34 percentage-point** primary improvement and a **4.0% relative** improvement.
- **3D visualisation:** detector and syndrome structure was visualised to inspect spatial-temporal error patterns and hardware drift. The visual analysis supported interpretation, but it was not presented as a separate performance breakthrough.
- **Quantum-assisted exploration:** a small quantum/QAOA-assisted screen was evaluated as an exploratory QEC component. It did not pass the confirmation criterion, so no quantum advantage is claimed.

These conclusions are intentionally limited to the public aggregate results above; the page does not disclose private code, raw data, credentials or experiment metadata.

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

This repository is a public paper landing page. It intentionally contains only a high-level summary and aggregate percentage results. Implementation details, raw data, credentials and private experiment metadata are not included.


