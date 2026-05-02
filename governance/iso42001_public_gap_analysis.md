# ISO/IEC 42001 Public Gap Analysis

Status checked: 2026-05-02.

This is a public, high-level ISO/IEC 42001-inspired gap analysis. It does not reproduce proprietary ISO control text, does not claim certification, and should not be used as certification evidence. Its purpose is to show management-system thinking for a portfolio project.

## Public Reference

- ISO/IEC 42001:2023 official page: https://www.iso.org/standard/42001

The ISO public page describes ISO/IEC 42001 as an international standard for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System within organizations. This pack maps the repository only at that public management-system level.

## Boundary

The repository is a non-production portfolio. It has model cards, validation artifacts, governance notes, and generated evidence, but it does not have an organization-wide AI management system, management approval, internal audit, supplier management, employee training, or certification scope.

## High-Level Gap Analysis

| Management-system area | Current evidence | Gap | Next action |
| --- | --- | --- | --- |
| AI policy and objectives | `README.md`, `docs/reviewer/CLAIMS_AND_LIMITATIONS.md`, role-specific route docs | No formal AI policy, measurable objectives, management approval, or periodic review cadence | Add a one-page AI policy statement with objectives for safety, transparency, reproducibility, and non-production boundaries |
| Scope of AIMS | `EVIDENCE_MAP.md`, `AI_INTERNSHIP_FIT.md`, lab READMEs | Scope is described for portfolio reviewers, not as a controlled management-system scope | Define in-scope artifacts, out-of-scope activities, stakeholders, and review frequency |
| Roles and responsibilities | Model cards, reviewer routes, validation checklist | No named process owner, validator, approver, incident owner, or record keeper | Add RACI table for each lab and governance artifact |
| Risk and opportunity assessment | NIST mapping, EU AI Act gap analysis, model-risk framework | Risk assessment is narrative, not a repeatable workflow | Add risk register with severity, likelihood, owner, mitigation, residual risk, and review date |
| Data and model lifecycle | Training scripts, metrics artifacts, model cards, change log | No formal lifecycle gates from idea intake to retirement | Add lifecycle gate checklist for data intake, training, validation, release, monitoring, change, and retirement |
| Performance evaluation | ML metrics, calibration, PSI, drift reports, threshold review | No independent validation or acceptance thresholds | Define minimum metric thresholds, calibration limits, drift triggers, and validation signoff |
| Human oversight and accountability | Human-review boundaries in model cards and policy brief | No operational oversight workflow, override log, or escalation path | Add sample oversight log, explanation note, and escalation template |
| Supplier and third-party dependency awareness | Public dataset references, package requirements, CDN notes | No full supplier risk register for datasets, packages, APIs, or hosted services | Add third-party dependency register with source, purpose, license, risk, and fallback |
| Incident and nonconformity management | Scope limitations and smoke-test evidence | No incident taxonomy, corrective action log, or postmortem template | Add incident severity table, corrective action template, and closure criteria |
| Documentation and record control | Git history, generated reports, evidence-lock outputs | No explicit document-control policy or retention rules | Use git plus `governance/model_change_log.md` as portfolio control evidence and add review dates |
| Continual improvement | Evidence map, validation checklist, generated reports | No scheduled management review or improvement backlog | Add quarterly review checklist and improvement backlog with owners and status |

## PDCA-Style Improvement Loop

| Phase | Portfolio evidence | Missing management-system element |
| --- | --- | --- |
| Plan | Governance pack, use-case boundaries, model-risk framework | Approved AI policy, scope, objectives, and risk appetite |
| Do | Executable pipelines, model cards, SDG brief, smoke checks | Controlled operating procedures and role-based training |
| Check | Metrics, calibration, PSI, tests, evidence-lock report | Independent validation, internal audit, and management review |
| Act | Change log and README updates | Corrective action process, residual-risk signoff, and retirement decisions |

## Recruiter-Safe Claim

This is an ISO/IEC 42001-inspired public gap analysis for a portfolio project. It demonstrates responsible AI management-system awareness, but it is not certification evidence and does not claim conformity.
