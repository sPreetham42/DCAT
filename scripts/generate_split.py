import pandas as pd
import hashlib
from dcat.preprocessing.mime_parser import MimeParser
import networkx as nx
from collections import Counter
import json
import time
import os
from concurrent.futures import ProcessPoolExecutor

def get_hashes(row_data):
    idx, row = row_data
    raw_text = row['origin']
    if pd.isna(raw_text):
        return None
        
    parser = MimeParser()
    try:
        parsed = parser.parse_bytes(raw_text.encode('utf-8'), email_id=str(idx))
        
        text_hash = hashlib.md5(parsed.text.encode('utf-8')).hexdigest() if parsed.text else None
        
        # Only use the first image hash for grouping, or all of them?
        # Let's use all image hashes to be rigorously safe
        img_hashes = []
        for img in parsed.images:
            if img.data:
                img_hashes.append(hashlib.md5(img.data).hexdigest())
                
        is_text_only = bool(parsed.text) and not parsed.images
        is_image_only = not parsed.text and parsed.images
        is_multimodal = bool(parsed.text) and parsed.images
        
        return {
            'id': idx,
            'label': row['label'],
            'text_hash': text_hash,
            'img_hashes': img_hashes,
            'is_text_only': is_text_only,
            'is_image_only': is_image_only,
            'is_multimodal': is_multimodal
        }
    except Exception:
        return None

def process_chunk(chunk):
    return [res for res in [get_hashes(row_data) for row_data in chunk.iterrows()] if res is not None]

def generate_split():
    df = pd.read_csv("data/processed/email_origin.csv")
    
    # We already have the dataset stats, but we need hashes for the graph.
    # To save time, we will process the whole 75k emails again to build the graph.
    print(f"Parsing 75k emails to build hash graph...")
    start = time.time()
    
    chunk_size = 5000
    chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
    
    records = []
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        for res_list in executor.map(process_chunk, chunks):
            records.extend(res_list)
            
    print(f"Parsed {len(records)} emails in {time.time()-start:.2f}s")
    
    # Build graph
    # Nodes: emails (str(idx)), text_hashes (str), img_hashes (str)
    # Edges: email -> text_hash, email -> img_hash
    G = nx.Graph()
    for r in records:
        email_node = f"email_{r['id']}"
        G.add_node(email_node, type='email', record=r)
        
        if r['text_hash']:
            th = f"txt_{r['text_hash']}"
            G.add_node(th, type='hash')
            G.add_edge(email_node, th)
            
        for ih in r['img_hashes']:
            ih_node = f"img_{ih}"
            G.add_node(ih_node, type='hash')
            G.add_edge(email_node, ih_node)
            
    # Connected components
    components = list(nx.connected_components(G))
    
    # Extract email groups
    groups = []
    for comp in components:
        email_ids = [n for n in comp if G.nodes[n].get('type') == 'email']
        if email_ids:
            groups.append(email_ids)
            
    print(f"Formed {len(groups)} discrete leakage-safe groups.")
    
    # Sort groups by size descending to distribute evenly
    groups.sort(key=len, reverse=True)
    print(f"Largest group size: {len(groups[0])}")
    
    # Greedy stratified allocation into Train (80%), Val (10%), Test (10%)
    target_train = 0.8 * len(records)
    target_val = 0.1 * len(records)
    target_test = 0.1 * len(records)
    
    train_recs = []
    val_recs = []
    test_recs = []
    
    for g in groups:
        g_recs = [G.nodes[n]['record'] for n in g]
        # Assign to the split that is furthest from its target, prioritizing test and val
        
        def diff(split, target):
            return target - len(split)
            
        train_diff = diff(train_recs, target_train)
        val_diff = diff(val_recs, target_val)
        test_diff = diff(test_recs, target_test)
        
        # Determine which split needs data most
        # We look at relative deficit: (target - current) / target
        train_rel = train_diff / target_train if target_train > 0 else -1
        val_rel = val_diff / target_val if target_val > 0 else -1
        test_rel = test_diff / target_test if target_test > 0 else -1
        
        if test_rel >= val_rel and test_rel >= train_rel:
            test_recs.extend(g_recs)
        elif val_rel >= train_rel:
            val_recs.extend(g_recs)
        else:
            train_recs.extend(g_recs)
            
    def print_stats(name, split_recs):
        total = len(split_recs)
        spam = sum(1 for r in split_recs if r['label'] == 1)
        ham = sum(1 for r in split_recs if r['label'] == 0)
        
        text_only = sum(1 for r in split_recs if r['is_text_only'])
        img_only = sum(1 for r in split_recs if r['is_image_only'])
        mm = sum(1 for r in split_recs if r['is_multimodal'])
        mm_spam = sum(1 for r in split_recs if r['is_multimodal'] and r['label'] == 1)
        mm_ham = sum(1 for r in split_recs if r['is_multimodal'] and r['label'] == 0)
        
        print(f"\n--- {name} ---")
        print(f"Total: {total}")
        print(f"Spam: {spam} ({(spam/total)*100:.1f}%) | Ham: {ham} ({(ham/total)*100:.1f}%)")
        print(f"Text-Only: {text_only} ({(text_only/total)*100:.1f}%)")
        print(f"Image-Only: {img_only} ({(img_only/total)*100:.1f}%)")
        print(f"Multimodal: {mm} ({(mm/total)*100:.1f}%)")
        print(f"  MM-Spam: {mm_spam}")
        print(f"  MM-Ham: {mm_ham}")
        
    print_stats("TRAIN", train_recs)
    print_stats("VALIDATION", val_recs)
    print_stats("TEST", test_recs)

if __name__ == "__main__":
    generate_split()
