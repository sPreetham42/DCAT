import pandas as pd
import hashlib

def get_hash(text):
    if not text or pd.isna(text):
        return None
    return hashlib.md5(text.encode('utf-8', errors='replace')).hexdigest()

def run_phase7():
    print("Loading datasets...")
    df_main = pd.read_parquet('data/processed/records.parquet')
    df_sa = pd.read_csv('data/manifests/spamassassin_profile.csv')
    
    usable = df_main[df_main['has_text'] | df_main['has_meaningful_image']].copy()
    
    # Compute md5 on main
    print("Hashing main...")
    usable['raw_text_hash'] = usable['text'].apply(get_hash)
    
    # Count overlap
    main_hashes = set(usable['raw_text_hash'].dropna())
    sa_hashes = set(df_sa['raw_text_hash'].dropna())
    
    overlap = main_hashes.intersection(sa_hashes)
    
    sa_mod = df_sa['modality'].value_counts()
    
    with open('experiments/75k_clean/SPAMASSASSIN_EVAL_DECISION.md', 'w') as f:
        f.write("# Phase 7: SpamAssassin External Evaluation Decision\n\n")
        f.write("## 1. Overlap Analysis\n")
        f.write(f"- Exact Text Hash Overlap between 75K Corpus and SpamAssassin: **{len(overlap)}** messages.\n")
        f.write(f"- Total SpamAssassin Records: {len(df_sa)}\n")
        f.write(f"- Safe External Population: {len(df_sa) - len(overlap)}\n\n")
        
        f.write("## 2. Modality Composition\n")
        f.write("SpamAssassin modality distribution:\n")
        for k, v in sa_mod.items():
            f.write(f"- {k}: {v}\n")
            
        mm_count = sa_mod.get('MULTIMODAL', 0)
        
        f.write(f"\n## 3. Decision\n")
        f.write(f"The SpamAssassin corpus contains **{mm_count}** multimodal items. ")
        f.write("Because the multimodal population is overwhelmingly deficient (or nonexistent), SpamAssassin **cannot** scientifically validate the multimodal cross-attention claims of DCAT.\n")
        f.write("It will be utilized strictly to validate the **text-pathway external generalization** of the baseline models.\n")

    print("Phase 7 Overlap completed.")

if __name__ == '__main__':
    run_phase7()
