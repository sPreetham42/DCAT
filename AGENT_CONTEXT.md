# AGENT CONTEXT

## What this project is
This project (DCAT) is a research investigation into **multimodal email spam detection**. It implements a conditional architecture (Dynamic Cross-Attention Transformer) that selectively processes text and image modalities depending on their presence, and uses a text-based early-exit mechanism to skip expensive vision computation for multimodal emails where text alone provides a confident prediction.

## Current research objective
To demonstrate that conditional modality routing and early-exit mechanisms can significantly reduce unnecessary computational cost while maintaining competitive predictive performance against standard late-fusion multimodal baselines (like MMTD).

## Base paper
The primary baseline for comparison is **MMTD** (DistilBERT + ResNet18 with late fusion).

## Our method
**DCAT**: DistilBERT (Text) + MobileViT (Image) + Bidirectional Cross-Attention + Shared Classifier.
Key feature: **Conditional Routing & Early Exit**. Vision models are *only* executed if an image exists AND the text-only auxiliary classifier is not highly confident ($<0.05$ or $>0.95$).

## Most important scientific finding
Architectural changes (cross-attention) alone **do not** guarantee significant performance gains over simple late-fusion when the multimodal training subset is extremely scarce and highly imbalanced.

## What is actually proven
1. The dataset is overwhelmingly text-only (~99.4%).
2. DCAT maintains equivalent predictive performance to baselines on the full test set (Macro-F1 ~0.986).
3. The early-exit mechanism successfully skips vision computation for ~4.45% of multimodal emails, mathematically reducing FLOPs.
4. Class weighting (Weighted-DCAT) provides a statistically significant improvement on the minority multimodal subset.

## What is NOT proven
- **DCAT does NOT significantly beat the baseline on accuracy.** 
- Cross-attention does not show a dominant, statistically significant improvement over late-fusion on the multimodal test set.

## Authoritative result sources
- `artifacts/final_results/results_lineage.csv` (The ultimate source of truth for where metrics came from).
- `results/final_report.md` (Synthesized high-level metrics).
- `experiments/final_results.json` (Raw predictions/metrics for main models).

## Current paper status
- **File:** `paper/main.tex` and `paper/PAPER_CONTENT.md`
- **Status:** The paper is mostly written but has **LaTeX compilation errors** (`\end occurred inside a group at level 1`, undefined references).
- The previous agent was actively trying to fix these formatting and LaTeX issues in `scratch/`.

## Current blockers
- **LaTeX Compilation:** The PDF builds but with severe warnings, missing references, and a fatal group error.

## P0 next actions
1. Fix the LaTeX compilation errors in `paper/main.tex`.
2. Ensure all tables and citations render correctly without undefined references.
3. Consolidate and clean up the git state (too many untracked scratch scripts).

## Files to read next
1. `HANDOVER.md`
2. `artifacts/final_results/results_lineage.csv`
3. `results/final_report.md`

## Rules for modifying the project
- **DO NOT** claim DCAT is more accurate than the baseline. Focus on efficiency and the rigorous evaluation of multimodal scarcity.
- **DO NOT** invent new results. You do not have the raw data to retrain models.
- **DO NOT** assume `scratch/` scripts are part of the core pipeline; they are temporary tools.

---

### ENTRY PROCEDURE FOR NEW AGENT:
```text
FIRST: Read this AGENT_CONTEXT.md
SECOND: Read HANDOVER.md
THIRD: Check `artifacts/final_results/results_lineage.csv`
FOURTH: Run `pdflatex -interaction=nonstopmode main.tex` in `paper/` to see the current build errors.
FIFTH: Fix the LaTeX errors and finalize the paper.
```
