# Regulated AI Governance & ML Engineering Cockpit

[Static demo on GitHub Pages](https://errer441122.github.io/regulated-ai-governance-cockpit/)  
[Live API on Render](https://regulated-ai-governance-api.onrender.com/docs)  
[![Validation](https://github.com/errer441122/regulated-ai-governance-cockpit/actions/workflows/validate.yml/badge.svg)](https://github.com/errer441122/regulated-ai-governance-cockpit/actions/workflows/validate.yml)

Applied portfolio project for regulated AI governance, credit-risk ML evidence, public-sector data/SDG analytics, production-style FastAPI packaging, and AI Factory/HPC readiness.

The repository is intentionally honest about scope: it combines executable labs, public data, local simulations, and deployment evidence, but it does not claim production use, employer/client data, real Slurm execution, regulatory certification, or real credit/public-benefit decisions.

## IT4LIA / AI Factory Spotlight

[Italian/EU NLP Training-to-Benchmark HPC Workload](it4lia-ai-factory-evidence/README.md) is a self-contained evidence artifact showing the full applied ML path: fine-tuning Italian BERT on SENTIPOLC public Italian tweet data, optimizing inference with `torch.compile`, ONNX export and dynamic quantization, packaging the workload for GPU execution with Apptainer, benchmarking latency/throughput/memory/accuracy, and serving optimized inference through FastAPI.

Scope boundary: this is AI Factory readiness evidence on public Italian/EU-style NLP data. It does not alter the CRIF credit-risk lab, PwC governance/RAG work, UNDP public-sector pack, BI-REX industrial IoT evidence, or CINECA Leonardo execution claims.

## Five Files To Review First

1. `docs/reviewer/CRIF_5_MIN_ROUTE.md`
2. `credit-risk-model-risk-lab/reports/validation_report.md`
3. `hpc-ai-rag-lab/artifacts/retrieval_benchmark.json`
4. `production-sim-stack/src/api.py`
5. `evidence-lock/results/portfolio_evidence_report.md`

## Three Commands To Reproduce

```bash
python -m pytest -q
python credit-risk-model-risk-lab/src/evaluate.py
python hpc-ai-rag-lab/src/benchmark.py
```

Full local evidence path:

```bash
make evidence
```

## Executable Evidence

| Area | Evidence |
| --- | --- |
| Credit-risk ML | OpenML GiveMeSomeCredit pipeline, model comparison, calibration, PSI, threshold review, permutation importance, validation report |
| Governance | NIST AI RMF, EU AI Act, and ISO/IEC 42001 public-gap mapping with clear non-certification boundaries |
| RAG / AI development | Public-source governance/SDG notes, ingestion, chunking, retrieval, answer generation, 10-question eval set, grounding checks, FastAPI-compatible endpoint |
| Production simulation | FastAPI-style scoring, Docker/Render packaging, API smoke evidence, model-source fallback boundaries |
| HPC / AI Factory readiness | Slurm and Apptainer packaging, CPU benchmarks, workload and data-management plans |
| Italian NLP AI Factory workload | `it4lia-ai-factory-evidence/`: training -> optimization -> Apptainer GPU packaging -> benchmark on public Italian SENTIPOLC data |
| Public-sector analytics | SDG risk lab, responsible data checklist, policy brief artifacts, public-data boundaries |

## Reviewer Routes

- `docs/reviewer/CRIF_5_MIN_ROUTE.md`
- `docs/reviewer/RECRUITER_5_MIN_ROUTE.md`
- `docs/reviewer/TECHNICAL_20_MIN_ROUTE.md`
- `docs/reviewer/CLAIMS_AND_LIMITATIONS.md`
- `docs/reviewer/COMPANY_FIT_MATRIX.md`
- `docs/reviewer/BI_REX_INDUSTRIAL_AI_ROUTE.md`
- `docs/reviewer/BI_REX_DEMO_SCRIPT.md`
- `docs/reviewer/DUCATI_FOLDER_BOUNDARY.md`
- `CINECA_IT4LIA_REVIEWER_ROUTE.md`
- `UNDP_REVIEWER_ROUTE.md`

## Role Fit

| Screening signal | Strongest path |
| --- | --- |
| Credit-risk ML engineering | `credit-risk-model-risk-lab/`, `production-sim-stack/src/api.py`, CI |
| Data and AI risk consulting | `governance/`, `credit-risk-model-risk-lab/reports/validation_report.md`, `EVIDENCE_MAP.md` |
| Public-sector data science | `undp-sdg-risk-lab/`, `hpc-ai-rag-lab/`, responsible data artifacts |
| AI Factory / HPC support | `it4lia-ai-factory-evidence/`, `hpc-ai-rag-lab/`, `ai-factory-workload-pack/`, `hpc-pytorch-benchmark/` |
| Industrial AI supplement | `hpc-mlops-industrial-lab/`, `production-sim-stack/` |

## Limits

- No real employer, client, customer, bureau, UNDP, Ducati, CINECA, IT4LIA, or BI-REX data.
- No production credit model, aid-allocation system, legal compliance tool, or automated decision system.
- No real Slurm cluster, GPU cluster, Leonardo, AI Factory, cloud security review, or production MLOps execution.
- The live Render API is public portfolio deployment evidence, not production infrastructure.
- Metrics are validation practice evidence on public or synthetic data; they are not independent model approval.
