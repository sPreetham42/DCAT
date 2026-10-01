# Phase 8: Retrain Decision

**Finding:** `RETRAIN REQUIRED FOR ALL HEADLINE MODELS`

## Rationale
The core mandate of this scientific re-evaluation is to ensure strict group-disjoint deduplication across the train, validation, and test splits (Phase 3 & 4). 
The historical dataset pipeline used a weaker definition of leakage (exact exact-hash components) which allowed near-duplicates across boundaries.

By enforcing a new strict TF-IDF Cosine Similarity >= 0.90 constraint, the assignment of emails to Train and Test has been fundamentally altered. 

Because the historical checkpoints (e.g. `checkpoints/full-dcat_seed42_best.pt`, `checkpoints/late-fusion_best.pt`) were trained on the older, mathematically leaky splits, they are **permanently incompatible with the new `75k_clean` evaluation split**. 
Evaluating them on the new test set would mean evaluating them on data they may have implicitly seen during their historical training phase.

## Matrix to Retrain (Single Seed due to Compute Constraints)
To construct the new source of truth, the following minimal essential grid will be trained from scratch on the new `75k_clean` Group-Disjoint Split:

1. **M1 (TF-IDF + Linear):** Cheap control text baseline.
2. **M2 (Text-only):** DistilBERT text baseline.
3. **M3 (Image-only):** MobileViT image baseline.
4. **M4 (Late Fusion):** Decoupled multimodal baseline.
5. **M5 (DCAT-No-Cross-Attention):** Capacity control baseline.
6. **M6 (Full DCAT):** The proposed cross-attention model.

Historical checkpoints will be completely excluded from `FINAL_RESEARCH_SOURCE_OF_TRUTH_75K.md` to guarantee absolute scientific provenance.
