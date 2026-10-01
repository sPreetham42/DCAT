import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def main():
    os.makedirs('results_final_70k/figures', exist_ok=True)
    
    with open('experiments/final_results.json', 'r') as f:
        data = json.load(f)
        
    # Re-structure for FINAL_RESULTS_70K.json
    final_results = {
        "dataset_statistics": {
            "total_records": 75419,
            "usable_records": 73206,
            "splits": {"train": 60335, "val": 7542, "test": 7542},
            "class_distribution": {"spam": 50199, "ham": 25220},
            "modality_distribution": {"text_only": 63772, "multimodal": 7867, "image_only": 1567, "empty": 2213}
        },
        "model_configurations": list(data.keys()),
        "primary_results": {},
        "modality_results": {},
        "ablations": {},
        "efficiency": {},
        "provenance": {
            "dataset": "data/processed",
            "leakage_audit": "Sampled TF-IDF showed 63.4% near-duplicate leakage at 0.90 threshold",
            "checkpoints": "checkpoints/"
        }
    }
    
    # Extract results
    for model, m_data in data.items():
        if "mean_test_metrics" in m_data:
            mean = m_data["mean_test_metrics"]
            final_results["primary_results"][model] = {
                "macro_f1": mean.get("macro_f1", 0),
                "spam_f1": mean.get("spam_f1", 0),
                "ham_f1": mean.get("ham_f1", 0),
                "accuracy": mean.get("accuracy", 0)
            }
            final_results["modality_results"][model] = {
                "text_only_macro_f1": mean.get("macro_f1_text", 0),
                "multimodal_macro_f1": mean.get("macro_f1_multimodal", 0),
                "image_only_macro_f1": mean.get("macro_f1_image", 0)
            }
            
    # Efficiency data from lineage
    final_results["efficiency"]["DCAT-Early-Exit"] = {
        "latency_reduction": "24.82%",
        "early_exit_skip_rate": "4.45%",
        "flops_reduction": "0.63%"
    }
    
    # Save JSON
    with open('results_final_70k/FINAL_RESULTS_70K.json', 'w') as f:
        json.dump(final_results, f, indent=2)
        
    # Generate Figure 1: Dataset Modality Distribution
    mods = ['Text-Only', 'Multimodal', 'Image-Only']
    counts = [63772, 7867, 1567]
    plt.figure(figsize=(8, 5))
    plt.bar(mods, counts, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('Dataset Modality Distribution (Usable Corpus)')
    plt.ylabel('Number of Samples')
    for i, v in enumerate(counts):
        plt.text(i, v + 500, str(v), ha='center', va='bottom')
    plt.savefig('results_final_70k/figures/fig1_modality_distribution.png')
    plt.close()
    
    # Generate Figure 2: Ablation Results (Macro-F1)
    models = ['Text-Only', 'Late-Fusion', 'Full-DCAT', 'DCAT-No-Cross-Attention']
    f1_scores = [final_results["primary_results"][m]["macro_f1"] for m in models if m in final_results["primary_results"]]
    models = [m for m in models if m in final_results["primary_results"]]
    
    if len(models) > 0:
        plt.figure(figsize=(10, 6))
        plt.bar(models, f1_scores, color='#9467bd')
        plt.title('Primary Performance (Macro-F1) across Configurations')
        plt.ylabel('Macro-F1 Score')
        plt.ylim(0.95, 1.0) # Zoomed in to see differences
        for i, v in enumerate(f1_scores):
            plt.text(i, v + 0.001, f"{v:.4f}", ha='center', va='bottom')
        plt.xticks(rotation=15)
        plt.tight_layout()
        plt.savefig('results_final_70k/figures/fig2_ablation_performance.png')
        plt.close()

if __name__ == '__main__':
    main()
