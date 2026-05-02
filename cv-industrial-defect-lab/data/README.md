# Data Boundary

Do not commit MVTec images, extracted archives, checkpoints, or generated artifact files.

## Official Source

Download MVTec AD from the official MVTec research dataset page:

- https://www.mvtec.com/research-teaching/datasets/mvtec-ad

Review the dataset terms on that page before using it in public artifacts.

## Expected Local Layout

Create a small reviewer subset under:

```text
cv-industrial-defect-lab/data/mvtec_subset/
```

The scripts expect:

```text
mvtec_subset/
  <category>/
    train/
      good/
        image.png
      <defect_type>/
        image.png
    test/
      good/
        image.png
      <defect_type>/
        image.png
```

`good` maps to label `0`; every other defect folder maps to label `1`.

## Honest Protocol Note

The official MVTec AD benchmark is designed for unsupervised anomaly detection with training on normal images. This lab's ResNet18 fine-tuning path is a supervised subset workflow for portfolio demonstration. Keep those two protocols separate when reporting metrics.
