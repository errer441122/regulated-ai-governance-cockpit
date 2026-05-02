from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "evidence-lock" / "results"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "missing", "path": _rel(path)}
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _copy_if_exists(source: Path, target: Path) -> bool:
    if not source.exists():
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return True


def _write_limitations(path: Path) -> None:
    path.write_text(
        "# Limitations\n\n"
        "- Synthetic regulated-risk data is used for the main ML baseline.\n"
        "- Public-data lab uses the Wisconsin Diagnostic Breast Cancer dataset as a compact real-data ML proxy, not a credit or governance dataset.\n"
        "- Docker evidence is documented smoke evidence; this report does not claim a production cloud deployment.\n"
        "- Slurm and Apptainer files are portability artifacts and were not executed on CINECA, IT4LIA, Leonardo, BI-REX, or another real cluster.\n"
        "- API scoring is a local FastAPI-compatible simulation with human-review boundaries.\n"
        "- Outputs are portfolio evidence for screening and technical review, not operational controls.\n",
        encoding="utf-8",
    )


def build_report() -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    screenshots_dir = RESULTS_DIR / "screenshots"
    terminal_dir = RESULTS_DIR / "terminal_logs"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    terminal_dir.mkdir(parents=True, exist_ok=True)

    metrics = _load_json(ROOT / "ml-baseline" / "artifacts" / "metrics.json")
    evidence_summary = _load_json(RESULTS_DIR / "metrics_summary.json")
    public_metrics = _load_json(ROOT / "public-risk-ml-lab" / "artifacts" / "metrics.json")
    credit_metrics = _load_json(ROOT / "credit-risk-model-risk-lab" / "reports" / "evaluation_metrics.json")
    sdg_metrics = _load_json(ROOT / "undp-public-data-gis-lab" / "artifacts" / "sdg_metrics.json")
    sdg_risk_summary = _load_json(ROOT / "undp-sdg-risk-lab" / "artifacts" / "sdg_risk_summary.json")
    hpc_metrics = _load_json(ROOT / "hpc-pytorch-benchmark" / "artifacts" / "cpu_benchmark.json")
    rag_metrics = _load_json(ROOT / "hpc-ai-rag-lab" / "artifacts" / "retrieval_benchmark.json")
    industrial_monitoring = _load_json(ROOT / "hpc-mlops-industrial-lab" / "artifacts" / "industrial_monitoring_summary.json")

    _copy_if_exists(ROOT / "ml-baseline" / "artifacts" / "model_card.md", RESULTS_DIR / "model_card.md")
    _copy_if_exists(ROOT / "ml-baseline" / "data_card.md", RESULTS_DIR / "data_card.md")
    _copy_if_exists(ROOT / "evidence" / "docker-smoke-test.md", RESULTS_DIR / "docker_smoke_test.md")
    _copy_if_exists(ROOT / "evidence" / "docker-smoke-test.json", terminal_dir / "docker_smoke_test.json")
    for screenshot in (ROOT / "evidence" / "technical-screenshots").glob("*.png"):
        _copy_if_exists(screenshot, screenshots_dir / screenshot.name)
    _write_limitations(RESULTS_DIR / "limitations.md")

    dataset_path = str(metrics.get("data_path", "ml-baseline/data/simulated_regulated_risk_dataset.csv")).replace("\\", "/")
    if dataset_path.startswith("data/"):
        dataset_path = f"ml-baseline/{dataset_path}"

    report = f"""# Portfolio Evidence Report

Generated at: {datetime.now(timezone.utc).isoformat(timespec="seconds")}

## Executive Summary

This Evidence Lock turns the repository from a static dashboard-first portfolio into a Python/ML-first evidence package. The static cockpit remains a demo layer; the permanent reviewer signal is executable Python, scikit-learn models, data-quality checks, drift/calibration artifacts, public-data lab outputs, API smoke evidence, Docker evidence, and Slurm/HPC portability files.

## Reproducibility

```bash
make setup
make evidence
```

Equivalent shell steps are listed in `evidence-lock/commands.sh`.

## Main ML Baseline

| Evidence | Value |
| --- | --- |
| Dataset | {dataset_path} |
| Rows | {metrics.get("rows", "missing")} |
| Model | Logistic Regression + RandomForest baseline |
| Selected model | {metrics.get("selected_model", "missing")} |
| ROC-AUC | {metrics.get("roc_auc", "missing")} |
| PR-AUC | {metrics.get("pr_auc", "missing")} |
| F1 | {metrics.get("f1", "missing")} |
| Recall | {metrics.get("recall", "missing")} |
| Brier score | {metrics.get("brier_score", "missing")} |
| Calibration | {evidence_summary.get("calibration", "missing")} |
| Drift check | {evidence_summary.get("drift_check", "missing")} |
| Data quality | {evidence_summary.get("data_quality", "missing")} |

## Public Real-Data Lab

| Evidence | Value |
| --- | --- |
| Dataset | {public_metrics.get("dataset", "missing")} |
| Source | UCI / scikit-learn Wisconsin Diagnostic Breast Cancer dataset |
| Selected model | {public_metrics.get("selected_model", "missing")} |
| ROC-AUC | {public_metrics.get("roc_auc", "missing")} |
| F1 | {public_metrics.get("f1", "missing")} |
| Brier score | {public_metrics.get("brier_score", "missing")} |

## Public Credit-Risk Model-Risk Lab

| Evidence | Value |
| --- | --- |
| Dataset | {credit_metrics.get("dataset", "missing")} |
| Dataset rows | {credit_metrics.get("dataset_rows", "missing")} |
| Evaluation rows | {credit_metrics.get("test_rows", credit_metrics.get("rows", "missing"))} |
| Selected model | {credit_metrics.get("selected_model", "missing")} |
| ROC-AUC | {credit_metrics.get("roc_auc", "missing")} |
| Gini | {credit_metrics.get("gini", "missing")} |
| KS statistic | {credit_metrics.get("ks_statistic", "missing")} |
| Brier score | {credit_metrics.get("brier_score", "missing")} |
| Expected calibration error | {credit_metrics.get("expected_calibration_error", "missing")} |
| Model card | `credit-risk-model-risk-lab/reports/model_card.md` |
| Validation report | `credit-risk-model-risk-lab/reports/validation_report.md` |
| Feature importance | `credit-risk-model-risk-lab/reports/feature_importance.csv` |
| Threshold review | `credit-risk-model-risk-lab/reports/threshold_review.csv` |

## API, Docker, and Operations Evidence

| Check | Status |
| --- | --- |
| API smoke test | `evidence-lock/results/api_smoke_test.md` |
| Docker smoke test | `evidence-lock/results/docker_smoke_test.md` |
| Model card | `evidence-lock/results/model_card.md` |
| Data card | `evidence-lock/results/data_card.md` |
| Limitations | `evidence-lock/results/limitations.md` |
| Screenshots | `evidence-lock/results/screenshots/` |
| Terminal logs | `evidence-lock/results/terminal_logs/` |

## UNDP Public Data / GIS-Lite Evidence

| Evidence | Value |
| --- | --- |
| Rows | {sdg_metrics.get("rows", "missing")} |
| Average SDG risk score | {sdg_metrics.get("average_sdg_risk_score", "missing")} |
| Map output | `undp-public-data-gis-lab/artifacts/map_output.png` |
| Policy note | `undp-public-data-gis-lab/artifacts/policy_note.md` |

## UNDP AI for SDGs Policy Evidence

| Evidence | Value |
| --- | --- |
| Rows | {sdg_risk_summary.get("rows", "missing")} |
| Capacity-support flags | {sdg_risk_summary.get("capacity_support_flags", "missing")} |
| Average SDG risk score | {sdg_risk_summary.get("average_sdg_risk_score", "missing")} |
| Top contexts | {", ".join(sdg_risk_summary.get("top_contexts", [])) if isinstance(sdg_risk_summary.get("top_contexts"), list) else "missing"} |
| Policy brief | `undp-sdg-risk-lab/artifacts/ai_for_sdgs_policy_brief.md` |
| Charts | `undp-sdg-risk-lab/artifacts/ai_for_sdgs_risk_ranking.svg`, `undp-sdg-risk-lab/artifacts/ai_for_sdgs_indicator_heatmap.svg` |

## CINECA / IT4LIA AI/HPC Evidence

| Evidence | Value |
| --- | --- |
| Benchmark backend | {hpc_metrics.get("backend", "missing")} |
| Runtime seconds | {hpc_metrics.get("runtime_seconds", "missing")} |
| Inference latency ms | {hpc_metrics.get("inference_latency_ms", "missing")} |
| Execution note | {hpc_metrics.get("execution_note", "missing")} |

## Governance / SDG RAG Evidence

| Evidence | Value |
| --- | --- |
| Documents | {rag_metrics.get("documents", "missing")} |
| Chunks | {rag_metrics.get("chunks", "missing")} |
| Eval questions | {rag_metrics.get("queries", "missing")} |
| Answerable questions | {rag_metrics.get("answerable_questions", "missing")} |
| Adversarial questions | {rag_metrics.get("adversarial_questions", "missing")} |
| Top-k accuracy | {rag_metrics.get("top_k_accuracy", "missing")} |
| Grounding coverage | {rag_metrics.get("grounding_coverage", "missing")} |
| Documented failures | {rag_metrics.get("documented_failures", "missing")} |
| Mean hallucination risk score | {rag_metrics.get("mean_hallucination_risk_score", "missing")} |
| Source manifest | `hpc-ai-rag-lab/data/source_manifest.json` |
| FastAPI-compatible endpoint | `hpc-ai-rag-lab/src/api.py` |

## Industrial AI Supplement Evidence

| Evidence | Value |
| --- | --- |
| Telemetry schema | {industrial_monitoring.get("schema", "missing")} |
| Anomaly threshold | {industrial_monitoring.get("anomaly_threshold", "missing")} |
| Alert rate | {industrial_monitoring.get("threshold_summary", {}).get("alert_rate", "missing") if isinstance(industrial_monitoring.get("threshold_summary"), dict) else "missing"} |
| Alerts | {industrial_monitoring.get("threshold_summary", {}).get("alerts", "missing") if isinstance(industrial_monitoring.get("threshold_summary"), dict) else "missing"} |
| Public dataset manifest | `hpc-mlops-industrial-lab/data/public_industrial_dataset_manifest.json` |
| Demo payload | `hpc-mlops-industrial-lab/demo/telemetry_payload.json` |
| Curl demo script | `docs/reviewer/BI_REX_DEMO_SCRIPT.md` |
| Reviewer route | `docs/reviewer/BI_REX_INDUSTRIAL_AI_ROUTE.md` |

## Scope Boundaries

This is not a production system, not a legal compliance tool, not a credit model, not an aid-allocation tool, and not a real CINECA/IT4LIA/CRIF/PwC/UNDP/BI-REX deployment.
"""
    report_path = RESULTS_DIR / "portfolio_evidence_report.md"
    report_path.write_text(report, encoding="utf-8")
    return report_path


def main() -> None:
    print(build_report())


if __name__ == "__main__":
    main()
