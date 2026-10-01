# HUMAN EDITING FACT-CHECK REFERENCE

This section is NOT part of the paper. After rewriting the prose, verify that
every item below still appears in the manuscript, unchanged.

## Corpus and dataset counts

| Item | Value |
|---|---|
| Processed corpus (primary evaluation) | 6,046 emails |
| Raw corpus on disk | ~16 GB (full raw corpus ≈ 73,500 emails) |
| Ham / spam | 4,150 / 1,896 (2.19:1) |
| TEXT / MULTIMODAL / IMAGE / EMPTY | 6,007 (99.4%) / 11 (0.2%) / 1 (0.02%) / 27 (0.4%) |
| MULTIMODAL composition | 4 ham, 7 spam |
| Split | 70/15/15, seed 42, stratified |
| Primary test set | n = 7,351 (weighted-primary lineage label: "10%") |
| Pooled out-of-fold McNemar samples | 7,867 |
| Multimodal CV evaluation subset | "8K subset" per artifact labeling |

## Headline results (Tables 2, 3)

| Item | Value |
|---|---|
| Full-DCAT full-test Macro-F1 (3-seed mean) | 0.9862 |
| Published Baseline | 0.9869 |
| Late Fusion | 0.9871 |
| DCAT-No-XAttn | 0.9867 |
| DCAT-Early-Exit | 0.9867 |
| Text-Only | 0.9827 |
| Image-Only | 0.3220 |
| All-Spam Prior / Modality Indicator (full test) | 0.4000 / 0.5500 |
| Multimodal Macro-F1: collapse level | 0.4968 (Ham F1 0.0000, Spam F1 0.9935) |
| Multimodal: DCAT-No-XAttn | 0.8317 (Ham F1 0.6667) |
| Multimodal: Text-Only | 0.5584 (Ham F1 0.1633, Spam F1 0.9535) |

## Statistical results

| Item | Value |
|---|---|
| McNemar, Full-DCAT vs Late Fusion (MM subset) | p = 1.0000 |
| McNemar, Full-DCAT vs DCAT-No-XAttn (MM subset) | p = 0.2482 |
| Significance threshold | α = 0.05 |
| McNemar, Weighted-DCAT vs Full-DCAT (pooled OOF, 7,867) | p = 2.49 × 10⁻⁴⁵ |
| McNemar, Weighted-DCAT vs Late Fusion (pooled OOF, 7,867) | p = 3.34 × 10⁻⁶ |
| Seed std (Tables 2/9) | ≤ 0.0003 (Full-DCAT 0.0002; PB and LF 0.0003) |

## Five-fold CV (Tables 5, 6)

| Item | Value |
|---|---|
| Full-DCAT mean / std | 0.7077 / 0.2639 |
| Late Fusion mean / std | 0.5453 / 0.1222 |
| Published Baseline mean / std | 0.5564 / 0.1192 |
| DCAT-No-XAttn mean / std | 0.5171 / 0.0597 |
| Full-DCAT per-fold (Table 6) | 0.4971, 0.4971, 0.4968, 1.0000, 1.0000 |

## Efficiency (Tables 7, 8)

| Item | Value |
|---|---|
| Parameters: Full-DCAT / Late Fusion / Published Baseline | 73,309,090 / 71,761,314 / 77,967,426 |
| Trainable: Full-DCAT / Late Fusion | 2,008,578 (2.01M) / 460,802 (0.46M) |
| FLOPs (always-on variants) | ~13B (estimated) |
| DCAT-Early-Exit FLOPs (Table 7) | ~11B (avg, 90% text-only — different convention, not comparable) |
| Total FLOPs measured (Table 8) | 12.8B → 12.7B (−0.63%) |
| Vision skip rate | 4.45% |
| Total latency | 59.9 ms → 74.7 ms (+24.82%) |
| P95 latency | 60.3 ms → 113.6 ms (+88.39%) |
| Latency/sample | PB 1.48 ms; LF 2.65; NoXAttn 2.66; Full-DCAT 2.70; EE 2.68 ms |

## Class-imbalance ablation (Table 4) and modality view (Table 10)

| Item | Value |
|---|---|
| Weighted-DCAT full-test Macro-F1 | 0.9880 (vs 0.9862) |
| Weighted-DCAT MM-Macro-F1 | 0.7478 (vs 0.6253) |
| Table 10 (seed 42): LF / NoXAttn / Full-DCAT text-only | 0.9858 / 0.9871 / 0.9865 |
| Table 10 multimodal column | 0.4968 / 0.8317 / 0.4968 |

## Confusion matrix (Figure 4a, weighted primary)

| Item | Value |
|---|---|
| DCAT, full test, n = 7,351 | [[2196, 57], [25, 5073]] — 57 FP, 25 FN |

## Architecture and preprocessing constants

| Item | Value |
|---|---|
| Shared latent d_model | 256 |
| Cross-attention layers / heads / d_k | 2 / 4 / 64 |
| Cross-attention d_ff / dropout / activation / norm | 1024 / 0.1 / GELU / Pre-LN |
| Classifier hidden / dropout | 128 / 0.3 |
| Encoders | DistilBERT-base-uncased (frozen), MobileViT-small via timm (frozen) |
| Max token length | 256 |
| Image filter / resize | ≥ 20×20 px, ≥ 1024 bytes; 224×224 bicubic |
| Text filter | ≥ 10 characters |
| Optimizer / LR / batch / epochs | AdamW / 1 × 10⁻⁴ / 64 / 1 |
| Precision / loss / threshold | FP16 mixed / BCEWithLogitsLoss / 0.5 |
| Early-exit thresholds | ≥ 0.95 spam, ≤ 0.05 ham |
| Seeds | 42, 43, 44 |

## Mandatory caveats (must survive editing)

1. **0.9855 → 0.9871 transcription correction** — resolved in the
   publication-readiness audit; disclosed in Section 7.1.
2. **Multimodal evaluation-set distinction** — subset-level metrics come from a
   ~155-sample archived evaluation set (0.9871 = 153/155); prevalence uses the
   sample-level counts (4 ham, 7 spam of 6,046). Disclosed in Section 7.2.
3. **Table 3 provenance** — source analysis's summary (Text-Only collapsed
   0.4968; Image-Only 0.2863/0.4444/0.1282) matches neither archived table;
   archived values reported, conflict disclosed, not reconciled (Section 7.2).
4. **Table 6 fold provenance** — per-fold values reproduced from the recorded
   analysis; fold ordering not independently re-derivable (Section 7.6).
5. **FLOPs conventions** — Table 7's ~11B early-exit figure ("avg, 90%
   text-only") vs Table 8's measured 12.7B are different averaging conventions,
   not comparable (Sections 7.7, 9.3).
6. **Total-time efficiency artifact** — original detailed source artifact no
   longer available; per-sample and total-time measurements differ and must not
   be combined (Section 9.3).
7. **Perceptual-leakage audit scope** — audit was pilot-scope, not a
   corpus-wide perceptual-hash audit (Section 9.4).
8. **Appendix C lineage** — lineage rows use different aggregation settings
   (seed-42 primary 0.9868; CV means 0.6609/0.5564/0.6824) and full-raw-corpus
   split labels (10% ≈ 7,351); headline tables cite their own sources.

## Structural inventory (post-edit targets)

| Item | Count |
|---|---|
| Numbered equations | 21 |
| Tables (10 main + 3 appendix) | 13 |
| Figures | 4 |
| References | 33 ([1]–[33], numbering unchanged) |
