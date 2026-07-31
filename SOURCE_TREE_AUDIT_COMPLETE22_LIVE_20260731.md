# Source-tree audit â€” Complete 22 July 2026 (live path)

Audit date: 31 July 2026 (Australia/Sydney)

## Scope

The live source root is:

`Z:\Meetings\Complete\22-7-2026`

The previously referenced literal path `Z:\Meetings\22-7-2026` remains absent; it is not the same path.

## Inventory

- Readable file paths discovered with `rg --files --hidden --no-ignore`: **22,808**.
- Broad QEC/decoder candidate paths after excluding virtual environments, site-packages, caches, node modules and `.git`: **8,993**.
- Existing prior audit count (before this path was live): 17,590 files; this report supersedes that count.

## Newly confirmed high-signal artifacts

- `external_open_models/Ising-Decoding-main`: NVIDIA surface/color pre-decoder training and inference implementation, including PyMatching downstream decoding and ONNX/TensorRT guidance.
- `external_open_models/ntu-decoder-main`: neural transfer-unification code with surface-code and bivariate-bicycle neural-BP/Transformer baselines.
- `166_PUBLIC_IBM_DATASET_20768087_20260730`: IBM public-data adapter, calibrated basis/BP/blossom smoke tests, temporal graph adapter and vendor-schema work.
- `127_EXTERNAL_REAL_IBM_DATASET_TRANSFER_20260725`: cross-backend FiLM/MMD and self-calibrating matching artifacts.
- `144_D5_KINGSTON_DATASET_AUDIT_20260729`: distance-5 dataset audit and model-job splits.
- `150_V240`â€“`158_V249`: canonical BP-OSD, basis hybrid, confidence/activity gates and their Wolffe evidence.
- `167_PUBLIC_GOOGLE_WILLOW_RAW_BENCHMARK_20260730`: public non-IBM DEM/shot benchmark; retained as cross-vendor diagnostic evidence only.

## Evidence boundary

Recovered source artifacts are not automatically new experiments. Existing V001â€“V421 registry rows were reconciled before any rerun. New work must use a new version identifier, frozen inputs, paired V12/MWPM comparison, X/Z and domain gates, and an explicit status. No vendor-universal claim is supported by this inventory alone.
