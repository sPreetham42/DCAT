import os
import hashlib
import time
import pypdf

def get_file_info(filepath):
    if not os.path.exists(filepath):
        return {"exists": False}
    
    stat = os.stat(filepath)
    with open(filepath, 'rb') as f:
        data = f.read()
        sha256 = hashlib.sha256(data).hexdigest()
        
    return {
        "exists": True,
        "size": stat.st_size,
        "mtime": time.ctime(stat.st_mtime),
        "sha256": sha256
    }

def count_placeholders(filepath, token):
    if not os.path.exists(filepath):
        return 0
    if filepath.endswith('.pdf'):
        try:
            with open(filepath, 'rb') as f:
                reader = pypdf.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text.count(token)
        except Exception as e:
            return f"Error reading PDF: {e}"
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content.count(token)

files = ['paper/PAPER_CONTENT.md', 'paper/main.tex', 'paper/main.pdf']

print("--- FILE INFO ---")
for f in files:
    info = get_file_info(f)
    print(f"File: {f}")
    if info['exists']:
        print(f"  Size: {info['size']} bytes")
        print(f"  MTime: {info['mtime']}")
        print(f"  SHA256: {info['sha256']}")
    else:
        print("  Not found.")

print("\n--- PLACEHOLDER COUNTS ---")
print(f"PAPER_CONTENT.md count: {count_placeholders('paper/PAPER_CONTENT.md', '[REFERENCE NEEDED]')}")
print(f"main.tex count: {count_placeholders('paper/main.tex', '[REFERENCE NEEDED]')}")
print(f"main.pdf count: {count_placeholders('paper/main.pdf', 'REFERENCE NEEDED')}")
