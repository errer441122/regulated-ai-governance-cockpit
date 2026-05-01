#!/bin/bash
#SBATCH --job-name=regulated-ai-review
#SBATCH --output=logs/regulated-ai-review-%j.out
#SBATCH --error=logs/regulated-ai-review-%j.err
#SBATCH --time=00:20:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --partition=cpu

set -euo pipefail

cd "${SLURM_SUBMIT_DIR:-$PWD}"

if [ -f ".venv/bin/activate" ]; then
  source ".venv/bin/activate"
fi

python3 hpc-mlops-industrial-lab/src/run_pipeline.py
python3 production-sim-stack/src/orchestrate.py
python3 ml-baseline/train_model.py
