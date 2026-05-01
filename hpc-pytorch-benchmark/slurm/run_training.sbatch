#!/usr/bin/env bash
#SBATCH --job-name=regulated-ai-pytorch-benchmark
#SBATCH --output=artifacts/slurm-training-%j.out
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G

python hpc-pytorch-benchmark/train.py
