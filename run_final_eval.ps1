$ErrorActionPreference = "Stop"
Write-Host "Running Weighted DCAT Primary Benchmark..."
.venv\Scripts\python.exe scripts\weighted_primary.py
if ($LASTEXITCODE -ne 0) { throw "Primary benchmark failed" }

Write-Host "Running Weighted DCAT 5-Fold CV..."
.venv\Scripts\python.exe scripts\weighted_cv.py
if ($LASTEXITCODE -ne 0) { throw "CV failed" }

Write-Host "Running Weighted DCAT Stats..."
.venv\Scripts\python.exe scripts\weighted_stats.py
if ($LASTEXITCODE -ne 0) { throw "Stats failed" }

Write-Host "All scripts finished successfully."
