# HPC PyTorch Benchmark

CPU-friendly AI/HPC readiness benchmark for CINECA/IT4LIA-style review. The code uses PyTorch when it is installed and falls back to a deterministic NumPy implementation so CI remains lightweight.

Executed locally on CPU. Slurm scripts are provided as portability artifacts. No claim is made of execution on Leonardo, CINECA, IT4LIA, or another real HPC cluster.

## Run

```bash
python hpc-pytorch-benchmark/benchmark.py --quick
python hpc-pytorch-benchmark/train.py
python hpc-pytorch-benchmark/infer.py
```
