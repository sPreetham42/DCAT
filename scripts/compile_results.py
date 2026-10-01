import os
import json
import pandas as pd
from glob import glob

def main():
    print(f"\n{'='*50}\nCompiling Final Paper-Ready Results (Upgrade 6)\n{'='*50}")
    
    os.makedirs("artifacts/final_results", exist_ok=True)
    
    # 1. Primary Benchmark Results
    with open("experiments/final_results.json", "r") as f:
        primary_data = json.load(f)
        
    primary_rows = []
    for model, data in primary_data.items():
        if "mean_test_metrics" in data:
            test = data["mean_test_metrics"]
            primary_rows.append({
                "Model": model,
                "Macro-F1": f"{test.get('macro_f1', 0):.4f}",
                "Spam-F1": f"{test.get('spam_f1', 0):.4f}",
                "Ham-F1": f"{test.get('ham_f1', 0):.4f}",
                "MM-Macro-F1": f"{test.get('macro_f1_multimodal', 0):.4f}" if "macro_f1_multimodal" in test else "N/A"
            })
    df_primary = pd.DataFrame(primary_rows)
    df_primary.to_csv("artifacts/final_results/primary_benchmark.csv", index=False)
    
    # 2. Multimodal CV Results
    if os.path.exists("artifacts/multimodal_cv/cv_results.csv"):
        df_cv = pd.read_csv("artifacts/multimodal_cv/cv_results.csv")
        df_cv_summary = df_cv.groupby('model')['macro_f1'].agg(['mean', 'std']).reset_index()
        df_cv_summary.columns = ["Model", "MM-Macro-F1 (Mean)", "MM-Macro-F1 (Std)"]
        df_cv_summary.to_csv("artifacts/final_results/multimodal_cv_summary.csv", index=False)
    else:
        df_cv_summary = pd.DataFrame()
        
    # 3. Imbalance Ablation Results
    if os.path.exists("artifacts/imbalance_ablation/results.json"):
        with open("artifacts/imbalance_ablation/results.json", "r") as f:
            imb_data = json.load(f)
            test = imb_data.get("test_metrics", {})
            df_imb = pd.DataFrame([{
                "Model": "Weighted Full-DCAT",
                "Macro-F1": f"{test.get('macro_f1', 0):.4f}",
                "Spam-F1": f"{test.get('spam_f1', 0):.4f}",
                "Ham-F1": f"{test.get('ham_f1', 0):.4f}",
                "MM-Macro-F1": f"{test.get('macro_f1_multimodal', 0):.4f}"
            }])
            df_imb.to_csv("artifacts/final_results/imbalance_ablation.csv", index=False)
    else:
        df_imb = pd.DataFrame()
        
    # 4. Efficiency Benchmark Results
    if os.path.exists("artifacts/efficiency/benchmark_results.csv"):
        df_eff = pd.read_csv("artifacts/efficiency/benchmark_results.csv")
        df_eff.to_csv("artifacts/final_results/efficiency_summary.csv", index=False)
    else:
        df_eff = pd.DataFrame()
        
    # Combine into a single JSON for easy programmatic access
    final_json = {
        "primary_benchmark": df_primary.to_dict(orient="records"),
        "multimodal_cv": df_cv_summary.to_dict(orient="records") if not df_cv_summary.empty else [],
        "imbalance_ablation": df_imb.to_dict(orient="records") if not df_imb.empty else [],
        "efficiency": df_eff.to_dict(orient="records") if not df_eff.empty else []
    }
    
    with open("artifacts/final_results/results_summary.json", "w") as f:
        json.dump(final_json, f, indent=2)
        
    # Generate unified Markdown table
    with open("artifacts/final_results/results_table.md", "w") as f:
        f.write("# Consolidated Paper Results\n\n")
        f.write("## 1. Primary Benchmark (3-Seed Average on Original Test Split)\n")
        f.write(df_primary.to_markdown(index=False) + "\n\n")
        f.write("## 2. Multimodal Robustness (5-Fold CV on 8k subset)\n")
        if not df_cv_summary.empty:
            f.write(df_cv_summary.to_markdown(index=False) + "\n\n")
        f.write("## 3. Imbalance Ablation (Weighted BCE Loss)\n")
        if not df_imb.empty:
            f.write(df_imb.to_markdown(index=False) + "\n\n")
        f.write("## 4. Empirical Efficiency\n")
        if not df_eff.empty:
            f.write(df_eff.to_markdown(index=False) + "\n\n")

if __name__ == "__main__":
    main()
