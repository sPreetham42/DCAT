# Protocol Amendment: Group-Stratified Cross-Validation

## Context and Rationale
1. The original evaluation split was deterministically frozen using `Seed 42` before any model training commenced.
2. An independent verification of this test split revealed that it yielded only **3 image-bearing ham** test cases out of 10,159 total test examples.
3. This population is mathematically inadequate for the planned conditioned multimodal analysis (McNemar's test and paired bootstrap CIs). A sample size of 3 prevents any determination of statistical significance regarding DCAT's multimodal contribution.
4. The severe imbalance is fundamentally caused by extreme corpus imbalance (only 327 total image-bearing hams exist in the 75k corpus) compounded by the indivisible connected-component grouping logic (the 327 hams are clumped into massive near-duplicate campaigns, three of which account for 276 of the 327 hams).
5. A second split procedure is therefore being introduced *before* any model results are generated or analyzed.

## Amendment Description
The new procedure is deterministic and introduces a **Group-Stratified K-Fold Cross-Validation**. 
- **Objective:** The objective is to evaluate all 327 image-bearing hams by aggregating out-of-fold predictions across the entire corpus, providing a statistically viable $N$ for hypothesis testing.
- **Design:** The procedure uses group-aware joint `label × modality` stratification to partition the connected components into $K=5$ or $K=10$ folds. This objective enforces distributional balance under strict group indivisibility constraints, explicitly not DCAT performance. 
- **Preservation:** The original Seed-42 split remains preserved as a separate reproducibility artifact (`experiments/75k_clean/ORIGINAL_PRE_REGISTERED_SPLIT/`). 

This protocol amendment addresses the impossibility of executing the originally planned hypothesis tests on a single randomized split while maintaining strict blinding and leakage control.
