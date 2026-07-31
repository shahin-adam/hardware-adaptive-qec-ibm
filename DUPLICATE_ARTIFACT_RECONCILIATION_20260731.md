# Duplicate-artifact reconciliation (31 July 2026)

The following two paths are byte-identical SHA-256 `4A98CBBC5B002D3B6B45C7F04E9C62CCEAB7FDBD7F0AD4A1D08DAC020152FFFF`:

- `Z:\Meetings\Complete\15-7-2026\qec_real_ibm_surface_d3\future_attention_confirmation_20260715\future_locked_predictions.npz`
- `Z:\Meetings\Complete\22-7-2026\QEC_AI_PAPER_MASTER_20260717\3D_TEAM_HANDOFF_ALL_EXPERIMENTS\D02_GRAPH_DRIFT_CONFIRMATION\future_locked_predictions.npz`

All six arrays (`sample_index`, `labels`, `mwpm`, `candidate`, `residual_probability`, `metadata`) compare equal. They represent one IBM Kingston block, not two independent confirmations. V422 therefore counts this block once.
