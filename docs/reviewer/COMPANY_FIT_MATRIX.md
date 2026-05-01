# Company Fit Matrix

This matrix maps target internship signals to repository evidence and honest gaps. It should be read together with `CLAIMS_AND_LIMITATIONS.md`.

| Target | Must-have to show | Repository artifacts | Honest gap |
| --- | --- | --- | --- |
| CRIF ML Engineering | Python, OOP, ML, data quality, data engineering, cloud-native interest, FastAPI, Dagster-equivalent | `ml-baseline/`, `orchestration/`, `production-sim-stack/`, `sql/`, `hpc/`, `scripts/validate-data.mjs` | No real CRIF data, no cloud deployment, no SaaS/PaaS integration |
| CRIF Data Enhancement | correctness checks, data-quality validation, explainable escalation logic | `ml-baseline/artifacts/drift_report.json`, `technical-lab/`, `ai-data-agentic-readiness-lab/` | Synthetic records, no real company registry updates |
| PwC Data & AI | consulting narrative, SQL, dashboarding, ML, model governance, stakeholder communication | `README.md`, cockpit UI, `EVIDENCE_MAP.md`, `ml-baseline/artifacts/model_card.md`, `sql/`, `docs/reviewer/` | No client deployment, no production Spark/Kubeflow |
| PwC Risk ML | risk modelling, calibration, classifier comparison, backtesting-style metrics, Python | `ml-baseline/artifacts/metrics.json`, `ml-baseline/artifacts/calibration.json`, `ml-baseline/artifacts/confusion_matrix.csv`, `ml-baseline/artifacts/feature_importance.csv` | Synthetic labels, not a financial-risk production model |
| UNDP Digital/Data Science | public data, SDG/public-value framing, responsible data, NLP/text mining, policy note | `undp-sdg-risk-lab/`, `production-sim-stack/PUBLIC_SECTOR_SDG_ROUTE.md`, responsible checklist, policy note | Not a real UNDP project, no country-office validation |
| CINECA HPC/Data Science | Slurm, Linux batch, AI workload, benchmark, reproducible packaging | `hpc/`, `hpc-ai-rag-lab/`, `ai-factory-workload-pack/` | No real cluster, GPU, or Leonardo execution |
| IT4LIA AI Factory | AI setup/development/test, data management, compliance/trust, metadata, container packaging | `ai-factory-workload-pack/`, `hpc-ai-rag-lab/apptainer/`, `hpc-ai-rag-lab/artifacts/retrieval_benchmark.json` | No real AI Factory access or project allocation |
| BI-REX supplement | industrial AI support, monitoring, data engineering, Slurm packaging | `production-sim-stack/`, `hpc-mlops-industrial-lab/`, `hpc/` | Ducati repo remains stronger for industrial telemetry, OPC UA/MQTT, and maintenance analytics |
