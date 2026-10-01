# HUMAN_EDITABLE_MANUSCRIPT_AUDIT.md — internal validation record

Not part of the paper. Documents the creation and validation of
`HUMAN_EDITABLE_MANUSCRIPT.md` from the frozen manuscript.

## Deliverable

`HUMAN_EDITABLE_MANUSCRIPT.md` — complete, byte-faithful Markdown master of the
finalized paper, structured for manual prose rewriting. Built by mechanical
transformation (`build_editable_manuscript.py`) from `PAPER_CONTENT_REGENERATED.md`
— no prose was retyped by hand, so transcription drift is structurally excluded.

## Counters

| Metric | Value |
|---|---|
| Source manuscript word count (`PAPER_CONTENT_REGENERATED.md`, wc) | 11,566 |
| New file word count (wc) | 13,717 |
| Delta | +2,151 (editorial header + editing rules + 4 expanded figure specifications + fact-check appendix — no manuscript prose added) |
| Top-level sections (`##`) in paper proper | 18 (Abstract, Sections 1–10, Data Availability, Declarations, Appendices A–C, References) |
| Subsections (`###`) | 48 manuscript subsections (unchanged hierarchy) + fact-check appendix subsections |
| Numbered equations | 21 (`[Equation 1]`–`[Equation 21]`, math preserved verbatim) |
| Tables | 13 (10 main + Appendix A, B, C tables), all rows/values/captions intact |
| Figure specifications | 4 (full marker + caption + placement/purpose/data-source blocks) |
| References | 33 (`[1]`–`[33]`, numbering unchanged, all entries present) |
| Human-editing markers | 25 (before all 15 major sections and 10 key subsections) |
| Validation checks | 17/17 passed (`validate_editable_manuscript.py`) |

## Validation summary (12-point brief)

1. Section structure vs source — PASS (every heading present, none added/renamed).
2. No major section missing — PASS.
3. All 21 equations present, sequentially numbered — PASS.
4. All 13 tables present — PASS (Table 1 rows verified byte-identical; Appendix B/C tables verified by content keys).
5. All four figure specifications present with titles/captions/data sources — PASS.
6. All 33 references present in order — PASS.
7. Important numerical values preserved — PASS (43 key values verified verbatim, listed below).
8. Documented caveats preserved — PASS (all nine disclosure notes verified).
9. No scientific content invented — PASS (multiset line-difference: every source line appears in the new file except the four intentionally transformed classes listed below; no unaccounted additions).
10. `PAPER_CONTENT.md` not modified — PASS (mtime unchanged: Sep 13 21:26; git-clean/untracked, never opened for write).
11. LaTeX project not modified — PASS (`latex/` mtimes unchanged since production: main.tex Sep 18 10:03; no writes this phase).
12. No LaTeX layout/TikZ/pgfplots/bibliography-implementation code — PASS (automated leak scan over 20 command patterns: zero hits).

## Key numerical values verified verbatim in the new file

Headline results: 0.9862 (Full-DCAT), 0.9871 (Late Fusion), 0.9869 (Published
Baseline), 0.9867 (No-XAttn and Early-Exit), 0.9827 (Text-Only), 0.3220
(Image-Only); multimodal: 0.4968/0.0000/0.9935 collapse level, 0.8317/0.6667
(No-XAttn), 0.5584/0.1633/0.9535 (Text-Only); CV: 0.7077/0.2639, 0.5453/0.1222,
0.5564/0.1192, 0.5171/0.0597, per-fold 0.4971/0.4971/0.4968/1.0000/1.0000;
imbalance: 0.9880, 0.6253 → 0.7478; statistics: p = 1.0000, p = 0.2482,
p = 2.49 × 10⁻⁴⁵, p = 3.34 × 10⁻⁶, α = 0.05, seed std ≤ 0.0003; counts: 6,046,
4,150, 1,896, 2.19:1, 6,007 (99.4%), 11 (0.2%), 4 ham/7 spam, 27 EMPTY, n = 7,351,
7,867 pooled OOF; efficiency: 73,309,090 / 71,761,314 / 77,967,426 params,
2,008,578 / 460,802 trainable, ~13B / ~11B (avg) / 12.8B → 12.7B FLOPs, 4.45%,
0.63%, 24.82%, 88.39%, 59.9/74.7/60.3/113.6 ms, 1.48/2.65/2.66/2.70/2.68 ms;
confusion matrix [[2196, 57], [25, 5073]]; hyperparameters: 256/2/4/64/1024/0.1,
GELU, Pre-LN, 128/0.3, max_length 256, 20×20 px / 1024 B / 224×224, AdamW,
1 × 10⁻⁴, batch 64, 1 epoch, FP16, 0.5, 0.95/0.05, seeds 42/43/44.

## Caveats verified present (mandatory disclosures)

0.9855 → 0.9871 transcription correction (§7.1); 155-sample MM evaluation-set
vs 4 ham/7 spam prevalence distinction (§7.2); Table 3 provenance conflict
disclosed, not reconciled (§7.2); Table 6 fold-provenance note (§7.6); FLOPs
conventions ~11B "(avg, 90% text-only)" vs 12.7B measured (§7.7, §9.3);
total-time efficiency artifact unavailability (§9.3); pilot-scope
perceptual-leakage audit (§9.4); Appendix C lineage aggregation/split-label
explanation (App. C); All-Spam-Prior 0.9871 arithmetic clarification (§7.2).

## Content not transferred byte-identically (all intentional, none scientific)

1. Equation `\tag{n}` markers → `[Equation n]` labels on their own line
   (math bodies preserved verbatim; whitespace-only normalization at the tag site).
2. Four `*[FIGURE n PLACEHOLDER: …]*` lines → full specification blocks
   (marker, finalized caption from the rendered PDF, placement/purpose, data source).
3. §7.9 first sentence → the production-finalized Figure-4 wording
   (`Figure 4 reports the archived confusion matrix…`), as recorded in
   `latex/PRODUCTION_QA_REPORT.md` during the final production stage; rest of the
   paragraph unchanged. This keeps the editable master consistent with the
   rendered PDF.
4. Internal `---` separator rules stripped (cosmetic; equations untouched).
5. Editorial additions outside the paper proper: status header + editing rules
   (top), `HUMAN EDITING FACT-CHECK REFERENCE` appendix (bottom), 25 editing
   markers — all clearly marked as non-paper content.

No research claim, number, citation, result, caveat, or structural element was
altered, added, or removed.

## Working files created this phase

* `HUMAN_EDITABLE_MANUSCRIPT.md` — the deliverable.
* `build_editable_manuscript.py` — reproducible builder (rerun after source updates).
* `factcheck_footer.md` — fact-check appendix source for the builder.
* `validate_editable_manuscript.py` — 17-check validator (rerun after manual editing).
* `editable_build_stats.json`, `HUMAN_EDITABLE_MANUSCRIPT_AUDIT.md` — this record.

Recommended post-editing workflow: rewrite prose in
`HUMAN_EDITABLE_MANUSCRIPT.md` → run `python validate_editable_manuscript.py`
(fact preservation) → regenerate LaTeX from the edited file.
