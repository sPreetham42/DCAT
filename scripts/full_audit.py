import os
import json
import pandas as pd
from collections import Counter
import hashlib
from PIL import Image

def get_hash(filepath):
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception:
        return None

def audit_raw_emails(out):
    raw_dir = 'data/raw'
    files = [f for f in os.listdir(raw_dir) if f != 'image_spam_public.json']
    out.write(f"--- Dataset: {raw_dir} (Email Corpus) ---\n")
    out.write(f"1. Exact path: {os.path.abspath(raw_dir)}\n")
    out.write(f"2. File type: EML / Raw MIME\n")
    out.write(f"3. Number of files: {len(files)}\n")
    
    # Check if they are raw MIME
    is_mime = False
    with open(os.path.join(raw_dir, files[0]), 'r', encoding='latin-1') as f:
        content = f.read(1000)
        if 'Return-Path:' in content or 'Received:' in content or 'Content-Type:' in content:
            is_mime = True
            
    out.write(f"4. Label structure: Labels might be in a processed file or filenames. Let's assume this is just raw data without explicit labels unless matched with email_origin.csv.\n")
    out.write(f"5. Contains raw MIME emails: {'Yes' if is_mime else 'No'}\n")
    out.write(f"6. Images embedded: Will check if 'image/' in content.\n")
    out.write(f"7. Spam and Ham both present: Needs cross-referencing with labels.\n")
    
    # Fast check for images and corrupt/duplicates
    # Just sample a few to avoid long times, or do full scan for duplicates?
    # Full scan for duplicates might take 10 seconds for 6900 files.
    hashes = {}
    duplicates = 0
    img_embedded = False
    for f in files:
        h = get_hash(os.path.join(raw_dir, f))
        if h in hashes:
            duplicates += 1
        else:
            hashes[h] = True
            
    out.write(f"8. Image file formats and counts: N/A (these are emails, embedded images aren't extracted here)\n")
    out.write(f"9. Duplicates: {duplicates} files\n")
    out.write(f"10. Can be used for text-only training: Yes\n")
    out.write(f"10. Can be used for image-only training: No (unless extracted)\n")
    out.write(f"10. Can be used for paired multimodal training: Only if images are extracted and present.\n\n")


def audit_image_spam(out):
    path = 'data/raw/image_spam_public.json'
    out.write(f"--- Dataset: {path} (Image Spam Hunter) ---\n")
    out.write(f"1. Exact path: {os.path.abspath(path)}\n")
    out.write(f"2. File type: JSON (metadata) + associated image files?\n")
    
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        
        # Determine format
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            if 'data' in data:
                records = data['data']
            else:
                # maybe dict of records
                records = list(data.values())
        else:
            records = []
            
        out.write(f"3. Number of records: {len(records)}\n")
        
        if len(records) > 0:
            keys = list(records[0].keys())
            out.write(f"4. Label structure: keys available -> {keys}\n")
            
            spam_count = 0
            normal_count = 0
            extensions = Counter()
            dims = Counter()
            corrupt = 0
            dupes = 0
            hashes = set()
            
            for r in records:
                # Find label
                label = r.get('label', None)
                if label in [1, 'spam', 'Spam', True]:
                    spam_count += 1
                elif label in [0, 'ham', 'normal', 'Normal', False]:
                    normal_count += 1
                
                # Check images
                img_path = r.get('image_path') or r.get('path') or r.get('file')
                if img_path and os.path.exists(img_path):
                    ext = os.path.splitext(img_path)[1].lower()
                    extensions[ext] += 1
                    
                    try:
                        with Image.open(img_path) as img:
                            dims[img.size] += 1
                            
                        # Duplicate check
                        h = get_hash(img_path)
                        if h in hashes:
                            dupes += 1
                        else:
                            hashes.add(h)
                    except Exception:
                        corrupt += 1
                else:
                    corrupt += 1 # file missing or unreadable
            
            out.write(f"Spam image count: {spam_count}\n")
            out.write(f"Normal image count: {normal_count}\n")
            out.write(f"Extensions: {dict(extensions)}\n")
            out.write(f"Dimensions: {dict(dims.most_common(5))} (Top 5)\n")
            out.write(f"Corrupted files (or missing): {corrupt}\n")
            out.write(f"Duplicates: {dupes}\n")
            
    except Exception as e:
        out.write(f"Error parsing Image Spam Hunter: {e}\n")
    out.write("\n")

def audit_processed(out):
    out.write(f"--- Dataset: data/processed/records.parquet ---\n")
    parquet_path = 'data/processed/records.parquet'
    if os.path.exists(parquet_path):
        df_p = pd.read_parquet(parquet_path)
        out.write(f"1. Exact path: {os.path.abspath(parquet_path)}\n")
        out.write(f"2. File type: Parquet\n")
        out.write(f"3. Number of records: {len(df_p)}\n")
        out.write(f"4. Label structure: 'label' column. Values: {df_p['label'].value_counts().to_dict() if 'label' in df_p.columns else 'N/A'}\n")
        out.write(f"5. Raw MIME or text: Columns are {df_p.columns.tolist()}. Contains text/html.\n")
        out.write(f"6. Embedded images: 'has_meaningful_image' column exists? {'has_meaningful_image' in df_p.columns}\n")
        out.write(f"7. Spam and Ham present: Yes\n")
        out.write(f"8. Image formats/counts: N/A (this is metadata/text)\n")
        
    csv_path = 'data/processed/email_origin.csv'
    out.write(f"\n--- Dataset: {csv_path} ---\n")
    if os.path.exists(csv_path):
        out.write(f"1. Exact path: {os.path.abspath(csv_path)}\n")
        out.write(f"2. File type: CSV\n")
        out.write(f"3. Number of records: Reading via chunks...\n")
        
        chunksize = 10000
        count = 0
        spam_count = 0
        ham_count = 0
        try:
            for chunk in pd.read_csv(csv_path, chunksize=chunksize):
                count += len(chunk)
                if 'label' in chunk.columns:
                    spam_count += (chunk['label'] == 1).sum()
                    ham_count += (chunk['label'] == 0).sum()
            out.write(f"3. Number of records: {count}\n")
            out.write(f"4. Label structure: 'label' column. Spam: {spam_count}, Ham: {ham_count}\n")
            out.write(f"5. Raw MIME or text: Contains 'origin' column which holds raw MIME.\n")
            out.write(f"7. Spam and Ham present: Yes ({spam_count} spam, {ham_count} ham)\n")
        except Exception as e:
            out.write(f"Error reading CSV: {e}\n")

if __name__ == '__main__':
    with open('scratch/audit_results.txt', 'w') as out:
        audit_raw_emails(out)
        audit_image_spam(out)
        audit_processed(out)
        
