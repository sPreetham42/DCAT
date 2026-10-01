# FINAL_PRESENTATION_AUDIT.md — Phase 5 Quality-Control Document

**Scope:** editorial/publication-presentation pass over `PAPER_CONTENT_REGENERATED.md` (Phase 4 output).
**Status:** complete. This file is internal QC and is not part of the manuscript.
**Benchmark:** `REFERENCE_STYLE_BLUEPRINT.md` presentation principles (structure, float discipline, tense, hedging, caption conventions, back matter). No reference-paper content or wording was copied; the two supplied papers remain uncited (smart-contract domain, per `LITERATURE_MAP.md` §8 policy).

---

## A. Structure

**Issues found**
1. Figure numbering gap: the four placeholders were numbered 1, 2, 3, 4 — but the confusion-matrix panel was scheduled as the 4th figure while the outline's F5/F6 panel content (confusion matrices + Macro-F1 plot) had been folded into it. Result: consistent 1–4 but no prose in §7.9 engaged with the panel.
2. One table (old Table 4, cross-attention ablation) was 100% redundant with Table 3 — it re-listed the same three models × three metrics on the same 11-message subset that Table 3 already reports.
3. Appendix C sat disconnected: readers hit lineage rows generated under an alternative split configuration (10% primary test) without having been told the manuscript's primary configuration is 70/15/15.

**Fixes made**
1. Figure 4 placeholder retained as Figure 4 (no gap); its description expanded to name the panel content (confusion-matrix panels for DCAT/Late Fusion/Text-Only on both evaluations + Macro-F1 comparison plot); the placeholder moved to §7.9's end so prose introduces it first. Figures 5–6 as separately numbered items are dropped (their content lives in Figure 4) — outline item E.15 resolved conservatively.
2. Old Table 4 merged into §7.3 prose (values cross-referenced from Table 3); Tables 5–11 renumbered to 4–10; all in-prose references updated. **No evidence lost** — the three numbers the table carried (0.4968/0.8317 rows) are verbatim Table 3 values, now cited rather than duplicated.
3. Bridge note added in §6.2 (split configuration disclosure) and a "(primary configuration)" clarification in Appendix A; Appendix C's existing "reproduced as recorded" note retained unchanged.

---

## B. Narrative

**Weak transitions/openings found and fixed**
1. Abstract opened with a one-sentence methodology paragraph ("DCAT is evaluated on … using three training seeds, …") — reads as an inventory, not a finding; the full protocol list is restated in §1. → Cut; abstract now presents motivation → design → two-sentence evidence → two-sentence interpretation.
2. §2.1 opened mid-substance with MIME; the pedagogical link to the paper's own task was implicit. → Opening sentence now frames why message structure matters for content-based classification ("The classifier developed in this paper makes decisions over message *content* …").
3. §2.3 opened with "The representation of text … has developed through several generations" without signposting; §2.4's encoder choice ended without a pointer. → Added orientation sentence ("This subsection traces how text came to be represented by the encoder DCAT adopts; Section 2.4 does the same for images") and a closing pointer ("As with text, Section 5.3 specifies the exact configuration used").
4. §3 opening did not separate the job of Background from the job of Related Work. → New opening: "Background and related work answer different questions…".
5. §6.1 opened with "The evaluation corpus" (method voice) rather than "The corpus used throughout the paper" (narrative voice carrying a §4.2 dependency). → Reworded.
6. §7 opening lacked a protocol→results pivot; §7.1's RQ was generic ("how do all variants compare"); §7.9's RQ was vague ("what kinds of errors remain?"). → §7 now opens "The protocol of Section 6 fixed what was measured and how; this section reports what the measurements show."; RQs sharpened to name the corpus-structure confound and the error-concentration question.
7. §8.1 ended on "not established causes" — accurate but a dead stop. → Closed with an explicit bridge to the evidence sections ("Whether the added interaction capacity helps … Sections 7.1–7.4 measure it directly, and Section 8.2 interprets the outcome."). A first attempt inserted this sentence mid-enumeration; it was re-sited to the end of the enumeration within the same pass.

---

## C. Background

