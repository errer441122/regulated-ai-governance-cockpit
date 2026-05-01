# AI Data and Agentic Readiness Lab

Portfolio project for AI/data consulting, reporting, responsible AI adoption, and AI Factory readiness roles.

This project uses a simulated dataset of organizations and AI workflow candidates. It validates the data, scores readiness for controlled pilots, generates recruiter-readable reports, and includes a small human-reviewed agentic brief workflow.

## Target Fit

- CRIF AI/Data/Agentic Solutions: data validation, reporting, functional documentation, anomaly flags, agentic workflow controls.
- PwC Data & AI Consulting: client-ready assessment logic, data-to-insight storytelling, business transformation framing.
- UNDP Digital, AI and Innovation: responsible AI, data governance, capacity building, public-sector programme support.
- CINECA / IT4LIA / BI-REX: AI Factory readiness, metadata quality, secure data management, industrial/public-sector AI workload triage.

## What It Demonstrates

- Python/pandas data pipeline with schema and quality checks.
- Readiness scoring across metadata, governance, stakeholder clarity, data maturity, and AI workload complexity.
- Simulated dashboard for executive review.
- Agentic brief generation using approved structured data only.
- Audit log and explicit human-review boundary.
- n8n workflow export showing how the process could be automated.
- Evidence map from job requirements to portfolio artifacts.

## Structure

| Path | Purpose |
| --- | --- |
| `data/workflow_candidates.csv` | Simulated dataset for AI/data workflow candidates. |
| `src/pipeline.py` | Validation, scoring, blocker detection, and report generation. |
| `src/generate_agentic_brief.py` | Human-reviewed agentic brief generator. |
| `tests/test_pipeline.py` | Minimal unit tests for readiness logic. |
| `dashboard/` | Static reviewer dashboard. |
| `agentic/n8n_workflow_export.json` | No-code/low-code automation example. |
| `notebooks/readiness_analysis.ipynb` | Notebook outline for EDA and interview discussion. |
| `EVIDENCE_MAP.md` | Job requirement to artifact map. |

## Run

```bash
python -m pip install -r requirements.txt
python src/pipeline.py
python src/generate_agentic_brief.py --workflow-id WF-006 --reviewer "Human reviewer"
python -m pytest tests
```

Open `dashboard/index.html` to review the static dashboard.

## Methodology

All data is simulated. The scoring model is intentionally transparent and uses weighted business/data/governance dimensions rather than a black-box model.

Readiness score:

```text
0.20 metadata_quality
0.20 data_governance
0.15 stakeholder_clarity
0.15 data_engineering_maturity
0.15 reporting_value
0.15 ai_workload_fit
```

Blockers are raised when a workflow has high sensitivity with weak governance, weak metadata, missing owners, or unapproved agentic use.

## Human Review Boundary

The agentic brief generator is deterministic and does not call a live LLM. It models the control pattern expected in responsible AI work:

1. Use approved structured data only.
2. Validate before generating.
3. Write an audit log.
4. Mark the brief as draft.
5. Require human review before use.

## What Not To Claim

- This is not a production AI governance platform.
- This is not a real CINECA, BI-REX, CRIF, PwC, UNDP, or Ducati implementation.
- This does not use confidential data.
- This does show the kind of thinking needed for junior AI/data consulting and AI Factory support roles.
