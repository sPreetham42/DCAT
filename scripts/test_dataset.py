import sys
from pathlib import Path
from torch.utils.data import DataLoader
from dcat.data.dataset import DcatDataset, DcatCollator

def test_dataset():
    parquet_path = Path("data/processed/records.parquet")
    if not parquet_path.exists():
        print(f"Dataset not found at {parquet_path}")
        sys.exit(1)
        
    print("Loading dataset...")
    dataset = DcatDataset(parquet_path)
    print(f"Dataset size: {len(dataset)}")
    
    collator = DcatCollator()
    dataloader = DataLoader(dataset, batch_size=4, collate_fn=collator)
    
    batch = next(iter(dataloader))
    print("\nBatch shapes:")
    for k, v in batch.items():
        if hasattr(v, 'shape'):
            print(f"{k}: {v.shape} (dtype: {v.dtype})")
        else:
            print(f"{k}: {len(v)} items")

if __name__ == "__main__":
    test_dataset()
