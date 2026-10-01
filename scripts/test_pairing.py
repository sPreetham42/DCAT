import pandas as pd
from dcat.preprocessing.mime_parser import MimeParser

def test_pairing():
    df = pd.read_csv("data/processed/email_origin.csv")
    parser = MimeParser()
    
    # Find one multimodal email
    for idx, row in df.iterrows():
        raw_text = row['origin']
        if pd.isna(raw_text):
            continue
            
        try:
            parsed = parser.parse_bytes(raw_text.encode('utf-8'), email_id=str(idx))
            if parsed.text and len(parsed.images) > 0:
                print(f"FOUND MULTIMODAL EMAIL AT INDEX: {idx}")
                print(f"Label: {row['label']}")
                print(f"Text length: {len(parsed.text)}")
                print(f"Number of images: {len(parsed.images)}")
                for i, img in enumerate(parsed.images):
                    print(f"  Image {i}: cid={img.cid}, disp={img.disposition.value if img.disposition else None}, size={len(img.content)} bytes")
                
                # Check if image CID is referenced in HTML
                if parsed.html:
                    for img in parsed.images:
                        if img.cid and img.cid in parsed.html:
                            print(f"  [SUCCESS] Image CID {img.cid} is explicitly referenced in the HTML payload.")
                
                break
        except Exception:
            continue

if __name__ == "__main__":
    test_pairing()
