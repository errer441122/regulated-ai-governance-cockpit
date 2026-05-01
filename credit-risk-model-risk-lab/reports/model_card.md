# Model Card - GiveMeSomeCredit Credit-Risk Baseline

## Scope

Public-data credit-risk baseline for model-risk documentation practice. This model estimates the probability of `FinancialDistressNextTwoYears` on the OpenML curation of the original Kaggle Give Me Some Credit dataset.

## Dataset

- OpenML dataset id: `46929`
- Name: `GiveMeSomeCredit`
- Rows used: `30000`
- Target event rate in test split: `0.066833`
- Original source: `https://www.kaggle.com/competitions/GiveMeSomeCredit`
- OpenML metadata: `https://api.openml.org/api/v1/json/data/46929`

## Model

- Selected model: `hist_gradient_boosting_probability`
- Split: stratified 80/20, random state 42
- Features: `RevolvingUtilizationOfUnsecuredLines, age, NumberOfTime30-59DaysPastDueNotWorse, DebtRatio, MonthlyIncome, NumberOfOpenCreditLinesAndLoans, NumberOfTimes90DaysLate, NumberRealEstateLoansOrLines, NumberOfTime60-89DaysPastDueNotWorse, NumberOfDependents`

## Metrics

- ROC-AUC: `0.870866`
- PR-AUC: `0.409538`
- Gini: `0.741732`
- KS statistic: `0.593015`
- Brier score: `0.04843`
- Expected calibration error: `0.003949`
- Score PSI train vs test: `0.000819`

## Intended Use

Portfolio evidence for credit-risk ML, calibration, drift monitoring, and model-risk documentation.

## Not For

- production lending decisions
- automated credit approval or denial
- legal or regulatory compliance certification
- CRIF, bank, or client deployment claims

## Human Review Boundary

Any score is advisory evidence only. No individual decision should be made from this model.
