import pandas as pd

df = pd.read_parquet('data/processed/records.parquet')
print("Columns in records.parquet:")
for col in df.columns:
    print(f"- {col}: {df[col].dtype}")

img_hams = df[(df['label'] == 0) & (df['has_meaningful_image'])]
print(f"\nTotal image-bearing hams in corpus: {len(img_hams)}")
