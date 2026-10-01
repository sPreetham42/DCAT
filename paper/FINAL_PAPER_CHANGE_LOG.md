# FINAL_PAPER_CHANGE_LOG.md — Final Human-Edited Paper Regeneration

> **FINAL PRODUCTION PASS (2026-09-19, this pass).** Scope: author block, figures,
> tables/floats, typography QA. **No prose changed, no content changed.**
>
> ### Author metadata
> - Guide/supervisor entry `(Guide: Dr. Prathima Mabel)` removed from the title block.
> - Author: `Preetham S` (retained). Email: `spreetham6442@gmail.com` (set as the only
>   contact line). No other author metadata added (no ORCID/phone/affiliation).
>
> ### Figure repairs
> - Figure 4 (results panels): rebuilt as intentionally paired panels — shared baseline
>   by construction (panel (a) matrix bottom and panel (b) pgfplots axis bottom both at
>   y = 0; equal plot heights 3.7; both (a)/(b) labels anchored south at the same y).
>   Verified in the render: both panel bottoms occupy the same pixel rows (300 dpi,
>   ~0.2 mm tolerance); axis tick labels hang outside the plot box (standard).
> - Figures 1–3 carry the previously documented source repairs (stray node removed;
>   cross-attention column gap 34→46 mm; modality-leaf gaps 1→8 mm), all present in
>   the regenerated source.
>
> ### Table repairs
> - Tables 11/12/13 (appendix): placement switched from deferred `[h]` floats to inline
>   `[H]` inside their dedicated appendix sections, and the `\clearpage` before the
>   bibliography removed. Result: Table 12 is followed naturally by Table 13 (no blank
>   band > 10.5 mm anywhere on pp. 29–30), and References begins on the same page where
>   Appendix C's note ends — no forced blank page, no gap.
>
> ### Typography / QA
> - `\emergencystretch` raised 1.5 em → 3 em (tolerance for the one remaining 4.2 pt
>   tokenizer-list line in §6.1). LaTeX log now: **0 errors, 0 undefined refs, 0
>   overfull boxes**, 32 pages. Ink-geometry QA: all 32 pages clean (no blank pages,
>   no margin violations). References region pure: 33 entries, zero tables/figures.
>
> ### Content corrections
> - **None in this pass** (content lock respected). All content corrections remain the
>   116 documented repairs of the previous regeneration pass (Categories 1–2 below).

> **UPDATE (layout-repair pass, 2026-09-19):** three figure-source defects were found
> by page-by-page visual QA and repaired in the figure sources (applied reproducibly in
> `md_to_latex.py`, documented in `FINAL_FIGURE_TABLE_AUDIT.md`):
> 1. Figure 1 — leftover unused node `(poolmm)` (`\phantom{Mean pooling}`) drew an empty
>    box overlapping the cross-attention block → node removed (no arrow referenced it).
> 2. Figure 2 — the two cross-attention formula boxes (~40mm wide) overlapped across the
>    34mm column gap → column separation widened to 46mm.
> 3. Figure 3 — TEXT/IMAGE/MULTIMODAL leaf boxes 1mm apart, labels collided →
>    separations widened to 8mm; EMPTY callout gap 8→13mm.
> Additionally, a `\clearpage` before the bibliography now flushes the appendix float
> queue: Tables 11–13 render inside Appendices A–C, strictly before References
> (previously they drifted onto the References pages). No prose was changed.

