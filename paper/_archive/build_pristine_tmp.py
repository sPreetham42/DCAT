# Builds HUMAN_EDITABLE_MANUSCRIPT.md from the frozen manuscript by mechanical
# transformation (no manual retyping of prose -> zero transcription drift).
# Also emits a JSON verification payload consumed by the audit step.
import json
import re

SRC = "PAPER_CONTENT_REGENERATED.md"
OUT = "pristine_baseline_tmp.md"

text = open(SRC, encoding="utf-8").read()

# ---------------------------------------------------------------------------
# 1. Strip internal separator lines ('---' between sections) so the editable
#    manuscript reads as one continuous document. Equations are untouched.
# ---------------------------------------------------------------------------
lines = text.splitlines()
out_lines = []
for ln in lines:
    if ln.strip() == "---" or ln.strip() == "***":
        out_lines.append("")
    else:
        out_lines.append(ln)
text = "\n".join(out_lines)

# ---------------------------------------------------------------------------
# 2. Equation handling: convert $$...$$ blocks carrying \tag{n} into
#    labeled blocks:  [Equation n]  followed by the math in $$ ... $$
#    (math notation itself is preserved verbatim, \tag{} removed).
# ---------------------------------------------------------------------------
eq_counter = 0

def eq_repl(m):
    global eq_counter
    eq_counter += 1
    body = m.group(1)
    tag = re.search(r"\\tag\{(\d+)\}", body)
    n = int(tag.group(1)) if tag else eq_counter
    # remove only the tag token itself, preserving all surrounding whitespace
    body = re.sub(r"\\tag\{\d+\}", "", body)
    return f"[Equation {n}]\n\n$${body}$$"

text = re.sub(r"\$\$(.*?)\\tag\{\d+\}\$\$", eq_repl, text, flags=re.S)

# ---------------------------------------------------------------------------
# 3. Figure placeholders -> full specification blocks (marker + caption from
#    the finalized production source, plus placement/purpose/source fields).
# ---------------------------------------------------------------------------
FIG_SPECS = {
    "1": (
        "DCAT OVERALL ARCHITECTURE",
        "DCAT architecture overview. Deterministic modality routing assigns each "
        "email to the TEXT, IMAGE, MULTIMODAL, or EMPTY category; only the required "
        "encoders are invoked. For MULTIMODAL emails, a text-only auxiliary "
        "classifier may exit early and classify without vision; otherwise "
        "bidirectional cross-attention exchanges information between the projected "
        "streams before pooling and fusion. Frozen components are shown in blue; "
        "trainable components in orange.",
        "Section 5.1 (after the architecture-overview paragraph). Purpose: show the "
        "actual DCAT pipeline — deterministic router, modality-specific encoders, "
        "projectors, bidirectional cross-attention, pooling/fusion, shared "
        "classifier, and the early-exit branch from the text-only auxiliary "
        "classifier. Data source: methodology of Sections 4 and 5 (Eqs. 2, 3, 7-21).",
    ),
    "2": (
        "CROSS-ATTENTION BLOCK",
        "One bidirectional cross-attention layer. Each stream's queries attend to "
        "the other stream's keys and values (Eqs. 12-15); the attended "
        "representation is added back to its own stream through a residual MLP "
        "update (Eqs. 16-17). Layer Normalization is applied before each sub-layer "
        "(Pre-LN). The layer is repeated N_xattn = 2 times with h = 4 heads and "
        "per-head dimension d_k = 64.",
        "Section 5.5 (after the bidirectional cross-attention equations). Purpose: "
        "make the Q/K/V relationships between the two streams concrete and "
        "consistent with Eqs. 12-17. Data source: methodology of Section 5.5 "
        "(Eqs. 12-17) and the hyperparameters of Appendix B.",
    ),
    "3": (
        "PREPROCESSING FLOW",
        "Preprocessing and data-flow diagram. Raw .eml files pass through the four "
        "deterministic stages of Section 6.1 (MIME parsing; content filtering with "
        "the size and quality thresholds annotated; image processing; text "
        "tokenization) before deterministic modality assignment. EMPTY messages are "
        "discarded from training and evaluation.",
        "Section 6.1 (after the four preprocessing stages). Purpose: show the "
        "pipeline from raw input to model-ready modalities with the exact "
        "thresholds annotated (>=10 chars text; >=20x20 px and >=1024 bytes image; "
        "224x224 resize). Data source: Section 6.1 stages 1-4.",
    ),
    "4": (
        "RESULTS VISUALIZATION PANEL",
        "Results visualization. (a) Confusion matrix of DCAT in the "
        "weighted-primary configuration on the full test set (n = 7,351; 57 false "
        "positives, 25 false negatives). (b) Multimodal Macro-F1 for all evaluated "
        "variants on the multimodal subset, reproducing the values of Table 3 "
        "(ASP: All-Spam Prior; MI: Modality Indicator; Text: Text-Only; Image: "
        "Image-Only; PB: Published Baseline; LF: Late Fusion; NoXAttn: "
        "DCAT-No-XAttn; DCAT: Full-DCAT; EE: DCAT-Early-Exit). Majority-collapsed "
        "variants sit at 0.4968; DCAT-No-XAttn reaches 0.8317.",
        "Section 7.9 (Confusion-Matrix Results). Purpose: make the contrast between "
        "corpus-level and subset-level behavior directly visible. Data source: "
        "(a) artifacts/experiments/weighted_primary/results.json "
        "(confusion matrix [[2196, 57], [25, 5073]], n = 7,351); (b) Table 3 values.",
    ),
}

