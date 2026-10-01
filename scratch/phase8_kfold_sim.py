import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold
import numpy as np

def simulate_kfold():
    df = pd.read_csv('scratch/joint_graph_df.csv')
    
    # We create a joint stratification label: label_x_modality
    df['strata'] = df['label'].astype(str) + '_' + df['has_meaningful_image'].astype(str)
    
    for K in [5, 10]:
        print(f"\n--- Simulating K={K} ---")
        sgkf = StratifiedGroupKFold(n_splits=K, shuffle=True, random_state=42)
        
        fold_idx = 0
        for train_idx, test_idx in sgkf.split(df, df['strata'], df['joint_group_id']):
            test_df = df.iloc[test_idx]
            
            img_hams = test_df[(test_df['label'] == 0) & (test_df['has_meaningful_image'])]
            records = len(img_hams)
            groups = img_hams['joint_group_id'].nunique()
            
            print(f"Fold {fold_idx}: Image-bearing Ham Records={records}, Groups={groups}")
            fold_idx += 1

if __name__ == "__main__":
    simulate_kfold()
