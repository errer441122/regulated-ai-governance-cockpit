# Reviewer SQL Module

This folder is the top-level shortcut for reviewers looking for SQL/DWH evidence.

The deeper project already contains SQL in:

- `hpc-mlops-industrial-lab/sql/build_feature_mart.sql`
- `production-sim-stack/sql/feature_mart.duckdb.sql`

`reviewer_feature_mart.duckdb.sql` is a compact DuckDB mart that can be inspected without opening the full production simulation stack.

## Example

```bash
duckdb regulated_ai_review.duckdb < sql/reviewer_feature_mart.duckdb.sql
```

It creates quality, blocker, and pilot-candidate views from the simulated regulated workflow dataset.
