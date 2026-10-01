import os
import sys
import torch
import numpy as np
import pandas as pd
import json
from pathlib import Path
from sklearn.model_selection import StratifiedGroupKFold
from torch.utils.data import DataLoader, Subset

sys.path.insert(0, os.path.abspath('src'))
from dcat.data.dataset import DcatDataset, DcatCollator
from dcat.models.dcat.model import DcatModel
from dcat.models.dcat.baseline import LateFusionBaseline
from dcat.training.engine import DcatTrainer
from dcat.evaluation.metrics import DcatMetrics
from dcat.data.modalities import Modality

def main():
    print("Starting Weighted Multimodal 5-Fold CV & OOF Prediction Generation...")
    os.makedirs("artifacts/weighted_cv", exist_ok=True)
    
    full_ds = DcatDataset("data/processed/records.parquet")
    manifest = pd.read_csv("data/manifests/leakage_groups.csv")
    group_map = dict(zip(manifest['sample_id'].astype(str), manifest['group_id'].astype(str)))
    
    mm_indices = []
    labels = []
    groups = []
    
    for i, r in enumerate(full_ds.records):
        if r.modality.value == 'multimodal':
            mm_indices.append(i)
            labels.append(r.label)
            groups.append(group_map[r.email_id])
            
    mm_indices = np.array(mm_indices)
    labels = np.array(labels)
    groups = np.array(groups)
    
    sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    all_results = []
    
    # We will store Out-Of-Fold (OOF) predictions for McNemar testing
    oof_predictions = {
        "Full-DCAT": {"labels": [], "preds": []},
        "Late-Fusion": {"labels": [], "preds": []},
        "Weighted-DCAT": {"labels": [], "preds": []}
    }
    
    for fold, (train_idx, val_idx) in enumerate(sgkf.split(mm_indices, labels, groups)):
        print(f"\n{'='*50}\nFold {fold+1}/5\n{'='*50}")
        
        abs_train_idx = mm_indices[train_idx]
        abs_val_idx = mm_indices[val_idx]
        
        train_ds = Subset(full_ds, abs_train_idx)
        val_ds = Subset(full_ds, abs_val_idx)
        
        # Calculate pos_weight for this fold ONLY from training data
        fold_train_labels = labels[train_idx]
        num_spam = np.sum(fold_train_labels == 1)
        num_ham = np.sum(fold_train_labels == 0)
        pos_weight_val = num_ham / num_spam if num_spam > 0 else 1.0
        pos_weight_tensor = torch.tensor([pos_weight_val], device=device)
        print(f"Fold {fold+1} pos_weight: {pos_weight_val:.4f} (Spam: {num_spam}, Ham: {num_ham})")
        
        fold_val_labels = labels[val_idx]
        print(f"Fold {fold+1} Validation -> Spam: {np.sum(fold_val_labels==1)}, Ham: {np.sum(fold_val_labels==0)}")
        
        collator = DcatCollator()
        train_loader = DataLoader(train_ds, batch_size=64, shuffle=True, collate_fn=collator, num_workers=2)
        val_loader = DataLoader(val_ds, batch_size=64, shuffle=False, collate_fn=collator, num_workers=2)
        
        models_to_evaluate = [
            ("Full-DCAT", lambda: DcatModel(cross_attention_layers=1), None),
            ("Late-Fusion", lambda: LateFusionBaseline(), None),
            ("Weighted-DCAT", lambda: DcatModel(cross_attention_layers=1), pos_weight_tensor)
        ]
        
        for model_name, model_fn, pos_w in models_to_evaluate:
            print(f"\n--- Training {model_name} (Fold {fold+1}) ---")
            model = model_fn().to(device)
            optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.01, betas=[0.9, 0.999], eps=1.0e-8)
            
            trainer = DcatTrainer(
                model=model,
                train_loader=train_loader,
                val_loader=val_loader,
                optimizer=optimizer,
                device=device,
                amp=True,
                pos_weight=pos_w
            )
            
            trainer.train_epoch()
            
            # Evaluate using threshold=0.5
            metrics = trainer.evaluate(threshold=0.5, return_preds=True)
            
            # Store OOF preds for stats testing later
            # Threshold them to 0 or 1 at 0.5
            bin_preds = (np.array(metrics["_raw_probs"]) >= 0.5).astype(int).tolist()
            oof_predictions[model_name]["labels"].extend(metrics["_raw_labels"])
            oof_predictions[model_name]["preds"].extend(bin_preds)
            
            # Clean up raw lists before saving to df
            del metrics["_raw_probs"]
            del metrics["_raw_labels"]
            
            metrics['model'] = model_name
            metrics['fold'] = fold + 1
            all_results.append(metrics)
            
            print(f"Fold {fold+1} {model_name} - Val Loss: {metrics['val_loss']:.4f} | Macro-F1: {metrics['macro_f1']:.4f} | Spam-F1: {metrics['spam_f1']:.4f} | Ham-F1: {metrics['ham_f1']:.4f}")
            
            del model
            torch.cuda.empty_cache()
            
    df = pd.DataFrame(all_results)
    df.to_csv("artifacts/weighted_cv/cv_results.csv", index=False)
    
    print("\nSummary (Mean +/- Std):")
    summary = df.groupby('model')[['macro_f1', 'spam_f1', 'ham_f1']].agg(['mean', 'std']).reset_index()
    print(summary)
    
    # Compute 95% CI based on the 5 fold values
    print("\n95% CI for Macro-F1 across the 5 folds:")
    for model_name in ["Full-DCAT", "Late-Fusion", "Weighted-DCAT"]:
        fold_f1s = df[df['model'] == model_name]['macro_f1'].values
        mean_f1 = np.mean(fold_f1s)
        std_f1 = np.std(fold_f1s, ddof=1)
        ci_lower = mean_f1 - 1.96 * (std_f1 / np.sqrt(5))
        ci_upper = mean_f1 + 1.96 * (std_f1 / np.sqrt(5))
        print(f"{model_name}: {mean_f1:.4f} (95% CI: [{ci_lower:.4f}, {ci_upper:.4f}])")
    
    # Save OOF predictions
    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer): return int(obj)
            if isinstance(obj, np.floating): return float(obj)
            if isinstance(obj, np.ndarray): return obj.tolist()
            return super(NpEncoder, self).default(obj)
            
    with open("artifacts/weighted_cv/oof_predictions.json", "w") as f:
        json.dump(oof_predictions, f, cls=NpEncoder)
        
    print("\nWeighted CV and OOF Generation Complete.")

if __name__ == "__main__":
    main()
