import json
import pandas as pd
from pathlib import Path
from dcat.preprocessing.mime_parser import MimeParser
from collections import Counter
import os

def inventory_email_origin():
    print("=== DATASET 1: email_origin.csv ===")
    df = pd.read_csv("data/processed/email_origin.csv")
    print(f"Total rows: {len(df)}")
    print(f"Spam: {len(df[df['label'] == 1])}")
    print(f"Ham: {len(df[df['label'] == 0])}")
    
    parser = MimeParser()
    has_text = 0
    has_html = 0
    has_image = 0
    has_inline_image = 0
    has_attached_image = 0
    naturally_paired = 0
    
    # Process only 5,000 as a representative sample so we don't block for 10 minutes
    sample_df = df.sample(min(5000, len(df)), random_state=42)
    
    for idx, row in sample_df.iterrows():
        raw_text = row['origin']
        if pd.isna(raw_text):
            continue
            
        try:
            parsed = parser.parse_bytes(raw_text.encode('utf-8'), email_id=str(idx))
            if parsed.text: has_text += 1
            if parsed.html: has_html += 1
            
            inline_images = [img for img in parsed.images if (img.disposition and img.disposition.value == 'inline') or img.cid]
            attached_images = [img for img in parsed.images if img.disposition and img.disposition.value == 'attachment']
            
            if len(parsed.images) > 0: has_image += 1
            if len(inline_images) > 0: has_inline_image += 1
            if len(attached_images) > 0: has_attached_image += 1
            
            if parsed.text and len(parsed.images) > 0:
                naturally_paired += 1
                
        except Exception:
            pass
            
    # Extrapolate to full size
    scale = len(df) / len(sample_df)
    print(f"--- ESTIMATED FROM {len(sample_df)} SAMPLE ---")
    print(f"Has Text: ~{int(has_text * scale)}")
    print(f"Has HTML: ~{int(has_html * scale)}")
    print(f"Has Images: ~{int(has_image * scale)}")
    print(f"Has Inline Images: ~{int(has_inline_image * scale)}")
    print(f"Naturally Paired (Text + Image): ~{int(naturally_paired * scale)}")

def inventory_raw_emls():
    print("\n=== DATASET 2: RAW EMLs (SpamAssassin subset) ===")
    raw_dir = Path("data/raw")
    emls = [f for f in raw_dir.iterdir() if f.is_file() and not f.name.endswith('.json') and not f.name.endswith('.eml')]
    print(f"Total raw files (excluding json/dummy .eml): {len(emls)}")
    
def inventory_json():
    print("\n=== DATASET 3: image_spam_public.json ===")
    path = Path("data/raw/image_spam_public.json")
    if path.exists():
        size_gb = path.stat().st_size / (1024**3)
        print(f"Size: {size_gb:.2f} GB")
        print("Note: File is 16GB, likely contains heavy base64 encoded images. Skipping full parse.")
        
if __name__ == "__main__":
    inventory_raw_emls()
    inventory_json()
    inventory_email_origin()