**Meaningful explanatory additions retained** (from Phase 4; verified intact): the MIME-tree → modality definition chain (§2.1); dataset-shift consequence framing (§2.2); the full text-representation ladder ending in the frozen-DistilBERT rationale (§2.3); the image ladder ending in the timm preprocessing contract (§2.4); Eq. (1) with its origin-story citations and the self/cross/bidirectional distinctions (§2.5); deterministic-vs-learned routing and the encoder-skipping early exit with its overhead trade-off (§2.6). All define → explain → connect.

**Filler removed:** none needed in §2 — the section already passed the outline's per-subsection purpose test. Two sentences added in §2.2/§2.4 are connectors, not new content.

---

## D. Methodology

**Clarity improvements**
1. §3.4's final sentence now carries an explicitly hedged novelty statement ("to our knowledge, this combination has not previously been applied to email spam detection") replacing the bare descriptive claim — matching the blueprint's hedged-novelty convention without altering the factual scope.
2. §5.4: the LayerNorm *explanation* was buried after the projector paragraph's end while its sentence sat inside the equation block — reordered so the trainable-projection claim (substance) leads and the normalization rationale (why it matters) follows.
3. §5.7: removed the redundant restatement of classifier sharing after Eq. (19) (the sentence introducing Eq. (19) now states it once); Eq. (21) spacing normalized.
4. §6.8: error-record paths now state their downstream role (traceability basis for §7.9).
5. §10 future-work item 1 now names *why* corpus expansion matters (re-examining the class-weighting effect at scale) — connecting limitations to the study's strongest finding.
6. §7.2's "Three corpus-level facts explain this" paragraph moved to §8.1 in Phase 4 was verified intact and now also bridges forward correctly (see B.7).

**Notation issues fixed**
- Cross-attention layer-count symbol changed from bare `$L = 2$` (colliding with nothing but also introduced nowhere else) to `$N_{xattn} = 2$`, consistent with the Appendix-B symbol style; the configuration value (2 layers) is unchanged.
- Equations (2)–(6) `has\_text`/`has\_image` naming verified consistent with §4.2 prose and §6.1 thresholds (≥10 characters; ≥20×20 px; ≥1024 bytes).
- No mathematical content was invented or altered. The corrupted-placeholder equations were fully restored in Phase 4 and were re-checked, not rewritten.

---

## E. Results

**Repetition removed**
1. Redundant Table 4 (identical to the Table-3 rows) merged into §7.3 prose — the single largest de-duplication.
2. §5.7's duplicated classifier-sharing sentence removed (methodology restating itself).
3. Verified that no other subsection re-narrates a number already carried: 0.9862 appears 12× but always in a distinct analytical role (abstract, §1, §7.1, §7.4 baseline column, §7.8 per-seed table, §8.1/§8.3/§8.5, §10, Appendix C note); the 0.4968/0.8317 pair appears in §7.2/§7.3 (by cross-reference only), §7.8, §8.2, §10 — each mention adds the subset/full-test/seed/modality-specific lens it is attached to.

**Interpretation improved**
1. §7.1 RQ reframed around what the full-test metric can and cannot resolve.
2. §7.3 prose now names the ablation's design logic (no-interaction → shared-space → full interaction) before the numbers, so the comparison reads as a designed progression rather than three unrelated rows.
3. §7.8 (modality-specific): added that the MM-column ordering matches §§7.2–7.4, closing the loop between the seed-42 slice and the primary analyses.
4. §7.9: FP/FN cost asymmetry stated and tied to the per-sample error records; the figure's purpose ("make the contrast between corpus-level and subset-level behavior directly visible") is now explicit.
5. §7.7: FLOPs units in Table 7 ("~13B") vs Table 8 ("12.8M") are faithful to the source artifacts but sit in different unit conventions — **preserved verbatim and flagged** (see K and L); the prose already forbids combining the two latency procedures into one claim.

---

## F. Discussion

**Observation / interpretation / speculation separation** — verified and tightened:
1. §8.1: corpus-level facts are labeled as interpretations "consistent with the observed pattern, not established causes"; the added bridge directs readers to where the question is actually measured.
2. §8.2: the two candidate explanations remain explicitly "consistent with the evidence," disciplined by the non-significant McNemar result; the "opposite direction from the design's intent" clause was stiffened grammatically (em-dash apposition) without changing meaning.
3. §8.3: over-general claim softened ("does not establish that class weighting is universally dominant") while preserving the scoped evidential claim (gap 3).
4. §8.4: added the compact mechanism statement ("the savings scale with multimodal prevalence, not with the mechanism itself") — a faithful restatement of the measured workload dependence, not a new claim.
5. §8.5: the CV-variance clause now points to §7.6's fold evidence; all "what the evidence supports / does not support" boundaries retained verbatim.

