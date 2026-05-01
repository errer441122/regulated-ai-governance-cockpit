# AI Factory Benchmark Report

## Workload

- Task: human-escalation / capacity-support classification
- Dataset: simulated regulated workflow dataset
- Rows: 24 regulated workflow rows; 20 public-development programme rows in the production simulation sample
- Features: 8 engineered regulated-workflow features in `hpc-mlops-industrial-lab`; 10 baseline features plus one-hot categorical expansion in `ml-baseline`
- Model: transparent logistic regression baseline plus rule/weighted baselines for comparison
- Output artifacts: metrics, predictions, model card, data card, SQLite/DuckDB mart design, lifecycle manifests, Slurm scripts, and Apptainer definition

## Local Execution

- Machine: local laptop / local development environment
- Python version: 3.10.11
- Commands:

```bash
python hpc-mlops-industrial-lab/src/run_pipeline.py
python ml-baseline/train_model.py
python production-sim-stack/src/orchestrate.py
```

## Runtime

| Component | Local runtime |
| --- | ---: |
| `hpc-mlops-industrial-lab/src/run_pipeline.py` | 0.16 seconds |
| `ml-baseline/train_model.py` | 1.35 seconds |
| `production-sim-stack/src/orchestrate.py` | 0.08 seconds |

The timings above were captured on the local portfolio environment on 2026-05-01. They are reviewer evidence for reproducibility and workload sizing, not cluster benchmarks.

## Current Metrics

| Component | Rows | Accuracy | F1 | Notes |
| --- | ---: | ---: | ---: | --- |
| `hpc-mlops-industrial-lab` | 24 | 0.8333 | 0.8889 | from-scratch logistic regression over engineered workflow features |
| `ml-baseline` | 24 | 0.7500 | 0.6667 | scikit-learn logistic regression with rule baseline comparison |
| `production-sim-stack` | 20 | 0.9500 | 0.9524 | transparent capacity-support scoring over public-development-style rows |

## Resource Estimate

- CPU: 2 cores
- RAM: less than 4 GB
- GPU: not required for the current baseline
- Storage: less than 100 MB for repository-scale artifacts
- Expected HPC partition: CPU for the baseline; GPU only for a future deep-learning extension

## Slurm Simulation

```bash
sbatch hpc/run_pipeline.sbatch
```

Additional Slurm evidence:

- `hpc-mlops-industrial-lab/slurm/run_regulated_ai_model.sbatch`
- `production-sim-stack/slurm/run_capacity_scoring_array.sbatch`

## What Would Change On Real CINECA / IT4LIA Infrastructure

- Package the environment with Apptainer/Singularity and approved base images.
- Increase dataset size and add realistic data-ingress controls.
- Run parallel feature generation or job arrays for larger workloads.
- Log metrics to MLflow or an equivalent experiment registry.
- Store artifacts in secure object storage or an approved project filesystem.
- Register dataset and artifact metadata in the project catalogue.
- Add GPU benchmarks only if the model changes from a tabular baseline to a larger deep-learning workload.

## Boundary

No real CINECA, IT4LIA, Leonardo, LISA, GAIA, MEGARIDE, or GPU execution is claimed. The current project is a simulation-only portfolio workload demonstrating how a small AI/HPC workload would be documented before real infrastructure review.
