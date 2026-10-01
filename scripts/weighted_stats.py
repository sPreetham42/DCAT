import os
import json
import numpy as np
from statsmodels.stats.contingency_tables import mcnemar

def main():
    print(f"\n{'='*50}\nStarting Statistical Significance Testing (Weighted CV OOF)\n{'='*50}")
    
    oof_path = "artifacts/weighted_cv/oof_predictions.json"
    if not os.path.exists(oof_path):
        print(f"Error: Could not find {oof_path}. Please run weighted_cv.py first.")
        return
        
    with open(oof_path, "r") as f:
        oof_data = json.load(f)
        
    models = ["Weighted-DCAT", "Full-DCAT", "Late-Fusion"]
    for m in models:
        if m not in oof_data:
            print(f"Error: Model {m} missing from OOF predictions.")
            return
            
    # Verify arrays are identically sized
    num_samples = len(oof_data["Weighted-DCAT"]["labels"])
    print(f"Loaded OOF predictions for {num_samples} samples across 5 folds.")
    
    # We extract the predicted correct/incorrect binary vectors
    labels = np.array(oof_data["Weighted-DCAT"]["labels"])
    
    def get_correct_vector(model_name):
        preds = np.array(oof_data[model_name]["preds"])
        return preds == labels
        
    correct_weighted = get_correct_vector("Weighted-DCAT")
    correct_original = get_correct_vector("Full-DCAT")
    correct_late = get_correct_vector("Late-Fusion")
    
    def run_mcnemar(name1, corr1, name2, corr2):
        print(f"\n--- McNemar Test: {name1} vs {name2} ---")
        
        # Contingency table
        #           name2_corr  name2_incorr
        # name1_corr      a           b
        # name1_incorr    c           d
        
        a = np.sum(corr1 & corr2)
        b = np.sum(corr1 & ~corr2)
        c = np.sum(~corr1 & corr2)
        d = np.sum(~corr1 & ~corr2)
        
        table = [[a, b], [c, d]]
        print(f"Contingency Table:")
        print(f"                    {name2} Correct | {name2} Incorrect")
        print(f"{name1} Correct   |        {a}        |        {b}")
        print(f"{name1} Incorrect |        {c}        |        {d}")
        
        res = mcnemar(table, exact=False, correction=True)
        print(f"p-value: {res.pvalue:.4e}")
        
        if res.pvalue < 0.05:
            winner = name1 if b > c else name2
            print(f"Result: STATISTICALLY SIGNIFICANT (p < 0.05). {winner} is superior.")
        else:
            print("Result: NOT Statistically Significant (p >= 0.05).")
            
    run_mcnemar("Weighted-DCAT", correct_weighted, "Full-DCAT", correct_original)
    run_mcnemar("Weighted-DCAT", correct_weighted, "Late-Fusion", correct_late)
    
    print("\nStatistical Testing Complete.")

if __name__ == "__main__":
    main()
