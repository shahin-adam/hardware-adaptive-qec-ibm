#!/bin/bash
#SBATCH --job-name=qec_v498
#SBATCH --partition=ampere24
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=03:00:00
#SBATCH --output=v498_%j.out
#SBATCH --error=v498_%j.err
set -euo pipefail
apptainer exec --nv /bigdata/users/22228049/containers/cudaqx_20260718.sif python qec_v498_multiseed_relay_consensus.py
