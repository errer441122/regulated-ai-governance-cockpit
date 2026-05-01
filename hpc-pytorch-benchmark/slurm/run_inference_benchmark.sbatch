#!/usr/bin/env bash
#SBATCH --job-name=regulated-ai-inference-benchmark
#SBATCH --output=artifacts/slurm-inference-%j.out
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G

python hpc-pytorch-benchmark/infer.py
