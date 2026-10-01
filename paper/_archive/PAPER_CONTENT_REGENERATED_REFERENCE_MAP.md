# PAPER_CONTENT_REGENERATED_REFERENCE_MAP.md — Phase 4 Traceability Artifact

**Purpose:** verification map for `PAPER_CONTENT_REGENERATED.md`. For every major claim/result: manuscript section → claim → OUR research vs external context → source. OUR-research items cite `PAPER_CONTENT.md` (PC §); external-context items cite `LITERATURE_MAP.md` keys (refN / newN — LM status). This file is a verification artifact, not part of the manuscript.

**Legend:** PC = `PAPER_CONTENT.md` (authoritative for our research) · LM = `LITERATURE_MAP.md` (citation plan; [V] = session-verified) · MS = `PAPER_CONTENT_REGENERATED.md` (the manuscript). Manuscript reference numbers [n] map to LM keys in the table at the end.

---

## 1. CLAIM-BY-CLAIM TRACEABILITY

### Abstract (MS Abstract)
| Claim/result | Type | Source |
|---|---|---|
| 6,046 processed emails; 11 multimodal; 99.4% text-only | OURS | PC §5.3 |
| Full-test Macro-F1 0.9862 vs 0.9869 baseline, 0.9871 Late Fusion (3 seeds) | OURS | PC §Abstract, §7.1, §7.8 |
| Multimodal subset: Full-DCAT no better than Late Fusion (McNemar p = 1.0000); No-XAttn 0.8317 vs 0.4968 | OURS | PC §Abstract, §7.2, §7.3 |
| 5-fold CV means 0.7077 / 0.5453; stds 0.2639 / 0.1222 | OURS | PC §Abstract, §7.5 |
| Weighted-DCAT 0.6253 → 0.7478; p < 10⁻⁴⁴ and p < 10⁻⁵ | OURS | PC §Abstract, §7.4 |
| Early exit: 4.45% vision skip; 0.63% FLOP reduction | OURS | PC §Abstract, §7.7 |
| Closing interpretation (architectural changes ≠ guaranteed gains under scarcity + text dominance) | OURS (interpretation) | PC §Abstract final sentence |

### §1 Introduction
| Claim | Type | Source |
|---|---|---|
| Spam as persistent cybersecurity problem; adaptive campaigns | EXTERNAL | LM ref3 [V] = MS [1] |
| Images used in spam (banners, phishing screenshots, rendered text) | EXTERNAL | LM ref24 [V] = MS [2]; LM new6 [V] = MS [3] |
| Prior multimodal systems: independent encoders + concatenation/late fusion | EXTERNAL | LM ref13 [V] = MS [4] |
| Attention/gating fusion explored in adjacent literature | EXTERNAL | LM ref8 [V] = MS [5]; LM ref14 [V] = MS [27] |
| DCAT description (bidirectional cross-attention, deterministic routing, early exit 0.05/0.95) | OURS | PC §1, §3.2–3.3, §4.8 |
| Evaluation components (3 seeds, ablations, CV, McNemar OOF, efficiency) | OURS | PC §1, §6 |
| Five contribution bullets | OURS | PC §1 (contribution list) |
| Roadmap paragraph | OURS | PC §1 (adapted to new section order) |

### §2.1 Email as a Multimodal Medium
| Claim | Type | Source |
|---|---|---|
| MIME structure (headers, multipart bodies, typed parts, MIME tree) | EXTERNAL | LM new11 [V] = MS [6] |
| Corpus retains original MIME structure | OURS | PC §5.1 |
| Text-only / image-only / multimodal message types | OURS (definitions used) | PC §3.2 |

### §2.2 Spam, Phishing, Threat Landscape
| Claim | Type | Source |
|---|---|---|
| Spam definition (unsolicited bulk email) | EXTERNAL | LM ref3 [V] = MS [1] |
| Phishing definition; overlap with spam; visual exploitation | EXTERNAL | LM new6 [V] = MS [3] |
| Dataset shift in spam corpora | EXTERNAL | LM ref3 [V] = MS [1] |
| Image-based spam rationale | EXTERNAL | LM ref24 [V] = MS [2] |

