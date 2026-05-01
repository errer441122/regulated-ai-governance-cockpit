# PyTorch GPU Readiness Lab

Mini-lab Colab per dimostrare readiness PyTorch GPU su un dataset tabular reale.

## Scope

- Dataset: GiveMeSomeCredit, OpenML id `46929`.
- Runtime target: Google Colab free GPU, preferably T4 when allocated.
- Model: MLP tabular PyTorch for binary credit-risk classification.
- GPU evidence: CUDA training, `torch.amp` mixed precision, PyTorch Profiler trace.
- Artifact: JSON with throughput, memory usage, profiler paths, and speedup vs CPU.

## Run

1. Open `notebooks/pytorch_gpu_readiness_colab.ipynb` in Google Colab.
2. Select `Runtime > Change runtime type > GPU`.
3. Run all cells.
4. Download or inspect the generated files:
   - `artifacts/gpu_readiness_metrics.json`
   - `artifacts/profiler/gpu_amp_profiler_summary.txt`
   - `reports/gpu_readiness_report_colab.md`

The committed `artifacts/gpu_readiness_metrics.example.json` is a schema-like example only. The real metrics must be produced by running the notebook on the assigned Colab GPU.

## Evidence Boundary

This lab is a portfolio evidence artifact, not a production lending system and not a claim of CINECA/IT4LIA execution. Colab free GPU availability and exact hardware are not guaranteed; the JSON records the actual allocated device.
