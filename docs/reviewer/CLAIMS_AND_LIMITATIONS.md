# Claims And Limitations

This file is the truth boundary for recruiter-facing and technical-reviewer-facing claims.

## Claims Supported By Repository Artifacts

| Claim | Artifact or command |
| --- | --- |
| Static regulated AI governance cockpit exists | `index.html`, `app.js`, `data.js` |
| Static data validation is executable | `npm test`, `scripts/validate-data.mjs` |
| Risk ML baseline is executable | `python ml-baseline/train_model.py` |
| Risk ML baseline has calibration, drift, feature importance, and model card artifacts | `ml-baseline/artifacts/` after training |
| Production-like scoring simulation exists | `production-sim-stack/src/api.py`, `production-sim-stack/src/ml_model_adapter.py` |
| SQL mart evidence exists | `sql/`, `production-sim-stack/sql/`, `hpc-mlops-industrial-lab/sql/` |
| Slurm-ready packaging exists | `hpc/`, `hpc-ai-rag-lab/slurm/`, `production-sim-stack/slurm/` |
| AI Factory packaging evidence exists | `ai-factory-workload-pack/`, `hpc-ai-rag-lab/apptainer/` |
| UNDP-style public-data path exists | `undp-sdg-risk-lab/`, `production-sim-stack/PUBLIC_SECTOR_SDG_ROUTE.md` |
| Local orchestration decomposition exists | `orchestration/local_orchestrator.py` |

## Do Not Claim

- Do not claim production deployment.
- Do not claim real cloud execution.
- Do not claim real Slurm, GPU, Leonardo, CINECA, IT4LIA, or AI Factory execution.
- Do not claim real CRIF, PwC, UNDP, CINECA, IT4LIA, BI-REX, Ducati, client, customer, or employer data.
- Do not claim legal compliance certification, credit decisioning, aid allocation, eligibility decisioning, procurement automation, or policy automation.
- Do not claim this is an enterprise MLOps platform.
- Do not claim the Docker Compose stack is production infrastructure.

## Safe Wording

Use:

- `simulation`
- `local-only`
- `production-like simulation`
- `HPC-ready packaging`
- `not executed on a real cluster`
- `synthetic data`
- `public-development-style sample`
- `advisory human-review triage`

Avoid:

- `production-ready`
- `deployed`
- `certified`
- `real client`
- `real cluster run`
- `real cloud run`
- `automated decision system`

## Data Boundary

The repository uses simulated regulated workflow data and small public-development-style samples. Any real public API output is documented as a small reproducibility artifact and must not be presented as a UNDP, CRIF, PwC, CINECA, IT4LIA, BI-REX, or customer dataset.

## Model Boundary

The ML baseline supports reviewer inspection of feature engineering, training, metrics, calibration, and model-card writing. It is not validated for production, fairness certification, legal compliance, credit risk approval, public-sector targeting, or any automated decision.
