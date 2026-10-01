import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
from pathlib import Path
import tempfile
import sys
import traceback

from dcat.data.dataset import DcatDataset, DcatCollator
from dcat.data.modalities import Modality
from dcat.models.dcat.model import DcatModel

def run_smoke_test():
    print("=== 1. DATA LOADING ===")
    
    # Use production dataset
    dataset = DcatDataset(
        records_path="data/processed/records.parquet",
        tokenizer_name="distilbert-base-uncased",
        max_length=128,
        image_size=(224, 224)
    )
    
    # Find 1 of each modality deterministically
    text_idx, img_idx, mm_idx = -1, -1, -1
    
    for i in range(len(dataset)):
        rec = dataset.records[i]
        if text_idx == -1 and rec.modality.value == 'text':
            text_idx = i
        elif img_idx == -1 and rec.modality.value == 'image':
            img_idx = i
        elif mm_idx == -1 and rec.modality.value == 'multimodal':
            mm_idx = i
            
        if text_idx != -1 and img_idx != -1 and mm_idx != -1:
            break
            
    print(f"Indices found -> Text: {text_idx}, Image: {img_idx}, Multimodal: {mm_idx}")
    
    indices = [idx for idx in [text_idx, img_idx, mm_idx] if idx != -1]
    
    print(f"Samples loaded: {len(indices)}")
    for idx in indices:
        item = dataset[idx]
        print(f" - Modality: {item['modality']}, Label: {item['label']}, Email ID: {item['email_id']}")
        
        if item['modality'] == 'multimodal':
            # Check if pixel_values is all zeros (due to missing source_path)
            if torch.all(item['pixel_values'] == 0):
                print(f"WARNING: Multimodal pixel_values are all zeros! Source path logic in DcatDataset is likely failing to find images.")
                raise RuntimeError("Image preprocessing failed: returned all zeros because source_path is missing in parquet.")
                
    smoke_subset = Subset(dataset, indices)
    
    print("\n=== 2. COLLATOR / BATCHING ===")
    collator = DcatCollator()
    loader = DataLoader(smoke_subset, batch_size=3, shuffle=False, collate_fn=collator)
    
    batch = next(iter(loader))
    print(f"Batch Modalities: {batch['modality']}")
    print(f"Input IDs shape: {batch.get('input_ids').shape if 'input_ids' in batch else 'N/A'}")
    print(f"Attention Mask shape: {batch.get('attention_mask').shape if 'attention_mask' in batch else 'N/A'}")
    print(f"Pixel Values shape: {batch.get('pixel_values').shape if 'pixel_values' in batch else 'N/A'}")
    print(f"Labels shape: {batch.get('labels').shape if 'labels' in batch else 'N/A'}")
    
    print("\n=== 3. DCAT FORWARD PASS ===")
    device = torch.device('cpu')
    model = DcatModel(
        text_model_name="distilbert-base-uncased",
        vision_model_name="mobilevit_s",
        shared_dim=256,
        cross_attention_layers=1,
        cross_attention_heads=4,
        classifier_hidden=128
    ).to(device)
    
    model.train()
    batch_dict = {
        "input_ids": batch['input_ids'].to(device),
        "attention_mask": batch['attention_mask'].to(device),
        "pixel_values": batch['pixel_values'].to(device),
        "modality": batch['modality']
    }
    outputs = model(batch_dict)
    
    print(f"Logits shape: {outputs.shape}")
    assert not torch.isnan(outputs).any(), "NaNs in output"
    assert not torch.isinf(outputs).any(), "Infs in output"
    print("Forward pass successful.")
    
    print("\n=== 4. LOSS + BACKWARD ===")
    criterion = nn.BCEWithLogitsLoss()
    loss = criterion(outputs, batch['labels'].to(device))
    print(f"Loss: {loss.item():.4f}")
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    optimizer.zero_grad()
    loss.backward()
    
    has_grad = any(p.grad is not None for p in model.parameters())
    print(f"Gradients exist: {has_grad}")
    optimizer.step()
    print("Optimizer step successful.")
    
    print("\n=== 5. CHECKPOINT ===")
    with tempfile.NamedTemporaryFile(suffix=".pt", delete=False) as f:
        ckpt_path = f.name
        
    torch.save(model.state_dict(), ckpt_path)
    
    new_model = DcatModel(
        text_model_name="distilbert-base-uncased",
        vision_model_name="mobilevit_s",
        shared_dim=256,
        cross_attention_layers=1,
        cross_attention_heads=4,
        classifier_hidden=128
    ).to(device)
    
    new_model.load_state_dict(torch.load(ckpt_path, weights_only=True))
    new_model.eval()
    with torch.no_grad():
        new_outputs = new_model({
            "input_ids": batch['input_ids'].to(device),
            "attention_mask": batch['attention_mask'].to(device),
            "pixel_values": batch['pixel_values'].to(device),
            "modality": batch['modality']
        })
    print("Checkpoint reload and inference successful.")
    Path(ckpt_path).unlink()
    
    print("\n=== 6. VALIDATION PASS ===")
    from dcat.training.engine import DcatTrainer
    # Create dummy trainer for metrics
    trainer = DcatTrainer(
        model=new_model,
        train_loader=loader,
        val_loader=loader,
        optimizer=optimizer,
        device=device
    )
    metrics = trainer.evaluate()
    print("SMOKE TEST — NOT A RESEARCH RESULT")
    print(f"Validation Metrics: {metrics}")
    
    print("\n=== 8. GPU / MEMORY CHECK ===")
    print(f"Device: {device}")
    print(f"Batch size: {len(indices)}")
    
    print("\nSMOKE TEST COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    try:
        run_smoke_test()
    except Exception as e:
        print(f"\nCRITICAL FAILURE IN SMOKE TEST:")
        traceback.print_exc()
        sys.exit(1)
