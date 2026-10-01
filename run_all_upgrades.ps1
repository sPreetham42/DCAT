$ErrorActionPreference = "Stop"

Write-Host "====================================="
Write-Host "Running Upgrade 1: Multimodal CV"
Write-Host "====================================="
.venv\Scripts\python.exe scripts\multimodal_cv.py

Write-Host "====================================="
Write-Host "Running Upgrade 2: Imbalance Ablation"
Write-Host "====================================="
.venv\Scripts\python.exe scripts\imbalance_ablation.py

Write-Host "====================================="
Write-Host "Running Upgrade 3: Efficiency Benchmark"
Write-Host "====================================="
.venv\Scripts\python.exe scripts\efficiency_benchmark.py

Write-Host "All scripts finished."
