import csv
import os

def main():
    os.makedirs("artifacts/final_results", exist_ok=True)
    
    lineage = [
        # metric, model, split, seed/fold, source artifact, value, aggregation method
        ["Macro-F1", "Full-DCAT", "Primary Test (10%)", "Seed 42", "artifacts/weighted_primary/results.json", "0.9868", "Unweighted mean of Spam and Ham F1"],
        ["MM-Macro-F1", "Full-DCAT", "Multimodal CV (5-Fold)", "5-Fold CV (Seed 42)", "artifacts/weighted_cv/cv_results.csv", "0.6609", "Mean across 5 folds"],
        ["MM-Macro-F1", "Late-Fusion", "Multimodal CV (5-Fold)", "5-Fold CV (Seed 42)", "artifacts/weighted_cv/cv_results.csv", "0.5564", "Mean across 5 folds"],
        ["MM-Macro-F1", "Weighted-DCAT", "Multimodal CV (5-Fold)", "5-Fold CV (Seed 42)", "artifacts/weighted_cv/cv_results.csv", "0.6824", "Mean across 5 folds"],
        ["Ham-F1", "Late-Fusion", "Multimodal CV (5-Fold)", "5-Fold CV (Seed 42)", "artifacts/weighted_cv/cv_results.csv", "0.1313", "Mean across 5 folds"],
        ["Ham-F1", "Full-DCAT", "Multimodal CV (5-Fold)", "5-Fold CV (Seed 42)", "artifacts/weighted_cv/cv_results.csv", "0.3291", "Mean across 5 folds"],
        ["Ham-F1", "Weighted-DCAT", "Multimodal CV (5-Fold)", "5-Fold CV (Seed 42)", "artifacts/weighted_cv/cv_results.csv", "0.3929", "Mean across 5 folds"],
        ["McNemar p-value", "Weighted-DCAT vs Full-DCAT", "Pooled OOF (7867 samples)", "All Folds", "task-1070 log (weighted_stats.py)", "2.49e-45", "Exact/Asymptotic McNemar with continuity correction"],
        ["McNemar p-value", "Weighted-DCAT vs Late-Fusion", "Pooled OOF (7867 samples)", "All Folds", "task-1070 log (weighted_stats.py)", "3.34e-06", "Exact/Asymptotic McNemar with continuity correction"],
        ["Early-Exit Latency", "DCAT-Early-Exit", "Primary Test (10%)", "Seed 42", "scratch/FINAL_RESULTS_SOURCE_OF_TRUTH.md", "+24.82%", "Empirical timing over 7.3k samples vs standard forward pass"],
        ["Early-Exit Vision Skip", "DCAT-Early-Exit", "Primary Test (10%)", "Seed 42", "scratch/FINAL_RESULTS_SOURCE_OF_TRUTH.md", "4.45%", "Count of (Text-only confidence > 0.95 or < 0.05)"],
        ["Early-Exit FLOP Reduction", "DCAT-Early-Exit", "Primary Test (10%)", "Seed 42", "scratch/FINAL_RESULTS_SOURCE_OF_TRUTH.md", "0.63%", "Theoretical calculation based on MobileViT skipping"]
    ]
    
    with open("artifacts/final_results/results_lineage.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "model", "split", "seed/fold", "source artifact", "value", "aggregation method"])
        writer.writerows(lineage)
        
    print("Created artifacts/final_results/results_lineage.csv")

if __name__ == "__main__":
    main()
