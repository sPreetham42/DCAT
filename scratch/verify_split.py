import json
import pandas as pd
import numpy as np

def verify_split():
    print("Loading data...")
    df = pd.read_parquet('data/processed/records.parquet')
    df['email_id'] = df.index.astype(str)
    
    print("Loading manifest...")
    manifest = pd.read_csv('experiments/75k_clean/manifests/split_manifest.csv')
    
    # 1. Independent overlap checks
    train_ids = set(manifest[manifest['split'] == 'train']['email_id'].astype(str))
    val_ids = set(manifest[manifest['split'] == 'val']['email_id'].astype(str))
    test_ids = set(manifest[manifest['split'] == 'test']['email_id'].astype(str))
    
    assert len(train_ids.intersection(val_ids)) == 0, "Overlap train-val!"
    assert len(train_ids.intersection(test_ids)) == 0, "Overlap train-test!"
    assert len(val_ids.intersection(test_ids)) == 0, "Overlap val-test!"
    
    # 2. Check no group crosses split boundaries
    train_groups = set(manifest[manifest['split'] == 'train']['group_id'])
    val_groups = set(manifest[manifest['split'] == 'val']['group_id'])
    test_groups = set(manifest[manifest['split'] == 'test']['group_id'])
    
    assert len(train_groups.intersection(val_groups)) == 0, "Group overlap train-val!"
    assert len(train_groups.intersection(test_groups)) == 0, "Group overlap train-test!"
    assert len(val_groups.intersection(test_groups)) == 0, "Group overlap val-test!"
    
    # 3. Join with original df to recompute counts independently
    test_df = df[df['email_id'].isin(test_ids)]
    
    test_total = len(test_df)
    test_spam = len(test_df[test_df['label'] == 1])
    test_ham = len(test_df[test_df['label'] == 0])
    
    test_img_bearing = test_df['has_meaningful_image'].sum()
    test_img_ham = len(test_df[(test_df['label'] == 0) & (test_df['has_meaningful_image'])])
    test_img_spam = len(test_df[(test_df['label'] == 1) & (test_df['has_meaningful_image'])])
    
    test_text_only_ham = len(test_df[(test_df['label'] == 0) & (~test_df['has_meaningful_image'])])
    test_text_only_spam = len(test_df[(test_df['label'] == 1) & (~test_df['has_meaningful_image'])])
    
    test_img_only = len(test_df[(~test_df['has_text']) & (test_df['has_meaningful_image'])])
    test_multimodal = len(test_df[(test_df['has_text']) & (test_df['has_meaningful_image'])])
    
    result = {
        "train_count": len(train_ids),
        "validation_count": len(val_ids),
        "test_count": len(test_ids),
        "total_usable": len(train_ids) + len(val_ids) + len(test_ids),
        "overlap_errors": 0,
        "group_leak_errors": 0,
        "test_breakdown": {
            "total_test": test_total,
            "test_ham": test_ham,
            "test_spam": test_spam,
            "image_bearing_ham": test_img_ham,
            "image_bearing_spam": test_img_spam,
            "text_only_ham": test_text_only_ham,
            "text_only_spam": test_text_only_spam,
            "image_only": test_img_only,
            "multimodal": test_multimodal
        }
    }
    
    with open('experiments/75k_clean/INDEPENDENT_SPLIT_VERIFICATION.json', 'w') as f:
        json.dump(result, f, indent=2)
        
    md_out = f"""# Independent Split Verification

## Overlap Checks
- Train/Validation Overlap: 0
- Train/Test Overlap: 0
- Validation/Test Overlap: 0
- Cross-split Group Leakage: 0

## Record Counts
- Train: {len(train_ids)}
- Validation: {len(val_ids)}
- Test: {len(test_ids)}
- Total Usable: {len(train_ids) + len(val_ids) + len(test_ids)}

## Test Set Composition (Independent Audit)
- Total Test Examples: {test_total}
- Test Ham: {test_ham}
- Test Spam: {test_spam}

### Modality x Label
- Image-Bearing Ham: **{test_img_ham}**
- Image-Bearing Spam: {test_img_spam}
- Text-Only Ham: {test_text_only_ham}
- Text-Only Spam: {test_text_only_spam}

### Image Nature
- Pure Image-Only: {test_img_only}
- Multimodal (Text+Image): {test_multimodal}

*Note: Since the image-bearing ham count is likely strictly < 150 (since it was 3 under Seed 42 originally), the multimodal test power is severely limited and the Gate 0 claims MUST be narrowed. The scientific priority remains unbiased construction.*
"""
    with open('experiments/75k_clean/INDEPENDENT_SPLIT_VERIFICATION.md', 'w') as f:
        f.write(md_out)
        
    print("Verification complete.")

if __name__ == "__main__":
    verify_split()
