# Benchmark Plan

## Objective

Validate that the reviewer workload is reproducible, traceable, and small enough for CI while still resembling the shape of an AI Factory/HPC workload handoff.

## Baseline Run

```bash
python hpc-mlops-industrial-lab/src/run_pipeline.py
python production-sim-stack/src/orchestrate.py
python ml-baseline/train_model.py
```

Expected local runtime is under one minute on a laptop CPU. The Slurm version is represented by:

```bash
sbatch hpc/run_pipeline.sbatch
```

## Resource Assumptions

| Scenario | CPU | GPU | Memory | Time | Purpose |
| --- | --- | --- | --- | --- | --- |
| CI/local reviewer run | 2 vCPU | none | 4 GB | 10 min | Validate code, metrics, and artifacts |
| AI Factory pilot | 4-8 CPU cores | optional | 16-32 GB | 30 min | Larger dataset, richer logs, artifact registry |
| Future deep-learning workload | 8+ CPU cores | 1 GPU | 32+ GB | 1-4 h | Only if the task changes from tabular baseline to neural model |

## Metrics

- Pipeline completion status.
- Row counts and schema checks.
- Accuracy, precision, recall, F1, and confusion matrix.
- Artifact manifest completeness.
- Metadata completeness against `fair_metadata_example.json`.

## What Would Change On Leonardo / IT4LIA

- Replace local paths with project scratch/work storage paths.
- Pin approved Apptainer base images and module versions.
- Add allocation ID, partition, QoS, and account directives.
- Register metadata and outputs in the project catalogue.
- Add approved data ingress and egress controls for any non-public dataset.
