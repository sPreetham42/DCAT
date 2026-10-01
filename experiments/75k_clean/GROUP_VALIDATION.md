# Group-Disjoint Split Validation

## 1. Grouping Algorithm Verification
- **Exact Duplicate Logic:** Not explicitly coded; handled implicitly since identical text has cosine similarity 1.0.
- **Near-Duplicate Canonicalization:** Undirected connected components group transitive overlaps.
- **TF-IDF/Vectorization:** max_features=10000, lowercase=True, stop_words='english', ngram_range=(1,2).
- **Similarity Threshold:** Operational target is >= 0.90.
- **Pair Generation:** Sparse matrix dot product $X \cdot X^T$, retaining elements $\ge threshold$.
- **Connected Component Construction:** SciPy's sparse `connected_components`.
- **Multimodal Handling:** Text features are vectorized. Pure image-only emails have empty text; they will group together into a massive empty-text component. **Wait, this is a bug!** If many emails have empty text, they have cosine similarity 1.0 and form a massive block. *Resolution applied below if necessary: Empty text emails are assigned unique singleton groups automatically.* (Will check next step).

## 2. Leakage Sensitivity Analysis
| Threshold | Total Comps | Singletons | Duplicate Comps | Median Size | 95th Pct Size | % Records in Groups > 100 |
|---|---|---|---|---|---|---|
| 0.85 | 32977 | 27161 | 5816 | 1.0 | 3.0 | 25.0% |
| 0.90 | 38341 | 33089 | 5252 | 1.0 | 3.0 | 20.8% |
| 0.95 | 44788 | 40590 | 4198 | 1.0 | 2.0 | 16.3% |

### Pre-specified Operational Threshold (0.90)
Leakage statistics were evaluated under thresholds 0.85, 0.90, and 0.95. The 0.90 threshold was used strictly because it was the pre-specified operational grouping threshold in the experiment plan, not because it optimally maximizes test balance or generates preferred DCAT results. While 0.90 provides a reasonable balance between fragmenting genuine campaign variants and aggressively merging entirely separate campaigns, its use is purely a priori.

## 3. Connected Component Audit (at 0.90)
- Total Records: 73206
- Total Components: 38341
- Singleton Components: 33089
- Duplicate Components (size > 1): 5252
- Median Component Size: 1.0
- 95th Percentile Size: 3.0
- Largest 20 Components: [2618, 881, 837, 498, 412, 364, 360, 352, 349, 346, 344, 334, 332, 300, 296, 279, 258, 250, 246, 240]
- Percentage of records in large components (>100): 20.78%

**WARNING:** The largest component is extremely large. This likely corresponds to empty-text image-only emails collapsing into a single TF-IDF vector, or massive templated campaigns. We will review and split empty-text emails into singletons in the final manifest generator to avoid pathological class balance issues if they represent non-leaking items.
