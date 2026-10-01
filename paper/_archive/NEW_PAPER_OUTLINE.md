# NEW_PAPER_OUTLINE.md — DCAT Paper Architecture (Phase 2 Deliverable)

**Status:** architecture design only. No manuscript text is generated in this phase.

**Source-of-truth contract**

- `PAPER_CONTENT.md` — authoritative for every fact about our research: methodology, architecture, datasets, preprocessing, experiments, metrics, numbers, ablations, efficiency measurements, limitations, conclusions. Nothing below may alter, extend, or reinterpret any of those facts.
- `REFERENCE_STYLE_BLUEPRINT.md` — authoritative **only** for structure, organization, narrative flow, and presentation conventions. No scientific fact may be taken from it.

**Diagnosis in one paragraph.** The current manuscript is a *results ledger*, not a paper: it opens with an unexplained "published baseline," carries no foundational understanding of email as a multimodal medium, defines its method in a skeleton of equations with placeholder corruption, narrates tables in isolation, and sprinkles editorial meta-instructions through the Results. The architecture below rebuilds the paper around a reader who knows nothing of any prior project document: domain → technical background → prior approaches → gap → problem → method → experiment design → evidence → interpretation → honesty about limits.

---

# A. FINAL SECTION HIERARCHY

```
Title: DCAT: A Dynamic Cross-Attention Transformer for Conditional
       Multimodal Email Spam Detection
Abstract (single paragraph, ~250–300 words)
Keywords (5–6, Springer style)

1  Introduction                                              (un-subsectioned)
2  Background
   2.1 Email as a Multimodal Communication Medium
   2.2 Spam, Phishing, and the Modern Threat Landscape
   2.3 Content Representations for Text
   2.4 Content Representations for Images
   2.5 Attention and Cross-Modal Attention
   2.6 Conditional Computation and Early Exits
3  Related Work
   3.1 Text-Based Spam Detection
   3.2 Image-Based Spam Detection
   3.3 Multimodal Spam Detection and Fusion
   3.4 Conditional Computation in Classification Systems
   3.5 Evaluation Practice in Modality-Imbalanced Settings
   3.6 Summary of Gaps
4  Problem Formulation
   4.1 Task Definition
   4.2 Modality Routing
   4.3 Conditional Computation Paths
   4.4 Learning Objective
5  The DCAT Architecture
   5.1 Architecture Overview
   5.2 Text Encoder
   5.3 Vision Encoder
   5.4 Modality Projector
   5.5 Bidirectional Cross-Attention
   5.6 Pooling and Fusion
   5.7 Shared Classifier and Early-Exit Mechanism
   5.8 Training Procedure
   5.9 Inference Pipeline
6  Experimental Methodology
   6.1 Corpus and Preprocessing
   6.2 Dataset Composition, Splits, and Leakage Control
   6.3 Model Variants
   6.4 Ablation Design
   6.5 Evaluation Metrics
   6.6 Statistical Evaluation
   6.7 Efficiency Evaluation
   6.8 Error-Analysis Protocol
7  Results
   7.1 Full-Test-Set Benchmark
   7.2 Multimodal-Subset Results
   7.3 Cross-Attention Ablation
   7.4 Class-Imbalance Ablation
   7.5 Multimodal Robustness: Five-Fold Cross-Validation
   7.6 Per-Fold Behavior
   7.7 Efficiency Results
   7.8 Seed Variance and Modality-Specific Performance
   7.9 Confusion-Matrix Results
8  Discussion
   8.1 Why the Full-Test Metric Barely Moves
   8.2 The Multimodal Subset: Signal, Scarcity, and Sensitivity
   8.3 Class Weighting Changes More than Architecture Does
   8.4 Efficiency: Theoretical Savings versus Measured Overhead
   8.5 What DCAT Does and Does Not Establish
9  Limitations and Threats to Validity
   9.1 Dataset Limitations
   9.2 Architecture Limitations
   9.3 Evaluation Limitations
   9.4 Threats to Validity
10 Conclusion and Future Work
Appendix A  Dataset and Preprocessing Reference
Appendix B  Model Hyperparameters
Appendix C  Results Lineage and Reproducibility
Data Availability / Declarations (back matter)
References
```

Count: **10 top-level sections** (excluding abstract/keywords/appendices/back matter), **36 numbered subsections** (6+6+4+9+8+9+4 = 36; Section 1 and Section 10 intentionally have none), plus 3 appendices. Sub-subsections: **none** — three levels of numbering is unnecessary fragmentation for this paper; depth is created inside subsections, as the extended reference paper does with depth-3 only where a taxonomy demands it.

---

# B. SECTION-BY-SECTION BLUEPRINT

Conventions used below: "Source" = material already in `PAPER_CONTENT.md` (quoted facts must be preserved exactly); "Add" = foundational/contextual prose to be written in Phase 3 (explanatory teaching, never new facts, claims, or experiments); "Cite" = bibliography entries that will be needed (references exist in the current bibliography unless marked *new-lookup*); RQ = research question the section answers for the reader.

## 1. Introduction
- **Purpose:** establish the problem, the gap, and the contribution in ~5–6 paragraphs, self-contained.
- **RQ addressed:** "Why does email spam need conditional multimodal detection, and what does this paper contribute?"
- **Content:** (P1) email as dominant asynchronous communication; spam as persistent security problem [cite: spam survey ref3]; images now carry spam signals (promotional graphics, phishing screenshots, rendered text). (P2) two structural realities of real corpora: modality heterogeneity (text-only majority) and multimodal scarcity — the two conditions that shape this work. (P3) existing approaches process modalities independently and fuse late; cross-modal interaction exists in vision-language work but is unproven under multimodal scarcity; unconditional vision computation wastes work on text-only mail. (P4) DCAT in one paragraph: bidirectional cross-attention + deterministic routing + optional early exit, evaluated on a naturally paired corpus with multi-seed, ablations, CV, statistics, efficiency. (P5) contribution bullets (five, from the current contribution list, tightened to one sentence each). (P6) roadmap paragraph (current wording is already correct and kept).
- **Source:** Abstract paragraphs 1–2 (facts only), Intro P1–P5, contribution list, roadmap paragraph.
- **Add:** one or two sentences of domain framing per paragraph; nothing else.
- **Depth:** ~1–1.25 pages. No figures/tables/equations.
- **Cite:** ref3 (spam review) at minimum; optionally ref13 mention-free (keep names out of intro; reference only the phenomenon).
- **Reader understands:** the problem, the two corpus conditions, the three design ideas, the five contributions, the paper's map.
- **Transition:** roadmap paragraph hands off to Background/Related Work.

## 2. Background
- **Purpose:** teach exactly the concepts the method needs, progressively — the "progressive foundation" layer absent from the current manuscript. It is a *concept* chapter; attribution of specific prior *systems* is deferred to Section 3.
- **RQ addressed:** "What do I need to know before I can understand the method?"
- **Depth target:** ~2.5–3 pages total; each subsection 2–4 paragraphs; ends each subsection at the exact point the architecture will pick up.

