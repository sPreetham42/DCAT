import pandas as pd
import json

def inspect_dataset():
    records_path = r"C:\Users\Preetham S\Documents\antigravity projects\dcat\data\processed\records.parquet"
    df = pd.read_parquet(records_path)
    
    print("--- SCHEMA ---")
    print(df.dtypes)
    
    print("\n--- TOTAL RECORDS ---")
    print(f"Total rows: {len(df)}")
    
    print("\n--- LABELS ---")
    if 'label' in df.columns:
        print(df['label'].value_counts(dropna=False))
    elif 'is_spam' in df.columns:
        print(df['is_spam'].value_counts(dropna=False))
        
    print("\n--- MODALITIES (Derived) ---")
    if 'text' in df.columns and 'image_paths' in df.columns:
        has_text = df['text'].str.strip().astype(bool) & df['text'].notna()
        # image_paths might be list or string of paths
        if df['image_paths'].dtype == 'object':
            # Handle if it's stored as list or JSON or empty string
            try:
                has_image = df['image_paths'].apply(lambda x: len(x) > 0 if isinstance(x, (list, tuple)) else (len(json.loads(x)) > 0 if isinstance(x, str) and x.startswith('[') else bool(x)))
            except:
                has_image = df['image_paths'].astype(bool) & df['image_paths'].notna()
        else:
            has_image = df['image_paths'].notna()
            
        print(pd.DataFrame({'has_text': has_text, 'has_image': has_image}).value_counts())
        
    print("\n--- FIRST 2 ROWS (head) ---")
    print(df.head(2).to_dict(orient='records'))

if __name__ == '__main__':
    inspect_dataset()
