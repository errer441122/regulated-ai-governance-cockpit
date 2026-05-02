# Model Card: Industrial Defect Vision Classifier

## Model

ResNet18 binary image classifier for MVTec-style industrial defect detection. The implementation also includes a `tiny-cnn` smoke-test architecture for local CI checks when `torchvision` is unavailable.

## Intended Use

- Demonstrate computer-vision engineering for an AI Developer portfolio.
- Score images as `normal` or `anomaly` in a documented demo API.
- Produce reviewer-facing metrics: AUROC, precision, recall, F1, accuracy, and defect-folder counts.

## Not Intended For

- Production factory inspection.
- Automated shutdown, rejection, or quality-control decisions.
- Safety-critical monitoring.
- Claims of standard MVTec benchmark performance unless the official protocol is followed.

## Data

The intended real dataset is MVTec AD, downloaded separately from the official MVTec site. Images and checkpoints are excluded from git.

The supervised fine-tuning path expects a small held-out subset with both `good` and defect folders under `train/` and `test/`. This is not the official unsupervised MVTec protocol.

## Metrics

Target reviewer metric after real training:

| Metric | Target |
| --- | --- |
| Image-level AUROC | >= 0.90 on a documented held-out subset |
| Recall | Report at selected threshold |
| Precision | Report at selected threshold |
| F1 | Report at selected threshold |

Current repository status: code and smoke tests are present; real MVTec training metrics are not committed.

## Limitations

- Performance depends heavily on category, lighting, split hygiene, and defect type.
- A supervised subset can overstate real-world performance if defect images leak between train and test.
- The fallback API score is deterministic smoke-check behavior, not a trained model.
- No claim is made about robustness to new factories, cameras, materials, or acquisition settings.

## Decision Boundary

The API response includes:

```text
portfolio demo only; no automated quality decision
```

Any real deployment would require representative data, camera/process validation, drift monitoring, operator review, and a quality-management sign-off.
