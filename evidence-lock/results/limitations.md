# Limitations

- Synthetic regulated-risk data is used for the main ML baseline.
- Public-data lab uses the Wisconsin Diagnostic Breast Cancer dataset as a compact real-data ML proxy, not a credit or governance dataset.
- Docker evidence is documented smoke evidence; this report does not claim a production cloud deployment.
- Slurm and Apptainer files are portability artifacts and were not executed on CINECA, IT4LIA, Leonardo, BI-REX, or another real cluster.
- API scoring is a local FastAPI-compatible simulation with human-review boundaries.
- Outputs are portfolio evidence for screening and technical review, not operational controls.
