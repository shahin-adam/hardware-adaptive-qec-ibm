# QEC recovered-artifact and experiment deduplication decision

Date: 1 August 2026  
Authoritative archive roots: `Z:\Meetings\Complete\22-7-2026` and
`Z:\Meetings\Complete\15-7-2026`

## Newly converted into controlled evidence

### Batched closure-gated Relay/OSD systems path (V497)

The archive contained the CUDA-QX Relay/OSD direction but no repeated,
same-node sequential-versus-batched benchmark. V497 filled that gap without
changing the decoder: five repeats on each of 24 preserved Fez/Marrakesh
contracts, exact closure enforced. Median per-contract speedup is 2.252x with a
contract-bootstrap 95% interval [2.135x,2.362x]. All 24 contracts favor
batching. This is an offline A30 replay systems result, not QPU feedback latency.

### Per-shot routing stability (V497)

The earlier V495 aggregate did not retain the evidence needed to assess route
stability. V497 records per-shot masks. Existing operating points agree on only
66.0%--72.1% of route decisions. Escalated-shot difficulty enrichment ranges
from -2.149 to +4.579 pp and every interval includes zero. Accuracy is null in
all required basis, distance, and backend gates. Conclusion: Relay convergence
is not a demonstrated confidence score.

### Multi-seed consensus control (V498)

No prior Relay multi-seed logical-consensus control was found in the ledger.
Five-seed unanimity was tested as a routing—not decoder—change. It retained only
2.865% fast-path coverage, cost 5.797 ms/shot, and found that 23.633% of shots
had all seeds algebraically close while disagreeing on the logical correction.
It is rejected. All X/Z-by-distance accuracy intervals include zero.

## High-signal recovered artifacts that are not new claims

1. **V389--V392 paired Fez records** were previously missing from placeholder
   ledger rows but are already recovered and audited. Their pooled abstention
   gains have subgroup regressions and are not V12 replacements.
2. **Public IBM calibration-conditioned repetition-code dataset** contains
   QASM circuits, physical-qubit register names, calibration snapshots, and raw
   bitstrings across Fez/Kingston/Pittsburgh. It can support a calibration/router
   prototype, but it is a different code/endpoint and cannot validate a
   surface-code or V12 improvement.
3. **Kingston D5 archive** contains detectors, labels, masks, calibration/job
   metadata, and canonical DEM controls, but no paired V12 predictions and no
   complete operation-faithful detector-to-instruction map. V237--V253 already
   exhaust the safe hard-bit transformations; rerunning them would duplicate
   negative work.
4. **NVIDIA Ising-Decoding and NTU transfer artifacts** are reusable source and
   training references, not directly transferable checkpoints. Earlier graph,
   transformer, BP-OSD, FiLM, and transfer variants already test their relevant
   architecture families.
5. **Archived QPY/circuit/calibration material** is valuable only when joined to
   the exact scored shots and detector/observable convention. Presence on disk
   alone does not establish an operation-faithful comparator.

## V12 comparison boundary

V12 remains the authoritative Kingston confirmation result on its own frozen
contract. V497/V498 use a later 1,536-shot Fez/Marrakesh contract family and are
not head-to-head V12 tests. Cross-experiment percentages are reported side by
side only as provenance, never as paired improvement.

The preserved Fez artifact with MWPM and V12 predictions has already been used
by V38/V39/V149. Reusing it for a newly tuned router would be retrospective
reuse, not independent confirmation.

## Next non-duplicative IBM experiment

Do not tune another Relay configuration. The next performance experiment must
be prospective and save, in one immutable bundle:

1. exact baseline and frozen V12 predictions for every shot;
2. transpiled ISA/QPY circuit, final layout, detector coordinates/order, and
   logical observable map;
3. identical DD and compilation settings across distance/backend comparisons;
4. timestamped per-qubit/per-gate calibration and, if available, raw/soft
   readout;
5. logical preparations `0`, `1`, `+`, `-` and an `N=0` SPAM calibration;
6. a frozen development/validation/test split by complete hardware job/day;
7. separate X/Z, distance, rounds, state, backend, and day gates.

Only then should a calibrated escalation score be trained on development
domains, frozen on validation domains, and evaluated once against MWPM and V12
on untouched hardware jobs. A power calculation must target that experiment's
primary endpoint; it cannot reuse V494's within-replay effect automatically.

## Decision

- Promote V497 closure and offline batching performance with its exact scope.
- Retain V497/V498 accuracy results as null/negative routing evidence.
- Reject five-seed consensus and further uncalibrated Relay sweeps.
- Preserve V12 as fallback and request the prospective matched artifact bundle
  before any cross-chip suppression or calibrated-router claim.

