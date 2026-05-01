#!/usr/bin/env bash
#SBATCH --job-name=rag_benchmark_sim
#SBATCH --output=logs/rag-benchmark-%j.out
#SBATCH --error=logs/rag-benchmark-%j.err
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G

# This script is HPC-ready packaging only; not executed on a real CINECA/IT4LIA cluster.

set -euo pipefail

cd "${SLURM_SUBMIT_DIR:-$PWD}"
python hpc-ai-rag-lab/src/benchmark.py --quick
