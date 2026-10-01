# Final Evaluation Design Decision

### Original Split
**Is Seed 42 retained as the original protocol artifact?**
Yes. The original Seed-42 split is preserved in `experiments/75k_clean/ORIGINAL_PRE_REGISTERED_SPLIT/` as a strictly immutable scientific artifact, complete with independent verification mathematically proving its group-disjoint boundary integrity. 

### Main Evaluation
**Which evaluation design will be used for the new experiment?**
A deterministic **Group-Stratified K-Fold Cross-Validation** (K=10). 
The final results for the multimodal claim will be derived by aggregating the out-of-fold predictions across all K folds. 

### Why
**Explain the statistical/data-composition rationale.**
The dataset exhibits an extreme natural imbalance: out of 73,206 usable emails, only 327 are image-bearing hams. Furthermore, these 327 emails are heavily clumped into a small handful of massive connected components (near-duplicate campaign bursts). Because a mathematically valid split must respect group indivisibility (to prevent leakage), any single randomized split—including the pre-registered Seed 42—will randomly allocate these massive blocks entirely to train, validation, or test. Seed 42 resulted in exactly 3 image-bearing hams in the test split. 
A sample size of 3 completely precludes paired statistical hypothesis testing. By shifting to a K-Fold design, we deterministically evaluate all 327 image-bearing hams while strictly preventing any train/test group overlap within any fold.

### Leakage
**Are both text and image duplication adequately controlled?**
No. Text duplication is adequately controlled via the 0.90 TF-IDF sparse similarity matrix. However, an audit (`IMAGE_LEAKAGE_AUDIT.md`) proved that explicit image-level perceptual hashes (`perceptual_hash`, `exact_hash`) are missing from the dataset. Consequently, the grouping logic is entirely blind to identical images that may have been embedded within non-overlapping text templates. The evaluation cannot yet claim to be *fully* leakage-controlled across the multimodal surface.

### Image-Bearing Ham
**How many are available in the proposed primary evaluation?**
The aggregate K-Fold evaluation will produce exactly **327** out-of-fold image-bearing ham predictions. 

### Protocol Status
**Original preregistration or explicit amendment?**
Explicit Protocol Amendment (`PROTOCOL_AMENDMENT.md`). The shift from a single random split to a deterministic group-stratified K-Fold design occurred after the original split failed the baseline power requirement, but *before* any models were trained or evaluated. 

### GPU Status
**Still blocked or ready?**
**STILL BLOCKED.** The evaluation design is scientifically sound, but GPU execution remains blocked by two factors:
1. The execution environment remains CPU-only.
2. The K-Fold design increases the required compute budget by a factor of $K$ (e.g., training the M1-M6 matrix 10 separate times). Before executing, the exact K parameter must be approved against the GPU compute budget, and image hashing must be addressed.
