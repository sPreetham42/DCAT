import os
import json
import pandas as pd
import numpy as np

def main():
    print("Aggregating Final Results...")
    
    # Check OOF count
    oof_path = "artifacts/weighted_cv/oof_predictions.json"
    with open(oof_path, "r") as f:
        oof_data = json.load(f)
    oof_count = len(oof_data["Weighted-DCAT"]["labels"])
    print(f"OOF predictions found: {oof_count}")
    
    # Read CV results
    cv_df = pd.read_csv("artifacts/weighted_cv/cv_results.csv")
    summary = cv_df.groupby('model')[['macro_f1', 'spam_f1', 'ham_f1']].agg(['mean', 'std']).reset_index()
    
    # Build replacement strings
    def get_mean(model, metric):
        return cv_df[cv_df['model'] == model][metric].mean()
        
    def get_ci(model, metric):
        vals = cv_df[cv_df['model'] == model][metric].values
        mean = np.mean(vals)
        std = np.std(vals, ddof=1)
        lower = mean - 1.96 * (std / np.sqrt(5))
        upper = mean + 1.96 * (std / np.sqrt(5))
        return f"{mean:.4f} (95% CI: [{lower:.4f}, {upper:.4f}])"
        
    lf_ci = get_ci('Late-Fusion', 'macro_f1')
    fd_ci = get_ci('Full-DCAT', 'macro_f1')
    wd_ci = get_ci('Weighted-DCAT', 'macro_f1')
    
    lf_ham = get_mean('Late-Fusion', 'ham_f1')
    fd_ham = get_mean('Full-DCAT', 'ham_f1')
    wd_ham = get_mean('Weighted-DCAT', 'ham_f1')
    
    lf_spam = get_mean('Late-Fusion', 'spam_f1')
    wd_spam = get_mean('Weighted-DCAT', 'spam_f1')
    
    # Update FINAL_RESEARCH_STATUS.md
    with open("docs/FINAL_RESEARCH_STATUS.md", "r", encoding="utf-8") as f:
        content = f.read()
        
    import re
    # Replace CV section
    content = re.sub(r"- \*\*Late-Fusion MM-Macro-F1\*\*: .*?\| Ham-F1: .*?\n", f"- **Late-Fusion MM-Macro-F1**: {lf_ci} | Ham-F1: {lf_ham:.4f}\n", content)
    content = re.sub(r"- \*\*Full DCAT MM-Macro-F1\*\*: .*?\| Ham-F1: .*?\n", f"- **Full DCAT MM-Macro-F1**: {fd_ci} | Ham-F1: {fd_ham:.4f}\n", content)
    content = re.sub(r"- \*\*Weighted DCAT MM-Macro-F1\*\*: .*?\| Ham-F1: .*?\n", f"- **Weighted DCAT MM-Macro-F1**: {wd_ci} | Ham-F1: {wd_ham:.4f}\n", content)
    
    # Replace the OOF sample count in the header for Stats
    content = re.sub(r"## 5\. Statistical Evidence \(McNemar on .*? pooled OOF predictions\)", f"## 5. Statistical Evidence (McNemar on {oof_count} pooled OOF predictions)", content)
    
    with open("docs/FINAL_RESEARCH_STATUS.md", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Updated docs/FINAL_RESEARCH_STATUS.md")

if __name__ == "__main__":
    main()
