# IBM QEC source-tree audit â€” Complete/22-7-2026

The literal path `Z:\Meetings\22-7-2026` is absent. The available corresponding source is `Z:\Meetings\Complete\22-7-2026`.

## Inventory

- `rg --files` found 17,590 readable path entries under the available source tree.
- 8,872 names matched the QEC/IBM/decoder/V12/Stim/surface-code candidate filter used for follow-up review.
- The source contains the canonical 164-row `02_MASTER_EXPERIMENT_LEDGER.csv` and a 167-row AlphaQubit metric audit.
- The 15 July source tree remains separately audited and contains the 120,000-shot locked IBM Kingston confirmation package recovered as V417.

## Recovered high-value evidence

The Complete/22 source confirms the matched-baseline correction already recovered in V417:

- MWPM: 42.6442% logical error on 120,000 locked Kingston shots.
- BP-OSD: 43.2592%.
- Frozen four-model ensemble: 44.0908%.
- Frozen Transformer: 44.9292%.
- The true 3D-vs-2D development comparison was +0.4968 percentage points, but its 95% CI crossed zero and McNemar p=0.1219.

These are audit findings, not a new rerun. The MWPM result is phenomenological/calibration-selected rather than an exact pulse-level DEM reconstruction, so it is not a universal or final hardware claim.

## Follow-up candidates

The source includes V109â€“V118 implementation records, IBM metric audits, Qiskit repository relevance tables, and the 100-idea backlog. They are retained as source evidence and should only generate a new version when paired with a new frozen comparison; previously failed/recovered work will not be rerun solely to increase the version count.