### 2.1 Email as a Multimodal Communication Medium
- **Content (Add):** MIME structure of email (headers, text bodies, HTML parts, inline images, attachments); why a single message is naturally a bundle of modality-bearing parts; HTML-to-text and image extraction as the practical consequence. Ends by defining text-only / image-only / multimodal messages.
- **Source:** vocabulary used by §5.1–5.2 of the manuscript (MIME structure, `.eml`, inline images, attachments).
- **Cite:** none strictly required; MIME/MHTML specification *new-lookup* optional.
- **Reader understands:** where text and images in an email physically come from — prerequisite for §5.1 routing and §6.1 preprocessing.

### 2.2 Spam, Phishing, and the Modern Threat Landscape
- **Content (Add + Source):** definition of spam vs phishing (spam = volume/unsolicited; phishing = deceptive credential capture; overlap is real and the boundary is blurred); campaign behavior; image-based spam rationale (filter evasion, rendered text); why the spam decision can live in the image.
- **Source:** Intro P1 ("promotional images, phishing screenshots, brand graphics"), §2.2 sentence 1–2 of the manuscript.
- **Cite:** ref3, ref24.
- **Reader understands:** what the positive class really is, and why image content is evidentiary, not decorative.

### 2.3 Content Representations for Text
- **Content (Add):** from bag-of-words/TF-IDF → word embeddings → CNN/LSTM text classifiers → pretrained transformer encoders; tokenization; contextual embeddings; what "frozen encoder" means (feature extractor).
- **Source:** terms used in §4.2 and §5.2 Stage 4 (DistilBERT tokenizer, `max_length=256`, attention masks).
- **Cite:** ref7 (BERT), ref4 (DistilBERT), ref18, ref19, ref20 as the progression.
- **Reader understands:** what DistilBERT consumes and emits; why the text pathway alone can classify email.

### 2.4 Content Representations for Images
- **Content (Add):** CNN feature hierarchies; modern encoders (VGG/ResNet/MobileNet) and vision transformers; resizing/normalization as interface contracts; spatial feature maps vs pooled vectors.
- **Source:** terms used in §4.3, §5.2 Stage 3 (224×224, RGB, bicubic, `timm` normalization).
- **Cite:** ref15, ref16, ref17, ref5 (MobileViT), ref6 (`timm`).
- **Reader understands:** what MobileViT consumes and emits; why preprocessing must match the pretrained model's expectations.

### 2.5 Attention and Cross-Modal Attention
- **Content (Add):** attention as learned alignment (Q/K/V in words and one general equation), self- vs cross-attention, bidirectional co-attention, multi-head attention; why one modality's representation can become a function of the other.
- **Source:** conceptual content of manuscript §2.4 (rewritten as neutral background; the DCAT-specific comparison moves to §5.5).
- **Cite:** ref22 (attention), ref8 (ViLBERT), ref9, ref10.
- **Equations:** **Eq. (1)** general scaled dot-product attention (background-level, generic form). Numbering starts here so §5 can continue the sequence.
- **Reader understands:** exactly what "bidirectional cross-attention" will mean in §5.5.

### 2.6 Conditional Computation and Early Exits
- **Content (Add):** the idea of input-dependent computation; early-exit classifiers; routing as deterministic conditional computation; the cost/benefit tension (skipped work vs branch overhead) — no numbers here, those live in Results.
- **Source:** conceptual content of manuscript §2.5.
- **Cite:** ref23 (BranchyNet).
- **Reader understands:** what an "early exit" is before §5.7 uses the term.

## 3. Related Work
- **Purpose:** situate DCAT among approach families; end with the aggregate gap. No system is the paper's anchor; no ranking tables.
- **RQ addressed:** "What has been done, what has not, and where exactly is the opening?"

### 3.1 Text-Based Spam Detection
- **Content (Source):** manuscript §2.1 nearly verbatim (rule-based/SpamAssassin ref1; classical classifiers ref2; deep text classifiers ref18–ref20; transformer encoders ref7/ref21/ref4; the DistilBERT cost rationale). **Add:** one closing sentence tying to this paper's design choice (frozen DistilBERT).
- **Cite:** ref1, ref2, ref18, ref19, ref20, ref7, ref21, ref4.

### 3.2 Image-Based Spam Detection
- **Content (Source):** manuscript §2.2 (CNN visual patterns ref24; VGG/ResNet/MobileNet as components ref15–ref17; the ambiguity limitation of image-only classification). **Add:** one sentence on why image-only remains a weak primary signal.
- **Cite:** ref24, ref15, ref16, ref17.

### 3.3 Multimodal Spam Detection and Fusion
- **Content (Source):** manuscript §2.3 (late fusion as standard; MMTD ref13; MDL-SPAM ref2; attention/gating fusion families; the corpus-distribution warning paragraph). **Add:** one closing sentence positioning bidirectional token-level cross-attention as the under-explored point for email.
- **Cite:** ref13, ref2, ref14 (gated multimodal units; already in bibliography).

### 3.4 Conditional Computation in Classification Systems
- **Content (Source):** manuscript §2.5's literature half (early exit ref23) plus the deterministic-routing observation. **Add:** one sentence noting that input-conditional *modality* selection is a special, simple case suited to email structure.
- **Cite:** ref23.

### 3.5 Evaluation Practice in Modality-Imbalanced Settings
- **Content (Source):** manuscript §2.6 (full-test metric can mask multimodal failure; small-subset F1 volatility; paired statistics via McNemar ref11). **Add:** two sentences framing this as an evaluation-methodology contribution area, not just a caveat.
- **Cite:** ref11, ref3 (dataset-shift discussion, already cited for spam review).

### 3.6 Summary of Gaps
- **Content (Add, derived strictly from Source):** a short enumerated gap statement: (i) cross-modal interaction largely unexplored for email spam; (ii) unconditional vision computation ignores text-only-dominated corpora; (iii) class imbalance in multimodal subsets under-treated; (iv) evaluation rarely separates full-test from multimodal-subset views or reports significance and variance. One paragraph, four numbered gaps — the contract for the rest of the paper.
- **Cite:** none needed; it compresses 3.1–3.5.
- **Transition:** gap list → "This paper addresses these gaps as follows" is implicit in §4–§6 ordering; §4 formally defines the problem.

## 4. Problem Formulation
- **Purpose:** formalize task, routing, paths, and objective before any architecture detail.
- **RQ addressed:** "Precisely what problem is solved, and what is optimized?"
- **Source:** manuscript §3 entirely (task definition; the four modality categories; EMPTY excluded; routing is deterministic, no learned classifier; three computation paths; BCE objective; weighted objective; w_pos = N_ham/N_spam).
- **Add:** connective prose only ("The routing rule is deliberately deterministic because…" — no new claims).
- **Equations:** **Eq. (2)** routing rule (piecewise); **Eq. (3)** BCE loss; **Eq. (4)** weighted BCE; **Eq. (5)** w_pos. All carried from the current manuscript; all placeholders (the `$p < 10^{-44}$N__` artifacts) restored to their original symbols: N, ŷ_i/z_i, σ, y_i, w_pos, i, d_model, 256, mask, B, 224, x_img, S, 15, d_model = 256 (see C.14 and F).
- **Figures:** none. **Tables:** none.
- **Reader understands:** inputs, modalities, output, loss; can state why EMPTY is excluded and why routing is not learned.
- **Transition:** "Having defined the objective, we now describe the architecture that realizes it."

