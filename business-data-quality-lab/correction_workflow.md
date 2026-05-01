# Correction Workflow

1. Validate required fields and numeric ranges.
2. Flag placeholder identifiers, missing locations, and impossible counts.
3. Detect duplicate candidates by VAT match and legal-name similarity.
4. Route candidates to human review before merge, correction, or external confirmation.
5. Preserve audit notes for every accepted or rejected correction.

## Duplicate Candidates

| Left ID | Right ID | Same VAT | Name Similarity | Action |
| --- | --- | --- | --- | --- |
| IT-0002 | IT-0005 | True | 0.897 | human_review_merge_or_confirm |

Boundary: synthetic registry-like records only; no automated legal, credit, or official register update.
