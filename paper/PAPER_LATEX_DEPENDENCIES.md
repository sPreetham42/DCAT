# PAPER_LATEX_DEPENDENCIES.md — Dependency Audit of `latex/main.tex`

Parsed from the final root source. Result: **`latex/main.tex` has exactly one
external dependency — the bibliography.** Every asset (all four figures) is
inline TikZ/pgfplots vector code inside `main.tex`; there are no
`\includegraphics`, `\input`, `\include`, or `\usepackage{...sty}` local-file
references.

## External file dependencies

| File | Required by | Keep/Delete |
|---|---|---|
| `latex/references.bib` | `\bibliography{references}` (line 1208) | **KEEP** |
| — (none) | figures: inline TikZ/pgfplots | n/a |
| — (none) | tables: inline `booktabs` (13 tables embedded) | n/a |

## Class / package dependencies (TeX distribution, not project files)

| Package | Purpose |
|---|---|
| `article` (class) | base document |
| `geometry` (155×235 mm) | page size/margins |
| `newtxtext`, `newtxmath` (+ TeX Gyre Termes) | Times-like text+math fonts |
| `natbib` + `unsrtnat` | numbered citations, order of first appearance |
| `booktabs` | table rules |
| `fancyhdr` | running headers |
| `tikz`, `pgfplots` | the four vector figures |
| `xurl` | breakable paths/URLs |
| `hyperref`, `adjustbox`, `enumitem`, `caption`, `microtype`, `eurosym`, `lmodern` (fallback) | typography/links/floats |

All ship with MiKTeX/TeX Live — no project-local `.sty`/`.cls`/`.ttf` files are
required. The `sn-jnl` class was evaluated and deliberately **not** used (see
`_archive/PRODUCTION_QA_REPORT.md`); the layout is a documented equivalent.

## Build artifacts (generated, not dependencies)

| File | Status |
|---|---|
| `build/main.pdf` | generated output — copy becomes `DCAT_Final_Practice_Paper.pdf` |
| `build/main.aux/.bbl/.blg/.out/.log` | generated; regenerated on every build |

## Removed non-dependencies (final cleanup)

- `main_prerepair_backup2.tex` — byte-identical duplicate of `main.tex` (deleted)
- `main_frozen_backup.tex`, `main_prerepair_backup.tex`, `DCAT_Final_Rendered.pdf`,
  `PRODUCTION_QA_REPORT.md` — superseded backups (archived in `_archive/`)
- `latex/figures/` — empty vestigial directory (removed; figures are inline)

**Conclusion: nothing required by the final LaTeX source was removed.**
