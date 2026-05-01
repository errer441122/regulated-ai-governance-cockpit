# PyTorch GPU Readiness Mini-Lab Report

## Objective

Create a compact Google Colab lab that demonstrates practical PyTorch GPU readiness on a real tabular credit-risk dataset.

The lab covers:

- Public-data ingestion from OpenML GiveMeSomeCredit (`data_id=46929`).
- MLP tabular training in PyTorch.
- CPU baseline vs CUDA baseline vs CUDA mixed precision.
- Modern mixed precision through `torch.amp`.
- PyTorch Profiler trace and summary table.
- JSON artifact with throughput, memory usage, and speedup vs CPU.

## Execution Path

Notebook:

`notebooks/pytorch_gpu_readiness_colab.ipynb`

Runtime target:

Google Colab free GPU runtime. The target GPU is T4 when allocated, but free-tier allocation can vary. The notebook records the actual device name through PyTorch and `nvidia-smi`.

Generated run outputs:

- `artifacts/gpu_readiness_metrics.json`
- `artifacts/profiler/gpu_amp_profiler_summary.txt`
- `reports/gpu_readiness_report_colab.md`

Committed example artifact:

- `artifacts/gpu_readiness_metrics.example.json`

## Dataset

Source:

- OpenML dataset id: `46929`
- Dataset name: `GiveMeSomeCredit`
- Original source: Kaggle Give Me Some Credit competition
- Rows: approximately `150000`
- Features: `10`
- Target: `FinancialDistressNextTwoYears`

The notebook downloads the ARFF file from OpenML, parses it with `scipy.io.arff`, imputes numeric missing values with train-set medians, scales features with `StandardScaler`, and uses stratified train/validation/test splits.

## Model

The benchmark model is intentionally small and tabular:

- Input: 10 engineered numeric credit-risk fields.
- Architecture: dense MLP with batch normalization, ReLU activations, and dropout.
- Loss: `BCEWithLogitsLoss`.
- Optimizer: AdamW.
- Metrics: ROC-AUC and average precision on the held-out test split.

This is a training-readiness benchmark, not a production credit scorecard.

## Benchmark Contract

The notebook records three runs when CUDA is available:

- `cpu_fp32`: CPU baseline.
- `gpu_fp32`: CUDA baseline without mixed precision.
- `gpu_amp`: CUDA run with `torch.amp.autocast` and `torch.amp.GradScaler`.

The JSON artifact reports:

- Wall-clock training time.
- Training throughput in samples per second.
- CPU process memory delta.
- CUDA peak allocated and reserved memory.
- Speedup vs CPU by wall time and throughput.
- Speedup of GPU AMP vs GPU FP32 by throughput.
- Profiler output paths.

## Profiler

The GPU AMP run is profiled with PyTorch Profiler using CPU and CUDA activities when CUDA is present.

Profiler outputs:

- TensorBoard-compatible trace files under `artifacts/profiler/`.
- Text summary sorted by CUDA time when available.

## Portfolio Impact

Target scoring impact after running the notebook and attaching the generated JSON artifact:

- CINECA: `5.8 -> 7.0` (`+1.2`)
- IT4LIA: `7.5 -> 8.0` (`+0.5`)
- Average: `7.7 -> 8.0`

Rationale: this adds direct GPU readiness evidence, mixed-precision familiarity, PyTorch Profiler usage, and reproducible performance instrumentation.

## Boundary

Do not claim production model validity, lending readiness, CINECA execution, IT4LIA execution, or guaranteed Colab T4 allocation. The notebook is designed to generate honest measured evidence on the GPU actually assigned by Colab.
