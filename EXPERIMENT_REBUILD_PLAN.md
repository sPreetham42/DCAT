# Full Experimental Rebuild Plan (DCAT)

This document formalizes the final experimental rebuild plan for the DCAT research project using the **new 75k processed dataset**, adhering to Phase 6 requirements.

## 1. Dataset Provenance & Configuration
- **Dataset:** `data/processed/records.parquet` and `data/processed/email_origin.csv`.
- **Total Records:** 75,419
  - Text-Only: 63,772
  - Multimodal: 7,867
  - Image-Only: 1,567
  - Empty: 2,213 (to be excluded)
- **Usable Records:** 73,206
- **Spam:** 50,199, **Ham:** 25,220 (Class imbalance: ~2:1 Spam:Ham)
- **Splits:** Train (60,335), Validation (7,542), Test (7,542).
- **Leakage Grouping:** Managed via `data/manifests/leakage_groups.csv` and `manifest.csv`.

## 2. Experimental Population
The DCAT model will be evaluated on the **full usable corpus** (73,206 records). We will not artificially restrict training or evaluation to the 7,867 multimodal samples, as DCAT is designed to dynamically handle missing modalities (e.g., via conditional routing/early exit). We will slice the evaluation to report modality-specific performance (Text-Only, Image-Only, Multimodal).

## 3. Model Variants to Retrain
We will retrain the following configurations to support the scientific claims of the paper:
1. **Text-Only Baseline:** Isolates text capabilities.
2. **Image-Only Baseline:** Isolates image capabilities.
3. **Late Fusion Baseline:** Standard concatenation/averaging before the classifier.
4. **Early Fusion Baseline:** (If supported/applicable in existing config).
5. **Full DCAT:** Dynamic Cross-Attention Transformer (with routing).
6. **Ablation 1 - DCAT w/o Cross-Attention:** Validates the cross-attention component.
7. **Ablation 2 - DCAT w/o Conditional Routing:** Validates the dynamic routing/early-exit component.

## 4. Evaluation Protocol
- **Metrics:** Accuracy, Precision, Recall, F1, Macro-F1, per-class F1, PR-AUC, ROC-AUC.
- **Modality Analysis:** Separate tables/metrics for Text-Only, Image-Only, Multimodal, and Full Corpus.
- **Variance Analysis:** Multiple random seeds (e.g., 3 seeds) for the primary configurations if computationally feasible.
- **Statistical Tests:** McNemar's test (or paired t-test over seeds) for full DCAT vs. Late Fusion baseline.
- **Efficiency Benchmark:** Latency, FLOPs, parameters, and early-exit rate.

## 5. Implementation Steps
1. **Phase 1-4 Audit & Update (Completed):** Schema validated, splits validated, 75k dataset identified.
2. **Phase 5 Data Config:** Update `src/dcat/config` or scripts to definitively use `data/processed`.
3. **Phases 7-8 Training:** Execute training for all model variants.
4. **Phases 9-15 Evaluation & Analysis:** Generate primary metrics, ablations, seed variance, stats, efficiency, and robustness analyses.
5. **Phases 16-17 Figure & Table Gen:** Generate publication-ready `.csv`, `.json`, and `.pdf/.png` figures.
6. **Phases 18-20 Freezing Results:** Create `results_final_70k/` directory containing outputs, `FINAL_RESULTS_70K.json`, and `FINAL_RESEARCH_SOURCE_OF_TRUTH_70K.md`.
