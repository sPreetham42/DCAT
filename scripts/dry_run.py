import sys
import torch
from pathlib import Path
from torch.utils.data import DataLoader

from dcat.data.dataset import DcatDataset, DcatCollator
from dcat.models.dcat.model import DcatModel
from dcat.training.engine import DcatTrainer

def dry_run():
    print("Initializing dummy dry-run validation...")
    
    parquet_path = Path("data/processed/records.parquet")
    if not parquet_path.exists():
        print("Dataset missing, please build the dummy dataset first.")
        sys.exit(1)
        
    dataset = DcatDataset(parquet_path)
    # Split into mock train/val
    train_size = int(len(dataset) * 0.8)
    val_size = len(dataset) - train_size
    train_ds, val_ds = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    collator = DcatCollator()
    train_loader = DataLoader(train_ds, batch_size=4, collate_fn=collator, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=4, collate_fn=collator)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    print("Instantiating model...")
    # Instantiate with tiny dimensions for fast dry run
    model = DcatModel(
        text_model_name="distilbert-base-uncased",
        vision_model_name="mobilevit_s",
        freeze_encoders=True,
        shared_dim=256,
        cross_attention_layers=1,
        cross_attention_heads=2
    )
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    
    trainer = DcatTrainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        optimizer=optimizer,
        device=device,
        amp=False # disable amp for simplicity in dry run on cpu
    )
    
    print("Running 1 dummy epoch...")
    loss = trainer.train_epoch()
    print(f"Training Loss: {loss:.4f}")
    
    print("Running evaluation...")
    metrics = trainer.evaluate()
    print("Validation Metrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v:.4f}")
        
    print("Dry-run complete! All components connect successfully.")

if __name__ == "__main__":
    dry_run()