### §2.3 Text Representations
| Claim | Type | Source |
|---|---|---|
| BoW/TF-IDF classical filtering | EXTERNAL | LM ref3 [V] = MS [1] |
| Word embeddings | EXTERNAL | LM new5 [V] = MS [8] |
| Character-level / word-level CNNs; LSTM | EXTERNAL | LM ref19, ref18, ref20 [V] = MS [9], [10], [11] |
| Transformer; self-attention Q/K/V | EXTERNAL | LM new1 [V] = MS [12] |
| BERT, RoBERTa | EXTERNAL | LM ref7, ref21 [V] = MS [13], [14] |
| DistilBERT: distilled, 6-layer, 768-d, cheaper | EXTERNAL | LM ref4 [V] = MS [15] |

### §2.4 Image Representations
| Claim | Type | Source |
|---|---|---|
| VGG / ResNet / MobileNet | EXTERNAL | LM ref15, ref16, ref17 [V] = MS [16], [17], [18] |
| Visual spam patterns (colors, shapes, overlays) | EXTERNAL | LM ref24 [V] = MS [2] |
| ViT patch-sequence classification | EXTERNAL | LM new2 [V] = MS [19] |
| MobileViT hybrid design; timm preprocessing contract | EXTERNAL | LM ref5, ref6 [V] = MS [20], [21]; **MS [20] arXiv ID corrected to 2110.02178 in Phase 5 (1810.03775 was an unrelated physics paper — verified via arXiv API)** |

### §2.5 Attention and Cross-Modal Attention
| Claim | Type | Source |
|---|---|---|
| Scaled dot-product attention Eq. (1); multi-head attention | EXTERNAL (formulation) | LM new1 [V] = MS [12] |
| Attention in seq2seq alignment; visual attention in captioning | EXTERNAL | LM ref22 [V] = MS [22]; LM new3 [V] = MS [23] |
| Bidirectional attention flow | EXTERNAL | LM new4 [V] = MS [24] |
| ViLBERT co-attention; LXMERT; CLIP contrastive | EXTERNAL | LM ref8, ref9, ref10 [V] = MS [5], [25], [26] |
| Late fusion vs gating contrast | EXTERNAL | LM ref14 [V] = MS [27] |

### §2.6 Conditional Computation
| Claim | Type | Source |
|---|---|---|
| Dynamic networks survey taxonomy | EXTERNAL | LM new10 [V] = MS [28] |
| Early exits (BranchyNet) | EXTERNAL | LM ref23 [V] = MS [29] |
| Dynamic routing (SkipNet) | EXTERNAL | LM new9 [V] = MS [30] |
| Email's deterministic modality signal; exit avoids whole encoder; overhead caveat | OURS (framing) | PC §2.5, §4.8, §7.7 |

### §3 Related Work (incl. §3.6 gaps)
| Claim | Type | Source |
|---|---|---|
| §3.1 text-spam lineage (rule-based → ML → deep → transformers) | EXTERNAL | MS [7], [1], [9]–[15] (LM map) |
| §3.1 "strong text-only performance confirmed in our own evaluation" | OURS | PC §7.1 |
| §3.2 image-spam line + ambiguity limitation | EXTERNAL + OURS | MS [2], [16]–[18]; PC §7.1 (Image-Only result) |
| §3.3 MMTD late fusion; GMU gating; VL cross-attention | EXTERNAL | MS [4], [27], [5], [25], [26] |
| §3.3 two corpus-level facts (text dominance; unconditional vision) | EXTERNAL + OURS | LM ref3/ref24/ref13; PC §5.3, §6.2 |
| §3.4 early-exit + routing lineage; email's zero-cost routing signal | EXTERNAL + OURS | MS [29], [30], [28]; PC §3.2, §2.5 |
| §3.5 evaluation practice; McNemar | EXTERNAL + OURS | MS [1], [31] (LM ref11 [V]); PC §2.6, §6.5 |
| §3.6 four gaps (cross-attention unexplored; unconditional vision; imbalance under-treated; evaluation separation) | EXTERNAL-backed gap statements | LM §7 (gap evidence: ref13, ref14, ref8, ref3, new6, new7, ref1, ref11); hedged phrasing per LM REQ-14/REQ-17 — **MDL-SPAM (LM ref2 [NV]) was NOT used; gap 1 wording does not depend on it** |

