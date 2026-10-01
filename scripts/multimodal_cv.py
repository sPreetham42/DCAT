import os
import sys
import torch
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import StratifiedGroupKFold
from torch.utils.data import DataLoader, Subset

sys.path.insert(0, os.path.abspath('src'))
from dcat.data.dataset import DcatDataset, DcatCollator
from dcat.models.dcat.model import DcatModel
from dcat.models.dcat.baseline import LateFusionBaseline, PublishedBaseline
from dcat.training.engine import DcatTrainer

def main():
    print("Starting Multimodal 5-Fold Robustness CV...")
    os.makedirs("artifacts/multimodal_cv", exist_ok=True)
    
    # 1. Load entire dataset, filter to Multimodal
    full_ds = DcatDataset("data/processed/records.parquet")
    
    # Load manifest to get group_ids
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
    
    print(f"Total Multimodal emails: {len(mm_indices)}")
        
    sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
    
    models_to_evaluate = {
        "Full-DCAT": lambda: DcatModel(cross_attention_layers=1),
        "Late-Fusion": lambda: LateFusionBaseline(),
        "Published-Baseline": lambda: PublishedBaseline(vision_model_name="resnet18"),
        "DCAT-No-XAttn": lambda: DcatModel(cross_attention_layers=0)
    }
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    all_results = []
    
    print(f"Plan: 4 models x 5 folds = 20 training runs.")
    print(f"Estimated runtime: ~15 mins.")
    
    for fold, (train_idx, val_idx) in enumerate(sgkf.split(mm_indices, labels, groups)):
        print(f"\n{'='*50}\nFold {fold+1}/5\n{'='*50}")
        
        train_groups = set(groups[train_idx])
        val_groups = set(groups[val_idx])
        overlap = train_groups.intersection(val_groups)
        assert len(overlap) == 0, f"Leakage detected! Overlapping groups: {overlap}"
        
        abs_train_idx = mm_indices[train_idx]
        abs_val_idx = mm_indices[val_idx]
        
        train_ds = Subset(full_ds, abs_train_idx)
        val_ds = Subset(full_ds, abs_val_idx)
        
        # Verify Fold Counts
        fold_train_labels = labels[train_idx]
        fold_val_labels = labels[val_idx]
        print(f"Fold {fold+1} Validation:")
        print(f"  Total samples: {len(fold_val_labels)}")
        print(f"  Spam count: {np.sum(fold_val_labels==1)}")
        print(f"  Ham count: {np.sum(fold_val_labels==0)}")
        print(f"  Unique groups: {len(val_groups)}")
        
        # Ensure every fold has both classes
        assert np.sum(fold_val_labels==1) > 0 and np.sum(fold_val_labels==0) > 0, "Fold does not contain both classes!"
        
        collator = DcatCollator()
        train_loader = DataLoader(train_ds, batch_size=64, shuffle=True, collate_fn=collator, num_workers=2)
        val_loader = DataLoader(val_ds, batch_size=64, shuffle=False, collate_fn=collator, num_workers=2)
        
        for model_name, model_fn in models_to_evaluate.items():
            print(f"\n--- Training {model_name} (Fold {fold+1}) ---")
            model = model_fn().to(device)
            optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.01) # Match 1e-4 from base.yaml
            
            trainer = DcatTrainer(
                model=model,
                train_loader=train_loader,
                val_loader=val_loader,
                optimizer=optimizer,
                device=device,
                amp=True
            )
            
            # Match 1 Epoch constraint
            trainer.train_epoch()
            
            # Evaluate using threshold=0.5 for stability in small set comparisons without tuning
            metrics = trainer.evaluate(threshold=0.5)
            
            metrics['model'] = model_name
            metrics['fold'] = fold + 1
            all_results.append(metrics)
            
            print(f"Fold {fold+1} {model_name} - Val Loss: {metrics['val_loss']:.4f} | Macro-F1: {metrics['macro_f1']:.4f} | Spam-F1: {metrics['spam_f1']:.4f} | Ham-F1: {metrics['ham_f1']:.4f}")
            
            del model
            torch.cuda.empty_cache()
            
    df = pd.DataFrame(all_results)
    df.to_csv("artifacts/multimodal_cv/cv_results.csv", index=False)
    
    print("\nSummary (Mean +/- Std):")
    summary = df.groupby('model')['macro_f1'].agg(['mean', 'std']).reset_index()
    print(summary)

if __name__ == "__main__":
    main()