## 5. The DCAT Architecture
- **Purpose:** staged, figure-anchored methodology — what → why → how per component, with every dimension stated.
- **RQ addressed:** "How does DCAT work, and could I re-implement it?"
- **Source:** manuscript §4 entirely (five components; DistilBERT-base-uncased 6-layer/768-d frozen; MobileViT-small via `timm`, 224×224, frozen; projector to shared latent space, LayerNorm; L=2 cross-attention layers, h=4, d_k=64, Pre-LN ref12; residual updates with MLP; mean pooling; element-wise average fusion to d_model; shared classifier on all paths; auxiliary classifier thresholds 0.95/0.05 trained jointly; AdamW lr 1e-4, cosine schedule, FP16 AMP, batch 64, 1 epoch, deterministic seeding; 73,309,090 total / 2,008,578 trainable = 2.74%; six-step inference pipeline).
- **Add:** per-component "why this component" sentences drawn only from already-present facts (frozen encoders ⇒ 2.74% trainable; fusion averages instead of concatenates ⇒ d_model vs 2·d); a walked example of the multimodal path; no new design claims.
- **Figures:** **Fig. 1** DCAT architecture overview (three computation paths, early-exit branch marked) in §5.1; **Fig. 2** bidirectional cross-attention detail (Q/K/V flows, residual MLP, Pre-LN) in §5.5. *(Both are listed as `[FIGURE: …]`/absent in the current manuscript and must be drawn in Phase 3 — flagged as unresolved in the final report.)*
- **Tables:** none (hyperparameters live in Appendix B).
- **Equations:** **Eq. (6)** H_text; **Eq. (7)** H_img; **Eq. (8–9)** projections Z_text, Z_img; **Eq. (10–11)** Q/K/V for the two directions; **Eq. (12–13)** attended representations; **Eq. (14–15)** residual updates (the current manuscript's missing closing brace and the "computed analogously" shortcut are both made explicit); **Eq. (16–17)** mean pooling and fusion; **Eq. (18)** classifier; **Eq. (19)** auxiliary exit probability; **Eq. (20)** exit rule (piecewise ≥0.95 / ≤0.05). Inline math otherwise.
- **Reader understands:** end-to-end flow and every interface dimension; where the 2.74% trainable parameters live; when the vision encoder runs.
- **Transition:** "The architecture defines *what* is computed; the next section defines *how it is evaluated*."

## 6. Experimental Methodology
- **Purpose:** complete, reproducible experiment design, cleanly separated from outcomes.
- **RQ addressed:** "What exactly was measured, on what data, under what protocol?"

### 6.1 Corpus and Preprocessing
- **Source:** manuscript §5.1 (SpamAssassin public corpus ref1; MIME preserved; 6,046-email processed subset; ~16 GB raw; selection rationale) and §5.2 (four deterministic stages: MIME parsing via Python `email`; BeautifulSoup/lxml HTML-to-text; ≥10-char text rule; ≥20×20 px and ≥1024-byte image rule with drop-reason logging; largest-image selection with pixel-area tie-break; 224×224 bicubic RGB + `timm` normalization; DistilBERT tokenization max_length=256, longest_first, max_length padding).
- **Add:** one framing sentence; a numbered pipeline description is already present — keep as prose+list.
- **Figures:** **Fig. 3** preprocessing/data-flow diagram (raw `.eml` → four stages → routed dataset) *(must be drawn in Phase 3)*.
- **Cite:** ref1, ref6.

### 6.2 Dataset Composition, Splits, and Leakage Control
- **Source:** manuscript §5.3 (full composition: 6,046 total; 4,150 ham / 1,896 spam; 6,007 TEXT / 11 MULTIMODAL / 1 IMAGE / 27 EMPTY; TEXT ham 4,146 / TEXT spam 1,861; MM ham 4 / MM spam 7; 2.19:1 ratio; 99.4% text-only; EMPTY excluded), §5.4 (70/15/15, seed 42, stratified, disjoint subsets, sender/campaign leakage controls), §5.5 (five leakage checks; exact+hash dedup on full data; perceptual pilot on limited subset; the pilot's stated interpretation boundary). **Table 1** = current Table 1 (composition), renumbered as **Table 1**.
- **Add:** nothing factual; one sentence introducing the table.
- **Note:** Appendix A duplicates Table 1 → merged here (see E.1); Appendix A keeps only the processing-parameters block (tokens/resolution/split).

### 6.3 Model Variants
- **Source:** manuscript §6.2: the eight variants (All-Spam Prior; Modality Indicator; Text-Only; Image-Only; Late Fusion; DCAT-No-XAttn; Full-DCAT; DCAT-Early-Exit) plus the published-baseline reimplementation sentence (late fusion of DistilBERT + ResNet-18). **Add:** a variant table is NOT introduced here (it would duplicate §7.1's table); instead one paragraph per *family*: sanity priors / unimodal / fusion / DCAT family. The phrase "published baseline" becomes "a reimplementation of a published late-fusion architecture [ref13]" — cited, defined once, never again structurally central.

### 6.4 Ablation Design
- **Source:** manuscript §6.3 (cross-attention ablation = Late Fusion vs DCAT-No-XAttn vs Full-DCAT on the multimodal subset; imbalance ablation = unweighted vs weighted BCE with w_spam = N_ham/N_spam; early-exit ablation = Full vs Early-Exit on latency/FLOPs/skip rate). **Add:** one sentence each stating *which gap* (§3.6) the ablation addresses — architecture ↔ gap contract.

### 6.5 Evaluation Metrics
- **Source:** manuscript §6.4 (Macro-F1 = unweighted mean of ham-F1 and spam-F1; Ham F1; Spam F1; Ham PR-AUC; ROC-AUC; Accuracy; multimodal recomputation). **Add:** **Eq. (21)** Macro-F1 as the weighted harmonic-mean form (standard definition, no new claim). Metrics are defined here, used in §7 — the current manuscript never defines them formally.

### 6.6 Statistical Evaluation
- **Source:** manuscript §6.5 (McNemar ref11 with continuity correction; two settings: ~11-sample multimodal subset and 7,867-sample pooled out-of-fold; explicit power limitation). **Add:** **Eq. (22)** McNemar statistic with continuity correction (standard form).

### 6.7 Efficiency Evaluation
- **Source:** manuscript §6.6 (parameter counts; approximate FLOPs; per-sample and P95 latency; vision skip rate; FLOP reduction; per-sample vs total-time measured separately).

### 6.8 Error-Analysis Protocol
- **Source:** manuscript §6.7 (confusion matrices for main variants, FP/FN/cross-model disagreement; artifacts at `artifacts/error_analysis/dcat_errors.csv` and `late_fusion_errors.csv`).
- **Transition:** "The next section reports the outcomes of this protocol."

## 7. Results
- **Purpose:** outcomes only, organized by research question; every table introduced, best values marked, numbers narrated verbatim; zero editorial meta-instructions in prose (all provenance moves to prose "source" notes or Appendix C).
- **RQ addressed:** per-subsection, below.

### 7.1 Full-Test-Set Benchmark — RQ: "How do all variants compare when evaluated on the entire corpus?"
- **Source:** current Table 2 (nine models × six metrics, 3-seed means) → **Table 2**; narrative from §7.1 (Text-Only 0.9827; Late Fusion 0.9855 with the documented 0.9871 reconciliation note; Full DCAT 0.9862; Published Baseline 0.9869; DCAT-No-XAttn 0.9868; Image-Only 0.3220 below the 0.4000 All-Spam prior; encoder-dominated FLOPs). The in-file reconciliation instruction is preserved as an explicit source-consistency note in prose or Appendix C — **never silently resolved** (see C.14, unresolved item).
- **Figure:** **Fig. 4** Macro-F1 bar chart across variants (optional, only if drawn in Phase 3).

### 7.2 Multimodal-Subset Results — RQ: "What happens on the 11 multimodal emails?"
- **Source:** current Table 3 → **Table 3**; narrative (most models collapse to the All-Spam behavior 0.4968 / Ham-F1 0.0000; DCAT-No-XAttn 0.8317/0.6667 exception; the 0.9871-accuracy vs 4-ham/7-spam reconciliation note preserved as an explicit caveat).

### 7.3 Cross-Attention Ablation — RQ: "Does bidirectional cross-attention help on multimodal inputs?"
- **Source:** current Table 4 → **Table 4**; narrative (Late Fusion and Full DCAT identical 0.4968; DCAT-No-XAttn 0.8317; McNemar p=1.0000 Full vs Late Fusion, p=0.2482 Full vs No-XAttn; neither < α=0.05; ~11 samples ⇒ limited power).

### 7.4 Class-Imbalance Ablation — RQ: "Does class weighting matter more than architecture?"
- **Source:** current Table 5 → **Table 5**; narrative (full-test 0.9862→0.9880; MM 0.6253→0.7478; pooled OOF McNemar p=2.49×10⁻⁴⁵ vs Full-DCAT, p=3.34×10⁻⁶ vs Late Fusion).

### 7.5 Multimodal Robustness: Five-Fold Cross-Validation — RQ: "Is the multimodal signal stable?"
- **Source:** current Table 6 → **Table 6** (DCAT-No-XAttn 0.5171±0.0597; Full DCAT 0.7077±0.2639; Late Fusion 0.5453±0.1222; Published Baseline 0.5564±0.1192); narrative (highest mean, highest variance; folds from 1.0000 to prior-level; generalization explicitly limited).

### 7.6 Per-Fold Behavior — RQ: "Where does the variance come from?"
- **Source:** current Table 7 → **Table 7** (fold-level values incl. 1.0000 in folds 4–5; source `artifacts/weighted_cv/cv_results.csv`); interpretation limited to sensitivity-to-composition.

### 7.7 Efficiency Results — RQ: "What does conditional computation actually save?"
- **Source:** current Table 8 → **Table 8** (params/FLOPs/latency incl. Published Baseline 77,967,426 params / 428,034 trainable / ~13B / 1.48 ms; Full DCAT 73,309,090 / 2,008,578 / ~13B / 2.70 ms) and Table 9 → **Table 9** (early-exit: +24.82% total latency, +88.39% P95, −0.63% FLOPs, 4.45% skip); narrative incl. the 2.01M vs 0.46M trainable comparison and the measurement-procedure caveat.

### 7.8 Seed Variance and Modality-Specific Performance — RQ: "How stable are the headline numbers?"
- **Source:** current Table 10 → **Table 10** (per-seed values, std ≤0.0003) merged narratively with current Table 11 → **Table 11** (modality-specific Macro-F1, seed 42; IMAGE n=1 caveat). Merging two thin tables' *narration* is allowed; the tables themselves remain separate (different conditions).

### 7.9 Confusion-Matrix Results — RQ: "What kinds of errors remain?"
- **Source:** manuscript §7.10 (matrices for DCAT, Late Fusion, Text-Only on full test and multimodal subset + Macro-F1 comparison plot; weighted-primary DCAT 57 FP / 25 FN on full test). **Fig. 5** confusion-matrix panel and **Fig. 6** Macro-F1 comparison plot *(must be drawn in Phase 3)*.

## 8. Discussion
- **Purpose:** interpretation, organized by finding; no new numbers.
- **RQ addressed:** "What do the results mean?"
- **Source:** manuscript §8.1–8.6 nearly intact, retitled and lightly resequenced:
  - **8.1 Why the Full-Test Metric Barely Moves** ← §8.1 (99.4% text-only; cross-attention exercised on ~0.2% of data; shared classifier shaped by text-dominated batches).
  - **8.2 The Multimodal Subset: Signal, Scarcity, and Sensitivity** ← §8.2 (11 samples; No-XAttn's decoupled averaging less sensitive to scarce interaction signal; p=0.2482 ⇒ treat as observation, not law).
  - **8.3 Class Weighting Changes More than Architecture Does** ← §8.4 (loss change > architecture change on multimodal metrics; scoped conclusion).
  - **8.4 Efficiency: Theoretical Savings versus Measured Overhead** ← §8.5 (branch/aux overhead vs FLOP saving; per-sample vs total-time non-combinable; different-workload case not evaluated).
  - **8.5 What DCAT Does and Does Not Establish** ← §8.3 (text-dominated corpus framing; no generalization to image-heavy corpora) + §8.6 (the two protocols give different views of the architecture) + the honest bottom line already present in the Conclusion.
  - The old §8.6 "Comparison to Prior Work" content is absorbed here as two sentences inside 8.5 — the comparison is a finding about the architecture, not a section (see E.4).
- **Transition:** "These interpretations are bounded by the following limitations."

## 9. Limitations and Threats to Validity
- **Source:** manuscript §9.1–9.4 essentially verbatim (dataset: 11 multimodal, single corpus, no OCR, single-image; architecture: frozen encoders, average fusion, fixed thresholds; evaluation: small test subset, single epoch, no adversarial eval, efficiency-measurement uncertainty with the missing-artifact disclosure; threats: internal/construct/external). No additions — this section is already honest and complete.

## 10. Conclusion and Future Work
- **Purpose:** two-paragraph recap + findings + explicit future-work list (the extended reference paper's conclusion shape, which our current draft already matches).
- **Source:** manuscript §10 (six recap paragraphs condensed to two) + Future Work items 1–7 (corpus expansion; OCR; encoder fine-tuning; multi-image; learned routing; contrastive pre-training; larger-scale efficiency analysis). Fix typo "cross-valuation" → "cross-validation". No new results.

## Appendices (retained)
- **Appendix A — Dataset and Preprocessing Reference:** processing-parameters block only (256 tokens; 224×224; 70/15/15; seeds) — composition table merged into §6.2 (E.1).
- **Appendix B — Model Hyperparameters:** current Appendix B verbatim (the authoritative settings table; resolves every placeholder symbol in §5).
- **Appendix C — Results Lineage and Reproducibility:** current Appendix C verbatim (lineage table incl. the seed-42 0.9868 / 10% split entry and artifact paths) — this is where the §7.1 reconciliation note points.

## Back matter
Data Availability (from repository layout; artifact paths already cited in-text), Declarations/Competing interests, (template-dependent) Publisher notes — per blueprint §2.2/§4. References: current 24-entry IEEE-style list retained and extended per §G; renumber in citation order at write time.

---

# C. CONTENT PRESERVATION MAP

Legend: §-numbers on the right are the new architecture. "✓" = preserved verbatim or with connective prose only. Every substantive item in `PAPER_CONTENT.md` is mapped.

| # | Item (source location) | Destination | Status |
|---|---|---|---|
| C.1 | Abstract P1–P2 facts (all headline numbers) | Abstract (rewritten, same numbers) | ✓ |
| C.2 | Intro P1–P5 + 5 contributions + roadmap | §1 | ✓ |
| C.3 | §2.1 text-detection literature (ref1,2,18,19,20,7,21,4) | §3.1 | ✓ |
| C.4 | §2.2 image-detection content + ambiguity limitation (ref24,15,16,17) | §2.2 (concept) + §3.2 (literature) | ✓ |
| C.5 | §2.3 multimodal literature (ref13, ref2; attention/gating; corpus-distribution warning) | §3.3 | ✓ |
| C.6 | §2.4 cross-attention background (ref22,8,9,10) | §2.5 (concept) + §3.3 (ViLBERT lineage) | ✓ |
| C.7 | §2.5 conditional computation (ref23; 0.95/0.05 fact → §5.7) | §2.6 (concept) + §3.4 + §5.7 | ✓ |
| C.8 | §2.6 evaluation challenges + McNemar | §3.5 + §6.6 | ✓ |
| C.9 | §3.1 task definition (m, t, I₁..I_K, y∈{0,1}) | §4.1 | ✓ |
| C.10 | §3.2 routing rule + four categories + EMPTY exclusion + determinism | §4.2 | ✓ |
| C.11 | §3.3 three computation paths | §4.3 (+ Fig. 1 encodes them) | ✓ |
| C.12 | §3.4 BCE, weighted BCE, w_pos = N_ham/N_spam | §4.4 (Eqs. 3–5) | ✓ |
| C.13 | §4.1 five components + placeholder dims | §5.1 | ✓ |
| C.14 | §4.2–4.7 all component math and every dimension (768, 256, d_model, 224, S, 15, h=4, d_k=64, L=2, Pre-LN) | §5.2–5.7 (Eqs. 6–18) | ✓ |
| C.15 | §4.8 early-exit mechanism (0.95/0.05; joint training; separate aux classifier) | §5.7 (Eqs. 19–20) | ✓ |
| C.16 | §4.9 training procedure (AdamW 1e-4, cosine, AMP FP16, batch 64, 1 epoch, freezing, seeding) + 73,309,090 / 2,008,578 / 2.74% | §5.8 + Appendix B | ✓ |
| C.17 | §4.10 six-step inference pipeline | §5.9 | ✓ |
| C.18 | §5.1 corpus facts (6,046; 16 GB; MIME; rationale; ref1) | §6.1 | ✓ |
| C.19 | §5.2 four-stage preprocessing (all thresholds: 10 chars; 20×20 px; 1024 B; largest-image tie-break; 224×224 bicubic RGB; tokenizer settings) | §6.1 | ✓ |
| C.20 | §5.3 full composition table + ham/spam 2.19:1 + 99.4% TEXT + MM 4 ham/7 spam | §6.2 (Table 1) | ✓ |
| C.21 | §5.4 split strategy (70/15/15, seed 42, stratified, disjoint, sender/campaign controls) | §6.2 | ✓ |
| C.22 | §5.5 leakage checks + perceptual-pilot scope disclosure | §6.2 | ✓ |
| C.23 | §6.1 protocol (3 seeds 42/43/44; 1 epoch; frozen encoders; 0.5 threshold) | §6.3 preamble | ✓ |
| C.24 | §6.2 eight variants + published-baseline reimplementation sentence | §6.3 | ✓ (renamed & cited) |
| C.25 | §6.3 three ablation designs + w_spam formula | §6.4 | ✓ |
| C.26 | §6.4 six metrics + multimodal recomputation | §6.5 (Eq. 21) | ✓ |
| C.27 | §6.5 McNemar with continuity correction; two settings; ~11 and 7,867 sample counts; power caveat | §6.6 (Eq. 22) | ✓ |
| C.28 | §6.6 efficiency measurement list + per-sample/total-time separation | §6.7 | ✓ |
| C.29 | §6.7 error-analysis protocol + artifact paths | §6.8 | ✓ |
| C.30 | Table 2 full-test results (9×6) + narration + Image-Only 0.3220 < 0.4000 | §7.1 (Table 2) | ✓ |
| C.31 | Late Fusion 0.9855 vs 0.9871 reconciliation instruction | §7.1 prose note + Appendix C pointer | ✓ (explicit, unresolved) |
| C.32 | Table 3 multimodal subset (9×3) + narration + 0.9871-accuracy caveat (4 ham/7 spam) | §7.2 (Table 3) | ✓ (explicit caveat) |
| C.33 | Table 4 cross-attention ablation + p=1.0000, p=0.2482, α=0.05, power note | §7.3 (Table 4) | ✓ |
| C.34 | Table 5 imbalance ablation + p=2.49×10⁻⁴⁵, p=3.34×10⁻⁶ | §7.4 (Table 5) | ✓ |
| C.35 | Table 6 5-fold CV means/stds (4 models) + variance narrative | §7.5 (Table 6) | ✓ |
| C.36 | Table 7 per-fold values + cv_results.csv source + fold 4–5 = 1.0000 | §7.6 (Table 7) | ✓ |
| C.37 | Table 8 efficiency (5 models incl. Published Baseline row) + 2.01M vs 0.46M trainable + ~13B FLOPs rationale | §7.7 (Table 8) | ✓ |
| C.38 | Table 9 early-exit details (+24.82%, +88.39%, −0.63%, 4.45%) + measurement-procedure caveat | §7.7 (Table 9) | ✓ |
| C.39 | Table 10 3-seed variance (≤0.0003; per-seed values) | §7.8 (Table 10) | ✓ |
| C.40 | Table 11 modality-specific Macro-F1 (seed 42; IMAGE n=1 caveat) | §7.8 (Table 11) | ✓ |
| C.41 | §7.10 confusion matrices + 57 FP / 25 FN | §7.9 (Figs. 5–6) | ✓ |
| C.42 | §8.1–8.6 all six discussion threads (incl. §8.6 baseline comparison) | §8.1–8.5 (§8.6 absorbed) | ✓ |
| C.43 | §9.1–9.4 limitations, incl. missing-artifact disclosure | §9.1–9.4 | ✓ |
| C.44 | §10 conclusion + 7 future-work items | §10 | ✓ (typo fixed) |
| C.45 | Appendix A composition rows | §6.2 Table 1 (merged) | ✓ |
| C.46 | Appendix A processing-parameter rows | Appendix A | ✓ |
| C.47 | Appendix B hyperparameters | Appendix B | ✓ |
| C.48 | Appendix C lineage table + artifact paths | Appendix C | ✓ |
| C.49 | References 1–24 | References (renumbered) | ✓ |

**No important evidence is lost.** The only removals are duplications and structural scaffolding (E below); every number, threshold, ratio, p-value, artifact path, and caveat survives.

---

# MEANINGFUL LENGTH STRATEGY

Target: a full-length journal paper (~14–20 formatted pages) achieved **only** through the seven legitimate depth channels below. Each item states what meaningful depth adds versus what filler would look like, so Phase 3 can audit itself.

1. **Foundational explanation (§2, ~2.5–3 pp).**
   *Meaningful:* teaching MIME-structured email, spam-vs-phishing, representation learning for text and images, attention/cross-attention, conditional computation — each anchored to a component used later, each 2–4 paragraphs, each ending where §5 picks up.
   *Filler to reject:* textbook history of email; generic "deep learning is revolutionizing…" chapters; definitions of classification/accuracy at tutorial level; any paragraph not used later.

2. **Technical background in Related Work (§3, ~2–2.5 pp).**
   *Meaningful:* per-family evolution with citations; each paragraph ending in its implication for DCAT; §3.6 compressing into four testable gaps.
   *Filler to reject:* paragraph-per-paper listings of works never used again; restating §2 concepts with citations; ranking tables of prior papers.

3. **Detailed methodology (§5, ~3.5–4.5 pp).**
   *Meaningful:* what→why→how per component; every dimension stated (768, 256, 224, S, 15, h=4, d_k=64, L=2, 2.74% trainable); two architecture figures; walked multimodal-path example; equations 6–20.
   *Filler to reject:* restating Appendix B in prose; pseudo-code duplicating Fig. 1; marketing adjectives ("powerful", "novel state-of-the-art").

4. **Complete experimental documentation (§6, ~2.5–3 pp).**
   *Meaningful:* all thresholds (10 chars, 20×20 px, 1024 B), split/seed/stratification details, leakage-check scope disclosure, the eight variants each tied to a purpose, metric/statistic definitions as equations.
   *Filler to reject:* restating the same protocol per results subsection; narrating obvious steps ("we saved the CSV").

5. **Meaningful result analysis (§7, ~3.5–4 pp).**
   *Meaningful:* every table introduced and narrated verbatim; best values marked; each subsection answering its RQ; measurement-procedure caveats stated where they exist.
   *Filler to reject:* re-quoting entire tables in prose; repeating the same sentence per model; duplicate rows for the same metric.

6. **Discussion (§8, ~1.5–2 pp).**
   *Meaningful:* causal explanations already present in the source (corpus dominance, scarcity sensitivity, objective-vs-architecture contrast, overhead-vs-savings) written out in full arguments.
   *Filler to reject:* restating Results numbers; speculative claims not supported by any experiment.

7. **Limitations + academically useful context (§9–§10, ~1.5 pp).**
   *Meaningful:* the four validity categories; future work tied one-to-one to limitations.
   *Filler to reject:* apology paragraphs; future work unconnected to any observed limitation.

**Arithmetic sanity check:** 1 + 3 + 2.25 + 1 + 4 + 2.75 + 3.75 + 1.75 + 1.5 ≈ **21 pp** of body + front/back matter — in range without a single padded paragraph. If Phase 3 lands shorter, the correct response is tighter writing, not added filler.

---

# E. CONTENT CONSOLIDATION PLAN

**Merge**
- **E.1** Appendix A's composition table = §5.3/Table 1 → merged into §6.2. Reason: exact duplicate of the same facts; two copies invite divergence.
- **E.2** §7.8 (seed variance) and §7.9 (modality-specific) narrated together under one subsection heading — two separate tables retained (different conditions), one shared interpretation.
- **E.3** §2.4 (cross-attention background) splits: concept → Background 2.5; the ViLBERT-lineage citations → Related Work 3.3. Reason: concept-vs-attribution separation is the core fix of this architecture.

**Shorten**
- **E.4** §8.6 "Comparison to Prior Work" (~1 page of prose around one contrast) → two sentences inside Discussion 8.5. Reason: the finding is "the two protocols give different views of the architecture"; it does not need a prior-work section. **This is the single biggest de-comparison move.**
- **E.5** Intro P3 (prior-approaches paragraph) → 2–3 sentences. Reason: the literature belongs in §3; the intro needs only the gap.
- **E.6** Abstract P2: keep all numbers, drop the narrative recap of ablations that §7 will repeat. Reason: abstract states findings, not the full result tree.
- **E.7** §10's six recap paragraphs → two paragraphs. Reason: the blueprint's conclusion shape; no new information is lost (every claim already appears in §7–§8).

**Move**
- **E.8** 0.95/0.05 thresholds: mentioned in §2.5 of the source (background) and §4.8 (method) → methodology only (§5.7). Reason: concrete operating parameters live in method; background keeps only the concept.
- **E.9** "The early-exit path is triggered when…" detail from source-Background → §5.7 (same as E.8).
- **E.10** Metric narration currently embedded in Results prose that interprets ("plausible explanations for why…") stays in Results as factual observations; *causal* interpretation moves to §8. Boundary rule: results state what happened; discussion states why.
- **E.11** Appendix C's lineage table stays in Appendix C, but §7.1's "Source: results/tables/final_results.csv" style notes point to it once, in prose. Reason: provenance discoverable without cluttering every table.

**Remove**
- **E.12** All editorial meta-instructions inside Results prose ("the final manuscript should use the authoritative source table consistently…", "should not be interpreted as evidence of…"). The **factual caveats they encode are preserved** as explicit statements (C.31, C.32); only the self-referential instruction language is dropped. Reason: a manuscript cannot contain instructions to itself.
- **E.13** Source-artifact path annotations currently pasted under tables ("Source: …") → moved to a single provenance note + Appendix C. Reason: format, not fact.
- **E.14** Duplicate empty-line-ridden pseudo-tables (the non-piped Table 2/3 renderings) → replaced by proper single versions. No fact lost (rows are identical).

**Convert**
- **E.15** The eight variants (§6.2 prose list) → **Table: variant configurations** in §6.3 (variant × components used × fusion × objective) *if* Phase 3 needs it; otherwise prose remains acceptable. Decision deferred, flagged.
- **E.16** The four-stage preprocessing pipeline → **Fig. 3** (flow diagram) + compact prose. Reason: pipelines are shapes, not paragraphs.
- **E.17** The modality-routing piecewise rule already is an equation — retained as Eq. (2), illustrated inside Fig. 1 rather than given a second figure.

**Nothing is removed that carries evidence.** Removals are: duplicates (E.1, E.14), self-instructions (E.12), format scaffolding (E.13), and over-length prose whose facts are preserved elsewhere (E.4–E.7).

---

# F. FIGURE / TABLE / EQUATION PLAN

**Figures**

| ID | Location | Purpose | Question answered | Surrounding discussion | Narrative role |
|---|---|---|---|---|---|
| Fig. 1 | §5.1 | DCAT architecture: three paths, early-exit branch, shared classifier | How do the paths differ and when does the vision encoder run? | Walked example of a MULTIMODAL email through the graph | Anchors all of §5 |
| Fig. 2 | §5.5 | Cross-attention block detail: Q/K/V, residuals, MLP, Pre-LN | What exactly is exchanged between modalities? | Ties Eqs. 10–15 to the diagram | Justifies the ablation axis |
| Fig. 3 | §6.1 | Preprocessing/data flow: `.eml` → parse → filter → image → tokenize → routed dataset | How does raw mail become model input? | Stated thresholds annotated on the figure | Links §2.1 concepts to §6.2 composition |
| Fig. 4 | §7.1 | Macro-F1 bar chart, full test set (optional) | How tightly do variants cluster? | One paragraph; table remains authoritative | Quick-read companion to Table 2 |
| Fig. 5 | §7.9 | Confusion-matrix panel (DCAT, Late Fusion, Text-Only × full/multimodal) | What error types remain? | FP/FN narration incl. 57/25 | Error-analysis evidence |
| Fig. 6 | §7.9 | Macro-F1 comparison plot | How do variants rank visually? | Points to tables for exact values | Interpretability aid |

*(Figs. 4–6 correspond to the plot mentioned in source §7.10; Figs. 1–3 must be created in Phase 3 — flagged unresolved.)*

**Tables**

| ID | Location | Content | Purpose / question | Notes |
|---|---|---|---|---|
| Table 1 | §6.2 | Dataset composition (full, incl. per-class modality rows) | What data did we evaluate on? | Absorbs old Appendix A composition block |
| Table 2 | §7.1 | Full-test benchmark, 9 variants × 6 metrics, 3-seed means | Overall standing of every variant | Best per column marked; reconciliation note in prose/App. C |
| Table 3 | §7.2 | Multimodal subset, 9 variants × 3 metrics | What happens under scarcity? | 4-ham/7-spam caveat stated adjacent |
| Table 4 | §7.3 | Cross-attention ablation | Does cross-attention help under scarcity? | With both p-values |
| Table 5 | §7.4 | Imbalance ablation | Does the objective matter more than architecture? | With both pooled-OOF p-values |
| Table 6 | §7.5 | 5-fold CV means/stds | Is the multimodal signal stable? | Std column essential |
| Table 7 | §7.6 | Per-fold MM-Macro-F1 | Where does variance come from? | Folds 4–5 = 1.0000 visible |
| Table 8 | §7.7 | Efficiency (params, trainable, FLOPs, latency) | What does DCAT cost? | Published Baseline row included |
| Table 9 | §7.7 | Early-exit details (latency, P95, FLOPs, skip rate) | Do savings survive measurement? | Measurement-procedure caveat adjacent |
| Table 10 | §7.8 | 3-seed variance | Are headline numbers seed-stable? | std ≤ 0.0003 |
| Table 11 | §7.8 | Modality-specific Macro-F1 | Where does each model earn its score? | IMAGE n=1 caveat |
| Table 12 (opt.) | §6.3 | Variant configurations | What exactly differs between variants? | E.15 decision deferred |
| App. A | App. A | Processing parameters | Reproducibility reference | Slimmed per E.1 |
| App. B | App. B | Hyperparameters | Re-implementation reference | Verbatim |
| App. C | App. C | Results lineage | Provenance of every number | Verbatim |

**No table ranks prior papers.** The only prior-work visibility is (i) the Published Baseline row inside our own benchmark tables (a configuration in our controlled experiment, not a citation ranking) and (ii) two sentences in §8.5.

**Equations (numbered, symbol-defined, referenced in prose)**

| Eq. | Location | Content |
|---|---|---|
| 1 | §2.5 | Scaled dot-product attention (generic background form) |
| 2 | §4.2 | Modality routing rule (piecewise) |
| 3 | §4.4 | BCE loss |
| 4 | §4.4 | Weighted BCE |
| 5 | §4.4 | w_pos = N_ham/N_spam |
| 6–7 | §5.2–5.3 | H_text, H_img |
| 8–9 | §5.4 | Projections Z_text, Z_img (+ matrix dims) |
| 10–13 | §5.5 | Q/K/V and attended outputs, both directions |
| 14–15 | §5.5 | Residual updates with MLP (both directions explicit) |
| 16–17 | §5.6 | Mean pooling; element-wise-average fusion |
| 18 | §5.7 | Shared classifier |
| 19–20 | §5.7 | Auxiliary exit probability; exit rule (0.95/0.05) |
| 21 | §6.5 | Macro-F1 definition |
| 22 | §6.6 | McNemar statistic with continuity correction |

All equations exist in the source or are standard-form definitions of metrics/statistics already used; none introduces a new claim.

---

# G. LITERATURE INTEGRATION PLAN

Where external literature will be needed in Phase 3 (no references invented here; *new-lookup* = not yet in the 24-entry bibliography):

| Location | Concept needing support | Existing refs | New-lookup needed? |
|---|---|---|---|
| §1 P1 | Spam as persistent, costly problem; image use in campaigns | ref3, ref24 | No |
| §2.1 | MIME/email structure standards | — | Optional (MIME RFC) |
| §2.2 | Spam vs phishing definitions; image-based evasion | ref3, ref24 | Optional (1 phishing-survey) |
| §2.3 | Representation-learning progression | ref18, ref19, ref20, ref7, ref4, ref21 | No |
| §2.4 | CNN/ViT encoders; preprocessing contracts | ref15, ref16, ref17, ref5, ref6 | No |
| §2.5 | Attention, cross-attention, co-attention | ref22, ref8, ref9, ref10 | No |
| §2.6 | Early exit / conditional computation | ref23 | Optional (1–2 recent conditional-computation) |
| §3.1 | Rule-based & classical spam filters | ref1, ref2, ref3 | No |
| §3.2 | Image-spam systems | ref24 | No |
| §3.3 | Multimodal spam: MMTD, MDL-SPAM, gated fusion | ref13, ref2, ref14 | No |
| §3.4 | Early-exit systems | ref23 | No |
| §3.5 | Evaluation practice, dataset shift, McNemar | ref3, ref11 | No |
| §4/§5 | Loss weighting rationale (class imbalance) | — | Optional (1 focal-loss/weighting citation) |
| §5.5 | Pre-LN stability | ref12 | No |
| §6.1 | SpamAssassin corpus provenance | ref1 | No |
| §6.3 | Reimplemented baseline identity | ref13 | No |
| §8 | (No new citations; interpretation only) | — | No |

Estimated final bibliography: 24 existing + 0–5 optional lookups ≈ **24–29 entries**. If a fuller related-work feel is wanted, the extension path is more *foundational* citations in §2 (representation learning, vision transformers), never padding §3 with uncited-claim survey paragraphs.

---

# H. NARRATIVE BLUEPRINT

The reader journey, end to end:

1. **§1 — Orientation.** Spam is a persistent security problem; images now carry part of the spam signal. Two structural facts about real corpora — text-only dominance and multimodal scarcity — make naive multimodal designs both wasteful and hard to train. DCAT answers with three mechanisms: bidirectional cross-attention, deterministic modality routing, optional early exit. Five contributions; roadmap. *(Reader state: knows what the paper claims and why it might matter.)*
2. **§2 — Concepts.** Email's MIME anatomy explains where modalities come from; spam-vs-phishing explains what the positive class is; representation learning for text and images explains what encoders do; attention explains what cross-attention will mean; conditional computation explains what early exit will mean. *(Reader state: can understand every word of the abstract.)*
3. **§3 — Position.** Prior work by family: text filters → image-spam detectors → multimodal fusion → conditional computation → evaluation practice. Four numbered gaps emerge, none tied to any single paper. *(Reader state: can state the gap in one sentence.)*
4. **§4 — Formalization.** Inputs, modalities, routing rule, computation paths, objective. Determinism of routing is justified; EMPTY exclusion is stated. *(Reader state: could define the task to a colleague.)*
5. **§5 — Mechanism.** The architecture, stage by stage, with Fig. 1 as the map and every dimension on the page; the 2.74%-trainable fact explains the efficiency premise. *(Reader state: could re-implement DCAT.)*
6. **§6 — Contract.** Data, preprocessing, splits, leakage scope, eight variants, three ablations, metrics as equations, statistical protocol, efficiency measurement definitions. *(Reader state: knows exactly what evidence will count and how it was produced.)*
7. **§7 — Evidence.** Results by research question: full test → multimodal subset → architecture ablation → objective ablation → CV robustness → per-fold → efficiency → stability → errors. Numbers narrated verbatim; best values marked; caveats stated where the source states them. *(Reader state: knows what happened.)*
8. **§8 — Meaning.** Why the full-test metric barely moves (99.4% text-only); why the multimodal subset is volatile (11 samples); why the objective change outweighed the architecture change; why measured overhead can cancel FLOP savings; and the honest summary of what DCAT does and does not establish. *(Reader state: knows why it happened.)*
9. **§9 — Boundaries.** Dataset, architecture, evaluation limitations; internal/construct/external validity. *(Reader state: knows exactly how far the claims reach.)*
10. **§10 — Close.** Two-paragraph recap tied to the evidence; seven future-work items, each traceable to a limitation. *(Reader state: done, with a correct mental model.)*

Progressive-depth check: no concept is used before it is taught (attention taught §2.5, used §5.5; early exit taught §2.6, used §5.7; McNemar introduced §3.5/§6.6, used §7). No section depends on knowledge of any specific earlier paper; the reimplemented baseline is defined operationally in §6.3 and cited.

---

# I. OLD VS NEW STRUCTURE DIAGNOSIS

**What is wrong with the current structure**

1. **Reader abandoned at the door.** The abstract/intro reference "the published multimodal baseline reimplementation" with no identity, and the paper never establishes what email spam *is* or why images matter — it presumes a reader who already knows the project.
2. **Comparison-heavy spine.** The "Published Baseline" is a de-facto second protagonist: it structures variant lists, results narration, and an entire Discussion subsection (§8.6). The paper reads as a reply to another paper rather than a standalone study.
3. **Background/Related Work conflated.** §2 mixes concept teaching (what cross-attention is) with attribution (who did what), so neither is done well; there is no progressive foundation and no gap statement.
4. **Skeleton methodology.** §4 lists components with placeholders and a broken equation block; "computed analogously" hides half the cross-attention; no architecture figure exists despite `[FIGURE: DCAT Architecture]`.
5. **Results ledger with editorial scars.** Tables are narrated in isolation; in-file meta-instructions ("the final manuscript should use the authoritative source table consistently") sit inside Results; provenance lines interrupt prose.
6. **Discussion partly duplicative.** §8.3/§8.6 overlap the corpus-framing and baseline content; the strongest finding (objective > architecture under scarcity) is buried as §8.4.
7. **Appendix duplication.** Appendix A's composition table duplicates Table 1.

**How the new architecture fixes each**

1. → New §2 builds the domain and technical foundation progressively (blueprint §6 profile: "teach what the reader needs"); baseline defined once, operationally, in §6.3 with citation.
2. → The baseline is demoted to *one configuration among eight* in our controlled experiment; old §8.6 is absorbed into two sentences of §8.5; no section's purpose is comparison.
3. → Concept/attribution split: §2 teaches, §3 attributes; §3.6 converts the literature into four testable gaps that the ablation design (§6.4) explicitly answers.
4. → §5 restores all placeholders via Appendix B, completes the math (Eqs. 6–20), adds Figs. 1–2; §4 formalizes the problem before any architecture appears.
5. → §7 reorganized around research questions; meta-instructions become explicit data caveats (C.31/C.32) plus Appendix C provenance; every table introduced and best values marked (blueprint §3 conventions).
6. → Discussion restructured finding-first (§8.1–8.5), with the objective-vs-architecture result promoted to its own subsection.
7. → Appendix A slimmed to processing parameters; composition lives once, in §6.2.

**Readability improvements:** every acronym expanded at first mention; one-idea paragraphs; RQ-titled results; transitions that state each section's job; floats introduced before they appear.

**Meaningful depth created:** ~10 pages of legitimate new length (foundation §2 ≈ 3 pp; gap-anchored related work ≈ 2 pp; completed methodology ≈ 1.5 pp; expanded results narration and discussion ≈ 2 pp; formalized metrics/statistics ≈ 1 pp) — all channelled through the MEANINGFUL LENGTH STRATEGY, none through padding.

**Result-interpretation improvement:** results report *what*; discussion argues *why* with only source-supported mechanisms (corpus dominance, scarcity, shared-classifier bias, branch overhead); limitations bound every interpretation; the conclusion's honesty ("does not demonstrate a consistent full-test advantage…") is kept as the paper's signature claim.

---

# FINAL STRUCTURE FAILURE TEST — RESULTS

| # | Check | Verdict | Where ensured |
|---|---|---|---|
| 1 | Understandable without knowing any particular earlier paper | **PASS** | §2 foundation; baseline defined operationally in §6.3 |
| 2 | The banned lineage phrase appears nowhere | **PASS** | Sections A–I use "published baseline (reimplementation)" only, cited via ref13 in Phase 3; the phrase itself is banned and used nowhere in the architecture |
| 3 | No section centered on one prior work | **PASS** | Old §8.6 dissolved into §8.5 (E.4); §6.3 treats all variants equally |
| 4 | Opening provides domain/context | **PASS** | §1 P1–P2 + §2.1–2.2 |
| 5 | Foundational sections meaningful & relevant | **PASS** | §2.1–2.6 each end at a component used in §5 |
| 6 | Basic → advanced progression | **PASS** | H.1–H.10; no concept used before taught |
| 7 | Many pages via legitimate depth | **PASS** | Length strategy arithmetic ≈ 21 pp body |
| 8 | No filler-dependent length | **PASS** | Filler-reject list per channel; Phase 3 audit rule |
| 9 | Methodology ≠ experimental setup | **PASS** | §5 vs §6 |
| 10 | Results ≠ interpretation | **PASS** | §7 vs §8 with E.10 boundary rule |
| 11 | Important experiments easy to locate | **PASS** | §7.1–7.9 one RQ each; Table of floats |
| 12 | Every float/equation has purpose | **PASS** | Section F plans all 6 figures, 12+3 tables, 22 equations |
| 13 | Redundant material consolidated | **PASS** | E.1, E.2, E.3, E.14 |
| 14 | Contribution clear from intro | **PASS** | §1 contribution bullets (C.2) |
| 15 | Conclusion follows from PAPER_CONTENT.md evidence | **PASS** | §10 sources: C.1, C.30–C.41, C.44 |
| 16 | No numerical result altered | **PASS** | C-map: all numbers carried verbatim |
| 17 | No new experiment invented | **PASS** | §6 sources are C.18–C.29 only; F adds figures, not experiments |
| 18 | No important evidence lost | **PASS** | C.1–C.49 complete map |
| 19 | Follows blueprint lessons without copying domain organization | **PASS** | Structure adopted; smart-contract patterns excluded per blueprint §5 |

**Unresolved items carried to Phase 3 (also in final report):** (i) Figs. 1–3 (and optionally 4–6) must be drawn; (ii) the two in-source data reconciliation notes (C.31, C.32) must be resolved against authoritative artifacts by the user or kept as explicit caveats; (iii) E.15 variant-table decision; (iv) equation-placeholder symbols must be restored from Appendix B during writing; (v) optional literature lookups (§G) are user-approved additions, not yet fetched.
