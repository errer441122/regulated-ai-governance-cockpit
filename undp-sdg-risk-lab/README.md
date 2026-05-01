# UNDP SDG / Public-Data Risk Lab

This mini lab adds UNDP-style public-data and responsible-data evidence to the regulated AI governance cockpit.

It is offline-first and uses a small public-development-style sample dataset. It is not a real UNDP project, country-office tool, aid allocation system, eligibility system, procurement workflow, or policy decision system.

## What It Shows

- Public-development-style indicators with a local fallback CSV.
- Lightweight SDG/crisis-risk feature scoring.
- TF-IDF/topic-keyword text mining when scikit-learn is available, with a deterministic fallback.
- Responsible data checklist.
- Short stakeholder-readable policy note.
- Smoke tests for pipeline outputs.

## Run

```bash
python undp-sdg-risk-lab/src/run_pipeline.py
python -m pytest -q undp-sdg-risk-lab/tests
```

Generated artifacts:

- `artifacts/sdg_risk_summary.json`
- `artifacts/sdg_policy_note.md`
- `artifacts/responsible_data_checklist.md`
- `artifacts/nlp_topic_summary.csv`

## Responsible Use Boundary

The output is a briefing aid for human-reviewed capacity-support discussion. It must not be used to allocate aid, rank people, determine eligibility, automate procurement, or make policy decisions.
