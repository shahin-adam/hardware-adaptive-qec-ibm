# Verified literature-to-experiment gates (1 August 2026)

This document turns the proposed reading list into executable research gates. It
does not treat a literature claim, simulated gain, or unverified dataset as an
experimental result from this project.

## QEC: required reading and the gate it changes

1. **Heavy-hex suppression methodology — arXiv:2510.18847.** Read before any
   Heron suppression-factor claim. Existing Fez/Marrakesh records do not contain
   explicit dynamical-decoupling provenance or the state-preparation data needed
   for the paper's SPAM-aware entanglement-fidelity construction. Therefore the
   legacy single-parameter Lambda values remain exploratory. Required next data:
   identical DD policy at every distance/backend; X, Z, + and - logical input
   states; and an N=0 SPAM calibration.

2. **Hardware-in-the-loop syndrome-to-decoder validation — arXiv:2607.19447.**
   Its relevant contribution is an auditable circuit/readout-to-decoder
   interface, including backend routing and bit/check ordering. Our corresponding
   gate is stricter: every returned correction must satisfy `H e = s (mod 2)`.
   V494 passes this gate on all 1,536 replayed Fez/Marrakesh shots. This paper is
   an interface-validation reference, not evidence of threshold performance.

3. **Improving error suppression with noise-aware decoding — arXiv:2502.21044.**
   The reported suppression-factor improvement is based on ACES-calibrated
   circuit-level simulations. It motivates a calibration-aware comparison, but
   does not establish that our static DEM probabilities improve real IBM data.
   Gate: compare frozen MWPM/BP-OSD and calibration-aware variants on the same
   held-out shots, separately for X/Z, distance and backend, with paired CIs.

4. **Quantum error correction below the surface-code threshold — Nature 2025,
   DOI 10.1038/s41586-024-08449-y.** This is the external benchmark (reported
   Lambda 2.14 +/- 0.02 and real-time decoding), not a directly comparable IBM
   result. Gate: never compare its Lambda numerically to ours unless code,
   circuit, cycles, decoder, SPAM and fit definitions are aligned.

5. **Minimum-Weight Parity Factor / HyperBlossom — arXiv:2508.04969.** Hyperion
   reports 4.8x lower logical error than MWPM for a distance-11 surface code under
   code-capacity simulation, and 1.6x versus tuned BPOSD for a BB code. Gate:
   independently reproduce the public `mwpf` implementation first on matched
   synthetic controls, then on the same real-IBM contracts; retain 100% closure
   and report unsupported DEM features rather than silently dropping them.

6. **Belief-matching — arXiv:2203.04948.** This combines BP-derived information
   with matching and reports simulated threshold improvement. Gate: it is a new
   candidate only if the exact implementation has not already appeared in the
   version ledger; benchmark against V12 and V494 on identical IBM shots with
   separate domain gates.

7. **DAQEC-Benchmark — Zenodo record 18045662.** The record URL is retained as a
   candidate external cross-check, but its metadata/content could not be fetched
   in the current audit. No claim will rely on it until checksum, license,
   circuit semantics and backend provenance are verified.

### QEC promotion contract

- Synthetic closure: 100%.
- Real-shot closure: 100%.
- Primary comparison: paired against authoritative V12 and a frozen conventional
  baseline; no tuning on test labels.
- Report X and Z separately, plus distance, backend and round domains.
- A subgroup result found after a configuration sweep is hypothesis-generating
  until confirmed on a preregistered holdout with multiplicity control.
- Latency includes warm-up, repeated batches and tail percentiles; GPU launch
  overhead is not hidden.
- No Lambda/subthreshold claim without DD provenance and SPAM-aware inputs.

### Authoritative V12 comparison target recovered from the local archive

V12 is not a vague historical percentage. Its frozen independent confirmation
ran on `ibm_kingston` job `d9ct8mphtsac739c7qi0`: 108,000 requested shots,
21,600 label-free context shots and 86,400 untouched scored shots. It reduced
exact-circuit MWPM LER from 36.4120% to 35.5301%, a paired gain of **0.8819 pp**
(95% CI **[0.6979, 1.0613] pp**, McNemar p = 5.23e-21). No tuning or checkpoint
selection used the scored block.

