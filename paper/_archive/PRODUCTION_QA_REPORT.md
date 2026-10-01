# PRODUCTION_QA_REPORT.md — Final Production Stage

**Manuscript:** `../PAPER_CONTENT_REGENERATED.md` (content locked)
**LaTeX source:** `main.tex` · **Bibliography:** `references.bib`
**Final PDF:** `DCAT_Final_Rendered.pdf` (copy of `build/main.pdf`)
**Page previews:** `build/rendered_pages/page-01..32.png` (32 pages, 100 dpi)

---

## Compilation status

| Item | Result |
|---|---|
| Engine | pdfLaTeX (MiKTeX 25.12) + BibTeX; sequence pdflatex → bibtex → pdflatex ×2 |
| Errors (`!` lines in log) | **0** |
| Undefined citations/references | **0** |
| Missing glyphs / characters | **0** |
| Overfull hbox > 2pt | **0** (worst remaining event: none) |
| Underfull boxes | 14 (cosmetic, standard journal acceptance) |
| BibTeX warnings | 4 ("empty journal" for arXiv-only entries: RoBERTa, DistilBERT, MobileNets, GMU) — faithful to the source citations |
| Fonts | newtx (TeX Gyre Termes X text + NewTX math), Type 1, fully embedded |
| Page count | **32** (155 × 235 mm) |

## Counts

| Item | Count |
|---|---|
| Pages | 32 |
| Words (extracted, incl. captions/refs) | 11,626 |
| Figures | 4 (all real vector graphics; zero placeholders) |
| Tables | 13 (10 main + 3 appendix; manuscript counts the 3 appendix tables as part of Appendices A–C) |
| Numbered equations | 21 (labels eq:attention … eq:exit; sequential in PDF) |
| References | 33 (unsrtnat, order of first appearance; all resolve) |

## Visual QA performed

1. **LaTeX log audit** (scripted): overfull/underfull mapping to pages, missing-glyph scan — 3 layout fixes applied, final pass clean.
2. **Raster bounds audit** (scripted, all 32 page images): ink-bounds detection per page against printable-area thresholds — **no page exceeds bounds**; running header confirmed at 10.2 mm from top edge (journal-conventional placement) after one geometry adjustment.
3. **Text-layer content audit** (scripted, full extracted text): all 10 numbered sections + back matter + Appendices A–C present; Figure 1–4 and Table 1–13 captions all present and sequential; all 21 equation numbers sequential; all 33 bibliography entries present; every key result value verified present verbatim (0.9862, 0.9871, 0.8317, 0.4968, 0.7077, 0.5453, 0.6253→0.7478, 0.9880, p = 2.49×10⁻⁴⁵, p = 3.34×10⁻⁶, 12.8B/12.7B, 73,309,090, 7,867, 4.45%, 24.82%); all four documented caveats verbatim; zero figure placeholders; zero Markdown artifacts; MobileViT = arXiv:2110.02178 (the erroneous 1810.03775 appears nowhere); no "state-of-the-art" or banned lineage phrasing.
4. **Float placement audit**: Figure 1→p11, Figure 2→p13, Figure 3→p16, Tables 1–10→pp17–24, Figure 4→p24, appendix tables→pp28–30. Sequential, no float pile-up, no "float too large" warnings.

## Fixes made during production

| Issue | Fix |
|---|---|
| Custom TikZ style `step` collided with TikZ's built-in `/tikz/step` key (4 errors) | Renamed style to `stage` |
| Figure-4 confusion-matrix colors defined inside a TikZ scope were invisible to the pgfplots axis scope (3 errors) | Moved `cellhi`/`celllo` color definitions to the preamble |
| Figures 1–4 TikZ pictures wider than the 121 mm text block (up to 69 pt overfull) | Wrapped each in `adjustbox{max width=\textwidth}` (downscale only when needed) |
| Unbreakable `artifacts/...` paths overfull in §6.8, §7.2, Data Availability, lineage table (up to 131 pt) | Switched to `url`-package `\path{}` (breakable) typography for long paths |
| Appendix C 7-column lineage table overfull (~90–131 pt per row) | Wrapped in `\resizebox{\textwidth}{!}{...}` |
| Tables 1, 2, 7 marginally overfull | Reduced `\tabcolsep` (3.4–4 pt) — no font shrinking |
| Running header 5 mm from paper edge | Set `headsep=4mm, headheight=13pt` (header now ~10 mm, text block unchanged) |
| `latexmk` one-time hang | MiKTeX was generating newtx font metrics on first run (one-time cost); subsequent compiles are fast. Documented in README |

## Content integrity

No scientific claim, number, dataset, methodology, or conclusion was changed relative to the frozen manuscript. The only manuscript-consistency adjustments are formatting-level conversions: Markdown emphasis → `\emph{}`; the two supplied reference papers remain uncited; back matter limited to the manuscript's own Data Availability and Declarations (no fabricated funding/ethics/contribution statements).

## Remaining non-blocking items

1. **Figures 1–3 are correct vector schematic diagrams** but are functional-dense; if publication at Springer is targeted, the figures may be restyled by a designer later without touching content (TikZ source is fully editable).
2. 14 underfull boxes (slightly loose lines/pages) — cosmetic, invisible at reading zoom.
3. 4 BibTeX "empty journal" warnings are inherent to arXiv-only citations.
4. Figure 4 panel (a) reproduces the DCAT weighted-primary confusion matrix only; the Late Fusion / Text-Only matrices named in the pre-production §7.9 sentence are not archived in the repository and were deliberately **not** fabricated. The caption and §7.9 text state exactly what is shown.
5. `sn-jnl.cls` was not used (Springer's template servers were unreachable during this session); the layout is a documented Springer-compatible equivalent (see README.md). If the venue is later confirmed as Springer MTA, the content ports directly.
