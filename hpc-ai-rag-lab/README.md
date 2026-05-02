# HPC AI / RAG Lab

This lab provides a CPU-friendly retrieval workload for AI Factory and governance/SDG review. It uses local notes paraphrased from public NIST, EUR-Lex, UNDP, and UNSD sources, TF-IDF retrieval when scikit-learn is available, deterministic fallback retrieval when it is not, extractive answer generation, source attribution, grounding checks, hallucination-risk scoring, documented abstentions, and a FastAPI-compatible endpoint.

It does not claim GPU use, real Slurm execution, CINECA/IT4LIA access, Leonardo execution, or production RAG deployment.

## IT4LIA Mapping

| IT4LIA signal | Evidence here |
| --- | --- |
| AI setup | local Python retrieval scripts and deterministic sample documents |
| AI development | `src/build_index.py`, `src/retrieve.py`, `src/rag_answer_stub.py` |
| AI test | `src/benchmark.py`, `tests/` |
| Data preparation | chunking and public-source local notes |
| Data management | `data/source_manifest.json`, benchmark output |
| Compliance/trust | source attribution, grounding checks, explicit no-invention boundary |

## Run

```bash
python hpc-ai-rag-lab/src/benchmark.py
python -m pytest -q hpc-ai-rag-lab/tests
```

Optional API run, with FastAPI and Uvicorn installed:

```bash
cd hpc-ai-rag-lab/src
python -m uvicorn api:app --port 8001
```

Generated artifacts:

- `artifacts/retrieval_benchmark.json`
- `artifacts/sample_queries.json`

The benchmark intentionally includes 7 answerable questions and 3 adversarial / out-of-scope questions. A credible run should show documented failures instead of perfect performance; the current artifact reports `top_k_accuracy=0.7`, `grounding_coverage=0.7`, `documented_failures=3`, and a non-zero `mean_hallucination_risk_score`.

Public-source manifest:

- `data/source_manifest.json`

## HPC Boundary

`slurm/run_rag_benchmark.sbatch` and `apptainer/Apptainer.def` are packaging evidence only. They have not been executed on a real CINECA, IT4LIA, or other Slurm cluster.
