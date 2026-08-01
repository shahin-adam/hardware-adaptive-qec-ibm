#!/bin/bash
#SBATCH --job-name=qec_v497_env
#SBATCH --partition=ampere24
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=v497_env_%j.out
#SBATCH --error=v497_env_%j.err
set -euo pipefail
IMAGE=/bigdata/users/22228049/containers/cudaqx_20260718.sif
echo "slurm_job_id=$SLURM_JOB_ID"
echo "node=$SLURMD_NODENAME"
echo "image=$IMAGE"
stat --printf='image_size_bytes=%s\nimage_mtime=%y\n' "$IMAGE"
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
apptainer exec --nv "$IMAGE" python - <<'PY'
import importlib.metadata as md
import platform
print('python=' + platform.python_version())
for name in ['cudaq-qec', 'cuda-quantum', 'numpy']:
    try:
        print(f'{name}={md.version(name)}')
    except md.PackageNotFoundError:
        print(f'{name}=NOT_RECORDED')
for module_name in ['cudaq_qec', 'cudaq']:
    try:
        module = __import__(module_name)
        print(f'{module_name}.__version__={getattr(module, "__version__", "UNDECLARED")}')
        print(f'{module_name}.__file__={getattr(module, "__file__", "UNDECLARED")}')
    except Exception as exc:
        print(f'{module_name}.import_error={type(exc).__name__}:{exc}')
PY
