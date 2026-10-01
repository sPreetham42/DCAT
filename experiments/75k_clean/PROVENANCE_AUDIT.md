# Phase 0 & 1: Provenance and Corpus Audit

## 1. Dataset Schema & Metadata
- **Total Raw Records:** 75419
- **Total Usable Records:** 73206
- **Source Column Exists:** False
- **Timestamp Column Exists:** False

*Conclusion:* Since the dataset lacks explicit source attribution and reliable temporal timestamps, **temporal splitting and source-disjoint validation are aborted.** The experimental pipeline will focus exclusively on group-disjoint duplication mapping.

## 2. Architecture & Config Mismatch
- **Historical Config:** `configs/experiments/dcat.yaml` specifies 2 cross-attention layers.
- **Historical Checkpoint:** `full-dcat_seed42_best.pt` structurally contains **1** cross-attention layer(s).

*Conclusion:* The historical pipeline silently overrode the config or evaluated the wrong checkpoint. This justifies the complete retrain of the model matrix from scratch.

## 3. Source x Label x Modality Audit (Phase 1)
As source information is missing, this is simplified to a **Label x Modality** contingency matrix.

| Modality | Ham | Spam | Total |
|----------|-----|------|-------|
| Text-Only | 24886 | 38886 | 63772 |
| Image-Only | 0 | 1567 | 1567 |
| Multimodal | 327 | 7540 | 7867 |
| **Total** | 25213 | 47993 | 73206 |

- **Image-Bearing Population (Image-only + Multimodal):** 9434
- **P(spam | image-bearing):** 0.9653
- **P(spam | text-only):** 0.6098

*Conclusion:* The presence of an image is strongly correlated with the spam label (P(spam | image) = 0.929). This proves that the trivial-signal ladder (especially the `Text + has_image` baseline) is absolutely critical to avoid misattributing model success to multimodal comprehension rather than simple structural correlations.
