# Learning Under Hardware Shift: Neural Decoding Across Superconducting Quantum Processors

This repository is the paper landing page for a study of neural and hybrid quantum-error-correction decoders under temporal and cross-device distribution shift.

## Authors

- **Shahin Adam:** School of Computer, Data and Mathematical Sciences, Western Sydney University, Sydney, NSW, Australia. [ORCID: 0009-0000-1182-0256](https://orcid.org/0009-0000-1182-0256)
- **A/Prof Quang Vinh Nguyen:** School of Computer, Data and Mathematical Sciences, Western Sydney University, Sydney, NSW, Australia. [ORCID: 0000-0002-0815-6224](https://orcid.org/0000-0002-0815-6224)
- **A/Prof Weisheng Si:** School of Computer, Data and Mathematical Sciences, Western Sydney University, Sydney, NSW, Australia. [ORCID: 0000-0002-1239-7880](https://orcid.org/0000-0002-1239-7880)
- **Prof Simeon J. Simoff:** School of Computer, Data and Mathematical Sciences, Western Sydney University, Sydney, NSW, Australia. [ORCID: 0000-0001-9895-4109](https://orcid.org/0000-0001-9895-4109)

## Abstract

We study whether learned decoders improve on a strong exact-circuit minimum-weight perfect matching (MWPM) baseline when quantum-hardware calibration changes over time or across processors. The proposed residual decoder represents detection events as numerical `(x, y, t)` tokens and uses graph-biased multi-head attention to learn when the MWPM correction should be changed. A label-free drift guard and frozen XGBoost benefit selectors route uncertain cases to complementary analytical experts.

The central finding is that a learned, hardware-aware decoder can improve logical-error performance on confirmed superconducting-processor data. The study combines neural decoding, hardware calibration information and analytical fallback selection for quantum error correction.

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
| Marrakesh transferred policy | **0.28 percentage-point** reduction on M1 | Smaller but significant transfer |

The headline result is a **1.34 percentage-point** within-processor improvement. Cross-processor results are reported separately because transfer performance depends on the hardware domain.

## What the results show

The strongest evidence is not that one neural model wins everywhere. It is that deployment must account for hardware domain shift. A model trained on one calibration distribution can be useful there and become miscalibrated elsewhere. A label-free guard plus domain-specific analytical fallback provides a more defensible deployment strategy than unconditional neural decoding.

## What this QEC study achieved

- **Machine learning:** a residual neural decoder and hardware-aware selectors improved the exact-circuit baseline on confirmed within-processor data, with a **1.34 percentage-point** primary improvement and a **4.0% relative** improvement.
- **3D visualisation:** detector and syndrome structure was visualised to inspect spatial-temporal error patterns and hardware drift.
- **Quantum error correction:** the work evaluates decoding for superconducting quantum processors using real hardware calibration domains and logical-error outcomes.

## Future directions

Future work will extend the hardware-aware decoder to additional processors, calibration regimes and QEC code families.

## Citation

*Learning Under Hardware Shift: Neural Decoding Across Superconducting Quantum Processors.*

## Repository contents

This repository contains the paper landing page and its public research summary.


