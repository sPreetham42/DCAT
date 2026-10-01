import os
import tarfile
import urllib.request
import pandas as pd
from pathlib import Path
from dcat.preprocessing.mime_parser import MimeParser
from dcat.preprocessing.router import ModalityRouter, RouterConfig
from collections import defaultdict
import hashlib

# 1. ACQUIRE THE DATASET
BASE_URL = "https://spamassassin.apache.org/old/publiccorpus/"
ARCHIVES = [
    ("20030228_easy_ham.tar.bz2", 0),      # ham
    ("20030228_hard_ham.tar.bz2", 0),      # ham
    ("20030228_easy_ham_2.tar.bz2", 0),    # ham
    ("20030228_spam.tar.bz2", 1),          # spam
    ("20050311_spam_2.tar.bz2", 1),        # spam
]

DATA_DIR = Path("data/spamassassin")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_and_extract():
    records = []
    total_size = 0
    for archive_name, label in ARCHIVES:
        archive_path = DATA_DIR / archive_name
        url = BASE_URL + archive_name
        
        if not archive_path.exists():
            print(f"Downloading {url}...")
            urllib.request.urlretrieve(url, archive_path)
            
        size = archive_path.stat().st_size
        total_size += size
        
        extract_dir = DATA_DIR / archive_name.replace(".tar.bz2", "")
        if not extract_dir.exists():
            print(f"Extracting {archive_path}...")
            with tarfile.open(archive_path, "r:bz2") as tar:
                tar.extractall(path=DATA_DIR)
                
        for root, dirs, files in os.walk(DATA_DIR):
            if root == str(DATA_DIR): continue
            dir_name = Path(root).name
            if dir_name in archive_name:
                for f in files:
                    if f == "cmds": continue
                    file_path = Path(root) / f
                    records.append({
                        "path": str(file_path),
                        "label": label,
                        "message_id": f"{dir_name}_{f}"
                    })
    return records

def profile_corpus(records):
    parser = MimeParser()
    router = ModalityRouter(RouterConfig())
    stats = []
    
    for rec in records:
        path = rec["path"]
        label = rec["label"]
        msg_id = rec["message_id"]
        
        with open(path, "rb") as f:
            raw_bytes = f.read()
            
        try:
            parsed = parser.parse_bytes(raw_bytes, email_id=msg_id)
            routed = router.route(parsed, label=label, split="train")
            
            has_plain_text = bool(parsed.text)
            has_html = bool(parsed.html)
            
            inline_images = [img for img in parsed.images if (img.disposition and img.disposition.value == 'inline') or img.cid]
            attached_images = [img for img in parsed.images if img.disposition and img.disposition.value == 'attachment']
            
            has_image = len(parsed.images) > 0
            has_inline_image = len(inline_images) > 0
            has_image_attachment = len(attached_images) > 0
            
            usable_image_count = len(routed.record.images)
            
            stats.append({
                "message_id": msg_id,
                "label": "spam" if label == 1 else "ham",
                "parse_success": True,
                "has_plain_text": has_plain_text,
                "has_html": has_html,
                "has_image": has_image,
                "has_inline_image": has_inline_image,
                "has_image_attachment": has_image_attachment,
                "text_length": len(parsed.text) if parsed.text else 0,
                "html_length": len(parsed.html) if parsed.html else 0,
                "image_count": len(parsed.images),
                "usable_image_count": usable_image_count,
                "modality": routed.record.modality.name if routed.record.modality else "UNKNOWN",
                "raw_text_hash": hashlib.md5(parsed.text.encode('utf-8')).hexdigest() if parsed.text else None
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            stats.append({
                "message_id": msg_id,
                "label": "spam" if label == 1 else "ham",
                "parse_success": False,
                "has_plain_text": False,
                "has_html": False,
                "has_image": False,
                "has_inline_image": False,
                "has_image_attachment": False,
                "text_length": 0,
                "html_length": 0,
                "image_count": 0,
                "usable_image_count": 0,
                "modality": "FAILED",
                "raw_text_hash": None
            })
            
    df = pd.DataFrame(stats)
    out_dir = Path("data/manifests")
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "spamassassin_profile.csv", index=False)
    
    print("=== MODALITY DISTRIBUTION ===")
    print(df['modality'].value_counts(normalize=True) * 100)
    print("\n=== SPAM MODALITY ===")
    print(df[df['label'] == 'spam']['modality'].value_counts(normalize=True) * 100)
    print("\n=== HAM MODALITY ===")
    print(df[df['label'] == 'ham']['modality'].value_counts(normalize=True) * 100)
    
    print(f"\nTotal messages: {len(df)}")
    print(f"Spam: {len(df[df['label'] == 'spam'])}")
    print(f"Ham: {len(df[df['label'] == 'ham'])}")
    print(f"Failed to parse: {len(df[~df['parse_success']])}")
    print(f"Messages with text: {len(df[df['has_plain_text']])}")
    print(f"Messages with HTML: {len(df[df['has_html']])}")
    print(f"Messages with inline images: {len(df[df['has_inline_image']])}")
    print(f"Messages with attached images: {len(df[df['has_image_attachment']])}")
    print(f"Messages with usable multimodal content: {len(df[df['modality'] == 'MULTIMODAL'])}")
    
    dup_texts = df[df['raw_text_hash'].notnull()].duplicated(subset=['raw_text_hash']).sum()
    print(f"\nDuplicate message texts: {dup_texts}")
    
if __name__ == "__main__":
    records = download_and_extract()
    unique_records = {r["path"]: r for r in records}.values()
    profile_corpus(unique_records)
