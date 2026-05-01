# ISO/IEC 42001 Public Gap Analysis

## Boundary

ISO/IEC 42001 is a management-system standard for responsible AI governance. This file uses only public, high-level ISO descriptions and does not reproduce proprietary ISO controls.

Public reference: https://www.iso.org/standard/42001

## High-Level Gap Analysis

| Management-System Area | Current Evidence | Gap | Next Action |
| --- | --- | --- | --- |
| AI policy and objectives | README positioning, claims and limitations | No formal AI policy or measurable AI governance objectives | Add short AI policy statement and measurable portfolio objectives |
| Roles and responsibilities | Reviewer routes and model cards | No named process owner, validator, approver, or incident owner | Add RACI-style table for portfolio artifacts |
| Risk assessment | Model cards, EU AI Act gap analysis, NIST mapping | Risk assessment is narrative, not a repeatable workflow | Add risk register with severity, likelihood, owner, mitigation, residual risk |
| Data and model lifecycle | Training scripts, model cards, change log | No full lifecycle gates from intake to retirement | Add lifecycle checklist for data, training, validation, release, monitoring, retirement |
| Performance evaluation | ML metrics, calibration, drift evidence | No independent validation or acceptance thresholds | Define acceptance criteria and validation signoff |
| Monitoring and improvement | PSI reports and evidence map | No continuous improvement cadence | Add quarterly review template and incident/postmortem section |
| Documentation control | Git history and reports | No explicit doc-control policy | Use git commit history and model change log as portfolio-level control evidence |

## Recruiter-Safe Claim

This is an ISO/IEC 42001-inspired public gap analysis for a portfolio project. It is not certification evidence and does not claim conformity.
