$ErrorActionPreference = "Stop"

Write-Host "====================================="
Write-Host "Running Upgrade 4: Statistical Eval"
Write-Host "====================================="
.venv\Scripts\python.exe scripts\statistical_evaluation.py

Write-Host "====================================="
Write-Host "Running Upgrade 5: Leakage Audit"
Write-Host "====================================="
.venv\Scripts\python.exe scripts\leakage_audit.py

Write-Host "====================================="
Write-Host "Running Upgrade 7: Error Analysis"
Write-Host "====================================="
.venv\Scripts\python.exe scripts\error_analysis.py

Write-Host "Analysis scripts finished."
