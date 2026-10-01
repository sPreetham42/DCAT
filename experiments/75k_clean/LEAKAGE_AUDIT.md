# Leakage Audit

## 1. Historical Estimate (Obsolete)
The historical leakage figure of **63.4%** was based strictly on a constrained empirical sample:
- 1,000 sampled test records
- Compared against 10,000 sampled training records
- Cosine threshold >= 0.90

This historical figure must **NOT** be described as an exhaustive corpus-wide leakage rate. It is a sample-based estimate that significantly underestimated the true structural memorization present in the older split.

## 2. New Exhaustive Group Analysis
The new group-disjoint evaluation implements an exhaustive $N \times N$ similarity matrix using unigram/bigram TF-IDF over the complete 73,206 usable records.

### Corpus-Wide Deduplication (Threshold 0.90)
- **Total Usable Records:** 73,206
- **Total Unique Components (Groups):** 38,341
- **Exact/Near-Duplicate Implicit Leaks:** 34,865 records were successfully merged into existing connected components.
- **Singletons:** 33,089

### Sensitivity Analysis
| Threshold | Component Count | Fragmented/Merged |
|-----------|-----------------|-------------------|
| 0.85      | 33,520          | More aggressive merging (combining independent campaigns with shared boilerplates) |
| **0.90**  | **38,341**      | **Pre-specified operational grouping threshold** |
| 0.95      | 44,788          | More fragmentation (separating genuine variants of the same campaign) |

### Cross-Split Leakage
- **Cross-split leakage BEFORE repair (Historical Union-Find Split):** Rampant. The historical split randomized individual records, allowing near-duplicate campaign templates to freely cross the Train/Test boundary.
- **Cross-split leakage AFTER repair (Group-Disjoint Split):** **0**. Connected components are assigned strictly to a single split. No group crosses the Train/Validation or Train/Test boundaries.