**Input manuscript:** `HUMAN_EDITABLE_MANUSCRIPT.md` (author's manual rewrite — the writing authority)
**Repaired master:** `REGENERATED_SOURCE.md` == `FINAL_PAPER.md`
**LaTeX build:** `latex/main.tex` (from `md_to_latex.py`) + `latex/references.bib` (unchanged, 33 entries)
**Final PDF:** `DCAT_Final_Practice_Paper.pdf` (copy of `latex/build/main.pdf`, 32 pages)

---

## Executive summary

The author's manual edit of `HUMAN_EDITABLE_MANUSCRIPT.md` introduced extensive genuine
voice rewrites (all preserved verbatim) alongside **accidental editing damage**: pasted-in
foreign text, corrupted equations, lost superscripts, fabricated numbers, and glue damage
from heading edits. Every repair below is a minimal, individually documented surgical
replacement. No scientific result was changed; no prose was stylistically rewritten.

**Total documented repairs: 116.** Breakdown: 48 destructive-edit repairs,
26 artifact-verified value/citation repairs, 22 structural repairs, 20 debris removals
(precise counts in `FINAL_HUMANIZED_PAPER_AUDIT.md`).

---

## Category 1 — Fabricated or corrupted content removed (destructive edits)

| # | Location | Removed/repaired | Evidence |
|---|---|---|---|
| 1 | §4.3 | Pasted-in gentrification/economics paragraph | No source in any project artifact |
| 2 | §6.1 | Pasted-in econometrics paragraph | No source |
| 3 | §7.x | Pasted-in EFS/UMass paragraph | No source |
| 4 | §9.2 | Pasted-in thermodynamics paragraph | No source |
| 5 | Conclusion | Debris annotation ("Timothy Hosp") | Not author content |
| 6–9 | Abstract, §1, §6.1, §8.2 | Fabricated "1800:1" ham:spam ratios | Artifacts: 25,213:47,993 ≈ 1.90:1 |
| 10 | §7.1 | Fabricated "9.84%/6.36%" latency claims | No artifact |
| 11 | §6.6 | Fabricated "0.001 significance level" | Manuscript uses α = 0.05 |
| 12 | §6.2 | Fabricated "4.46%" | Verified: 0.2% (11/6,046) |
| 13 | §9.1 | "five emails" (multimodal ham count) | Artifacts: 6 ham in test; 327 corpus-wide |
| 14 | §7.x | "4 of 4 models" | Table 3 lists more variants |
| 15–19 | Eqs 1, 3, 5, 14, 15 | Scrambled equation bodies | Frozen `PAPER_CONTENT_REGENERATED.md` |
| 20–21 | Eqs 7, 8 | Deleted bodies restored | Frozen source |
| 22 | Eq 4 | Body lost to a broken regex (`\1` literal) | Frozen source |
| 23 | Eqs 9–11 | Deleted bodies restored | Frozen source |
| 24 | Eq 4 prose | "where $\\hat z_i$..." restored | Frozen source |
| 25–29 | §2.1–§9 headings | ~12 glued/broken headings restored (e.g. "2.1 Email as a Multimodal Communication Medium" glued into prose; `### ###` doubles; `#####` artifacts) | Approved outline |
| 30 | §6.2 | Missing subsection heading restored | Outline |
| 31–35 | Lists §1, §5.1, §6.1, §6.4, §6.4 | Glued enumerations re-split into items | Outline |
| 36–38 | §7.2/§7.3 | Corrupted p-value superscripts ("p = 2.49 10") restored to $2.49\times10^{-45}$, $3.34\times10^{-6}$ | `results_lineage.csv`, frozen source |
| 39 | §3.x | "Res Net"/"Mobile Net" splits fixed to ResNet/MobileNet | Standard names |
| 40–48 | various | Duplicate/fragmented sentences from partial pastes removed (individually anchored) | Frozen source |

## Category 2 — Artifact-verified value corrections

| # | Location | Edited value | Corrected value | Authoritative evidence |
|---|---|---|---|---|
| 1 | §6.1/§9.1 | Corpus counts missing/stale | 75,419 total records; 73,206 usable | `data/manifests/leakage_groups.csv` row count; `data/README.md`; repo audit |
| 2 | §6.2 | Split counts stale | 60,335 / 7,542 / 7,542 (group-disjoint) | leakage manifest split counts |
| 3 | §6.2/§7.2 | Multimodal population | 7,867 multimodal messages (327 ham / 7,540 spam) | pooled OOF artifact + PROVENANCE_AUDIT |
| 4 | §7.2 | Speculative "155-sample" subset caveat | 465-message multimodal test subset (459 spam + 6 ham); 459/465 = 0.9871, Spam-F1 = 918/924 = 0.9935 — matches archived values exactly | `artifacts/experiments/weighted_primary/results.json` (`_raw_modalities`, `accuracy_multimodal`) |
| 5 | §6.1 | "99.4% text-only" misattributed to primary corpus | SpamAssassin profile is 99.4% TEXT; primary corpus is 87.1% text-only (63,772/73,206) | `spamassassin_profile.csv`; corpus modality counts |
| 6 | §6.2 | Test-set attribution ambiguity | Test evaluation ran on the primary corpus (n = 7,351); 6,046 is the supplementary SpamAssassin profile | artifact totals + HANDOVER naming |
| 7 | §7.4/Table 4 | Full-DCAT row provenance | 3-seed means (0.9862/0.9916/0.9809/0.6253); Weighted-DCAT row = imbalance artifact single run (0.9880/0.9927/0.9833/0.7478) | `weighted_cv/` seed files, `final_results.csv` |
| 8 | Appendix C | Lineage note numbers stale | 0.9868 seed-42 entry; CV means 0.6609/0.5564/0.6824 kept as recorded (documented aggregation difference, not silently resolved) | `results_lineage.csv` |
| 9 | §7.5 | Table 6 provenance caveat | Preserved as recorded (documented conflict — reported, not resolved) | PUBLICATION_READINESS_REPORT |
| 10 | Citations | Broken citation remnants in edited regions restored to [1]–[33] numbering | LITERATURE_MAP + frozen source |

## Category 3 — Structural repairs

- Restored the approved 10-section hierarchy + Data Availability, Declarations, Appendices A–C, References (`NEW_PAPER_OUTLINE.md`).
- Re-attached 10 main tables + 3 appendix tables with captions and source notes.
- Restored 4 figure specifications at approved positions (converted to the frozen TikZ figure environments in LaTeX).
- Restored 21 numbered equations at approved positions.
- Reference list re-anchored to the verified bibliography (33 entries, unsrtnat order of first appearance).

## Category 4 — What was NOT changed

- The author's sentence construction, paragraph rhythm, transitions, and vocabulary
  (141 diff blocks vs the edited file, all traceable to the repairs above; no
  stylistic rewrites).
- All verified numerical results: 0.9862, 0.9869, 0.9871, 0.8317, 0.4968, 0.7077,
  0.5453, 0.7478, p-values, 4.45%, 0.63%, 24.82%, 12.8B/12.7B, ~11B early-exit
  convention, 73,309,090 parameters, 2,008,578 trainable (2.74%).
- The documented caveats: Table 3/6 provenance notes, Appendix C lineage explanation,
  FLOPs measurement conventions, efficiency artifact limitation, leakage-audit scope.
- The evidence-based research-gap framing (no "first ever"/"state of the art" claims).
- MobileViT = arXiv:2110.02178 (unchanged in `references.bib`).

## Category 5 — Production-only transforms (no content)

- `[Equation n]` markers → numbered `\begin{equation}` environments.
- `[FIGURE n …]` spec blocks → the four approved vector figure environments.
- Markdown tables → booktabs tables (13), captions from the manuscript.
- Numeric citations `[n]` → `\citep{key}` (33 keys, all resolve).
- Unicode → LaTeX (×, →, superscripts, dashes); file paths → breakable `\path{}`.

---

## Verification trail

- `verify_final.py`: 12/12 PASS on the repaired master (equations, debris, counts, structure, values).
- LaTeX: 0 errors, 0 undefined references/citations, 1 overfull (4.2pt, §6.1 tokenizer list).
- Visual QA: all 32 pages within printable bounds (`qa_pixels.py`), no sparse pages.
- Text-layer checks: 23 key values present, zero banned patterns, 33 bibliography entries.