The domain gate is the six frozen cohorts, each with 14,400 shots:

- X3: +1.6181 pp; X5: +0.3472 pp with CI crossing zero; X7: exact MWPM fallback.
- Z3: +1.3958 pp; Z5: +1.1806 pp; Z7: +0.7500 pp.

Consequently, a later method does not “beat V12” merely by exceeding 0.8819 pp
on pooled Fez/Marrakesh replay. It must be evaluated on the same V12 scored block
or on a preregistered independent block with the frozen V12 policy, and must
report every cohort. V494/V495 use different shots and therefore remain a
separate hardware-contract/latency study, not a head-to-head V12 comparison.

## PVC: required reading and the gate it changes

1. **Ezendu, Soyemi and Szilvasi, “Multiscale simulation of plastic
   transformations: The case of base-assisted dehydrochlorination of PVC,”
   AIChE Journal 70 (2024), e18559, DOI 10.1002/aic.18559.** The paper reports
   that E2 dominates in its multiscale model. Our novelty cannot be “first to
   decide E2 versus another pathway.” Gate: reproduce its relevant fragment,
   conformer, level-of-theory and barrier conventions, then test whether
   multireference treatment changes the ranking outside its uncertainty.

2. **Lei et al., “Quantum mechanical nanoreactor simulations reveal PVC
   pyrolysis pathways,” AIChE Journal 71 (2025), e18913,
   DOI 10.1002/aic.18913.** Gate: use its reported mechanism set to define
   candidate pathways, but verify every transition state with exactly one
   imaginary mode and an IRC/path connection before barrier comparison.

3. **Becker et al., “Electrochemical Chlorine Shuttle from PVC Waste to Vinyl
   Ether Acceptors...,” Advanced Materials 38 (2026), e17489,
   DOI 10.1002/adma.202517489.** This is the experimental motivation for
   electrochemical dechlorination. Gate: do not convert bare electronic energy
   differences into a reduction potential; require thermal, standard-state,
   solvent, electron-reference and electrode-reference terms before comparison.

4. **Chen et al., “Mechanochemical upcycling of poly(vinyl chloride) for alcohol
   halogenation,” Nature Communications 17 (2026), 1222,
   DOI 10.1038/s41467-025-67978-w.** This establishes a distinct experimental
   route. It informs scope and candidate routes, but does not validate the
   electrochemical or E2 calculations.

5. **Wouters et al., “A Practical Guide to Density Matrix Embedding Theory in
   Quantum Chemistry,” JCTC (2016), DOI 10.1021/acs.jctc.6b00316.** Gate: bath
   orbitals must follow a documented Schmidt/1-RDM construction; include core
   environment contributions; demonstrate fragment/bath and active-space
   convergence. An arbitrary choice of six eigenvectors nearest occupation one
   is not production DMET.

6. **PySCF geometry optimization and geomeTRIC transition-state documentation.**
   Gate: constrained/path maximum -> unconstrained first-order saddle -> Hessian
   with one imaginary frequency -> mode/IRC connection to intended endpoints.

### PVC promotion contract

- Current stable STO-3G four-energy contrast: **7.7106 mHa**, not 17.31 mHa.
- Larger-basis/root-tracking and active-space robustness must pass before QPU.
- QPU uncertainty is propagated for the four-energy contrast and must be
  meaningfully narrower than the validated target.
- Exact-classical, noisy-simulator and real-QPU results remain separate.
- No quantum advantage or laboratory validation claim without the corresponding
  classical scaling evidence or physical experiment.

## Items requiring correction or further verification

- The generic titles “Quantum Chemistry of Radical Anions...” and “Statistical
  Power and Confidence Bounds in Hardware Validations of QEC” were not uniquely
  identifiable as cited. They are not included as references until an exact DOI
  or arXiv identifier is supplied.
- “Skinner et al.” was not accepted as the latency reference. Verified current
  benchmarks include the Willow real-time decoder and 2025/2026 FPGA decoder
  demonstrations; their latency definitions and hardware differ from V494.
- The FeMoco “Zhai and Chan, 2026” item needs an exact title/DOI before citation.
