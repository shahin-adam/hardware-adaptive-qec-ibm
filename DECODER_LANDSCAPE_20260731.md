# Decoder resources reviewed

| Family | Open resource | Use in this project |
|---|---|---|
| BP-OSD | https://github.com/quantumgizmos/bp_osd | Algebraic d5/qLDPC baseline; Python 3.8 dependency compatibility remains to be resolved |
| Tesseract | https://github.com/quantumlib/tesseract-decoder | DEM-compatible search referee; native build not yet available locally |
| qLDPC | https://github.com/qLDPCOrg/qLDPC | Common code/decoder interface |
| NVIDIA Ising | https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Accurate | 5D input (batch, channels, time, distance, distance) pre-decoder; weights not yet replayed locally |
| PyMatching | https://github.com/quantumlib/PyMatching | Frozen MWPM/V12 baseline |
| Local clustering | https://www.nature.com/articles/s41467-025-66773-x | Distance-5 adaptive Union-Find direction; requires compatible implementation |
