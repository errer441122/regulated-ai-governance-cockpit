# Recruiter 5-Minute Route

This repository is the flagship portfolio project for regulated AI governance and ML engineering screening. It is a simulation using synthetic and public-development-style sample data; it is not a production system and does not use real CRIF, PwC, UNDP, CINECA, IT4LIA, BI-REX, customer, or employer data.

## Fast Review Path

1. Open `README.md` and read `Portfolio positioning`.
2. Open `AI_INTERNSHIP_FIT.md` for the target-company fit summary and do-not-claim boundaries.
3. Open `EVIDENCE_MAP.md` for role-to-artifact mapping.
4. Check one executable technical proof:
   - CRIF / PwC risk ML: `ml-baseline/README.md`
   - UNDP public-data path: `undp-sdg-risk-lab/README.md`
   - CINECA / IT4LIA AI workload: `hpc-ai-rag-lab/README.md`
5. If time allows, inspect `docs/reviewer/CLAIMS_AND_LIMITATIONS.md`.

## Best Reviewed For

| Target | What to inspect first | Honest boundary |
| --- | --- | --- |
| CRIF ML Engineering | `ml-baseline/`, `orchestration/`, `production-sim-stack/src/ml_model_adapter.py` | Synthetic data, no real CRIF deployment |
| PwC Data & AI / Risk | `ml-baseline/artifacts/model_card.md`, `sql/`, `EVIDENCE_MAP.md` | No client delivery or production risk model |
| UNDP Digital/Data Science | `undp-sdg-risk-lab/`, `production-sim-stack/PUBLIC_SECTOR_SDG_ROUTE.md` | Not a real UNDP project |
| CINECA / IT4LIA | `hpc-ai-rag-lab/`, `ai-factory-workload-pack/`, `hpc/` | HPC-ready packaging only, no real cluster run |
| BI-REX supplement | `production-sim-stack/`, `hpc-mlops-industrial-lab/` | Ducati repo should carry the stronger industrial telemetry story |

## What Is Executable

```bash
npm test
python ml-baseline/train_model.py
python orchestration/local_orchestrator.py
python undp-sdg-risk-lab/src/run_pipeline.py
python hpc-ai-rag-lab/src/benchmark.py --quick
```

## What Is Simulated

- All regulated-risk and workflow data.
- All production, cloud, MLOps, Slurm, AI Factory, and public-sector deployment contexts.
- The FastAPI/Docker stack is a local production-like simulation, not production infrastructure.
- Slurm and Apptainer files are packaging evidence, not proof of real HPC execution.
