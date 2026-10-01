import os
import json
import time
import hashlib
import pandas as pd
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from collections import Counter
import random

from dcat.preprocessing.mime_parser import MimeParser
from dcat.preprocessing.router import ModalityRouter
from dcat.data.parquet import ParquetDatasetWriter

class UnionFind:
    def __init__(self):
        self.parent = {}
        
    def find(self, i):
        if self.parent.setdefault(i, i) == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
        
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j

def _parse_row(args):
    row_num, raw_text, label = args
    parser = MimeParser()
    try:
        parsed = parser.parse_bytes(raw_text.encode('utf-8'), email_id=str(row_num))
        
        clean_text = parsed.text.strip() if parsed.text else None
        text_hash = hashlib.md5(clean_text.encode('utf-8')).hexdigest() if clean_text else None
        
        # Use raw payload bytes for image hashes
        img_hashes = [hashlib.md5(img.data).hexdigest() for img in parsed.images if img.data]
        
        return {
            'row_num': str(row_num),
            'label': label,
            'parsed': parsed,
            'text_hash': text_hash,
            'img_hashes': img_hashes
        }
    except Exception:
        return None

def build_dataset():
    raw_csv = Path("data/processed/email_origin.csv")
    processed_dir = Path("data/processed")
    manifest_dir = Path("data/manifests")
    
    processed_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    
    if not raw_csv.exists():
        print(f"Dataset not found at {raw_csv}")
        return
        
    print(f"Loading {raw_csv}...")
    df = pd.read_csv(raw_csv)
    
    print("Parsing 75k emails (Pass 1)...")
    start = time.time()
    
    args_list = []
    for row_num, (idx, row) in enumerate(df.iterrows()):
        raw_text = row['origin']
        if pd.isna(raw_text):
            continue
        args_list.append((row_num, raw_text, row['label']))
        
    parsed_results = []
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        for res in executor.map(_parse_row, args_list, chunksize=1000):
            if res is not None:
                parsed_results.append(res)
                
    print(f"Parsed {len(parsed_results)} emails in {time.time()-start:.2f}s")
    
    # ---------------------------------------------------------
    # 1. Deterministic Union-Find Transitive Grouping
    # ---------------------------------------------------------
    print("Building Deterministic Union-Find graph...")
    uf = UnionFind()
    
    text_hash_freq = Counter()
    img_hash_freq = Counter()
    
    for r in parsed_results:
        email_node = f"email_{r['row_num']}"
        
        if r['text_hash']:
            th = f"txt_{r['text_hash']}"
            text_hash_freq[r['text_hash']] += 1
            uf.union(email_node, th)
            
        for ih in r['img_hashes']:
            ih_node = f"img_{ih}"
            img_hash_freq[ih] += 1
            uf.union(email_node, ih_node)
            
    # Resolve groups
    groups_dict = {}
    for r in parsed_results:
        email_node = f"email_{r['row_num']}"
        root = uf.find(email_node)
        groups_dict.setdefault(root, []).append(r['row_num'])
        
    groups = list(groups_dict.values())
    
    # Sort groups deterministically: by size descending, then by minimum row_num ascending
    groups.sort(key=lambda g: (-len(g), int(min(g, key=int))))
    
    # High-Frequency Hash Analysis
    print("\n=== High-Frequency Hash Analysis ===")
    print(f"Number of leakage groups: {len(groups)}")
    group_sizes = [len(g) for g in groups]
    print(f"Largest group size: {max(group_sizes)}")
    print(f"Mean group size: {sum(group_sizes) / len(group_sizes):.2f}")
    
    sorted_sizes = sorted(group_sizes)
    median = sorted_sizes[len(sorted_sizes)//2] if len(sorted_sizes) % 2 != 0 else (sorted_sizes[len(sorted_sizes)//2 - 1] + sorted_sizes[len(sorted_sizes)//2]) / 2
    print(f"Median group size: {median}")
    print(f"Percentage in top 10 largest groups: {(sum(group_sizes[:10]) / sum(group_sizes)) * 100:.2f}%")
    
    print("\nTop 20 text hashes:")
    for h, c in text_hash_freq.most_common(20):
        print(f"  {h}: {c}")
        
    print("\nTop 20 image hashes:")
    for h, c in img_hash_freq.most_common(20):
        print(f"  {h}: {c}")
    print("====================================\n")
    
    # ---------------------------------------------------------
    # 2. Greedy Stratified Split
    # ---------------------------------------------------------
    target_train = 0.8 * len(parsed_results)
    target_val = 0.1 * len(parsed_results)
    target_test = 0.1 * len(parsed_results)
    
    split_assignments = {}
    train_count = val_count = test_count = 0
    
    # Seed for shuffling groups of IDENTICAL size if any exist (though sort key handles mostly)
    random.seed(42)
    
    for g in groups:
        train_rel = (target_train - train_count) / target_train if target_train > 0 else -1
        val_rel = (target_val - val_count) / target_val if target_val > 0 else -1
        test_rel = (target_test - test_count) / target_test if target_test > 0 else -1
        
        if test_rel >= val_rel and test_rel >= train_rel:
            assignment = 'test'
            test_count += len(g)
        elif val_rel >= train_rel:
            assignment = 'val'
            val_count += len(g)
        else:
            assignment = 'train'
            train_count += len(g)
            
        # Group id is just the string of the root
        root_id = uf.find(f"email_{g[0]}")
        for row_num in g:
            split_assignments[row_num] = (assignment, root_id)
            
    print(f"Split sizes -> Train: {train_count}, Val: {val_count}, Test: {test_count}")
    
    # ---------------------------------------------------------
    # 3. Create Manifest and Route
    # ---------------------------------------------------------
    print("Saving manifest, dumping images, and routing dataset...")
    router = ModalityRouter()
    final_records = []
    
    manifest_rows = []
    
    image_dir = processed_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    
    from dataclasses import replace
    
    for r in parsed_results:
        row_num = r['row_num']
        split, group_id = split_assignments[row_num]
        
        manifest_rows.append({
            "sample_id": row_num,
            "group_id": group_id,
            "split": split
        })
        
        routed = router.route(r['parsed'], label=r['label'], split=split)
        
        new_images = []
        for i, img_rec in enumerate(routed.record.images):
            if img_rec.selected:
                raw_img = r['parsed'].images[i]
                img_path = image_dir / f"{raw_img.image_id}.jpg"
                with open(img_path, "wb") as f:
                    f.write(raw_img.data)
                img_rec = replace(img_rec, source_path=str(img_path.resolve()))
            new_images.append(img_rec)
            
        final_record = replace(routed.record, images=tuple(new_images))
        final_records.append(final_record)
        
    manifest_df = pd.DataFrame(manifest_rows)
    manifest_path = manifest_dir / "leakage_groups.csv"
    manifest_df.to_csv(manifest_path, index=False)
    print(f"Saved reproducible group manifest to {manifest_path}")
        
    output_path = processed_dir / "records.parquet"
    ParquetDatasetWriter.save_records(final_records, output_path)
    print(f"Successfully wrote {len(final_records)} records to {output_path}")
    
    # Compute and print split statistics
    def print_split_stats(name, target_split):
        recs = [r for r in final_records if r.split == target_split]
        total = len(recs)
        if total == 0: return
        spam = sum(1 for r in recs if r.label == 1)
        ham = sum(1 for r in recs if r.label == 0)
        
        text_only = sum(1 for r in recs if r.modality.value == 'text')
        img_only = sum(1 for r in recs if r.modality.value == 'image')
        mm = sum(1 for r in recs if r.modality.value == 'multimodal')
        
        print(f"| {name} | {total} | {spam} | {ham} | {text_only} | {img_only} | {mm} |")
        
    print("\n| Split | Total | Spam | Ham | Text-only | Image-only | Multimodal |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    print_split_stats("Train", "train")
    print_split_stats("Val", "val")
    print_split_stats("Test", "test")
    
if __name__ == "__main__":
    build_dataset()
