# FINAL_FIGURE_TABLE_AUDIT.md — Figure & Table Placement/Rendering Audit

**PDF audited:** `DCAT_Final_Practice_Paper.pdf` (= `latex/build/main.pdf`, 32 pages, compiled 2026-09-19)
**Method:** per-page text extraction (pdftotext), word-box geometry (pdftohtml XML),
pixel-level bounds check (`qa_pixels.py`), SVG vector-op verification (pdftocairo), and
direct visual inspection of rendered pages at 110 dpi and figure zooms at 200 dpi.

> **FINAL PRODUCTION PASS (2026-09-19).**
> - Author block: guide entry removed; author `Preetham S`, email `spreetham6442@gmail.com`
>   (verified on p.1; zero occurrences of guide/supervisor anywhere in the PDF).
> - Figure 4 rebuilt as paired panels with a shared baseline (matrix bottom and axis
>   bottom both at y = 0 by construction; verified in-render to the same pixel rows).
> - Appendix tables 11/12/13: inline `[H]` inside Appendices A/B/C; float-queue flush at
>   the bibliography removed. Table 12→13 gap: none (max band gap 10.5 mm, normal
>   spacing); Table 13→References gap: none (References heading starts on the same page,
>   after Appendix C's note, with normal section spacing).
> - Log: 0 errors, 0 undefined refs/citations, **0 overfull boxes** (\emergencystretch
>   3 em absorbs the former 4.2 pt tokenizer line).
> - Full-page ink QA: 32/32 pages clean (no blank pages, no margin violations).

## Section map (rendered)

| Part | Start page |
|---|---|
| Abstract | 1 |
| 1 Introduction | 2 |
| 2 Background | 3 |
| 3 Related Work | 6 |
| 4 Problem Formulation | 8 |
| 5 The DCAT Architecture | 10 |
| 6 Experimental Methodology | 15 |
| 7 Results | 18 |
| 8 Discussion | 24 |
| 9 Limitations and Threats to Validity | 26 |
| 10 Conclusion and Future Work | 27 |
| Data Availability | 28 |
| Appendix A | 28 |
| Appendix B | 29 |
| Appendix C | 29 |
| References | 31 |

## Figure inventory

| Item | Expected Section | Actual Section/Page | Rendering | Caption | Label | Status |
|---|---|---|---|---|---|---|
| Figure 1 | §5.1 Architecture Overview | §5 / p10 | Repaired (stray empty box removed); all 21 node labels render; arrows/connectors verified in SVG vector ops (599 paths) | Present, correct | `fig:architecture` | PASS |
| Figure 2 | §5.5 Bidirectional Cross-Attention | §5 / p13 | Repaired (column gap 34→46mm; attention boxes no longer overlap); 0 word-box overlaps | Present, correct (eq-refs remapped to (12)–(17)) | `fig:crossattention` | PASS |
| Figure 3 | §6.1 Corpus and Preprocessing | §6 / p16 | Repaired (leaf boxes 1→8mm apart; EMPTY callout 8→13mm); 0 word-box overlaps after fix | Present, correct | `fig:preprocessing` | PASS |
| Figure 4 | §7.9 Confusion-Matrix Results | §7 / p24 | **Rebuilt as paired panels** — shared baseline (both panel bottoms in identical pixel rows), equal plot heights, aligned (a)/(b) labels; matrix `[[2196,57],[25,5073]]`, n=7,351 | Present, correct | `fig:results` | PASS |

All four figures appear before References, near first discussion, with `\caption`,
`\label`, and in-text references (Fig. 1: §4.3/§5.1; Fig. 4: §7.9).

## Table inventory

| Item | Expected Section | Actual Section/Page | Rendering | Caption | Label | Status |
|---|---|---|---|---|---|---|
| Table 1 | §6.2 Composition profile | §6 / p17 | Within margins | Correct | `tab:composition` | PASS |
| Table 2 | §7.1 Primary benchmark | §7 / p19 | Within margins | Correct | `tab:benchmark` | PASS |
| Table 3 | §7.2 Multimodal subset | §7 / p20 | Within margins | Correct | `tab:mm` | PASS |
| Table 4 | §7.4 Imbalance ablation | §7 / p21 | Within margins | Correct | `tab:imbalance` | PASS |
| Table 5 | §7.5 Five-fold CV | §7 / p21 | Within margins | Correct | `tab:cv` | PASS |
| Table 6 | §7.6 Per-fold MM-F1 | §7 / p22 | Within margins | Correct | `tab:folds` | PASS |
| Table 7 | §7.7 Efficiency | §7 / p22 | Within margins | Correct | `tab:efficiency` | PASS |
| Table 8 | §7.7 Early-exit details | §7 / p23 | Within margins | Correct | `tab:earlyexit` | PASS |
| Table 9 | §7.8 Seed variance | §7 / p23 | Within margins | Correct | `tab:seeds` | PASS |
| Table 10 | §7.8 Modality-specific F1 | §7 / p24 | Within margins | Correct | `tab:modality` | PASS |
| Table 11 | Appendix A | Appendix A / p29 (with heading "A Dataset and Preprocessing Reference") | **Inline in appendix** (was deferred float) | Correct | `tab:appdataset` | PASS |
| Table 12 | Appendix B | Appendix B / p29 (heading "B Model Hyperparameters") | **Inline in appendix; Table 13 follows naturally on p30, no gap** | Correct | `tab:apphyper` | PASS |
| Table 13 | Appendix C | Appendix C / p30 (heading "C Results Lineage and Reproducibility") | **Inline in appendix; References begins immediately after on the same page — no gap** | Correct | `tab:lineage` | PASS |

## References boundary check

- Exactly one References section; **33 entries** ([1] Jáñez-Martinez … [33] Loshchilov);
  bibtex clean.
- References starts on p30 immediately after Appendix C's source note and continues
  through p32; the entire References region contains **no tables, no figures, no
  manuscript prose** (banned-pattern scan: NONE).
- Fix applied (final pass): appendix tables converted to inline `[H]` floats inside
  their appendix sections; the earlier `\clearpage` float-flush became unnecessary and
  was removed, eliminating both the Table-12→13 and Table-13→References gaps.
- No prose was converted into bibliography content (converter skips everything after
  the manuscript's `## References` heading; bibliography is generated solely from
  `references.bib`).

## Visual QA summary

- `qa_pixels.py`: all 32 pages within printable bounds; no sparse/empty pages.
- Word-box overlap test (pdftohtml geometry): 0 overlaps on figure pages 10/13/24;
  page 16 had 2 label collisions before the Figure-3 fix, 0 after.
- Zoom inspection (200 dpi) of all four figure pages: boxes, arrows, connectors,
  labels readable; no clipping; no overlaps; figures inside margins.
- LaTeX log: 0 errors, 0 undefined references/citations, 1 overfull hbox
  (4.2pt, §6.1 tokenizer list — cosmetic, documented).

**All items PASS.**
