import json
import pandas as pd
from pathlib import Path
from dcat.preprocessing.mime_parser import MimeParser
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import hashlib
import time

def process_chunk(chunk_df):
    parser = MimeParser()
    results = []
    
    for idx, row in chunk_df.iterrows():
        raw_text = row['origin']
        if pd.isna(raw_text):
            continue
            
        try:
            parsed = parser.parse_bytes(raw_text.encode('utf-8'), email_id=str(idx))
            
            inline_images = [img for img in parsed.images if (img.disposition and img.disposition.value == 'inline') or img.cid]
            attached_images = [img for img in parsed.images if img.disposition and img.disposition.value == 'attachment']
            external_images = [] # If HTML contains <img> but no embedded base64, parser handles this? MimeParser extracts attachments/inline.
            
            # Simple content hashing for duplicates
            text_hash = hashlib.md5(parsed.text.encode('utf-8')).hexdigest() if parsed.text else None
            html_hash = hashlib.md5(parsed.html.encode('utf-8')).hexdigest() if parsed.html else None
            
            # Image hashes (first image if multiple for simplicity of rough duplicate check)
            img_hash = hashlib.md5(parsed.images[0].content).hexdigest() if parsed.images else None
            
            res = {
                'id': idx,
                'label': row['label'],
                'has_text': bool(parsed.text),
                'has_html': bool(parsed.html),
                'has_images': len(parsed.images) > 0,
                'has_inline': len(inline_images) > 0,
                'has_attachments': len(attached_images) > 0,
                'text_hash': text_hash,
                'html_hash': html_hash,
                'img_hash': img_hash
            }
            results.append(res)
                
        except Exception:
            pass
    return results

def exact_inventory():
    print("=== EXACT INVENTORY ===")
    df = pd.read_csv("data/processed/email_origin.csv")
    print(f"Total rows: {len(df)}")
    print(f"Spam: {len(df[df['label'] == 1])}")
    print(f"Ham: {len(df[df['label'] == 0])}")
    
    # Process in chunks
    chunk_size = 5000
    chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
    
    all_results = []
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        for res_list in executor.map(process_chunk, chunks):
            all_results.extend(res_list)
            
    print(f"Finished parsing in {time.time() - start_time:.2f} seconds.")
    
    # Analyze
    stats = {
        'total_parsed': len(all_results),
        'usable_text': 0,
        'usable_html': 0,
        'usable_images': 0,
        'inline_images': 0,
        'image_attachments': 0,
        
        'spam': {'text_only': 0, 'image_only': 0, 'multimodal': 0},
        'ham': {'text_only': 0, 'image_only': 0, 'multimodal': 0},
    }
    
    text_hashes = Counter()
    img_hashes = Counter()
    
    for r in all_results:
        stats['usable_text'] += int(r['has_text'])
        stats['usable_html'] += int(r['has_html'])
        stats['usable_images'] += int(r['has_images'])
        stats['inline_images'] += int(r['has_inline'])
        stats['image_attachments'] += int(r['has_attachments'])
        
        # Classification
        # Text only: has text, no images
        # Image only: no text, has images
        # Multimodal: has text, has images
        is_text_only = r['has_text'] and not r['has_images']
        is_image_only = not r['has_text'] and r['has_images']
        is_multimodal = r['has_text'] and r['has_images']
        
        label_key = 'spam' if r['label'] == 1 else 'ham'
        
        stats[label_key]['text_only'] += int(is_text_only)
        stats[label_key]['image_only'] += int(is_image_only)
        stats[label_key]['multimodal'] += int(is_multimodal)
        
        if r['text_hash']: text_hashes[r['text_hash']] += 1
        if r['img_hash']: img_hashes[r['img_hash']] += 1
        
    print(json.dumps(stats, indent=2))
    
    # Duplicates
    print(f"\nUnique Text Hashes: {len(text_hashes)}")
    print(f"Top 5 Repeated Texts:")
    for h, c in text_hashes.most_common(5):
        if c > 1: print(f"Hash {h}: {c} times")
        
    print(f"\nUnique Image Hashes: {len(img_hashes)}")
    print(f"Top 5 Repeated Images:")
    for h, c in img_hashes.most_common(5):
        if c > 1: print(f"Hash {h}: {c} times")

if __name__ == "__main__":
    import os
    exact_inventory()
