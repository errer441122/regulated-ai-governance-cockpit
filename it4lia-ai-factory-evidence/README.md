# Italian/EU NLP Training-to-Benchmark HPC Workload

Self-contained IT4LIA/AI Factory evidence artifact showing the applied ML path end to end: training -> optimization -> packaging -> benchmark on public Italian NLP data, with HPC-oriented GPU packaging through Apptainer rather than Docker.

This directory is intentionally separate from the existing CRIF, PwC, UNDP, BI-REX, CINECA, governance, RAG, credit-risk, and industrial IoT artifacts. It does not modify their code, metrics, reports, or claims.

## Task

- Fine-tune `dbmdz/bert-base-italian-xxl-cased` for Italian sentiment analysis.
- Use `torchrun --nproc_per_node=2` to demonstrate DDP orchestration on a single VM/GPU-ready environment.
- Export the fine-tuned model to ONNX.
- Apply ONNX Runtime dynamic quantization.
- Benchmark PyTorch eager, `torch.compile`, ONNX Runtime, and ONNX Runtime quantized inference.
- Serve optimized inference through a minimal FastAPI API.
- Package the workload with an Apptainer GPU recipe aligned with Italian HPC deployment conventions.

## Dataset

Default dataset: `evalitahf/sentiment_analysis` on Hugging Face.

The dataset card identifies it as SENTIPOLC 2016, with 9,410 Italian tweets annotated for subjectivity, polarity, and irony. The artifact loads data directly from Hugging Face at runtime; `data/.gitignore` prevents dataset copies from being committed.

Alternative dataset path: change `dataset_name`, `text_column`, and label construction in `configs/train_ddp.yaml` and `src/train.py` for an Italian hate-speech dataset.

## Setup

```bash
cd it4lia-ai-factory-evidence
python -m venv .venv
. .venv/Scripts/Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Linux/macOS activation:

```bash
source .venv/bin/activate
```

## Run

DDP fine-tuning:

```bash
torchrun --standalone --nproc_per_node=2 src/train.py --config configs/train_ddp.yaml
```

ONNX export and quantization:

```bash
python src/optimize.py --config configs/optimize.yaml
```

Benchmark:

```bash
python src/benchmark.py --config configs/optimize.yaml
```

Serve optimized inference:

```bash
uvicorn src.inference_api:app --host 0.0.0.0 --port 8000
```

Example request:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"texts\":[\"Questo servizio funziona bene\"]}"
```

## Apptainer

Build from this artifact root:

```bash
apptainer build --fakeroot it4lia-gpu-workload.sif apptainer/it4lia-gpu-workload.def
```

Run training with GPU passthrough:

```bash
apptainer exec --nv --bind "$PWD":/workspace it4lia-gpu-workload.sif \
  torchrun --standalone --nproc_per_node=2 src/train.py --config configs/train_ddp.yaml
```

Run inference:

```bash
apptainer run --nv --bind "$PWD":/workspace it4lia-gpu-workload.sif
```

## Results

Committed report files are execution targets, not fabricated measurements:

- `reports/profiling_report.json` contains the benchmark schema and current `not_executed_in_this_checkout` status.
- `reports/optimization_report.md` is overwritten by `src/benchmark.py` with before/after metrics.
- `reports/model_card.md` records FAIR metadata, dataset/model provenance, risks, and evidence boundaries.

Expected post-run comparison:

| Engine | Metric family |
| --- | --- |
| PyTorch eager | baseline accuracy, latency, throughput, memory |
| `torch.compile` | graph-optimized PyTorch parity and latency delta |
| ONNX Runtime | portable optimized runtime latency and throughput |
| ONNX + quantization | quantized runtime size/latency trade-off and accuracy parity |

## Score Boundary

| Target | Boundary |
| --- | --- |
| IT4LIA | Adds Italian NLP fine-tuning, DDP readiness, ONNX quantization, API, and Apptainer evidence. |
| CRIF | Credit-risk lab remains separate; no financial metrics are touched. |
| PwC Risk | Governance pack remains unchanged; no new audit framework is introduced. |
| PwC AI Developer | RAG lab remains unchanged; this is NLP classification, not RAG or LLM development. |
| UNDP | Public-data policy artifacts remain unchanged. |
| BI-REX | Industrial IoT artifacts remain unchanged; no sensors or PLC workflow is added. |
| CINECA | DDP on a single VM/GPU-ready setup is readiness evidence, not Leonardo cluster execution evidence. |
