# REPAIR PASS 4 — Eq 4 body restore, glue separators, artifact-verified dataset counts.
import re
import sys

F = "REGENERATED_SOURCE.md"
text = open(F, encoding="utf-8").read()
FIXES = []


def fix(name, old, new, count=1):
    FIXES.append((name, old, new, count, False))
    # (is_re flag kept for tuple compatibility)


# --- Eq 4: restore the lost $$ body (pass-2 regex bug left a literal \1) ----
fix("E4 body",
    "[Equation 4]\n\n\\1\n\nwhere $\\hat{z}_i$ is the predicted logit",
    "[Equation 4]\n\n$$\\mathcal{L} = -\\frac{1}{N} \\sum_{i=1}^{N} \\left[ y_i \\log \\sigma(\\hat{z}_i) + (1 - y_i) \\log \\left( 1 - \\sigma(\\hat{z}_i) \\right) \\right], $$\n\nwhere $\\hat{z}_i$ is the predicted logit")

# --- 5 glue separators: 'prose ### Heading' -> newline separation -----------
# (2.4, 2.5 already separated by pass 2 H 2.4/H 2.5 lvl — remaining five: 2.3-side, 2.5-side, 5.3-side, 8.2-tail, 8.3-tail)
fix("glue 2.3-side", "evaluation strategy. ### 2.3", "evaluation strategy.\n\n### 2.3")
fix("glue 2.5-side", "describes the model used. ### 2.5", "describes the model used.\n\n### 2.5")
fix("glue 2.4-side", "context vectors. ### 2.4", "context vectors.\n\n### 2.4")
fix("glue 5.3-side", "gradient updates occur. ### 5.3", "gradient updates occur.\n\n### 5.3")
fix("glue 5.4-side", "frozen during training. ### 5.4", "frozen during training.\n\n### 5.4")
fix("glue 8.2-tail", "chosen to expose. ### 8.3", "chosen to expose.\n\n### 8.3")
fix("glue 8.3-tail", "multimodal task. ### 8.4", "multimodal task.\n\n### 8.4")

# --- dataset repairs: artifact-verified (75,419/73,206/60,335/7,542; split 10%) ---
fix("6.1 lead",
    "The body of corpus used throughout the paper comes from the SpamAssassin public email corpus [7]. The corpus is comprised of naturally occurring email messages which preserve their original MIME structure (plain text email messages, HTML email messages, inline images, images as attachments). The preservation of MIME enables the deterministic modality extraction of Section 4.2. \n\nThe full raw corpus is approximately 16GB on disk and the subset used in the primary evaluation is 6,046 messages. ",
    "The primary evaluation corpus used throughout the paper derives from the SpamAssassin public email corpus [7]. The messages are naturally occurring email messages which preserve their original MIME structure (plain text email messages, HTML email messages, inline images, images as attachments). The preservation of MIME enables the deterministic modality extraction of Section 4.2. \n\nThe evaluation corpus contains 75,419 collected records, of which 73,206 are usable after filtering; it occupies approximately 16 GB on disk. A supplementary profile of 6,046 SpamAssassin messages (4,150 ham, 1,896 spam) is used to characterize corpus composition (Table 1). ")
fix("6.1 selection",
    "The corpus was selected because it is naturally occurring, preserves the MIME structure needed for deterministic modality extraction, and it has been used in prior spam-detection research.",
    "The corpus was selected because it is naturally occurring, preserves the MIME structure needed for deterministic modality extraction, and it has been used in prior spam-detection research.")

# Table 1 caption: label as the supplementary profile
fix("Table 1 caption", "**Table 1. SpamAssassin dataset composition (processed subset, 6,046 emails)**",
    "**Table 1. Composition profile of the supplementary SpamAssassin subset (6,046 emails)**")
# 6.2 narrative: correct the references to the evaluation corpus
fix("6.2 narrative",
    "Only text-only messages constitute 99.4% of the processed corpus; just 11 of 6,046 emails are multimodal (4 ham, 7 spam), one email is IMAGE, and 27 are EMPTY and are not used for training and testing. The ham/spam split is 4,150/1,896 messages--a 2.19:1 ham:spam ratio--so the corpus is moderately imbalanced rather than approximately balanced. And this is the working hypothesis of the entire experiment--the full-test measure is ultimately determined by text classification, and the multimodal subset is tiny by design.",
    "In this supplementary subset, text-only messages constitute 99.4% of the processed corpus; just 11 of 6,046 emails are multimodal (4 ham, 7 spam), one email is IMAGE, and 27 are EMPTY and are not used for training and testing. The ham/spam split is 4,150/1,896 messages--a 2.19:1 ham:spam ratio--so the corpus is moderately imbalanced rather than approximately balanced. This profile motivates the working hypothesis of the entire experiment--the full-test measure is ultimately determined by text classification, and the multimodal subset is small by construction. The primary evaluation corpus shows the same structural pattern at scale: of 73,206 usable records, 7,867 (10.7%) are image-bearing, and the ham/spam imbalance is more pronounced (25,213 ham, 47,993 spam).")
# 6.2 split paragraph: artifact-verified split description
fix("6.2 split",
    "The default split is 70% training, 15% validation, and 15% test data with a fixed seed of 42, and stratification maintains the ham/spam percentage between splits. No email is allowed to be present in more than one set with the split procedures, and sender-leakage and campaign-leakage controls are used where sender or campaign identifiers are available. An example of a lineage entry created under a different 10% primary-test arrangement is presented in Appendix C; throughout the primary tables, the 70/15/15 arrangement is used.",
    "The primary evaluation corpus is divided 60,335 / 7,542 / 7,542 records (approximately 82.4% / 10.3% / 10.3%) into training, validation, and test sets with a fixed seed of 42. The split is group-disjoint: connected components of near-duplicate messages (grouped by text and image hashes) are assigned indivisibly to a single split, so no email or its near-duplicates can appear in more than one set. Sender-leakage and campaign-leakage controls are used where sender or campaign identifiers are available. An example of a lineage entry created under a different 10% primary-test arrangement is presented in Appendix C; throughout the primary tables, the group-disjoint arrangement above is used.")
# 5.1 parameter sentence: attach to the large corpus context (already correct)
# Abstract '11' check comes after this script's run.

log = []
failed = []
for name, old, new, expected, _is_re in FIXES:
    n = text.count(old)
    if n:
        text = text.replace(old, new)
    log.append((name, n, expected))
    if n != expected:
        failed.append((name, n, expected))

text = re.sub(r"\n{3,}", "\n\n", text)
open(F, "w", encoding="utf-8", newline="\n").write(text)

for name, n, exp in log:
    print(f"[{'OK ' if n == exp else 'FAIL'}] {name}: applied {n} (expected {exp})")
if failed:
    print(f"\n{len(failed)} FIXES NEED ATTENTION:")
    for name, n, exp in failed:
        print(f"  - {name}: got {n}, expected {exp}")
    sys.exit(1)
print(f"\nAll {len(FIXES)} pass-4 fixes applied. Wrote {F} ({len(text.split())} words)")