### §4 Problem Formulation
| Claim | Type | Source |
|---|---|---|
| Task definition (m, t, I₁..I_K, y ∈ {0,1}) Eq. (2) | OURS | PC §3.1 |
| Routing rule Eq. (3); four categories; ≥10 chars; EMPTY discarded; determinism (no learned router) | OURS | PC §3.2 |
| Three computation paths | OURS | PC §3.3 |
| BCE Eq. (4); weighted BCE Eq. (5); w_pos Eq. (6) — placeholders restored (N, i, ŷ_i, σ, y_i, w_pos) | OURS | PC §3.4 (symbols resolved via PC App. B: d_model = 256 etc.) |

### §5 Architecture
| Claim | Type | Source |
|---|---|---|
| Five components; shared latent d_model = 256; LayerNorm projections | OURS | PC §4.1, §4.4, App. B |
| DistilBERT-base-uncased, 6-layer, 768-d, frozen; 256 tokens; attention mask; batch B — Eq. (7) | OURS + EXTERNAL | PC §4.2, App. B; LM ref4 [V] |
| MobileViT-small via timm; 224×224; S tokens; 15×15 grid; frozen — Eq. (8) | OURS + EXTERNAL | PC §4.3 (placeholders resolved via App. B), LM ref5/ref6 [V] |
| Projector Eqs. (9)–(11); W_text ∈ R^{768×d_model}; W_img ∈ R^{D_img×d_model} | OURS | PC §4.4 |
| Cross-attention: L = 2, h = 4, d_k = 64, Pre-LN [32]; Eqs. (12)–(17) incl. image-to-text made explicit and closing brace fixed | OURS + EXTERNAL | PC §4.5 (formulation completed per outline); LM new1, ref12 [V] |
| Pooling/fusion Eqs. (18); d_model vs 2·d rationale | OURS | PC §4.6 |
| Shared classifier Eq. (19); aux classifier Eq. (20); exit rule Eq. (21) with 0.95/0.05; joint training | OURS | PC §4.7, §4.8 |
| Training config (AdamW [33] 1e-4, cosine, AMP FP16, batch 64, 1 epoch, freezing, seeding); 73,309,090 / 2,008,578 / 2.74% | OURS + EXTERNAL | PC §4.9, App. B; LM new8 [V] |
| Six-step inference pipeline; 0.5 threshold | OURS | PC §4.10, §6.1 |
| Figures 1–2 marked as PLACEHOLDERS | — | Outline §F (figures to be drawn) |

### §6 Experimental Methodology
| Claim | Type | Source |
|---|---|---|
| SpamAssassin corpus; MIME preserved; ~16 GB raw; 6,046 processed; selection rationale | OURS + EXTERNAL | PC §5.1; LM ref1 [V] = MS [7] |
| Four preprocessing stages with all thresholds (10 chars; 20×20 px; 1024 B; largest-image tie-break; 224×224 bicubic RGB; timm normalization; tokenizer max_length 256/longest_first/max_length padding) | OURS | PC §5.2 |
| Table 1 composition (all 14 rows verbatim) | OURS | PC §5.3 (Table 1) |
| 99.4% text-only; 11 MM (4 ham/7 spam); 1 IMAGE; 27 EMPTY excluded; 2.19:1 ratio | OURS | PC §5.3 |
| Split 70/15/15, seed 42, stratified, disjoint, sender/campaign controls | OURS | PC §5.4 |
| Five leakage checks; exact+hash dedup full-data; perceptual pilot scope disclosure | OURS | PC §5.5 (verbatim caveat preserved) |
| Eight variants + published-baseline reimplementation (DistilBERT + ResNet-18) framed as one controlled configuration, cited [4]; **variant label unified to "Modality Indicator" (PC names the variant; artifact tables label it Image-Presence)** | OURS | PC §6.1–6.2 |
| Three ablation designs; w_spam formula; gap linkage | OURS | PC §6.3 |
| Metrics (Macro-F1, Ham/Spam F1, Ham PR-AUC, ROC-AUC, Accuracy; MM recomputation) | OURS | PC §6.4 (definition) |
| McNemar with continuity correction [31]; two settings (11 samples; 7,867 pooled OOF); power caveat | OURS + EXTERNAL | PC §6.5; LM ref11 [V] |
| Efficiency measurement list; per-sample vs total-time separation | OURS | PC §6.6 |
| Error-analysis protocol + artifact paths | OURS | PC §6.7 |

