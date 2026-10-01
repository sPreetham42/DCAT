import pandas as pd
from collections import Counter
import sys
sys.path.insert(0, 'src')
from dcat.data.dataset import DcatDataset

def main():
    print("Loading original CSV...")
    df = pd.read_csv("data/processed/email_origin.csv")
    
    ds = DcatDataset('data/processed/records.parquet')
    
    # 7867 multimodal samples
    mm = [r for r in ds.records if r.modality.value == 'multimodal']
    print(f"Total valid multimodal records in parquet: {len(mm)}")
    
    # Check text and image
    text_only = [r for r in ds.records if r.modality.value == 'text']
    img_only = [r for r in ds.records if r.modality.value == 'image']
    empty = [r for r in ds.records if r.modality.value == 'empty']
    
    print(f"Text only: {len(text_only)}")
    print(f"Image only: {len(img_only)}")
    print(f"Empty: {len(empty)}")
    print(f"Total records in parquet: {len(ds.records)}")
    
if __name__ == "__main__":
    main()
