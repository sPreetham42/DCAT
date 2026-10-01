# FINAL_HUMANIZED_PAPER_AUDIT.md — Final Production Audit

**Executive status: FINAL — ALL CHECKS PASS**

**Final production pass (2026-09-19) close-out:** the last minor item is resolved.
- The 4.2pt §6.1 overfull is absorbed (`\emergencystretch` 1.5→3 em): the log now shows
  **0 errors, 0 undefined references/citations, 0 overfull boxes**, 32 pages.
- Figure 4 rebuilt as properly paired panels ((a) confusion matrix, (b) MM-Macro-F1
  bars) with a shared baseline, verified in-render; Figures 1–3 carry the earlier
  source repairs.
- Tables 11/12/13 are inline in Appendices A/B/C; Table 12→13 and Table 13→References
  gaps eliminated (References begins right after Appendix C's note, same page).
- Author block: `Preetham S` + `spreetham6442@gmail.com` only; guide/supervisor entry
  removed (verified: zero occurrences in the PDF).
- Full-page ink QA: 32/32 clean; References region pure (33 entries, no floats).
- **Prose changes in this pass: zero.** The author's edited voice remains the paper's
  voice; the 116 documented content repairs of the regeneration pass stand unchanged.

**Layout-repair pass (2026-09-19) addendum:** page-by-page visual QA found and fixed
three figure-source defects (Fig. 1 stray empty node; Fig. 2 overlapping attention
columns; Fig. 3 colliding modality-leaf labels — details in
`FINAL_FIGURE_TABLE_AUDIT.md`) and the appendix-table drift into References
(Tables 11–13 now render inside Appendices A–C, strictly before References, enforced
by a `\clearpage` float flush at the bibliography boundary). Prose unchanged.

---

## 1. Human Content Preservation

- The author's manual rewrite in `HUMAN_EDITABLE_MANUSCRIPT.md` is the manuscript voice.
  Diff vs the repaired master: 141 changed blocks, each traceable to a documented repair
  (see `FINAL_PAPER_CHANGE_LOG.md`); zero stylistic rewrites; zero synonym passes.
- The regeneration chain (`build_editable_manuscript.py` → author edit → repair passes 1–6
  → `md_to_latex.py`) never rewrites prose mechanically. The only non-verbatim, disclosed
  transfer remains §7.9's production-finalized Figure-4 sentence.
- AI-style reintroduction check: PASS. No "notably/robust/leveraging/seamlessly" fillers,
  no padding; the repaired master contains the author's vocabulary throughout.

## 2. Structural Integrity

- Final hierarchy (converted 1:1 from the repaired master): Abstract; Keywords;
  1 Introduction; 2 Background (2.1–2.6); 3 Related Work (3.1–3.6); 4 Problem Formulation
  (4.1–4.4); 5 The DCAT Architecture (5.1–5.8); 6 Experimental Methodology (6.1–6.8);
  7 Results (7.1–7.9); 8 Discussion (8.1–8.5); 9 Limitations and Threats to Validity
  (9.1–9.4); 10 Conclusion and Future Work; Data Availability; Declarations;
  Appendices A–C; References. 15 sections / 49 subsections — matches `NEW_PAPER_OUTLINE.md`.

## 3. Scientific Integrity

- All 23 key values verified in the PDF text layer: 0.9862, 0.9869, 0.9871, 0.8317,
  0.4968, 0.7077, 0.5453, 0.7478, 4.45%, 0.63%, 24.82%, 12.8B, 12.7B, 73,309,090,
  75,419, 73,206, 7,867, 7,351, 6,046, p = 2.49×10⁻⁴⁵, p = 3.34×10⁻⁶.
- Headline numbers re-verified against raw artifacts during repair
  (`weighted_primary/results.json`, `weighted_cv/cv_results.csv`,
  `final_results.csv`, `results_lineage.csv`, leakage manifest).
- Dataset wording: "75,419 total records / 73,206 usable" for the primary corpus;
  6,046-message supplementary SpamAssassin profile (4,150 ham / 1,896 spam); multimodal
  population 7,867 (327 ham / 7,540 spam); test n = 7,351. No invented training
  provenance; pooled corpus claims avoided.

## 4. Discrepancies Found

Classification per the brief (counts and details in `FINAL_PAPER_CHANGE_LOG.md`):

- **C — human editing errors (corrected):** fabricated 1800:1 ratios, 9.84%/6.36%
  latencies, 0.001 significance level, 4.46%, "five emails", "4 of 4", corrupted
  p-value superscripts, scrambled/deleted equation bodies (Eqs 1,3,4,5,7,8,9–11,14,15),
  glued headings/lists, pasted-in foreign paragraphs, debris annotation.
- **D — preserved as authored:** none beyond the author's legitimate rewording.
- **E — unresolved:** none new. Pre-existing documented provenance caveats (Table 3
  designations, Table 6 fold provenance, Appendix C lineage aggregation, FLOPs
  conventions, missing total-time artifact) are preserved as disclosures, exactly as in
  the approved manuscript — they are recorded caveats, not silent resolutions.

## 5. Tables

13 tables (10 main + 3 appendix), sequential, all values from the verified sources,
captions from the manuscript, booktabs styling, all within margins (`qa_pixels.py`).
In-text references: Tables 1–10 present in prose.

## 6. Figures

4 vector figures from the approved production set (architecture; cross-attention block;
preprocessing flow; results panel with archived weighted-primary confusion matrix
`[[2196, 57], [25, 5073]]`, n = 7,351, and multimodal Macro-F1 panel). No fabricated
Late Fusion / Text-Only confusion matrices. Captions remapped to current equation
numbers; all figure references resolve.

## 7. Equations

21 numbered equations, labels `eq:1`–`eq:21`, sequential, notation from the frozen
source where the author's edit damaged bodies; the author's surrounding prose kept.

## 8. Citations

33 references, unsrtnat order of first appearance; all `\citep` keys resolve
(bibtex clean); 33 entries rendered in the PDF. MobileViT remains arXiv:2110.02178.
No placeholder citations anywhere.

## 9. Claim Audit

Abstract ↔ Introduction ↔ Results ↔ Discussion ↔ Conclusion are consistent: the paper
claims conditional architecture + evaluation insight (weighting > fusion on this corpus),
explicitly NOT outperformance on the tiny multimodal subset, with significance caveats.
No contradiction detected in the text-layer audit.

## 10. AI-Style Reintroduction Check

PASS — see §1. The converter (`md_to_latex.py`) performs format transforms only.

## 11. Visual QA

32 pages rendered at 100 dpi (`build/rendered_pages/page-01..32.png`). All pages within
printable bounds; no sparse/empty pages; running headers present; figures/tables placed
`[t]` and readable; one 4.2pt overfull line (§6.1) — the only minor item.

## 12. Remaining Issues

1. One 4.2pt overfull hbox (§6.1 tokenizer settings list) — cosmetic.
2. Pre-existing documented provenance caveats remain disclosed in the manuscript by
   design (they are features of the evidence record, not defects).

## Deliverables

- `paper/FINAL_PAPER.md` (master, == repaired manuscript)
- `paper/latex/main.tex`, `paper/latex/references.bib`
- `paper/DCAT_Final_Practice_Paper.pdf` (32 pages)
- `paper/FINAL_PAPER_CHANGE_LOG.md`
- `paper/latex/build/rendered_pages/` (32 page previews)
- Frozen sources untouched: `PAPER_CONTENT.md`, `PAPER_CONTENT_REGENERATED.md`,
  `NEW_PAPER_OUTLINE.md`, `latex/main_frozen_backup.tex`.
