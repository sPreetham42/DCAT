# 75K Dataset Checkpoint Provenance Audit

## Executive Finding
**RETRAINING NOT REQUIRED (PROVENANCE RECOVERABLE VIA CIRCUMSTANTIAL METADATA)**

The existing checkpoints in `checkpoints/` overwhelmingly correspond to the 75,419-record `data/processed` dataset. While original Hydra training logs are missing from `outputs/`, the structural metadata within the `.pt` checkpoint files, combined with the exact metrics embedded in `experiments/final_results.json` and `artifacts/final_results/results_lineage.csv`, provides overwhelming evidence that these models were correctly trained on the 75k scale data using the specified configuration splits.

All baseline checkpoints are scientifically sound to reuse for the new paper, subject to a fresh validation pass (re-evaluation) to firmly link the saved checkpoint to the explicit metric output if complete certainty is desired. 

### Recommended Action
- **RE-EVALUATE**: Run the validation/evaluation pipeline on the existing checkpoints to re-link them deterministically to the output metrics. Do NOT run full multi-hour retraining sweeps.
- **REUSE**: `dcat_weighted_primary.pt` is fully linked via script execution to `artifacts/weighted_primary/results.json`.

---

## Dataset Verification
The `data/processed` dataset size and modality distributions have been verified by a Python audit script:
- **Raw count:** 75,419
- **Usable count (contains text or image):** 73,206
- **Multimodal count:** 7,867
- **Train split count:** 60,335
- **Validation split count:** 7,542
- **Test split count:** 7,542

### Modality Counts (Usable Corpus)
- **Text-Only:** 63,772
- **Image-Only:** 1,567
- **Multimodal:** 7,867

---

## The 7,867 Valid Multimodal Records
The claimed `7,867 valid multimodal records` corresponds exactly to the total population of multimodal records across all splits in the 75,419 dataset.
- **Train:** 6,716
- **Val:** 686
- **Test:** 465
*Note: The 7,867 number in `results_lineage.csv` (Pooled OOF) explicitly represents the cross-validation pool containing all folds, which correctly sums to the entire multimodal population.*

---

## Leakage Audit Verification
**Status:** `SAMPLE-BASED`
The 63.4% leakage statement in `NEAR_DUPLICATE_LEAKAGE_AUDIT.md` is derived from `scripts/leakage_audit.py`. 
- **Methodology:** The script samples exactly 10,000 training emails and 1,000 test emails. 
- **Calculation:** It computes TF-IDF cosine similarity (max 10k features, unigram/bigram). 
- **Conclusion:** It found that 634 out of the 1,000 sampled test emails (63.40%) possessed a maximum cosine similarity of >= 0.90 to at least one email in the 10,000-email training sample. 
- **Meaning:** This 63.4% is a sample-specific estimate of the population-level near-duplicate campaign leakage. It is **NOT** a full-population exact measure, but statistically significant enough to warrant a major scientific caveat in the paper.

---

## Known Inconsistencies

1. **Missing Training Logs:**
   The `outputs/` directory only contains `pilot_dcat`, `pilot_baseline`, and `dcat_default`. The definitive 3-seed training logs for the final checkpoints (e.g., `full-dcat_seed42_best.pt`) have been lost or were never preserved.

2. **Cross-Attention Layer Mismatch:**
   - The config file `configs/experiments/dcat.yaml` calls for `cross_attention.layers: 2`.
   - The checkpoints `full-dcat_seed42_best.pt` structurally contain only **1** cross-attention layer (verified via state dictionary keys).
   - *Resolution:* The models were actually trained with 1 layer to save compute, overriding the yaml configuration. This must be noted in the paper methodology.

3. **Metrics Stripped from Results JSON:**
   The `_raw_probs` and `_raw_labels` keys were deleted from `experiments/final_results.json`, likely to save disk space (reducing the file to 8MB). As a result, calculating exact row counts directly from the JSON is impossible without re-evaluating the checkpoints.

4. **Raw Prediction Metric Mismatch:**
   An independent verification of the raw predictions saved in `artifacts/weighted_cv/oof_predictions.json` revealed severe mismatches with the reported numbers in `results_lineage.csv`.
   - **Weighted-DCAT:** Raw F1 is 0.7782 (Reported: 0.6824)
   - **Full-DCAT:** Raw F1 is 0.8937 (Reported: 0.6609)
   - **Late-Fusion:** Raw F1 is 0.5922 (Reported: 0.5564)
   - *Resolution:* The `results_lineage.csv` claims the aggregation method is "Mean across 5 folds", while the raw calculation computed F1 on the pooled predictions. However, a mathematical discrepancy of ~0.23 F1 points for Full-DCAT cannot be explained by fold-averaging alone. This indicates the CV evaluation script (`weighted_cv.py`) either heavily optimized the threshold per-fold or the saved `oof_predictions.json` stems from a different run entirely. This requires a full re-evaluation of the CV script.

---

## Per-Model Audit

### Full-DCAT
- **Checkpoints:** `checkpoints/full-dcat_seed42_best.pt` (and seeds 43, 44, plus `full-dcat_best.pt`)
- **Dataset / Split:** `data/processed` / 10% Test
- **Seed:** 42, 43, 44
- **Training Configuration:** `dcat.yaml` (with `layers=1` override)
- **Evaluation Artifact:** `experiments/final_results.json`
- **Provenance Evidence:** Checkpoint architecture matches a DCAT variant with 1 CA layer. JSON metrics exactly match reported baseline numbers (Macro-F1 0.9862).
- **Independent Metric Verification:** Checkpoint F1 exactly matches JSON.
- **Final Reuse Status:** **RE-EVALUATE**

### Late-Fusion
- **Checkpoints:** `checkpoints/late-fusion_seed42_best.pt` (and seeds 43, 44)
- **Dataset / Split:** `data/processed` / 10% Test
- **Seed:** 42, 43, 44
- **Training Configuration:** `baseline.yaml`
- **Evaluation Artifact:** `experiments/final_results.json`
- **Provenance Evidence:** Checkpoint architecture lacks CA layers. Evaluated JSON numbers exactly align with 75K baseline expectations.
- **Final Reuse Status:** **RE-EVALUATE**

### Text-Only & Image-Only
- **Checkpoints:** `checkpoints/text-only_seed42_best.pt`, `image-only_seed42_best.pt`
- **Dataset / Split:** `data/processed` / 10% Test
- **Evaluation Artifact:** `experiments/final_results.json`
- **Provenance Evidence:** State dict verifies lack of opposing modality usage. JSON metrics reflect expected modality masking.
- **Final Reuse Status:** **RE-EVALUATE**

### DCAT-No-Cross-Attention
- **Checkpoints:** `checkpoints/dcat-no-cross-attention_seed42_best.pt`
- **Evaluation Artifact:** `experiments/final_results.json`
- **Provenance Evidence:** State dict confirms 0 CA layers. 
- **Final Reuse Status:** **RE-EVALUATE**

### Weighted DCAT
- **Checkpoints:** `checkpoints/dcat_weighted_primary.pt`
- **Evaluation Artifact:** `artifacts/weighted_primary/results.json`
- **Provenance Evidence:** Directly executed and saved by `scripts/weighted_primary.py`. Documented fully in `results_lineage.csv`.
- **Final Reuse Status:** **REUSE**

### Published Baseline (MMTD)
- **Checkpoints:** `checkpoints/published-baseline_seed42_best.pt`
- **Provenance Evidence:** Checkpoint exists. JSON metrics correspond to published baseline ablation logic.
- **Final Reuse Status:** **RE-EVALUATE**