def fig_repl(m):
    num = m.group(1)
    title, caption, purpose = FIG_SPECS[num]
    return (
        f"[FIGURE {num} — {title}]\n\n"
        f"**Caption:** {caption}\n\n"
        f"**Placement & purpose:** {purpose}\n\n"
        f"**Note:** final graphics are produced in the LaTeX project "
        f"(`latex/figures/`, vector sources); the specifications above are the "
        f"approved rendering contract for regeneration."
    )

text = re.sub(
    r"\*\[FIGURE (\d) PLACEHOLDER:.*?\]\*",
    fig_repl,
    text,
    flags=re.S,
)

# ---------------------------------------------------------------------------
# 4. Section-7.9 sentence: production finalized a provenance-accurate wording
#    for Figure 4 (recorded in PRODUCTION_QA_REPORT.md). Transfer the
#    finalized form so the editable master matches the rendered PDF, and
#    disclose the substitution here (this file, not the manuscript body).
# ---------------------------------------------------------------------------
MD_79 = (
    "Confusion matrices for DCAT, Late Fusion, and Text-Only on both the full "
    "test set and the multimodal subset, together with a Macro-F1 comparison "
    "plot, are provided in Figure 4."
)
PROD_79 = (
    "Figure 4 reports the archived confusion matrix for DCAT in the "
    "weighted-primary configuration (panel a), the configuration in which the "
    "class-weighting analysis of Section 7.4 was performed, together with a "
    "Macro-F1 comparison across the evaluated variants on the multimodal subset "
    "(panel b, values from Table 3)."
)
sec79_replaced = MD_79 in text
if sec79_replaced:
    text = text.replace(MD_79, PROD_79)

# ---------------------------------------------------------------------------
# 5. Human-editing markers before each major section (top-level numbered
#    sections + back matter + appendices), and before selected subsections.
# ---------------------------------------------------------------------------
EDIT_MSG = (
    "<!-- HUMAN EDITING: Rewrite this section in your own natural academic "
    "voice while preserving all facts, numbers, citations, and technical "
    "meaning. -->"
)

MAJOR_SECTIONS = [
    "1. Introduction",
    "2. Background",
    "3. Related Work",
    "4. Problem Formulation",
    "5. The DCAT Architecture",
    "6. Experimental Methodology",
    "7. Results",
    "8. Discussion",
    "9. Limitations and Threats to Validity",
    "10. Conclusion and Future Work",
    "Data Availability",
    "Declarations",
    "Appendix A. Dataset and Preprocessing Reference",
    "Appendix B. Model Hyperparameters",
    "Appendix C. Results Lineage and Reproducibility",
]

SUBSECTIONS = [
    "2.6 Conditional Computation and Early Exits",
    "3.6 Summary of Gaps",
    "4.4 Learning Objective",
    "5.5 Bidirectional Cross-Attention",
    "5.7 Shared Classifier and Early-Exit Mechanism",
    "6.2 Dataset Composition, Splits, and Leakage Control",
    "7.2 Multimodal-Subset Results",
    "7.4 Class-Imbalance Ablation",
    "7.7 Efficiency Results",
    "9.3 Evaluation Limitations",
]

for name in MAJOR_SECTIONS + SUBSECTIONS:
    # subsections are '###', major sections '##' -> match both
    pattern = re.compile(r"(?m)^(#{2,3} " + re.escape(name) + r")\s*$")
    text = pattern.sub(EDIT_MSG + "\n\n\\1", text)

# ---------------------------------------------------------------------------
# 6. Assemble the final document: status header + body + fact-check appendix.
# ---------------------------------------------------------------------------
HEADER = """# HUMAN EDITING STATUS

* Source manuscript: `PAPER_CONTENT_REGENERATED.md`
* Scientific source of truth: `PAPER_CONTENT.md`
* Structure source: `NEW_PAPER_OUTLINE.md`
* Citation source: `LITERATURE_MAP.md`
* Status: `NOT YET HUMAN-EDITED`
* Scientific content: `FROZEN`
* Manual prose editing: `PENDING`

Editing rules:

* Rewrite voice, rhythm, transitions, and wording freely — but every fact,
  number, citation, caveat, equation, table value, and figure datum below is
  frozen and must survive your edits verbatim.
* The `<!-- HUMAN EDITING -->` markers are guidance only; remove them as you go.
* Equations appear as `[Equation n]` + the math in `$$ ... $$` — keep the
  numbering and notation unchanged.
* Tables: keep every row and value; you may adjust wording in captions.
* `HUMAN EDITING FACT-CHECK REFERENCE` at the end of this file lists every
  value to verify after editing. It is NOT part of the paper.

---
"""

FOOTER = open("factcheck_footer.md", encoding="utf-8").read()
final = HEADER.rstrip() + "\n\n" + text.strip() + "\n\n---\n\n" + FOOTER
open(OUT, "w", encoding="utf-8", newline="\n").write(final)

# ---------------------------------------------------------------------------
# 7. Verification payload for the audit step.
# ---------------------------------------------------------------------------
payload = {
    "equations_tagged": eq_counter,
    "fig_specs_inserted": len(re.findall(r"\[FIGURE \d — ", final)),
    "edit_markers": final.count(EDIT_MSG),
    "expected_markers": len(MAJOR_SECTIONS) + len(SUBSECTIONS),
    "refs": len(re.findall(r"(?m)^\[\d+\] ", final)),
    "sec79_replaced": sec79_replaced,
    "word_count": len(final.split()),
    "src_word_count": len(text.split()),
}
json.dump(payload, open("editable_build_stats.json", "w"), indent=2)
print(json.dumps(payload, indent=2))
