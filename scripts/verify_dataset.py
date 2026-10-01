import os
import torch
from pathlib import Path
from collections import Counter
import psutil

from dcat.data.dataset import DcatDataset, DcatCollator
from dcat.models.dcat.model import DcatModel
from dcat.data.modalities import Modality

def print_memory():
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1024**2
        peak = torch.cuda.max_memory_allocated() / 1024**2
        print(f"GPU Memory - Allocated: {allocated:.2f} MB, Peak: {peak:.2f} MB")
    else:
        mem = psutil.Process(os.getpid()).memory_info().rss / 1024**2
        print(f"CPU Memory - RSS: {mem:.2f} MB")

def verify_dataset_and_smoke_test():
    parquet_path = Path("data/processed/records.parquet")
    if not parquet_path.exists():
        print("Dataset missing.")
        return
        
    ds = DcatDataset(parquet_path)
    print(f"Total Samples: {len(ds)}")
    
    # Calculate modality distribution
    modalities = [item["modality"] for item in ds]
    labels = [item["label"] for item in ds]
    
    mod_counts = Counter(modalities)
    print("\nModality Distribution:")
    for mod in Modality:
        count = mod_counts.get(mod.value, 0)
        pct = count / len(ds) * 100
        
        # Spam percentage within modality
        mod_indices = [i for i, m in enumerate(modalities) if m == mod.value]
        spam_count = sum(1 for i in mod_indices if labels[i] == 1)
        spam_pct = (spam_count / count * 100) if count > 0 else 0
        
        print(f"  {mod.name}: {count} ({pct:.1f}%) | Spam: {spam_pct:.1f}%")
        
    # Smoke Test
    print("\nRunning Smoke Test and Gradient Verification...")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = DcatModel().to(device)
    
    # Freeze check
    print(f"DistilBERT frozen: {not next(model.text_encoder.parameters()).requires_grad}")
    
    collator = DcatCollator()
    # Let's take the first batch
    batch = collator([ds[i] for i in range(min(4, len(ds)))])
    
    # Move to device
    for k, v in batch.items():
        if isinstance(v, torch.Tensor):
            batch[k] = v.to(device)
            
    print(f"\nBatch Size: {len(batch['email_id'])}")
    print(f"Text Input Shape: {batch['input_ids'].shape}")
    print(f"Image Input Shape: {batch['pixel_values'].shape}")
    print(f"Batch Modalities: {batch['modality']}")
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    criterion = torch.nn.BCEWithLogitsLoss()
    
    logits = model(batch)
    print(f"\nLogits shape: {logits.shape}, finite: {torch.isfinite(logits).all().item()}")
    
    loss = criterion(logits, batch["labels"].float().to(device))
    print(f"Loss finite: {torch.isfinite(loss).item()}")
    
    loss.backward()
    
    print("\nGradients finite:")
    print(f"  Text Projector: {torch.isfinite(model.projector.text_proj.weight.grad).all().item() if model.projector.text_proj.weight.grad is not None else 'No grad (expected if no TEXT)'}")
    print(f"  Image Projector: {torch.isfinite(model.projector.image_proj.weight.grad).all().item() if model.projector.image_proj.weight.grad is not None else 'No grad (expected if no IMAGE)'}")
    print(f"  Cross-Attention: {torch.isfinite(model.cross_attention.layers[0].mha_t2i.in_proj_weight.grad).all().item() if model.cross_attention.layers[0].mha_t2i.in_proj_weight.grad is not None else 'No grad (expected if no MULTIMODAL)'}")
    print(f"  Classifier: {torch.isfinite(model.classifier.net[0].weight.grad).all().item()}")
    
    optimizer.step()
    print_memory()
    print("\nSmoke Test PASSED.")

if __name__ == "__main__":
    verify_dataset_and_smoke_test()
