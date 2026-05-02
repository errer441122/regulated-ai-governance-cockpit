# Optimization Report

This report is the benchmark output location for `src/benchmark.py`.

Current status: the artifact contains the executable optimization and benchmark pipeline, but this checkout does not claim local fine-tuning or benchmark execution. Running the commands in `README.md` will replace this file with measured before/after results.

Expected comparison matrix:

| Engine | Purpose | Output |
| --- | --- | --- |
| PyTorch eager | Baseline checkpoint inference | Accuracy, latency, throughput, memory |
| `torch.compile` | PyTorch graph optimization | Accuracy parity and latency delta |
| ONNX Runtime | Portable optimized runtime | Accuracy parity and latency delta |
| ONNX + dynamic quantization | CPU-friendly compressed runtime | Accuracy and latency/size trade-off |

Evidence boundary:

- This is IT4LIA AI Factory readiness evidence for Italian NLP fine-tuning and optimized deployment.
- It is not CINECA Leonardo execution evidence.
- It does not change the credit-risk, governance, RAG, public-sector, or industrial IoT project scores.
