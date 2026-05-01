# Public Risk ML Lab

Small real-data ML lab for reviewer evidence. It uses the public Wisconsin Diagnostic Breast Cancer dataset distributed with scikit-learn as a compact proxy for model lifecycle handling: dataset preparation, train/test split, baseline models, calibration bins, feature importance, model card, data card, and limitations.

It is not a credit model, medical device, compliance tool, or production model.

## Run

```bash
python public-risk-ml-lab/fetch_or_prepare_data.py
python public-risk-ml-lab/train.py
python public-risk-ml-lab/evaluate.py
```
