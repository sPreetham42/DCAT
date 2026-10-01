import os
import email
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
import random

def create_eml(path: Path, subject: str, text: str, label: int, is_spam: bool):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'sender@example.com'
    msg['To'] = 'recipient@example.com'
    msg['Message-ID'] = make_msgid()
    msg.set_content(text)
    
    # We can add a dummy image if we want to test multimodal
    if random.random() > 0.5:
        # Create a tiny valid GIF to pass pillow verify
        # 25x25 transparent GIF so it bypasses the 20x20 minimum threshold in ImageProcessor
        # Wait, I should make it larger than 20x20 and > 1024 bytes if I want it to be considered meaningful.
        pass
    
    with open(path, 'wb') as f:
        f.write(bytes(msg))

if __name__ == "__main__":
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir = Path("data/manifests")
    manifest_dir.mkdir(parents=True, exist_ok=True)
    
    records = []
    
    for i in range(20):
        is_spam = i % 2 == 0
        eml_path = raw_dir / f"msg_{i}.eml"
        create_eml(
            eml_path,
            f"Test Subject {i}",
            f"This is the body of message {i}. Spam? {is_spam}",
            label=1 if is_spam else 0,
            is_spam=is_spam
        )
        split = 'train' if i < 14 else ('val' if i < 17 else 'test')
        records.append(f"msg_{i},msg_{i}.eml,{1 if is_spam else 0},{split}")
        
    with open(manifest_dir / "manifest.csv", "w") as f:
        f.write("email_id,path,label,split\n")
        f.write("\n".join(records))
    print("Dummy dataset created.")
