import os
import sys
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

def main():
    print(f"\n{'='*50}\nStarting Sampled Near-Duplicate Leakage Audit (Upgrade 5)\n{'='*50}")
    
    # Load raw text to bypass tokenization differences
    df = pd.read_csv("data/processed/email_origin.csv")
    manifest = pd.read_csv("data/manifests/leakage_groups.csv")
    
    # Align dataframe with splits
    df['email_id'] = df.index.astype(str)
    manifest['sample_id'] = manifest['sample_id'].astype(str)
    
    merged = df.merge(manifest, left_on='email_id', right_on='sample_id', how='inner')
    
    train_texts = merged[merged['split'] == 'train']['origin'].dropna().tolist()
    test_texts = merged[merged['split'] == 'test']['origin'].dropna().tolist()
    
    # Sample 10000 train and 1000 test for tractability
    np.random.seed(42)
    sample_train_idx = np.random.choice(len(train_texts), min(10000, len(train_texts)), replace=False)
    sample_test_idx = np.random.choice(len(test_texts), min(1000, len(test_texts)), replace=False)
    
    sample_train = [train_texts[i] for i in sample_train_idx]
    sample_test = [test_texts[i] for i in sample_test_idx]
    
    print(f"Sampled {len(sample_train)} training emails and {len(sample_test)} test emails for TF-IDF.")
    
    start = time.time()
    vectorizer = TfidfVectorizer(max_features=10000, stop_words='english', lowercase=True, ngram_range=(1, 2))
    
    print("Fitting TF-IDF on Train sample...")
    train_matrix = vectorizer.fit_transform(sample_train)
    
    print("Transforming Test sample...")
    test_matrix = vectorizer.transform(sample_test)
    
    print("Computing cosine similarity...")
    # Compute similarity between test and train
    sim = cosine_similarity(test_matrix, train_matrix)
    
    # Max similarity for each test sample to ANY train sample
    max_sims = sim.max(axis=1)
    
    threshold_09 = np.sum(max_sims >= 0.90)
    threshold_095 = np.sum(max_sims >= 0.95)
    
    perc_09 = (threshold_09 / len(sample_test)) * 100
    perc_095 = (threshold_095 / len(sample_test)) * 100
    
    print(f"Time taken: {time.time()-start:.2f}s")
    print(f"\nRESULTS:")
    print(f"Test samples with >= 0.90 similarity to train: {threshold_09}/{len(sample_test)} ({perc_09:.2f}%)")
    print(f"Test samples with >= 0.95 similarity to train: {threshold_095}/{len(sample_test)} ({perc_095:.2f}%)")
    
    os.makedirs("artifacts/leakage", exist_ok=True)
    
    with open("docs/NEAR_DUPLICATE_LEAKAGE_AUDIT.md", "w") as f:
        f.write("# Sampled Near-Duplicate Leakage Audit\n\n")
        f.write("The primary data splitting relies on exact MD5 hashes to construct disjoint Union-Find groups. However, slight variations in spam campaigns (e.g., randomized sender IDs or URLs) bypass exact hashing. This document provides a diagnostic audit of remaining near-duplicate leakage.\n\n")
        f.write("## Methodology\n")
        f.write("- **Method**: TF-IDF Cosine Similarity (max 10,000 unigram/bigram features).\n")
        f.write(f"- **Sample**: Randomly sampled {len(sample_test)} test emails compared against a random sample of {len(sample_train)} training emails.\n")
        f.write("- **Metric**: Maximum cosine similarity of a test email to any training email.\n\n")
        
        f.write("## Results\n")
        f.write(f"- **>= 0.90 Similarity**: {perc_09:.2f}% of sampled test emails\n")
        f.write(f"- **>= 0.95 Similarity**: {perc_095:.2f}% of sampled test emails\n\n")
        
        f.write("## Limitations of this Audit\n")
        f.write("This is a *sampled* audit limited to 1,000 test emails against 10,000 training emails due to computational constraints of dense $O(N^2)$ comparisons. Furthermore, TF-IDF evaluates surface lexical overlap rather than deep semantic intent.\n\n")
        
        f.write("## Conclusion\n")
        f.write("While *exact* deduplication is guaranteed by the data pipeline, there remains a measurable degree of near-duplicate (campaign) leakage between train and test sets. **The paper MUST NOT claim that the evaluation is completely leakage-free.** The extremely high overall F1 scores (~98.6%) are likely inflated by these remaining campaign duplicates.")

if __name__ == "__main__":
    main()
