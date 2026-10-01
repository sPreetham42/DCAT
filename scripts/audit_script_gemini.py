import os
import torch
import json
import pandas as pd
from collections import Counter
import hashlib

def print_section(title):
    print(f"\n{'='*60}\n{title}\n{'='*60}")

def audit_dataset():
    print_section("DATASET AUDIT")
    if os.path.exists("data/processed/records.parquet"):
        df = pd.read_parquet("data/processed/records.parquet")
        print(f"records.parquet Total rows: {len(df)}")
        
        # Determine usable
        # In DcatDataset, Modality.EMPTY are filtered out.
        if 'has_text' in df.columns and 'has_meaningful_image' in df.columns:
            empty = df[(~df['has_text']) & (~df['has_meaningful_image'])]
            usable = df[df['has_text'] | df['has_meaningful_image']]
            print(f"Empty records: {len(empty)}")
            print(f"Usable records: {len(usable)}")
            
            text_only = usable[(usable['has_text']) & (~usable['has_meaningful_image'])]
            image_only = usable[(~usable['has_text']) & (usable['has_meaningful_image'])]
            multimodal = usable[(usable['has_text']) & (usable['has_meaningful_image'])]
            print(f"Text-only: {len(text_only)}")
            print(f"Image-only: {len(image_only)}")
            print(f"Multimodal: {len(multimodal)}")
            
            if 'label' in df.columns:
                spam = usable[usable['label'] == 1]
                ham = usable[usable['label'] == 0]
                print(f"Spam: {len(spam)}, Ham: {len(ham)}")
                
            if 'split' in usable.columns:
                mm_splits = multimodal['split'].value_counts()
                print(f"Multimodal per split: {mm_splits.to_dict()}")
                
def audit_checkpoints():
    print_section("CHECKPOINTS AUDIT")
    if not os.path.exists("checkpoints"):
        print("No checkpoints directory.")
        return
        
    ckpts = [f for f in os.listdir("checkpoints") if f.endswith(".pt")]
    for c in sorted(ckpts):
        path = os.path.join("checkpoints", c)
        sz = os.path.getsize(path)
        mtime = os.path.getmtime(path)
        print(f"\nCheckpoint: {c}")
        print(f"Size: {sz / (1024*1024):.2f} MB")
        
        # Load state dict lightly
        try:
            sd = torch.load(path, map_location='cpu', weights_only=True)
            keys = list(sd.keys())
            print(f"Total keys: {len(keys)}")
            
            # Detect architecture
            has_text = any("text_model" in k for k in keys)
            has_vision = any("vision_model" in k for k in keys)
            has_ca = any("cross_attention" in k for k in keys)
            has_router = any("router" in k for k in keys) or any("text_only_classifier" in k for k in keys)
            
            ca_layers = set()
            for k in keys:
                if "cross_attention.layers." in k:
                    layer_num = k.split("cross_attention.layers.")[1].split(".")[0]
                    ca_layers.add(layer_num)
                    
            print(f"Architecture -> Text: {has_text}, Vision: {has_vision}, CA: {has_ca} (Layers: {len(ca_layers)}), Router/EarlyExit: {has_router}")
        except Exception as e:
            print(f"Failed to load: {e}")

def audit_results():
    print_section("RESULTS AUDIT")
    res_path = "experiments/final_results.json"
    if os.path.exists(res_path):
        with open(res_path, 'r') as f:
            data = json.load(f)
        print(f"final_results.json keys: {list(data.keys())}")
        for k, v in data.items():
            if 'mean_test_metrics' in v:
                mean = v['mean_test_metrics']
                print(f"  {k} -> Macro-F1: {mean.get('macro_f1')}, MM-F1: {mean.get('macro_f1_multimodal')}, Total Samples Evaluated: {mean.get('total_samples', 'Not found in mean')}")
                
            if 'seeds' in v:
                first_seed = list(v['seeds'].keys())[0]
                seed_data = v['seeds'][first_seed]
                if 'test_metrics' in seed_data:
                    t = seed_data['test_metrics']
                    samples = len(t.get('_raw_labels', [])) if '_raw_labels' in t else 'Unknown'
                    print(f"  {k} Seed {first_seed} -> Samples in _raw_labels: {samples}")

if __name__ == "__main__":
    audit_dataset()
    audit_checkpoints()
    audit_results()
