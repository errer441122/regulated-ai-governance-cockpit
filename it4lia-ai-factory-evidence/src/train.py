from __future__ import annotations

import argparse
import json
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class TrainConfig:
    model_name: str = "dbmdz/bert-base-italian-xxl-cased"
    dataset_name: str = "evalitahf/sentiment_analysis"
    dataset_config: str | None = None
    text_column: str = "text"
    output_dir: str = "artifacts/model"
    metrics_path: str = "reports/train_metrics.json"
    max_length: int = 128
    num_labels: int = 3
    train_batch_size: int = 8
    eval_batch_size: int = 16
    learning_rate: float = 2e-5
    weight_decay: float = 0.01
    epochs: int = 3
    warmup_ratio: float = 0.06
    seed: int = 42
    max_train_samples: int | None = None
    max_eval_samples: int | None = None
    validation_size: float = 0.15
    dataloader_workers: int = 2
    allow_single_gpu_ddp_demo: bool = True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fine-tune Italian BERT with torchrun/DDP.")
    parser.add_argument("--config", default="configs/train_ddp.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Load config and exit.")
    return parser.parse_args()


def load_config(path: str) -> TrainConfig:
    with open(path, "r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    known_fields = TrainConfig.__dataclass_fields__.keys()
    unknown = sorted(set(raw) - set(known_fields))
    if unknown:
        raise ValueError(f"Unknown config keys: {unknown}")
    return TrainConfig(**raw)


def set_seed(seed: int) -> None:
    import numpy as np
    import torch

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def distributed_context() -> tuple[bool, int, int, int]:
    world_size = int(os.getenv("WORLD_SIZE", "1"))
    rank = int(os.getenv("RANK", "0"))
    local_rank = int(os.getenv("LOCAL_RANK", "0"))
    return world_size > 1, rank, local_rank, world_size


def resolve_device(local_rank: int, world_size: int, allow_single_gpu_demo: bool) -> torch.device:
    import torch

    if not torch.cuda.is_available():
        return torch.device("cpu")

    device_count = torch.cuda.device_count()
    if device_count >= world_size:
        device_index = local_rank
    elif allow_single_gpu_demo and device_count == 1:
        device_index = 0
    else:
        raise RuntimeError(
            f"torchrun requested {world_size} processes but only {device_count} CUDA devices are visible."
        )

    torch.cuda.set_device(device_index)
    return torch.device(f"cuda:{device_index}")


def init_distributed_if_needed(device: torch.device) -> bool:
    import torch
    import torch.distributed as dist

    is_distributed, _rank, _local_rank, world_size = distributed_context()
    if not is_distributed:
        return False
    backend = "nccl" if device.type == "cuda" and torch.cuda.device_count() >= world_size else "gloo"
    dist.init_process_group(backend=backend)
    return True


def cleanup_distributed() -> None:
    import torch.distributed as dist

    if dist.is_available() and dist.is_initialized():
        dist.destroy_process_group()


def is_main_process() -> bool:
    return int(os.getenv("RANK", "0")) == 0


def sentipolc_label(example: dict[str, Any]) -> int:
    positive = int(example.get("opos", example.get("positive", 0)))
    negative = int(example.get("oneg", example.get("negative", 0)))
    if positive == 1 and negative == 0:
        return 1
    if negative == 1 and positive == 0:
        return 0
    return 2


def load_sentiment_dataset(config: TrainConfig) -> DatasetDict:
    from datasets import Dataset, DatasetDict, load_dataset

    raw = load_dataset(config.dataset_name, config.dataset_config) if config.dataset_config else load_dataset(config.dataset_name)
    if isinstance(raw, Dataset):
        split = raw.train_test_split(test_size=config.validation_size, seed=config.seed)
        return DatasetDict(train=split["train"], validation=split["test"])

    if "validation" in raw:
        return DatasetDict(train=raw["train"], validation=raw["validation"])
    if "test" in raw and "train" in raw:
        return DatasetDict(train=raw["train"], validation=raw["test"])
    if "train" not in raw:
        first_split = next(iter(raw))
        split = raw[first_split].train_test_split(test_size=config.validation_size, seed=config.seed)
        return DatasetDict(train=split["train"], validation=split["test"])

    split = raw["train"].train_test_split(test_size=config.validation_size, seed=config.seed)
    return DatasetDict(train=split["train"], validation=split["test"])


def prepare_dataset(config: TrainConfig, tokenizer: AutoTokenizer) -> DatasetDict:
    dataset = load_sentiment_dataset(config)
    if config.text_column not in dataset["train"].column_names:
        raise ValueError(f"Text column '{config.text_column}' not found in {dataset['train'].column_names}")

    def add_labels(batch: dict[str, list[Any]]) -> dict[str, list[int]]:
        rows = [dict(zip(batch, values)) for values in zip(*batch.values())]
        return {"labels": [sentipolc_label(row) for row in rows]}

    def tokenize(batch: dict[str, list[Any]]) -> dict[str, Any]:
        return tokenizer(
            batch[config.text_column],
            truncation=True,
            max_length=config.max_length,
        )

    dataset = dataset.map(add_labels, batched=True)
    dataset = dataset.map(tokenize, batched=True)

    if config.max_train_samples:
        dataset["train"] = dataset["train"].shuffle(seed=config.seed).select(range(config.max_train_samples))
    if config.max_eval_samples:
        dataset["validation"] = dataset["validation"].select(range(config.max_eval_samples))

    keep_columns = ["input_ids", "attention_mask", "labels"]
    if "token_type_ids" in dataset["train"].column_names:
        keep_columns.append("token_type_ids")
    remove_columns = [col for col in dataset["train"].column_names if col not in keep_columns]
    dataset = dataset.remove_columns(remove_columns)
    dataset.set_format("torch")
    return dataset


def make_dataloaders(
    config: TrainConfig,
    dataset: DatasetDict,
    tokenizer: AutoTokenizer,
    distributed: bool,
) -> tuple[DataLoader, DataLoader]:
    import torch
    from torch.utils.data import DataLoader, DistributedSampler
    from transformers import DataCollatorWithPadding

    train_sampler = DistributedSampler(dataset["train"], shuffle=True) if distributed else None
    eval_sampler = None
    collator = DataCollatorWithPadding(tokenizer=tokenizer)
    train_loader = DataLoader(
        dataset["train"],
        batch_size=config.train_batch_size,
        sampler=train_sampler,
        shuffle=train_sampler is None,
        collate_fn=collator,
        num_workers=config.dataloader_workers,
        pin_memory=torch.cuda.is_available(),
    )
    eval_loader = DataLoader(
        dataset["validation"],
        batch_size=config.eval_batch_size,
        sampler=eval_sampler,
        shuffle=False,
        collate_fn=collator,
        num_workers=config.dataloader_workers,
        pin_memory=torch.cuda.is_available(),
    )
    return train_loader, eval_loader


def move_batch(batch: dict[str, torch.Tensor], device: torch.device) -> dict[str, torch.Tensor]:
    return {key: value.to(device) for key, value in batch.items()}


def evaluate(model: torch.nn.Module, loader: DataLoader, device: torch.device) -> dict[str, float]:
    import torch
    from sklearn.metrics import accuracy_score, f1_score

    model.eval()
    predictions: list[int] = []
    labels: list[int] = []
    with torch.no_grad():
        for batch in loader:
            batch = move_batch(batch, device)
            output = model(**batch)
            predictions.extend(torch.argmax(output.logits, dim=-1).cpu().tolist())
            labels.extend(batch["labels"].cpu().tolist())
    return {
        "accuracy": float(accuracy_score(labels, predictions)),
        "macro_f1": float(f1_score(labels, predictions, average="macro")),
    }


def save_metrics(path: str, metrics: dict[str, Any]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)


def train(config: TrainConfig) -> dict[str, Any]:
    import numpy as np
    import torch
    from torch.nn.parallel import DistributedDataParallel
    from torch.utils.data import DistributedSampler
    from tqdm.auto import tqdm
    from transformers import (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        get_linear_schedule_with_warmup,
    )

    set_seed(config.seed)
    is_distributed, rank, local_rank, world_size = distributed_context()
    device = resolve_device(local_rank, world_size, config.allow_single_gpu_ddp_demo)
    distributed = init_distributed_if_needed(device)

    try:
        tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        dataset = prepare_dataset(config, tokenizer)
        train_loader, eval_loader = make_dataloaders(config, dataset, tokenizer, distributed)

        model = AutoModelForSequenceClassification.from_pretrained(
            config.model_name,
            num_labels=config.num_labels,
            id2label={0: "negative", 1: "positive", 2: "neutral"},
            label2id={"negative": 0, "positive": 1, "neutral": 2},
        ).to(device)

        if distributed:
            ddp_kwargs = {"device_ids": [device.index]} if device.type == "cuda" else {}
            model = DistributedDataParallel(model, **ddp_kwargs)

        optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)
        total_steps = len(train_loader) * config.epochs
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=int(total_steps * config.warmup_ratio),
            num_training_steps=total_steps,
        )

        history: list[dict[str, float]] = []
        progress = range(config.epochs)
        if is_main_process():
            progress = tqdm(progress, desc="epochs")

        for epoch in progress:
            if distributed and isinstance(train_loader.sampler, DistributedSampler):
                train_loader.sampler.set_epoch(epoch)

            model.train()
            losses: list[float] = []
            for batch in train_loader:
                batch = move_batch(batch, device)
                optimizer.zero_grad(set_to_none=True)
                output = model(**batch)
                output.loss.backward()
                optimizer.step()
                scheduler.step()
                losses.append(float(output.loss.detach().cpu()))

            if is_main_process():
                metrics = evaluate(model.module if hasattr(model, "module") else model, eval_loader, device)
                metrics["epoch"] = float(epoch + 1)
                metrics["train_loss"] = float(np.mean(losses))
                history.append(metrics)

        if is_main_process():
            output_dir = Path(config.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            save_model = model.module if hasattr(model, "module") else model
            save_model.save_pretrained(output_dir)
            tokenizer.save_pretrained(output_dir)
            result = {
                "model_name": config.model_name,
                "dataset_name": config.dataset_name,
                "world_size": world_size,
                "rank": rank,
                "device": str(device),
                "history": history,
            }
            save_metrics(config.metrics_path, result)
            return result
        return {}
    finally:
        cleanup_distributed()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    if args.dry_run:
        print(json.dumps(config.__dict__, indent=2))
        return
    result = train(config)
    if is_main_process():
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
