import pandas as pd
import json

def inspect_parquet():
    df = pd.read_parquet('data/processed/records.parquet')
    print("Columns:", df.columns.tolist())
    
    # Check if 'source', 'date', 'received' exist
    for col in ['source', 'date', 'received', 'timestamp', 'time']:
        if col in df.columns:
            print(f"Found column: {col}, unique values count: {df[col].nunique()}")
        else:
            print(f"Column '{col}' NOT found.")
            
    # Print a few samples of metadata if they exist
    print("Head of dataframe:")
    print(df.head(2))

    # Determine usable
    usable = df[df['has_text'] | df['has_meaningful_image']]
    print(f"\nUsable records: {len(usable)} / {len(df)}")
    
    if 'source' in df.columns:
        print("\nSources:")
        print(df['source'].value_counts())
        
    print("\nLabels:")
    print(df['label'].value_counts())

if __name__ == '__main__':
    inspect_parquet()
