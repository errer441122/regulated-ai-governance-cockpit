# CINECA / IT4LIA Reviewer Route

This route is for reviewers looking for AI Factory, HPC workload readiness, metadata, secure data management, and reproducible AI packaging evidence. It does not claim real CINECA, IT4LIA, Leonardo, LISA, GAIA, MEGARIDE, or GPU execution.

1. Start here:
   - `AI_INTERNSHIP_FIT.md`

2. Workload packaging:
   - `ai-factory-workload-pack/README.md`
   - `ai-factory-workload-pack/workload_manifest.yaml`
   - `ai-factory-workload-pack/benchmark_report.md`
   - `hpc-ai-rag-lab/README.md`
   - `hpc-ai-rag-lab/apptainer/Apptainer.def`

3. Slurm/HPC evidence:
   - `hpc/run_pipeline.sbatch`
   - `hpc-mlops-industrial-lab/slurm/run_regulated_ai_model.sbatch`
   - `hpc-ai-rag-lab/slurm/run_rag_benchmark.sbatch`

4. Executable workload:
   - `hpc-ai-rag-lab/src/benchmark.py`
   - `hpc-ai-rag-lab/artifacts/retrieval_benchmark.json`
   - `hpc-mlops-industrial-lab/src/run_pipeline.py`
   - `ml-baseline/train_model.py`
   - `production-sim-stack/src/orchestrate.py`

5. Data, metadata, and compliance:
   - `ai-factory-workload-pack/fair_metadata_example.json`
   - `ai-factory-workload-pack/data_management_plan.md`
   - `ml-baseline/model_card.md`
   - `ml-baseline/data_card.md`
   - `sql/reviewer_feature_mart.duckdb.sql`

## Positioning

The project is intentionally small and transparent. The evidence is not that it needs a supercomputer today; the evidence is that the workload is documented in the shape an AI Factory reviewer would expect before scaling: dataset, metadata, compute estimate, Slurm entrypoint, container definition, model/data cards, output artifacts, and explicit decision boundaries.
