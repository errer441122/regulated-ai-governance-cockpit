# AI Factory Workload Pack

This micro-pack is reviewer evidence for CINECA, IT4LIA, BI-REX, and AI Factory-style screening. It does not claim access to Leonardo, IT4LIA infrastructure, or confidential datasets. It shows how the existing portfolio workload would be packaged, documented, and reviewed before a real HPC or AI Factory run.

## Workload

- Entry point: `hpc/run_pipeline.sbatch`
- Local pipeline: `hpc-mlops-industrial-lab/src/run_pipeline.py`
- Production-like scoring path: `production-sim-stack/src/orchestrate.py`
- Reviewer ML artifact path: `ml-baseline/artifacts/model.joblib`
- Lightweight RAG workload: `hpc-ai-rag-lab/src/benchmark.py`
- Container sketch: `apptainer.def`

## Reviewer Signals

- Input and output artifact declaration in `workload_manifest.yaml`.
- Secure data handling and lineage in `data_management_plan.md`.
- FAIR-style metadata in `fair_metadata_example.json`.
- CPU/GPU, memory, runtime, and benchmark assumptions in `benchmark_plan.md`.
- Captured local benchmark evidence in `benchmark_report.md`.
- CPU-friendly retrieval benchmark evidence in `../hpc-ai-rag-lab/artifacts/retrieval_benchmark.json`.
- HPC packaging boundary in `apptainer.def`.

## Packaging Note

`apptainer.def` is included as HPC packaging evidence for an Apptainer/Singularity-style workflow. It was not executed on a real cluster.

## Leonardo / IT4LIA Boundary

On a real CINECA/IT4LIA environment, this pack would need project allocation IDs, module paths, storage class choices, scheduler partition details, secrets management, and approved data-transfer controls. Those items are intentionally not simulated here.
