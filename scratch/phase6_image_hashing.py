import os
import json
import pandas as pd
import hashlib

def compute_hashes():
    print("Loading data...")
    df = pd.read_parquet('data/processed/records.parquet')
    
    # We only need to process images that actually exist and are marked as selected/meaningful
    img_df = df[df['has_meaningful_image']].copy()
    print(f"Total image-bearing records: {len(img_df)}")
    
    exact_hashes = {}
    perceptual_hashes = {}
    
    failed_decodes = 0
    processed = 0
    
    for idx, row in img_df.iterrows():
        try:
            images = json.loads(row['images_json'])
            for img in images:
                if img.get('selected', False):
                    path = img.get('source_path')
                    if path and os.path.exists(path):
                        # Exact hash (MD5)
                        with open(path, 'rb') as f:
                            h_exact = hashlib.md5(f.read()).hexdigest()
                        
                        exact_hashes[idx] = h_exact
        except Exception:
            pass
            
    print(f"Processed exact hashes for {processed} records. Failed decodes: {failed_decodes}")
    
    # Save the mappings for the next step (graph building)
    hash_df = pd.DataFrame({
        'email_id': list(exact_hashes.keys()),
        'exact_hash': list(exact_hashes.values())
    })
    hash_df.to_csv('scratch/image_hashes.csv', index=False)
    print("Saved image hashes to scratch/image_hashes.csv")

if __name__ == "__main__":
    compute_hashes()