### §7 Results (all OURS; every number verbatim from PC)
| MS item | Source |
|---|---|
| Table 2 (9 models × 6 metrics) + narration (0.9827; 0.9862; 0.9869; 0.9868; Image-Only 0.3220 < 0.4000; prior behavior) | PC §7.1 incl. Table 2; source note `results/tables/final_results.csv`. **Phase 6 integrity corrections:** Late Fusion 0.9855→0.9871, DCAT-No-XAttn 0.9862→0.9867, DCAT-Early-Exit 0.9862→0.9867 — transcription errors against the designated source artifact AND the per-seed master record (`experiments/final_results.json`), independently confirmed by `results/tables/seed_summary.csv`; FLOPs units 12.8M/12.7M→12.8B/12.7B per artifact "Avg FLOPs (B)" |
| **Preserved reconciliation note:** Late Fusion 0.9855 (table) vs 0.9871 (three-seed source elsewhere); manuscript uses the authoritative table and cross-references §7.8 | PC §7.1 (instruction converted to transparent note per Phase 4 rules) |
| Table 3 (9 × 3) + narration (majority collapse; No-XAttn exception) | PC §7.2 incl. Table 3; **Phase 6 provenance note added:** values reproduced from `results/tables/main_results_multimodal.csv` (+ `modality_analysis.csv`); PC's summary values for Text-Only/Image-Only MM (0.4968-collapsed / 0.2863) match neither archived table — SOURCE DISCREPANCY disclosed in §7.2, not reconciled |
| **Preserved caveat:** All-Spam Prior accuracy 0.9871 on MM subset inconsistent with 4 ham/7 spam; manuscript uses sample-level counts | PC §7.2 (verbatim caveat) |
| Table 4 + McNemar p = 1.0000 (Full vs Late Fusion), p = 0.2482 (Full vs No-XAttn); α = 0.05; power caveat | PC §7.3 incl. Table 4 (merged into prose; values cross-referenced from Table 3) |
| Table 4 + 0.9862→0.9880; 0.6253→0.7478; p = 2.49×10⁻⁴⁵; p = 3.34×10⁻⁶ | PC §7.4 incl. Table 5 (MS Table 4) |
| Table 5 (4 models, means/stds incl. 0.7077/0.2639; 0.5453/0.1222; 0.5171/0.0597; 0.5564/0.1192) + 8K subset + generalization caveat | PC §7.5 incl. Table 6 (MS Table 5) |
| Table 6 per-fold (incl. 1.0000 in folds 4–5) + source `artifacts/weighted_cv/cv_results.csv` + composition-sensitivity interpretation | PC §7.6 incl. Table 7 (MS Table 6) |
| Table 7 (5 models incl. 77,967,426/428,034/~13B/1.48 ms; 4× trainable 2.01M vs 0.46M; encoder-dominated FLOPs) | PC §7.7 incl. Table 8 (MS Table 7) |
| Table 8 (+24.82% total latency; +88.39% P95; −0.63% FLOPs; 4.45% skip) + measurement-procedure caveat | PC §7.7 incl. Table 9 (MS Table 8) |
| Table 9 per-seed values; std ≤ 0.0003; ordering of means | PC §7.8 incl. Table 10 (MS Table 9) |
| Table 10 (TEXT > 0.986; IMAGE n = 1 sensitivity; MM values) | PC §7.8 incl. Table 11 (MS Table 10) |
| Confusion matrices (DCAT/Late Fusion/Text-Only; 57 FP / 25 FN; FP/FN cost asymmetry); Figure 4 PLACEHOLDER (moved to §7.9 end) | PC §7.10 + Phase 5 editorial restructure |

### §8 Discussion
| Interpretation | Type | Source |
|---|---|---|
| 8.1 full-test explanation: 0.2% cross-attention usage; 11-example training signal; text-shaped decision space | OURS (interpretation, labeled plausible) | PC §8.1 |
| 8.2 No-XAttn MM result; scarcity sensitivity; decoupled-averaging reading; statistical discipline (p = 0.2482 ⇒ observation, not law); collapse pattern | OURS | PC §8.2 |
| 8.3 objective > architecture; significance; scoped conclusion | OURS | PC §8.4 |
| 8.4 savings vs overhead; non-combinable measurements; different-workload not evaluated | OURS | PC §8.5 |
| 8.5 what DCAT does/does not establish; "no full-test advantage from cross-attention; objective mattered"; non-generalization to image-heavy corpora | OURS | PC §8.3, §8.6, §10 |

