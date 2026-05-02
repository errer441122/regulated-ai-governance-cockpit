# CV Industrial Defect Lab

Computer-vision portfolio lab for industrial visual anomaly detection. This folder is intentionally isolated from the CRIF, PwC Risk, UNDP, IT4LIA, CINECA, and BI-REX evidence paths.

## What This Demonstrates

| PwC AI Developer signal | Evidence in this lab |
| --- | --- |
| Computer vision | MVTec-style image dataset discovery, RGB preprocessing, ResNet18 fine-tuning path |
| Industrial AI | Defect detection framing for objects, parts, and materials rather than generic image classification |
| Model evaluation | AUROC, precision, recall, F1, accuracy, confusion-matrix counts, defect-folder counts |
| API delivery | FastAPI `POST /predict` image upload endpoint |
| Responsible boundaries | No production inspection claim, no private factory data, no committed MVTec images or model checkpoints |

## Dataset

Use the official [MVTec AD dataset](https://www.mvtec.com/research-teaching/datasets/mvtec-ad), a public industrial anomaly-detection benchmark. The dataset is large and must not be committed.

This lab supports a supervised MVTec-style subset for ResNet18 fine-tuning:

```text
cv-industrial-defect-lab/data/mvtec_subset/
  bottle/
    train/good/*.png
    train/crack/*.png
    test/good/*.png
    test/crack/*.png
```

MVTec AD's standard protocol is unsupervised training on anomaly-free images. This portfolio lab uses the same folder conventions for a supervised reviewer subset; do not report results as standard MVTec benchmark numbers unless the evaluation protocol is changed and documented.

## Install

```bash
python -m pip install -r cv-industrial-defect-lab/requirements.txt
```

`torchvision` is required for the real ResNet18 path. The tests use `tiny-cnn` so they can run without GPU, downloaded weights, or the full MVTec dataset.

## Train

From the repository root:

```bash
python cv-industrial-defect-lab/src/train.py \
  --data-dir cv-industrial-defect-lab/data/mvtec_subset \
  --output-dir cv-industrial-defect-lab/artifacts \
  --architecture resnet18 \
  --pretrained \
  --epochs 5 \
  --batch-size 16 \
  --image-size 224
```

For a CPU smoke run on a tiny local subset:

```bash
python cv-industrial-defect-lab/src/train.py \
  --data-dir cv-industrial-defect-lab/data/mvtec_subset \
  --output-dir cv-industrial-defect-lab/artifacts \
  --architecture tiny-cnn \
  --epochs 1 \
  --image-size 64
```

Generated files:

- `cv-industrial-defect-lab/artifacts/model.pt`
- `cv-industrial-defect-lab/artifacts/training_summary.json`

## Evaluate

```bash
python cv-industrial-defect-lab/src/evaluate.py \
  --data-dir cv-industrial-defect-lab/data/mvtec_subset \
  --checkpoint-path cv-industrial-defect-lab/artifacts/model.pt \
  --output-dir cv-industrial-defect-lab/artifacts \
  --split test
```

Output:

- `cv-industrial-defect-lab/artifacts/evaluation_metrics.json`

The reviewer target is image-level AUROC >= 0.90 on a clearly documented held-out subset. The repository does not claim that target until real MVTec images are downloaded, trained, and evaluated.

## API

```bash
cd cv-industrial-defect-lab/src
python -m uvicorn inference_api:app --port 8002
```

Then upload an image:

```bash
curl -X POST "http://127.0.0.1:8002/predict" \
  -F "file=@../data/mvtec_subset/bottle/test/good/sample.png"
```

If `artifacts/model.pt` is missing, the API returns a documented `fallback_untrained` response. That mode exists only for smoke checks.

## Test

```bash
python -m pytest -q cv-industrial-defect-lab/tests
```

The tests create temporary images and do not require MVTec AD, GPU, network access, or `torchvision`.

## Portfolio Boundary

This is computer-vision evidence for an AI Developer internship screen. It is not factory validation, production QA, a safety system, a replacement for human inspection, or evidence of access to proprietary manufacturing data.
