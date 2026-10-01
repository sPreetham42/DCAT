# DCAT — Final LaTeX Source

This directory contains the complete, self-contained LaTeX source of the final paper.

- **Main source:** `main.tex` (all 10 sections + Data Availability + Declarations + Appendices A–C + bibliography; figures are inline TikZ/pgfplots vector code — no external image assets)
- **Bibliography:** `references.bib` (33 verified entries; `unsrtnat`, numbered by first appearance)
- **Build output:** `build/` (`main.pdf` plus aux files; `rendered_pages/` holds one PNG per page for visual QA; `approved_pages/` holds the QA page set of the approved build)
- **QA scripts:** `qa_pixels.py`, `qa_context.py`, `qa_log.py` (page-bounds / text-layer / log checks used for the final visual QA)

## Compilation

```bash
cd paper/latex
pdflatex -interaction=nonstopmode -output-directory=build main.tex
bibtex build/main
pdflatex -interaction=nonstopmode -output-directory=build main.tex
pdflatex -interaction=nonstopmode -output-directory=build main.tex
```

Verified state of the final build: **0 errors, 0 undefined references/citations,
0 overfull boxes, 32 pages**. The 4 harmless BibTeX "empty journal" warnings
correspond to arXiv-only entries (RoBERTa, DistilBERT, MobileNets, GMU) encoded
with `and others`.

Note (MiKTeX): the first compile after installing `newtx` may pause while font
metrics are generated on demand; this is one-time.

## Layout (do not change without need)

Native Springer-compatible journal layout from the `article` class: trim size
155 × 235 mm, single-column 10 pt (newtx Times-like text+math), numbered
sections/equations, `natbib`+`unsrtnat` citations, `fancyhdr` running headers,
`booktabs` tables, appendices via `\appendix`. No fabricated publication
metadata (no DOI/volume/received dates).

## Figure provenance (summary)

All four figures are vector TikZ/pgfplots drawn from the methodology and the
archived artifacts only. Figure 4 panel (a) uses the DCAT weighted-primary
confusion matrix `[[2196, 57], [25, 5073]]` (n = 7,351) from
`artifacts/weighted_primary/results.json`; no confusion matrix was fabricated.
The final-pass figure repairs (stray node removal, column-gap and leaf-spacing
fixes, Figure 4 shared-baseline rebuild) are already applied in `main.tex` and
documented in `../FINAL_FIGURE_TABLE_AUDIT.md` and `../FINAL_PAPER_CHANGE_LOG.md`.

Historical development material (old backups, earlier manuscripts, reference
PDFs, repair scripts) is in `../_archive/` — nothing there is needed to compile.
