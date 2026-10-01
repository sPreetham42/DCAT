# PAPER_SOURCE_OF_TRUTH.md — Final Paper Package

**MAIN LATEX FILE: `latex/main.tex`**

**BIBLIOGRAPHY FILE: `latex/references.bib`**

**FINAL PDF: `DCAT_Final_Practice_Paper.pdf`**

---

## Verification of the main LaTeX file

`latex/main.tex` was verified (not assumed) to be the root source that produced
`DCAT_Final_Practice_Paper.pdf`:

- contains exactly one `\documentclass`, `\begin{document}`, `\maketitle`,
  `\begin{abstract}`, `\bibliographystyle`, and `\end{document}`;
- title block: *DCAT: A Dynamic Cross-Attention Transformer for Conditional
  Multimodal Email Spam Detection*, author `Preetham S`,
  email `spreetham6442@gmail.com`;
- full 10-section body + Data Availability + Declarations + `\appendix`
  A–C + `\bibliography{references}`;
- all four figures are inline TikZ/pgfplots (the file has **no**
  `\includegraphics`/`\input`/`\include` — its only external dependency is the
  `.bib`);
- compiled from the cleaned package it reproduces the approved PDF exactly
  (text layer byte-identical, 32 pages, same vector operations on all figure
  pages).

## The three manuscript layers

### `HUMAN_EDITABLE_MANUSCRIPT.md`
Author-humanized editable source. The author's manual rewrite is the voice of
the paper. **Do not modify** — it is the preserved record of the human edit.

### `FINAL_PAPER.md`
Final cleaned manuscript == the repaired human-edited text (byte-identical to
the repair chain's output). This is the manuscript-content authority for the
final package; any future prose edit should start here.

### `latex/main.tex`
Actual typeset source used to compile the final PDF. Its prose corresponds to
`FINAL_PAPER.md` (transformed to LaTeX by the documented repair/conversion
chain; transformations recorded in `FINAL_PAPER_CHANGE_LOG.md`).

## Recompilation

```bash
cd paper/latex
pdflatex -interaction=nonstopmode -output-directory=build main.tex
bibtex build/main
pdflatex -interaction=nonstopmode -output-directory=build main.tex
pdflatex -interaction=nonstopmode -output-directory=build main.tex
```

Verified: 0 errors, 0 undefined references/citations, 0 overfull boxes,
32 pages. Details: `latex/README.md`.

## Package map

| Path | Role |
|---|---|
| `FINAL_PAPER.md` | Final manuscript content (human-edited voice) |
| `HUMAN_EDITABLE_MANUSCRIPT.md` | Author's human-edited source (preserved) |
| `DCAT_Final_Practice_Paper.pdf` | Final approved PDF |
| `latex/main.tex` | Root LaTeX source |
| `latex/references.bib` | Bibliography (33 entries) |
| `latex/README.md` | Build + layout + figure provenance |
| `PAPER_LATEX_DEPENDENCIES.md` | Complete dependency audit |
| `FINAL_DIRECTORY_AUDIT.md` | What was kept / archived / deleted |
| `FINAL_PAPER_CHANGE_LOG.md` | Every documented repair (author metadata, figures, tables, content) |
| `FINAL_HUMANIZED_PAPER_AUDIT.md` | Content-preservation + consistency audit |
| `FINAL_FIGURE_TABLE_AUDIT.md` | Figure/table placement + rendering audit |
| `latex/build/rendered_pages/` | PNG of every PDF page (visual QA) |
| `_archive/` | Historical development material (not needed to compile) |
