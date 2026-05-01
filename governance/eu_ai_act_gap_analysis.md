# EU AI Act Gap Analysis

## Scope

This is a public-source portfolio analysis, not legal advice. It maps the repository evidence against common EU AI Act themes: risk classification, data governance, technical documentation, transparency, human oversight, accuracy/robustness/cybersecurity, logging, and post-market monitoring.

Public references:

- European Commission AI Act navigation FAQ: https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act
- Council of the EU AI Act policy page: https://www.consilium.europa.eu/en/policies/artificial-intelligence-act/
- European Commission AI Act entry-into-force note: https://commission.europa.eu/news/ai-act-enters-force-2024-08-01_en

## Portfolio Position

The repository should be positioned as a non-production AI/data portfolio with advisory model outputs. It should not be marketed as a deployed high-risk AI system or a compliance-ready system.

## Gap Table

| Theme | Current Evidence | Gap | Next Action |
| --- | --- | --- | --- |
| Risk classification | README limitations and human-review boundaries | No formal AI Act risk classification worksheet | Add use-case inventory and classify each demo as prohibited, high-risk, limited-risk, or minimal-risk for analysis only |
| Data governance | Public-data source notes, model cards, drift reports | No complete lineage, consent, retention, or representativeness assessment | Add dataset cards with source, license, target population, missingness, and representativeness limits |
| Technical documentation | README, model cards, API metadata, OpenAPI docs | Documentation is portfolio-level, not conformity documentation | Keep technical docs but label them as reviewer evidence |
| Transparency | `/metadata`, model cards, limitations | No user-facing transparency notice for every workflow | Add a standard "advisory output" notice to API responses and reports |
| Human oversight | Decision boundary: advisory human-review triage only | No operational oversight role or escalation SLA | Add reviewer role, override log, and escalation template |
| Accuracy and robustness | ROC-AUC, PR-AUC, Gini, KS, Brier, ECE, PSI | No adversarial, subgroup, or stability test suite | Add robustness slices and threshold sensitivity tests |
| Logging | Contract tests and run manifests | No production logs or retention policy | Keep out of production claims; add sample audit-log schema |
| Post-market monitoring | PSI and drift reports | No live post-market monitoring process | Define monitoring triggers, alert thresholds, and model retirement criteria |

## Recruiter-Safe Claim

This repository contains a structured AI governance evidence pack mapped to public EU AI Act themes. It is not a legal compliance product and has not undergone conformity assessment.
