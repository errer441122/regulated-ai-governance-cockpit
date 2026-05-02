# Model Card: Italian BERT Sentiment Classifier

## Overview

- Base model: `dbmdz/bert-base-italian-xxl-cased`
- Task: Italian tweet sentiment classification
- Dataset: `evalitahf/sentiment_analysis`, SENTIPOLC 2016
- Labels: `negative`, `positive`, `neutral`
- Intended artifact scope: IT4LIA AI Factory readiness evidence for training, distributed execution, optimization, containerization, and inference packaging.

## FAIR Metadata

| FAIR dimension | Implementation in this artifact |
| --- | --- |
| Findable | Dataset and model are identified by stable Hugging Face repository IDs; reports use reproducible filenames. |
| Accessible | Data is loaded from Hugging Face at runtime; `data/.gitignore` prevents committing copied datasets. |
| Interoperable | Checkpoints are exported to ONNX with dynamic axes for batch and sequence length. |
| Reusable | Config files record model, dataset, batch sizes, max length, and benchmark targets. |

## Dataset

SENTIPOLC 2016 contains 9,410 Italian tweets annotated for subjectivity, polarity, and irony. This artifact derives a three-class label from overall positive and negative polarity fields:

- `positive`: `opos=1`, `oneg=0`
- `negative`: `oneg=1`, `opos=0`
- `neutral`: all other polarity combinations

The dataset is public benchmark data. It is not employer, client, CRIF, PwC, UNDP, BI-REX, CINECA, or IT4LIA operational data.

## Training

Training is launched with:

```bash
torchrun --standalone --nproc_per_node=2 src/train.py --config configs/train_ddp.yaml
```

The script supports real multi-GPU DDP and a single-GPU/VM readiness demonstration mode. The latter demonstrates distributed process orchestration, not production cluster execution.

## Optimization

The optimization path exports the fine-tuned checkpoint to ONNX and applies ONNX Runtime dynamic quantization:

```bash
python src/optimize.py --config configs/optimize.yaml
python src/benchmark.py --config configs/optimize.yaml
```

Benchmark engines:

- PyTorch eager
- `torch.compile`
- ONNX Runtime
- ONNX Runtime with dynamic quantization

## Risks and Limitations

- Tweets can contain slang, sarcasm, reclaimed language, and political context that a small supervised classifier may misread.
- SENTIPOLC is benchmark data, not a representative production monitoring stream.
- Dynamic quantization can change borderline predictions; accuracy parity must be checked after export.
- This model is not suitable for automated moderation or consequential decisions without a separate risk assessment and human review process.

## Evaluation Record

Measured metrics are written by `src/benchmark.py` to:

- `reports/profiling_report.json`
- `reports/optimization_report.md`

This committed model card does not claim benchmark values until those commands are run in the target environment.
