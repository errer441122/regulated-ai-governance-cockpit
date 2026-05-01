# HPC AI / RAG Lab

This lab provides a CPU-friendly retrieval workload for CINECA/IT4LIA-style AI Factory review. It uses small local governance documents, TF-IDF retrieval when scikit-learn is available, and a deterministic fallback when it is not.

It does not claim GPU use, real Slurm execution, CINECA/IT4LIA access, Leonardo execution, or production RAG deployment.

## IT4LIA Mapping

| IT4LIA signal | Evidence here |
| --- | --- |
| AI setup | local Python retrieval scripts and deterministic sample documents |
| AI development | `src/build_index.py`, `src/retrieve.py`, `src/rag_answer_stub.py` |
| AI test | `src/benchmark.py --quick`, `tests/test_retrieval.py` |
| Data preparation | chunking and sample governance docs |
| Data management | local artifact manifest and benchmark output |
| Compliance/trust | extractive-only answer stub and explicit no-invention boundary |

## Run

```bash
python hpc-ai-rag-lab/src/benchmark.py --quick
python -m pytest -q hpc-ai-rag-lab/tests
```

Generated artifacts:

- `artifacts/retrieval_benchmark.json`
- `artifacts/sample_queries.json`

## HPC Boundary

`slurm/run_rag_benchmark.sbatch` and `apptainer/Apptainer.def` are packaging evidence only. They have not been executed on a real CINECA, IT4LIA, or other Slurm cluster.
