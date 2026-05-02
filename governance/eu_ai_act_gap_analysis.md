# EU AI Act Gap Analysis - Public Portfolio Pack

Status checked: 2026-05-02.

This file is a public-source portfolio analysis, not legal advice, not a conformity assessment, and not a claim that any artifact is deployable in the EU. It maps this repository against the EU AI Act themes a PwC-style reviewer would expect to see: risk classification, data governance, technical documentation, transparency, human oversight, accuracy, robustness, cybersecurity, logging, and monitoring.

## Public References

- Regulation (EU) 2024/1689 official text: https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=en
- European Commission AI Act overview: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- European Commission AI Act Q&A: https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act
- Entry-into-force note: https://commission.europa.eu/news/ai-act-enters-force-2024-08-01_en

## Current Timeline Snapshot

The AI Act entered into force on 2024-08-01. The Commission states that most rules apply from 2026-08-02, with earlier application for prohibited practices and AI literacy from 2025-02-02, governance and general-purpose AI obligations from 2025-08-02, and an extended transition for high-risk AI systems embedded into regulated products until 2027-08-02. The Commission has also described a simplification proposal linked to implementation support; this portfolio pack treats the enacted Regulation as the baseline and tracks implementation changes as a watch item.

## Portfolio Position

The repository should be positioned as a non-production AI/data governance portfolio with advisory model outputs. It must not be marketed as a deployed high-risk AI system, a compliance-ready AI system, a conformity-assessed product, a credit decision system, an aid allocation system, or a legal compliance tool.

## Risk Classification Worksheet

| Artifact | Intended purpose in this repo | AI Act risk discussion | Portfolio position | Gap before any real deployment |
| --- | --- | --- | --- | --- |
| `credit-risk-model-risk-lab/` | Public competition dataset baseline for credit-risk ML documentation | Creditworthiness evaluation of natural persons can be high-risk in Annex III contexts when used for actual access to essential private services | Portfolio-only model-risk exercise, no decisions, no real applicants | Formal intended-purpose statement, data governance file, fundamental-rights review, conformity pathway, monitoring, incident process |
| `ml-baseline/` | Synthetic regulated-risk classification for reviewer evidence | Could resemble risk triage if repurposed, but current data are synthetic and advisory | Minimal portfolio artifact with explicit limitation | Prohibit operational use unless recast through full governance and validation |
| `production-sim-stack/` | Local scoring/API simulation for capacity-support workflow | Could become high-risk if used for public-service access, benefits, or rights-affecting decisions | Local simulation and public Render proof-of-execution only | User notice, logging, FRIA-style review for public authority use, human oversight role, incident handling |
| `undp-sdg-risk-lab/` | Public-development-style capacity-support brief | AI/data scoring in development settings can affect vulnerable groups if used for targeting or resource allocation | Briefing aid only, no aid allocation, eligibility, procurement, sanctions, or policy decision | Country-office validation, responsible data review, inclusion analysis, appeal/escalation pathway |
| Static cockpit | Business workflow and governance demonstration | Minimal risk as static case study if not connected to real decisions | Demo and documentation artifact | If connected to real users/data, add data protection review, transparency notice, security review, and monitoring |

## Gap Table

| Theme | Current evidence | Gap | Next action |
| --- | --- | --- | --- |
| Risk classification | This file, `README.md`, `EVIDENCE_MAP.md`, role-specific reviewer routes | No central use-case inventory with risk class, affected population, data source, and prohibited use | Add `governance/ai_use_case_inventory.csv` before any release claim |
| Data governance | OpenML metadata, public-development sample CSVs, model cards, responsible data checklist | No complete lineage, representativeness, consent, retention, data rights, or quality management record | Add dataset cards for credit-risk and SDG labs with source, license, limitations, missingness, freshness, and population caveats |
| Technical documentation | README files, model card, architecture notes, API docs, smoke evidence | Documentation is portfolio evidence, not EU technical documentation | Label all documentation as reviewer evidence and add a technical-doc index only if deployment scope changes |
| Transparency | Model cards, `/metadata`, limitations, responsible use boundaries | No standardized user-facing notice per workflow | Add a standard advisory-output notice to API responses, generated reports, and public-sector brief outputs |
| Human oversight | Human-review boundaries in model cards and policy notes | No named oversight role, override log, escalation SLA, or reviewer training record | Add sample oversight register and override-log schema |
| Accuracy and robustness | ROC-AUC, PR-AUC, Gini, KS, Brier, ECE, PSI, calibration bins, threshold table | No subgroup testing, adversarial testing, data-shift stress tests, or independent validation | Add subgroup/fairness caveat, robustness slices, threshold sensitivity signoff, and validation owner notes |
| Logging and traceability | Run manifests, smoke checks, generated metrics files | No production log retention, audit trail, or serious-incident process | Keep out of production claims; add sample audit log and incident template |
| Post-market monitoring | PSI report, drift report, evidence-lock outputs | No live monitoring, alert triage, rollback, or retirement workflow | Define monitoring triggers, alert thresholds, incident severity, rollback criteria, and retirement triggers |
| Governance and AI literacy | Governance README, validation checklist, limitations docs | No formal training or AI literacy record for operators | Add a short training checklist covering intended use, prohibited use, escalation, and reviewer responsibilities |

## Reviewer-Safe Claim

This repository contains a structured AI governance evidence pack mapped to public EU AI Act themes. It is not a legal compliance product, not conformity-assessment evidence, and not a deployed high-risk AI system.
