# Technical Lab - Data Validation and Human-Reviewed Agentic Briefs

This mini project adds executable technical evidence to the portfolio. It is intentionally small and transparent: a simulated regulated-AI workflow dataset is validated with Python/pandas, scored for readiness, and used by a deterministic agentic brief generator that writes logs and requires human review.

## Why This Exists

The main cockpit demonstrates product, governance, and consulting thinking. This lab adds proof for roles that ask for hands-on data work:

- CRIF: dataset checks, reporting inputs, validation mindset, functional documentation, agentic-solutions context.
- PwC: data-to-insight pipeline, consulting-ready outputs, clear assumptions and client-style framing.
- UNDP: responsible AI, data governance, capacity building, public-sector and programme-support readiness.
- CINECA / IT4LIA / BI-REX: metadata checks, secure data management signals, AI workload readiness, reproducible Python scripts.

## Contents

| Path | Purpose |
| --- | --- |
| `data/workflow_signals.csv` | Simulated dataset of regulated AI workflow candidates. |
| `src/validate_dataset.py` | Schema, missing-value, duplicate, range, and readiness checks. |
| `src/generate_agentic_brief.py` | Deterministic agentic brief generator using approved data only. |
| `agentic/n8n_agentic_brief_workflow.json` | Example n8n workflow export for the same human-reviewed process. |
| `notebooks/workflow_readiness_eda.ipynb` | Notebook outline for exploratory analysis and reviewer discussion. |

## Run

```bash
cd technical-lab
python -m pip install -r requirements.txt
python src/validate_dataset.py
python src/generate_agentic_brief.py --organization "Regional Health Data Office" --reviewer "Human reviewer"
```

Generated files are written to `technical-lab/reports/`.

## Human Review Boundary

The agentic brief script does not call a live LLM and does not make automated decisions. It simulates the structure of an AI-assisted workflow:

1. Load approved tabular data.
2. Validate the schema and key quality checks.
3. Select one organization/use case.
4. Generate a structured draft brief.
5. Write an audit-style log.
6. Mark the output as requiring human review before use.

This keeps the project credible for responsible AI roles without pretending to be a production agent.
