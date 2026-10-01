# DCAT — Final Paper Package

## Paper

**Title:**
`DCAT: A Dynamic Cross-Attention Transformer for Conditional Multimodal Email Spam Detection`

**Author:**
`Preetham S`

**Email:**
`spreetham6442@gmail.com`

## Final PDF

`DCAT_Final_Practice_Paper.pdf` (32 pages)

## Main LaTeX source

`latex/main.tex` — verified root source (all figures are inline TikZ/pgfplots;
the only external dependency is the bibliography)

## Bibliography

`latex/references.bib` (33 entries)

## Editable manuscript

`FINAL_PAPER.md` — final manuscript content (the author's voice)

## Human-edited source

`HUMAN_EDITABLE_MANUSCRIPT.md` — the author's manual rewrite, preserved as the
record of the human edit (do not modify)

## Documentation

- `PAPER_SOURCE_OF_TRUTH.md` — verified sources and how they relate
- `PAPER_LATEX_DEPENDENCIES.md` — what `main.tex` requires
- `FINAL_DIRECTORY_AUDIT.md` — what was kept / archived / deleted
- `FINAL_PAPER_CHANGE_LOG.md`, `FINAL_HUMANIZED_PAPER_AUDIT.md`,
  `FINAL_FIGURE_TABLE_AUDIT.md` — repair and QA records
- `_archive/` — historical development material (not needed to compile)

## Recompilation

Verified working build process (run from `paper/latex/`):

```bash
cd paper/latex
pdflatex -interaction=nonstopmode -output-directory=build main.tex
bibtex build/main
pdflatex -interaction=nonstopmode -output-directory=build main.tex
pdflatex -interaction=nonstopmode -output-directory=build main.tex
```

Expected result: **0 errors, 0 undefined references/citations, 0 overfull
boxes, 32 pages** (4 harmless BibTeX "empty journal" warnings for arXiv-only
entries). The compiled PDF is `build/main.pdf`; the approved copy is
`../DCAT_Final_Practice_Paper.pdf`.

To regenerate the per-page preview images used for visual QA:

```bash
cd build
pdftoppm -png -r 110 main.pdf rendered_pages/page
```