### §9 Limitations (all OURS, verbatim coverage)
Dataset: 11 MM emails; single corpus; no OCR; single image — PC §9.1. Architecture: frozen encoders; simple fusion; fixed thresholds — PC §9.2. Evaluation: small MM test set; single epoch; no adversarial; **efficiency-measurement uncertainty incl. missing total-time artifact disclosure** — PC §9.3. Threats: internal/construct/external — PC §9.4.

### §10 Conclusion + Future Work
All recap numbers (0.9862/0.9869/0.9871; 0.4968/0.8317; CV 0.7077/0.5453; 0.6253→0.7478; p-values; 4.45%; 0.63%; +24.82%) — PC §10. Seven future-work items — PC §10 Future Work 1–7. Typo "cross-valuation" → "cross-validation" corrected. Final claim ("does not demonstrate a consistent full-test advantage…") — PC §10 verbatim intent.

### Appendices / Back matter
App. A processing parameters — PC App. A (composition rows merged into MS Table 1 per outline E.1). App. B hyperparameters verbatim — PC App. B. App. C lineage table verbatim + **new explicit note** that lineage rows (seed-42 0.9868; CV 0.6609/0.5564/0.6824) use different aggregation settings than headline tables — derived from PC App. C + §7.1 reconciliation instruction, phrased without inventing facts. Data Availability paths — PC §6.7, §7.6, §7.1, App. C.

---

## 2. CITATION LEDGER (MS [n] → LM key → status)

[1] ref3* [V] · [2] ref24* [V] · [3] new6 [V] · [4] ref13* [V] · [5] ref8* [V] · [6] new11 [V] · [7] ref1 [V] · [8] new5 [V] · [9] ref19* [V] · [10] ref18* [V] · [11] ref20* [V] · [12] new1 [V] · [13] ref7* [V] · [14] ref21* [V] · [15] ref4 [V] · [16] ref15* [V] · [17] ref16* [V] · [18] ref17* [V] · [19] new2 [V] · [20] ref5 [V] (arXiv ID corrected to 2110.02178 in Phase 5) · [21] ref6 [V] · [22] ref22* [V] · [23] new3 [V] · [24] new4 [V] · [25] ref9* [V] · [26] ref10* [V] · [27] ref14* [V] · [28] new10 [V] (author list completion pending per LM §1.3) · [29] ref23* [V] · [30] new9 [V] (author list completion pending) · [31] ref11* [V] · [32] ref12* [V] · [33] new8 [V].

**Excluded (LM §1.3/§1.4):** ref2 MDL-SPAM [NV — not registry-verifiable; gap-1 wording made independent of it]; "Deep Delegate" [R]; new7 IEEE Access phishing review [V but page-span pending — dropped as redundant with new6]; all rejected ID guesses. **Supplied papers:** deliberately not cited (smart-contract domain; per LM §8 policy) — their real identities remain available in LM §8 if a venue-context citation is later wanted.

---

## 3. INTEGRITY SUMMARY

- Every number in MS traces to PC (verified section-by-section above; Tables 1–10 and all p-values reproduced verbatim; Phase 5 re-audit passed).
- No experiments, datasets, methods, or settings invented; placeholder symbols restored only from PC Appendix B; Phase 5 changes were presentational only.
- Three caveats preserved verbatim-equivalently: (1) Late Fusion 0.9855 vs 0.9871; (2) All-Spam Prior MM accuracy 0.9871 vs 4h/7s counts; (3) perceptual-leakage pilot scope + missing total-time artifact. Appendix C aggregation differences disclosed, not reconciled.
- Citations: 33 used, all [V] in LM; two carry pending author-list/page completions flagged for the formatting stage.
- Figures 1–4 are marked placeholders (Phase 5 folded the planned F5/F6 content into Figure 4 and re-sited it at §7.9's end); no fake visualizations.
