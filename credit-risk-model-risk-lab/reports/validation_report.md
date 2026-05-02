# Credit-Risk Validation Report

This report documents the public-data validation evidence for the GiveMeSomeCredit portfolio baseline. It is model-risk practice evidence, not a production validation sign-off.

## Train/Test Split And Feature Engineering

- Split: stratified 80/20 holdout with random state 42.
- Missing numeric values are median-imputed inside the model pipeline.
- Logistic regression uses standard scaling; the tree baseline uses raw numeric features after imputation.
- The target is `FinancialDistressNextTwoYears`, a public competition label and not an observed approval/decline population.

## Model Comparison

| model | roc_auc | pr_auc | brier_score | selected |
| --- | --- | --- | --- | --- |
| hist_gradient_boosting_probability | 0.870866 | 0.409538 | 0.04843 | yes |
| logistic_regression_balanced | 0.790436 | 0.308763 | 0.183284 | no |

## Calibration And Drift

- ROC-AUC: `0.870866`
- PR-AUC: `0.409538`
- Brier score: `0.04843`
- Expected calibration error: `0.003949`
- Train/test score PSI: `0.000819`

## Threshold Selection

Thresholds are treated as review-capacity scenarios, not approval or denial rules.

| threshold | review_rate | precision | recall |
| --- | --- | --- | --- |
| 0.05 | 0.296967 | 0.1879 | 0.834913 |
| 0.1 | 0.165433 | 0.280476 | 0.694264 |
| 0.15 | 0.115067 | 0.349942 | 0.602494 |
| 0.2 | 0.0898 | 0.392353 | 0.527182 |
| 0.3 | 0.058833 | 0.468555 | 0.412469 |
| 0.5 | 0.022433 | 0.610698 | 0.204988 |

## Explainability Evidence

| rank | feature | importance_mean | importance_std |
| --- | --- | --- | --- |
| 1 | RevolvingUtilizationOfUnsecuredLines | 0.073975 | 0.006156 |
| 2 | NumberOfTimes90DaysLate | 0.034748 | 0.000773 |
| 3 | NumberOfTime30-59DaysPastDueNotWorse | 0.032943 | 0.001973 |
| 4 | NumberOfTime60-89DaysPastDueNotWorse | 0.021353 | 0.000587 |
| 5 | age | 0.013722 | 0.001798 |
| 6 | NumberOfOpenCreditLinesAndLoans | 0.006177 | 0.00114 |
| 7 | NumberRealEstateLoansOrLines | 0.004284 | 0.000889 |
| 8 | MonthlyIncome | 0.004201 | 0.001163 |
| 9 | DebtRatio | 0.00348 | 0.001037 |
| 10 | NumberOfDependents | 0.000966 | 0.000775 |

## Proxy / Fairness Review

| feature | risk_area | review_note | action |
| --- | --- | --- | --- |
| age | demographic proxy | Potential protected-class proxy. Keep for transparent benchmark comparison only; do not use for automated production decisions without legal, fairness, and policy review. | Monitor score distribution by age bands where lawful; assess alternate models with and without this feature. |
| DebtRatio | affordability proxy | Debt ratio is domain-relevant but can amplify historical access-to-credit patterns. | Compare calibration and error rates across documented affordability bands. |
| MonthlyIncome | socioeconomic proxy | Income can proxy socioeconomic status and data availability. Missingness can itself become a protected-class proxy. | Track missingness, imputation impact, and feature contribution over time. |
| NumberRealEstateLoansOrLines | wealth / asset proxy | Property-related variables can proxy wealth and local housing-market access. | Review stability by macro period and document any segment-level degradation. |
| NumberOfDependents | household-composition proxy | Household composition may be a sensitive-context proxy depending on jurisdiction and policy use. | Use only with explicit policy approval and monitor missingness/imputation impact. |

## Reject-Inference Boundary

The public dataset contains observed distress labels for the competition population, but it does not provide a real lender's rejected-applicant population, policy rules, or application-time decision path. A production credit-risk validation would need reject-inference analysis, challenger assumptions, approval-policy context, and independent review before any model could influence credit decisions.

## Production Monitoring Plan

| control | metric | trigger |
| --- | --- | --- |
| Input data quality | missingness, range violations, imputation rate | material movement from training baseline |
| Score drift | monthly PSI and score-band volume | PSI above 0.10 for review, above 0.25 for escalation |
| Calibration | Brier score and expected calibration error | worse than validation baseline for two reporting periods |
| Threshold behavior | review rate, precision, recall, false-positive rate | policy threshold no longer meets agreed human-review capacity |
| Proxy/fairness watch | lawful segment-level error and calibration review | statistically meaningful degradation in a documented segment |

## Validation Decision

Acceptable as portfolio evidence for credit-risk modelling, calibration, drift, explainability, threshold discussion, and model-risk documentation. Not acceptable for production lending, automated decisions, or regulatory compliance claims.
