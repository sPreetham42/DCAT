# Project Handover: DCAT (Dynamic Cross-Attention Transformer)

**Date generated:** 2026-09-15
**Target Audience:** The next AI Agent inheriting this repository.

This document is the authoritative entry point for continuing work on the DCAT project. It has been audited against the actual repository state.

---

## 1. Project Overview & Verification Status
**STATUS:** VERIFIED

- **Research Problem:** Email spam detection using images and text, avoiding wasteful vision computation for text-only emails.
- **Research Question:** Can a conditional multimodal architecture combining cross-attention and modality-aware routing reduce computational cost while maintaining classification performance over late-fusion baselines?
- **Hypothesis:** Conditional routing reduces cost; cross-attention improves representation.
- **Current Positioning:** DCAT provides efficiency benefits via conditional early-exit routing while maintaining competitive detection performance. (Accuracy superiority is NOT claimed).

---

## 2. Authoritative Evidence Map
**STATUS:** VERIFIED via `results_lineage.csv`

| Claim / Metric | Authoritative File | Experiment / Source | Status |
| :--- | :--- | :--- | :--- |
| Full Test Macro-F1 | `experiments/final_results.json` | 3-seed unweighted mean | VERIFIED |
| MM-Macro-F1 (CV) | `artifacts/experiments/weighted_cv/cv_results.csv` | 5-Fold CV | VERIFIED |
| McNemar p-value | `task-1070 log (weighted_stats.py)` | Pooled OOF (7867 samples) | VERIFIED |
| Early-Exit Skip Rate | `scratch/FINAL_RESULTS_SOURCE_OF_TRUTH.md` | Primary Test (Seed 42) | VERIFIED (4.45%) |
| FLOP Reduction | `scratch/FINAL_RESULTS_SOURCE_OF_TRUTH.md` | Theoretical calculation | VERIFIED (0.63%) |

*Note: The final report states statistical tests were omitted, but the lineage file shows McNemar tests WERE run for the CV models. Trust `results_lineage.csv`.*

---

## 3. Paper Claim Audit
**STATUS:** REQUIRES ATTENTION

| Paper Claim | Evidence | Verdict | Required Change |
| :--- | :--- | :--- | :--- |
| "DCAT achieves Macro-F1 = 0.9862... Late Fusion 0.9871" | `final_results.json` | SAFE | None |
| "Full-DCAT does not outperform Late Fusion on multimodal..." | `cv_results.csv` | SAFE | None |
| "Weighted-DCAT increases multimodal Macro-F1 from 0.6253 to 0.7478" | Abstract vs Lineage | NEEDS VERIFICATION | Lineage shows 0.6609 to 0.6824. The abstract numbers (0.6253 to 0.7478) must be checked against `weighted_primary` vs `weighted_cv`. |
| "Early-exit skips 4.45%... reduces FLOPs by 0.63%" | Lineage | SAFE | None |

---

## 4. Actual Contributions
**STATUS:** VERIFIED

- **Intended Contribution:** A highly accurate and efficient multimodal spam detector.
- **Implemented Contribution:** Dynamic cross-attention with deterministic modality routing and text-first early-exit computation.
- **Demonstrated Contribution:** Conditional routing mathematically reduces unnecessary multimodal computation. Class-weighting improves minority multimodal performance.
- **Unsupported Ambition:** Statistically significant accuracy improvement on the full test set over standard late fusion.

---

## 5. Dataset Reproducibility Audit
**STATUS:** PARTIALLY REPRODUCIBLE (By Design)

- **Available in repository:** Dataset definitions, PyTorch DataLoaders, Split manifests (`data/manifests/`).
- **Available only locally:** Raw SpamAssassin corpus (`16GB`), Processed parquet files, Model checkpoints (`7.9GB`).
- **Consequence:** Training from scratch is **NOT CURRENTLY REPRODUCIBLE** without the local data. Evaluation from existing artifacts and table regeneration is **REPRODUCIBLE**.

---

## 6. Architecture & DCAT Story Verification
**STATUS:** VERIFIED via `src/dcat/models/dcat/model.py`

- **What DCAT does:** Routes inputs based on modality presence.
- **"Dynamic" / "Conditional":** The vision encoder (`MobileViT`) is NOT run if `has_image` is false, OR if the text-only early-exit classifier yields probability $>0.95$ or $<0.05$.
- **Cross-attention:** Text and Image tokens attend to each other *only* for non-exited multimodal emails.

---

## 7. Paper Build Status
**STATUS:** BROKEN / NEEDS FIXING

- **Entry Point:** `paper/main.tex`
- **Compilation:** `pdflatex main.tex`
- **Status:** Fails with exit code 1. Produces a PDF, but contains severe warnings (`\end occurred inside a group at level 1`, undefined references to Table 8 and 9, missing citations).
- **Formatting:** Frequent underfull/overfull \hbox warnings.

---

## 8. Scratch Directory Audit
**STATUS:** CLASSIFIED

- **Useful:** `clean_latex.py`, `resolve_references.py` (Used for fixing paper).
- **Temporary/Ad-hoc:** `patch*.py`, `audit_numbers.py`.
- **Warning to Next Agent:** Do NOT treat `scratch/` scripts as part of the core scientific pipeline. They are text-processing scripts used by the previous agent to wrestle with LaTeX.

---

## 9. Git State
**STATUS:** UNCLEAN

- **Branch:** `main`
- **Modified:** `README.md`, `.gitignore`, `src/dcat/scripts/audit_leakage.py`
- **Untracked:** Dozens of `scratch/` scripts, `paper/`, `results/`, `experiments/`, `HANDOVER.md`.
- **Action Required:** The next agent should commit these changes once the paper compiles successfully to create a clean checkpoint.

---

## 10. Research Decision Log

| Decision | Reason | Evidence | Consequence |
| :--- | :--- | :--- | :--- |
| Compare against MMTD | MDL-SPAM was flawed | `README.md` | Evaluation is honest but shows smaller gains. |
| Shift focus to Efficiency | Accuracy gains were negligible | `final_report.md` | Paper claims conditional routing is the main contribution. |
| Use 5-Fold CV for Multimodal | MM subset is too small | `artifacts/multimodal_cv/` | Provides statistically sound variance bounds for the minority class. |

---

## 11. Open Research Questions

1. **Discrepancy in Abstract Metrics:** The abstract claims Weighted-DCAT improved MM-Macro-F1 from `0.6253 to 0.7478`, but `results_lineage.csv` shows `0.6609 to 0.6824`. 
   - *Why it matters:* The paper's abstract must perfectly match the authoritative evidence.
   - *Next Agent Action:* Reconcile these numbers by checking `artifacts/experiments/weighted_primary/results.json` vs the CV results.

---

## 12. Base Paper Comparison

| Dimension | Base Paper (MMTD) | Our Work (DCAT) |
| :--- | :--- | :--- |
| **Dataset** | Unknown pairing | Naturally paired text/images |
| **Architecture** | DistilBERT + ResNet18 | DistilBERT + MobileViT + Cross-Attention |
| **Fusion strategy**| Late Fusion (Concat) | Bidirectional Cross-Attention |
| **Efficiency** | Always runs vision | Conditional routing + Early exit |

---
*End of Audited Handover Document.*