No promotional language found; no speculation promoted to fact.

---

## G. Figures

| Fig | Location | Caption/placeholder | Prose integration | Verdict |
|---|---|---|---|---|
| 1 | §5.1 (after component list) | Describes 3 paths + router + early-exit branch | Referenced from §4.3 and §5.1 context; "placeholder" word removed from body text (the bracketed placeholder block remains the single marker) | ✔ needed; publication-ready |
| 2 | §5.5 (after Eqs. 16–17) | Streams, Q/K/V both directions, residual MLP, Pre-LN placement | Directly interprets Eqs. (12)–(17) | ✔ needed; publication-ready |
| 3 | §6.1 (after stage 4) | Four preprocessing stages, thresholds annotated | Matches the enumerated stages verbatim | ✔ needed; publication-ready |
| 4 | §7.9 (end) | CM panels ×3 models ×2 evaluations + Macro-F1 plot | Introduced before appearance; purpose stated; FP/FN costs named | ✔ needed; re-sited and described this phase |

No fabricated figures; no new figures added. Figures 1–4 remain `[FIGURE n PLACEHOLDER]` blocks for Phase 6 rendering.

---

## H. Tables (all 10 audited post-consolidation; was 11)

| # | Purpose | Caption | Location | Prose refs | Verdict / change |
|---|---|---|---|---|---|
| 1 | Corpus composition (16 rows) | Informative | §6.2 | Introduced before, interpreted after | ✔ no change |
| 2 | Full-test benchmark (9×6) | Informative | §7.1 | Before + after | ✔ no change |
| 3 | Multimodal subset (9×3) | Informative | §7.2 | Before + after | ✔ no change |
| 4 | Class-imbalance ablation (2×4) | Informative | §7.4 | Before + after | ✔ renumbered from 5 |
| 5 | CV means/stds (4×2) | Informative | §7.5 | Now referenced at §7.5's intro sentence | ✔ renumbered from 6 |
| 6 | Per-fold values (5×3) | Informative | §7.6 | Before + after | ✔ renumbered from 7 |
| 7 | Efficiency (5 models) | Informative | §7.7 | Before + after | ✔ renumbered from 8 |
| 8 | Early-exit details | Informative | §7.7 | Before + after | ✔ renumbered from 9 |
| 9 | Seed variance (3×5) | Informative | §7.8 | Before + after | ✔ renumbered from 10 |
| 10 | Modality-specific (3×2) | Informative | §7.8 | Before + after | ✔ renumbered from 11; cross-ref added |
| (old 4) | — | — | — | — | **Removed as redundant** (Table-3 duplicate); values preserved in §7.3 prose |

No remaining table exists primarily for prior-paper comparison: the Published Baseline rows sit inside each benchmark as one controlled configuration among the variants, per the Phase 2 architecture.

---

## I. Equations (all 21 audited)

| Range | Content | Checks |
|---|---|---|
| (1) | Scaled dot-product attention | d_k defined; origin citations [12],[22],[23]; operative form reused by §5.5 — ✔ |
| (2) | Label space | y ∈ {0,1} defined with ham/spam — ✔ |
| (3) | Routing rule | has_text/has_image defined; thresholds anchor §6.1 — ✔ |
| (4)–(6) | BCE, weighted BCE, w_pos | σ, ẑ, N defined; w_pos = N_ham/N_spam; §6.4 uses consistent w_spam = N_ham/N_spam phrasing — ✔ |
| (7)–(8) | Encoder outputs | x_text/x_img, token/pixel constraints, freezing stated — ✔ |
| (9)–(11) | Projections | W dims (768×d_model; D_img×d_model), D_img defined — ✔ |
| (12)–(17) | Bidirectional cross-attention + residual updates | Q/K/V provenance explicit both directions; L→N_xattn renamed; h=4, d_k=64; Pre-LN citation [32] — ✔ |
| (18) | Fusion | d_model-dim shared space; rationale ties to shared classifier — ✔ |
| (19)–(20) | Shared + auxiliary classifiers | MLP_cls/MLP_aux distinct; sharing stated once — ✔ |
| (21) | Exit rule | 0.95/0.05 thresholds; §7.7/§9.2 cross-refs — ✔ |

