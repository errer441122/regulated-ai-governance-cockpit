# Data Management Plan

## Dataset Boundary

The pack uses simulated portfolio datasets only. The records are designed to resemble regulated workflow, industrial operations, and public-development schemas without containing confidential, customer, employee, health, credit, or institutional data.

## Lineage

| Stage | Input | Output | Control |
| --- | --- | --- | --- |
| Validation | `hpc-mlops-industrial-lab/data/regulated_workflows.csv` | schema and quality checks | deterministic local script |
| ML baseline | validated regulated workflow rows | metrics, predictions, model artifact | scikit-learn train/test split |
| Production simulation | public-development sample | feature mart, manifest, monitoring exports | local orchestration script |
| HPC packaging | code plus offline sample data | Slurm command and container recipe | no cluster execution claimed |

## Secure Data Handling

- No secrets, credentials, or tokens are required.
- No live CRM, legal, credit, healthcare, or government system is connected.
- Generated artifacts are reviewer evidence, not production records.
- A real AI Factory deployment would require approved ingress, retention, storage, audit, and deletion procedures before any non-public data is staged.

## Metadata And Retention

FAIR-style metadata is represented in `fair_metadata_example.json`. For a real CINECA/IT4LIA workload, metadata would be registered with the project catalogue, bound to allocation IDs, and connected to storage retention rules.

## Compliance Boundary

The workload supports human review and technical evaluation only. It must not be presented as a certified risk model, credit model, legal compliance system, or production AI service.
