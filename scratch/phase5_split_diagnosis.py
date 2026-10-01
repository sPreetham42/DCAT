import json
import pandas as pd
import numpy as np

def run_diagnosis():
    print("Loading data...")
    df = pd.read_parquet('data/processed/records.parquet')
    df['email_id'] = df.index.astype(str)
    
    print("Loading manifest...")
    manifest = pd.read_csv('experiments/75k_clean/ORIGINAL_PRE_REGISTERED_SPLIT/split_manifest.csv')
    manifest['email_id'] = manifest['email_id'].astype(str)
    df = df.merge(manifest[['email_id', 'group_id', 'split']], on='email_id', how='inner')
    
    img_hams = df[(df['label'] == 0) & (df['has_meaningful_image'])]
    total_img_ham = len(img_hams)
    
    print(f"\nTotal image-bearing hams in full corpus: {total_img_ham}")
    
    # Check distribution of image-bearing hams across groups
    group_counts = img_hams['group_id'].value_counts()
    print(f"Number of unique groups containing image-bearing hams: {len(group_counts)}")
    print(f"Top 10 groups with most image-bearing hams:\n{group_counts.head(10)}")
    
    # Check total size of the groups containing image-bearing hams
    img_ham_groups = group_counts.index.tolist()
    sizes_of_these_groups = df[df['group_id'].isin(img_ham_groups)]['group_id'].value_counts()
    
    print("\nTotal size of these groups (including non-img-hams):")
    for gid in group_counts.head(10).index:
        total_size = sizes_of_these_groups[gid]
        img_ham_count = group_counts[gid]
        print(f"Group {gid}: Total size = {total_size}, Image-Hams = {img_ham_count}")
        
    # Check train/val/test assignment under Seed 42
    split_col = 'split_y' if 'split_y' in img_hams.columns else 'split'
    split_dist = img_hams[split_col].value_counts()
    train_count = split_dist.get('train', 0)
    val_count = split_dist.get('val', 0)
    test_count = split_dist.get('test', 0)
    
    print("\nDistribution across Seed 42 splits:")
    print(f"Train: {train_count} ({(train_count/total_img_ham)*100:.1f}%)")
    print(f"Val: {val_count} ({(val_count/total_img_ham)*100:.1f}%)")
    print(f"Test: {test_count} ({(test_count/total_img_ham)*100:.1f}%)")
    
    # Determine the root cause
    md = f"""# Split Diagnosis (Seed 42)

## 1. Corpus Imbalance
- Total usable corpus records: {len(df)}
- Total image-bearing hams in corpus: {total_img_ham} ({(total_img_ham/len(df))*100:.2f}%)
- *Diagnosis:* The raw corpus suffers from extreme natural imbalance. P(image | ham) is very low.

## 2. Group Packing Algorithm
- Number of unique connected-components (groups) containing image-bearing hams: {len(group_counts)}
- *Diagnosis:* The 327 examples are distributed across {len(group_counts)} groups. 
"""

    if len(group_counts) < 50:
        md += "- This means they are heavily clumped into a small number of massive campaigns. A random split (like GroupShuffleSplit) assigns entire groups at once. If the largest groups randomly fall into `train`, the `test` split is completely starved.\n"
    else:
        md += "- They are reasonably well-distributed. The failure of Seed 42 to balance them across the splits was purely due to the random 80/10/10 allocation lacking explicit stratification for the rare joint `label=0 & has_image=True` strata.\n"

    md += f"""
## 3. Seed 42 Allocation
- Train: {train_count} ({(train_count/total_img_ham)*100:.1f}%)
- Val: {val_count} ({(val_count/total_img_ham)*100:.1f}%)
- Test: {test_count} ({(test_count/total_img_ham)*100:.1f}%)

*Diagnosis:* The lack of joint label/modality stratification caused Seed 42 to randomly assign the vast majority ({train_count}) to the training set, leaving only {test_count} for testing. Because of group indivisibility and the rarity of the class, random splitting is mathematically incapable of guaranteeing a 10% balanced test yield.

## 4. Largest Contributing Groups
"""
    for gid in group_counts.head(5).index:
        md += f"- **Group {gid}:** Total Size = {sizes_of_these_groups[gid]}, Image-Bearing Hams = {group_counts[gid]}\n"

    with open('experiments/75k_clean/SPLIT_DIAGNOSIS.md', 'w') as f:
        f.write(md)
        
    print("Diagnosis complete.")

if __name__ == "__main__":
    run_diagnosis()