Numbering sequential 1–21; every symbol introduced before use; no malformed syntax; no dangling notation. No equation was invented or mathematically altered in this phase.

---

## J. References

- All 33 in-text markers ([1]–[33]) verified present and in order of first appearance; bibliography mapping checked line-by-line.
- **One bibliographic error found and fixed:** entry [20] (MobileViT) carried `arXiv:1810.03775`, which resolves to an unrelated physics paper ("Rumor propagation meets skepticism: a parallel with zombies"). The correct ID, `arXiv:2110.02178`, was verified via the arXiv metadata API this session and substituted. `LITERATURE_MAP.md` updated with the same correction and a provenance note.
- Unverifiable sources remain excluded: MDL-SPAM (ref2), "Deep Delegate", the redundant IEEE Access review — unchanged from Phase 3/4.
- The two supplied papers remain uncited (identities preserved in the literature map).
- No citation dumping introduced; the phase added zero new citations.

---

## K. Scientific integrity

**Confirmed: no scientific fact changed.** This phase's edits were presentational only. Verified by grep audit after all edits: 0.9862 (12×), 0.9869 (8×), 0.9871 (11×), 0.8317 (7×), 0.4968 (15×), 0.7077 (5×), 0.5453 (4×), 0.6253 (5×), 0.7478 (5×), 4.45% (5×), 0.63% (5×), 24.82% (4×), 73,309,090 (4×), 2,008,578 (4×), 6,046 (7×) — all present; equation tags 1–21 intact; citations 1–33 intact.

Explicitly **not** changed: datasets and sizes; preprocessing thresholds; the eight variants + baseline configuration; architecture (encoders, projector, 2-layer/4-head cross-attention, fusion, shared/auxiliary classifiers); training setup (AdamW, lr 1×10⁻⁴, cosine, batch 64, 1 epoch, FP16, frozen encoders); all metrics, p-values, efficiency numbers, seed values, fold values; all limitations; the conclusion's bounded claims. Caveats preserved verbatim-equivalently: (1) Late Fusion 0.9855 vs 0.9871 reconciliation; (2) All-Spam Prior 0.9871-vs-4h/7s accuracy note; (3) perceptual-leakage pilot scope; (4) missing total-time artifact; (5) Appendix C aggregation differences (disclosed, not reconciled).

The only correction to previously published (Phase 4) text was the **reference [20] arXiv ID** — a transcription error against the verified registry record, i.e., exactly the "obvious transcription error demonstrably supported by the source" the phase permits.

Also renamed for consistency: the variant labeled "Image-Presence" in artifact tables is now "Modality Indicator" throughout the manuscript — this is the name the source content assigns to the variant; the rename aligns prose with the source's own naming and was not a value or concept change. Zero instances of either name remain mismatched; zero occurrences of the banned lineage phrase.

---

## L. Remaining issues for Phase 6

1. **Draw Figures 1–4** from the placeholder specifications (architecture; cross-attention layer; preprocessing flow; results panel).
2. **Resolve the two data-reconciliation notes with the user or artifact owners** (or keep as disclosed caveats): (a) Late Fusion 0.9855 (Table 2) vs 0.9871 (seed-level analysis); (b) All-Spam Prior multimodal accuracy 0.9871 vs the 4-ham/7-spam counts; (c) whether the Appendix C lineage's "10% primary test" label vs the manuscript's 15% test split reflects an alternative configuration (currently disclosed as such).
3. **FLOPs unit convention**: Table 7's "~13B" vs Table 8's "12.8M" are faithful to source artifacts but sit in different unit conventions; if the underlying artifacts can be re-examined, present both in one unit (a change requiring evidence, hence deferred).
4. **Two pending author-list completions** in the bibliography at formatting time: [28] (dynamic-networks survey, "Han et al." → full list) and [30] (SkipNet, "X. Wang, F. Yu, et al." → full list); also confirm new7-adjacent page spans if the IEEE Access review is ever reinstated (currently excluded).
5. **Variant-label provenance note (optional)**: if the final venue requires it, add one sentence stating that artifact tables record the Modality Indicator under its implementation label (Image-Presence).
6. **LaTeX conversion, venue styling, reference renumbering to venue format, and final packaging** — deliberately not started (phase boundary).
