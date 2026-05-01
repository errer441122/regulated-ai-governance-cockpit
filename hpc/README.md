# HPC / Slurm Review Shortcut

This folder makes HPC evidence visible from the repository root.

The project does not claim real CINECA, IT4LIA, or BI-REX cluster execution. It shows how the workload would be packaged for a Linux/Slurm environment and points to runnable local equivalents.

## Files

- `run_pipeline.sbatch` - top-level Slurm entrypoint for the reviewer.
- `hpc-mlops-industrial-lab/slurm/run_regulated_ai_model.sbatch` - lab-specific Slurm script.
- `production-sim-stack/slurm/run_capacity_scoring_array.sbatch` - job-array style production simulation.
- `hpc-ai-rag-lab/slurm/run_rag_benchmark.sbatch` - lightweight retrieval/RAG benchmark packaging for AI Factory review.

## Local Equivalent

```bash
python3 hpc-mlops-industrial-lab/src/run_pipeline.py
python3 production-sim-stack/src/orchestrate.py
python3 hpc-ai-rag-lab/src/benchmark.py --quick
```
