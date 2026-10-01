# DCAT Experimental Rebuild: Final Source of Truth (75k Dataset)

**STATUS**: FINALIZED & AUTHORITATIVE
**DATASET**: `data/processed` (75,419 total records)
**PREVIOUS PAPER STATUS**: OUTDATED (Do not use old 6,046-sample numbers).

This document serves as the absolute, frozen source of truth for all numerical data, tables, figures, and scientific claims that must be written into the new DCAT manuscript. 

## 1. Executive Summary of New Findings

The experimental rebuild on the full 75k dataset confirms the primary architectural hypothesis of DCAT: **Conditional routing and text-first early-exit mechanisms mathematically reduce computational waste without significantly degrading classification performance.** 
However, **DCAT does NOT significantly outperform a standard late-fusion baseline in overall accuracy or Macro-F1.** The primary contribution of this work is purely computational efficiency and robustness on minority multimodal samples, not state-of-the-art predictive dominance.

- **Primary Performance**: Full-DCAT achieves a Macro-F1 of 0.9862, statistically equivalent to the Late-Fusion baseline (0.9870).
- **Efficiency**: The conditional early-exit mechanism successfully skips expensive vision processing (MobileViT) for 4.45% of multimodal emails.
- **Multimodal Robustness**: Full-DCAT outperforms Late-Fusion on the rare multimodal subset (Macro-F1 0.6253 vs 0.4967), showing that cross-attention better captures the scarce paired signals.

## 2. Dataset Audit & Statistics

The dataset evaluated is significantly larger and more skewed than prior studies (e.g., MMTD), revealing the true nature of modern email spam: it is overwhelmingly text-only.

| Metric | Count |
| :--- | :--- |
| **Total Raw Records** | 75,419 |
| **Total Usable Records (Non-empty)** | 73,206 |
| **Training Split** | 60,335 |
| **Validation Split** | 7,542 |
| **Test Split** | 7,542 |

### Class & Modality Distribution
- **Class Imbalance**: Spam (50,199) vs Ham (25,220). Ratio ~ 2:1.
- **Modality Imbalance**: Text-Only (63,772, ~87%), Multimodal (7,867, ~10.7%), Image-Only (1,567, ~2.1%).

### Near-Duplicate / Leakage Caveat
**WARNING**: A sampled TF-IDF cosine similarity audit revealed that 63.4% of test emails share >= 0.90 similarity with at least one training email, and 11.8% share >= 0.95 similarity. 
*Scientific Claim Constraint*: The paper MUST explicitly state that while exact MD5 duplicates were removed, significant campaign-level near-duplicate leakage remains. The extremely high absolute F1 scores (~98.6%) are likely inflated by this leakage and should be interpreted as relative rather than absolute capabilities.

## 3. Primary Metric Results (Test Set)

*Note: All variants evaluated on the standard 10% Test Split.*

| Model Configuration | Accuracy | Macro-F1 | Spam F1 | Ham F1 |
| :--- | :--- | :--- | :--- | :--- |
| **Text-Only Baseline** | 0.9853 | 0.9827 | 0.9894 | 0.9759 |
| **Image-Only Baseline** | 0.3637 | 0.3220 | 0.1539 | 0.4901 |
| **Published-Baseline (MMTD)** | 0.9888 | 0.9868 | 0.9920 | 0.9817 |
| **Late-Fusion** | 0.9890 | 0.9870 | 0.9921 | 0.9820 |
| **Full-DCAT** | 0.9883 | 0.9862 | 0.9916 | 0.9808 |

*Observation*: DCAT performance is functionally equivalent to Late-Fusion across the entire test set.

## 4. Ablation & Modality Analysis Results

The value of the DCAT architecture becomes apparent only when evaluating the rare subset of multimodal emails.

| Model Configuration | Text-Only Macro-F1 | Multimodal Macro-F1 | Image-Only Macro-F1 |
| :--- | :--- | :--- | :--- |
| **Late-Fusion** | 0.9876 | 0.4967 | 1.0000 |
| **DCAT (No Cross-Attention)** | 0.9871 | 0.5923 | 0.8288 |
| **Full-DCAT** | 0.9867 | 0.6253 | 1.0000 |

*Observation*: Full-DCAT increases multimodal Macro-F1 by ~12.8 points over Late-Fusion (0.6253 vs 0.4967). Removing cross-attention (DCAT-No-Cross-Attention) drops multimodal performance to 0.5923, proving cross-attention provides a measurable benefit for paired data.

## 5. Efficiency Claims

The core contribution of DCAT. These metrics are derived from the conditional routing evaluation:
- **Early-Exit Skip Rate**: 4.45% of multimodal emails successfully triggered the text-only early exit (Text classifier confidence > 0.95 or < 0.05).
- **Latency Reduction**: +24.82% empirical throughput vs standard forward pass.
- **FLOPs Reduction**: 0.63% theoretical reduction in overall computation.

## 6. Required Scientific Conclusions

**What the new paper MUST claim:**
1. Real-world multimodal spam datasets are overwhelmingly text-dominated.
2. Standard late-fusion architectures perform exceptionally well overall, but struggle on the rare paired multimodal subset.
3. DCAT's conditional routing mechanism safely reduces vision computation without hurting overall F1.
4. Cross-attention improves the handling of minority multimodal samples over simple concatenation.

**What the new paper MUST NOT claim:**
1. Do NOT claim DCAT beats baselines in overall accuracy.
2. Do NOT claim the dataset is completely free of leakage (explicitly mention near-duplicate overlap).
3. Do NOT use the 6,046-sample numbers (e.g. do not mention the old dataset sizes in the methodology).
