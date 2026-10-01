# FINAL_DIRECTORY_AUDIT.md — Paper Folder Cleanup & Packaging

**Date:** 2026-09-19 · **Scope:** `paper/` only (research artifacts outside
`paper/` — `data/`, `results/`, `experiments/`, `src/`, `scripts/`, etc. —
were not touched).

## MAIN SOURCE

`paper/latex/main.tex` — verified root source (documentclass, begin/end
document, maketitle, abstract, bibliography command, full section structure;
only external file dependency is the `.bib`).

## BIBLIOGRAPHY

`paper/latex/references.bib` — 33 verified entries.

## FINAL PDF

`paper/DCAT_Final_Practice_Paper.pdf` — 32 pages, regenerated from the cleaned
package; text layer byte-identical to the previously approved build (11,785
words, all anchors verified: title, author `Preetham S`, email, `[1]`…`[33]`
bibliography).

## FIGURE DEPENDENCIES

None external. All four figures are inline TikZ/pgfplots in `main.tex`
(architecture; cross-attention; preprocessing flow; results panels with the
archived confusion matrix `[[2196,57],[25,5073]]`, n = 7,351).

## KEEP (final package)

```text
paper/
├── README.md                          ← new: short practical entry point
├── PAPER_SOURCE_OF_TRUTH.md           ← new: verified sources + rebuild
├── PAPER_LATEX_DEPENDENCIES.md        ← new: dependency audit
├── FINAL_DIRECTORY_AUDIT.md           ← this file
├── FINAL_PAPER.md                     final manuscript content (author's voice)
├── HUMAN_EDITABLE_MANUSCRIPT.md       author's human-edited source (preserved)
├── DCAT_Final_Practice_Paper.pdf      final PDF (32 pp)
├── FINAL_PAPER_CHANGE_LOG.md          every documented repair
├── FINAL_HUMANIZED_PAPER_AUDIT.md     content-preservation/consistency audit
├── FINAL_FIGURE_TABLE_AUDIT.md        figure/table placement audit
└── latex/
    ├── main.tex                       root LaTeX source
    ├── references.bib                 bibliography (33 entries)
    ├── README.md                      build + layout + figure provenance
    ├── qa_pixels.py / qa_context.py / qa_log.py   QA scripts (used by audits)
    └── build/
        ├── main.pdf                   latest verified build output
        ├── rendered_pages/            32 PNG page previews (current build)
        └── approved_pages/            QA page set of the approved build
```

## ARCHIVE (moved to `paper/_archive/` — 47 items)

| Group | Files |
|---|---|
| Research/structure phases | `PAPER_CONTENT.md`, `PAPER_CONTENT_backup.md`, `PAPER_CONTENT_REGENERATED.md`, `PAPER_CONTENT_REGENERATED_REFERENCE_MAP.md`, `NEW_PAPER_OUTLINE.md`, `REFERENCE_STYLE_BLUEPRINT.md`, `LITERATURE_MAP.md`, `PUBLICATION_READINESS_REPORT.md`, `FINAL_PRESENTATION_AUDIT.md`, `FINAL_RESEARCH_SOURCE_OF_TRUTH_70K.md`, `HUMAN_EDITABLE_MANUSCRIPT_AUDIT.md` |
| Reference PDFs | `base paper.pdf`, `ref1.pdf`, `ref2.pdf` |
| Old render | `final paper (30).pdf` |
| Superseded bib/template | `references.bib` (Phase-1 `ref1/ref2` keys), `template.tex` (IEEE) |
| Stale root compile | `stale_root_main.tex`, `stale_root_main.pdf` |
| LaTeX backups | `main_frozen_backup.tex`, `main_prerepair_backup.tex`, `DCAT_Final_Rendered.pdf`, `PRODUCTION_QA_REPORT.md` |
| Repair/conversion/QA scripts | `build_editable_manuscript.py`, `build_pristine_tmp.py`, `validate_editable_manuscript.py`, `repair_humanized.py`, `repair_pass2..6.py`, `probe4.py`, `probe_anchors*.py`, `scan_state.py`, `scan_formats.py`, `catalogue_state.py`, `verify_repaired.py`, `verify_final.py`, `md_to_latex.py` |
| Temp debris | `editable_build_stats.json`, `factcheck_footer.md`, `full_diff_tmp.txt`, `pristine_baseline_tmp.md`, `REGENERATED_SOURCE.md` (byte-identical to `FINAL_PAPER.md`) |

## DELETE (permanently, 9 items: 7 files + 2 empty dirs)

| File | Reason |
|---|---|
| `latex/main_prerepair_backup2.tex` | byte-identical duplicate of `main.tex` (MD5 match) |
| `latex/main.aux/.bbl/.blg/.log/.out`, `latex/missfont.log` | regenerable compile artifacts |
| `latex/figures/`, `temp/` | empty vestigial directories |
| `latex/build/` intermediate debris (50 files: probe XMLs/SVGs, zoom PNGs, review HTML sheets, scratch logs) | QA scratch; conclusions recorded in the audit docs |

## DUPLICATE RESOLUTION

- Final PDF: one authoritative copy at top level (== `latex/build/main.pdf`).
- `main.tex`: one authoritative copy (byte-identical backup deleted).
- `references.bib`: authoritative copy in `latex/` (superseded root copy archived).
- Manuscripts: `FINAL_PAPER.md` (final) and `HUMAN_EDITABLE_MANUSCRIPT.md`
  (human source) retained; `REGENERATED_SOURCE.md` duplicate archived.

## REBUILD STATUS

✅ **The cleaned package recompiles successfully from scratch:**
pdflatex → bibtex → pdflatex ×2 gives **0 errors, 0 undefined
references/citations, 0 overfull boxes, 32 pages**; the rebuilt PDF's text
layer is byte-identical to the approved final PDF. The only BibTeX messages are
the 4 documented harmless "empty journal" warnings for arXiv-only entries.
