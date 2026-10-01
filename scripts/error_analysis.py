import os
import sys
import torch
import numpy as np
import pandas as pd
from torch.utils.data import DataLoader, Subset

sys.path.insert(0, os.path.abspath('src'))
from dcat.data.dataset import DcatDataset, DcatCollator
from dcat.models.dcat.model import DcatModel
from dcat.models.dcat.baseline import LateFusionBaseline

def get_errors(model, dataloader, device, records):
    model.eval()
    model.to(device)
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for batch in dataloader:
            batch = {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in batch.items()}
            logits = model(batch)
            probs = torch.sigmoid(logits).cpu().numpy().flatten()
            preds = (probs >= 0.5).astype(int)
            all_preds.extend(preds)
            all_labels.extend(batch["labels"].cpu().numpy().flatten())
            
    preds = np.array(all_preds)
    labels = np.array(all_labels)
    
    # 1 is spam, 0 is ham
    fp_indices = np.where((preds == 1) & (labels == 0))[0]
    fn_indices = np.where((preds == 0) & (labels == 1))[0]
    
    # Sample up to 50
    np.random.seed(42)
    if len(fp_indices) > 50:
        fp_indices = np.random.choice(fp_indices, 50, replace=False)
    if len(fn_indices) > 50:
        fn_indices = np.random.choice(fn_indices, 50, replace=False)
        
    errors = []
    for idx in fp_indices:
        r = records[idx]
        errors.append({
            "Email ID": r.email_id,
            "True Label": "Ham",
            "Prediction": "Spam (FP)",
            "Text Preview": (r.text[:200] + "...") if r.text else "N/A"
        })
    for idx in fn_indices:
        r = records[idx]
        errors.append({
            "Email ID": r.email_id,
            "True Label": "Spam",
            "Prediction": "Ham (FN)",
            "Text Preview": (r.text[:200] + "...") if r.text else "N/A"
        })
        
    return pd.DataFrame(errors)

def main():
    print(f"\n{'='*50}\nStarting Error Analysis (Upgrade 7)\n{'='*50}")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    full_ds = DcatDataset("data/processed/records.parquet")
    test_mm_indices = [i for i, r in enumerate(full_ds.records) if r.split == "test" and r.modality.value == "multimodal"]
    test_ds = Subset(full_ds, test_mm_indices)
    mm_records = [full_ds.records[i] for i in test_mm_indices]
    
    collator = DcatCollator()
    dataloader = DataLoader(test_ds, batch_size=64, shuffle=False, collate_fn=collator)
    
    print("Loading models...")
    lf_model = LateFusionBaseline()
    lf_model.load_state_dict(torch.load("checkpoints/late-fusion_seed42_best.pt", map_location=device, weights_only=True))
    
    dcat_model = DcatModel(cross_attention_layers=1)
    dcat_model.load_state_dict(torch.load("checkpoints/full-dcat_seed42_best.pt", map_location=device, weights_only=True))
    
    print("Extracting errors for Late-Fusion...")
    df_lf = get_errors(lf_model, dataloader, device, mm_records)
    
    print("Extracting errors for Full DCAT...")
    df_dcat = get_errors(dcat_model, dataloader, device, mm_records)
    
    os.makedirs("artifacts/error_analysis", exist_ok=True)
    df_lf.to_csv("artifacts/error_analysis/late_fusion_errors.csv", index=False)
    df_dcat.to_csv("artifacts/error_analysis/dcat_errors.csv", index=False)
    
    with open("docs/ERROR_ANALYSIS.md", "w") as f:
        f.write("# Automatic Error Analysis\n\n")
        f.write("Extracted up to 50 False Positives and 50 False Negatives from the Multimodal Test Subset for qualitative analysis.\n\n")
        
        f.write("## Late-Fusion Errors\n")
        f.write(f"- False Positives (Ham predicted as Spam): {len(df_lf[df_lf['Prediction'].str.contains('FP')])}\n")
        f.write(f"- False Negatives (Spam predicted as Ham): {len(df_lf[df_lf['Prediction'].str.contains('FN')])}\n\n")
        
        f.write("## Full DCAT Errors\n")
        f.write(f"- False Positives (Ham predicted as Spam): {len(df_dcat[df_dcat['Prediction'].str.contains('FP')])}\n")
        f.write(f"- False Negatives (Spam predicted as Ham): {len(df_dcat[df_dcat['Prediction'].str.contains('FN')])}\n\n")
        
        f.write("## Note on Causality\n")
        f.write("These samples identify failure modes (e.g. text/image misalignment), but statistical claims cannot be drawn from these individual examples alone. The extreme FP rate on the 6 available ham samples dominates these lists.")
        
    print("Error analysis complete.")

if __name__ == "__main__":
    main()
