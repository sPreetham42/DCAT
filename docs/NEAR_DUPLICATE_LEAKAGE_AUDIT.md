# Sampled Near-Duplicate Leakage Audit

The primary data splitting relies on exact MD5 hashes to construct disjoint Union-Find groups. However, slight variations in spam campaigns (e.g., randomized sender IDs or URLs) bypass exact hashing. This document provides a diagnostic audit of remaining near-duplicate leakage.

## Methodology
- **Method**: TF-IDF Cosine Similarity (max 10,000 unigram/bigram features).
- **Sample**: Randomly sampled 1000 test emails compared against a random sample of 10000 training emails.
- **Metric**: Maximum cosine similarity of a test email to any training email.

## Results
- **>= 0.90 Similarity**: 63.40% of sampled test emails
- **>= 0.95 Similarity**: 11.80% of sampled test emails

## Limitations of this Audit
This is a *sampled* audit limited to 1,000 test emails against 10,000 training emails due to computational constraints of dense $O(N^2)$ comparisons. Furthermore, TF-IDF evaluates surface lexical overlap rather than deep semantic intent.

## Conclusion
While *exact* deduplication is guaranteed by the data pipeline, there remains a measurable degree of near-duplicate (campaign) leakage between train and test sets. **The paper MUST NOT claim that the evaluation is completely leakage-free.** The extremely high overall F1 scores (~98.6%) are likely inflated by these remaining campaign duplicates.