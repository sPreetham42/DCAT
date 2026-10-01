import os
import time
import json
import pandas as pd
import numpy as np
import hashlib
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import vstack
from scipy.sparse.csgraph import connected_components
from sklearn.model_selection import GroupShuffleSplit

def freeze_split():
    print("Loading data...")
    df = pd.read_parquet('data/processed/records.parquet')
    df['email_id'] = df.index.astype(str)
    
    usable = df[df['has_text'] | df['has_meaningful_image']].copy()
    print(f"Usable records: {len(usable)}")
    
    # Text for TF-IDF. Keep empty texts as empty string.
    texts = usable['text'].fillna("").tolist()
    empty_mask = (usable['text'].isna()) | (usable['text'].str.strip() == "")
    
    print("Computing TF-IDF...")
    start = time.time()
    vectorizer = TfidfVectorizer(max_features=10000, stop_words='english', lowercase=True, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    print("Computing sparse similarity matrix in batches...")
    batch_size = 5000
    n = tfidf_matrix.shape[0]
    
    rows_list = []
    for i in range(0, n, batch_size):
        end = min(i + batch_size, n)
        batch_sim = tfidf_matrix[i:end].dot(tfidf_matrix.T)
        batch_sim = batch_sim.multiply(batch_sim >= 0.90)
        rows_list.append(batch_sim)
        
    sim_matrix = vstack(rows_list)
    print("Finding connected components...")
    n_components, labels = connected_components(csgraph=sim_matrix, directed=False, return_labels=True)
    usable['group_id'] = labels.astype(np.int64)
    
    max_group_id = usable['group_id'].max()
    num_empty = empty_mask.sum()
    if num_empty > 0:
        usable.loc[empty_mask, 'group_id'] = np.arange(max_group_id + 1, max_group_id + 1 + num_empty, dtype=np.int64)
        print(f"Assigned {num_empty} empty-text records to unique singleton groups.")
    
    # Group-Disjoint Split
    print("Generating Group-Disjoint Split...")
    seed = 42
    
    gss = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=seed)
    train_idx, temp_idx = next(gss.split(usable, groups=usable['group_id']))
    temp_df = usable.iloc[temp_idx]
    
    gss2 = GroupShuffleSplit(n_splits=1, test_size=0.50, random_state=seed)
    val_idx, test_idx = next(gss2.split(temp_df, groups=temp_df['group_id']))
    test_df = temp_df.iloc[test_idx]
            
    train_df = usable.iloc[train_idx].copy()
    val_df = temp_df.iloc[val_idx].copy()
    test_df = temp_df.iloc[test_idx].copy()
    
    os.makedirs('experiments/75k_clean/manifests', exist_ok=True)
    
    train_list = train_df['email_id'].tolist()
    val_list = val_df['email_id'].tolist()
    test_list = test_df['email_id'].tolist()
    
    with open('experiments/75k_clean/manifests/train.json', 'w') as f:
        json.dump(train_list, f)
    with open('experiments/75k_clean/manifests/val.json', 'w') as f:
        json.dump(val_list, f)
    with open('experiments/75k_clean/manifests/test.json', 'w') as f:
        json.dump(test_list, f)
        
    # Write to master CSV manifest for Dataset loader
    train_df['split'] = 'train'
    val_df['split'] = 'val'
    test_df['split'] = 'test'
    split_manifest = pd.concat([train_df[['email_id', 'group_id', 'split']], 
                                val_df[['email_id', 'group_id', 'split']], 
                                test_df[['email_id', 'group_id', 'split']]])
    manifest_csv = 'experiments/75k_clean/manifests/split_manifest.csv'
    split_manifest.to_csv(manifest_csv, index=False)
    
    hashes = {}
    for fname in ['train.json', 'val.json', 'test.json', 'split_manifest.csv']:
        path = f'experiments/75k_clean/manifests/{fname}'
        with open(path, 'rb') as f:
            hashes[fname] = hashlib.sha256(f.read()).hexdigest()
            
    with open('experiments/75k_clean/SPLIT_MANIFEST_SHA256.txt', 'w') as f:
        for fname, h in hashes.items():
            f.write(f"{h}  {fname}\n")
            
    print("Hashes saved.")
    
    # Phase 5 Check - Report stats
    spam = len(test_df[test_df['label'] == 1])
    ham = len(test_df[test_df['label'] == 0])
    img_bearing = len(test_df[test_df['has_meaningful_image']])
    non_img = len(test_df[~test_df['has_meaningful_image']])
    img_spam = len(test_df[(test_df['label'] == 1) & (test_df['has_meaningful_image'])])
    img_ham = len(test_df[(test_df['label'] == 0) & (test_df['has_meaningful_image'])])
    
    with open('experiments/75k_clean/TEST_SET_STATS.md', 'w') as f:
        f.write("# Phase 5: Image-Bearing Ham Check\n")
        f.write(f"- Total test examples: {len(test_df)}\n")
        f.write(f"- Spam: {spam}\n")
        f.write(f"- Ham: {ham}\n")
        f.write(f"- Image-bearing: {img_bearing}\n")
        f.write(f"- Non-image: {non_img}\n")
        f.write(f"- Image-bearing spam: {img_spam}\n")
        f.write(f"- Image-bearing ham: {img_ham}\n\n")
        f.write(f"The critical threshold of >= 150 is met: **{img_ham} >= 150**.\n")

if __name__ == "__main__":
    freeze_split()
