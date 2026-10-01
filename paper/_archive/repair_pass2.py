# REPAIR PASS 2 — residual fixes for REGENERATED_SOURCE.md
# Addresses the 17 missed anchors + structural residue from pass 1.
# All anchors verified against current file bytes (scan_state.py / catalogue_state.py).
import re
import sys

F = "REGENERATED_SOURCE.md"
text = open(F, encoding="utf-8").read()

FIXES = []


def fix(name, old, new, count=1):
    FIXES.append((name, old, new, count, False))


def fixre(name, pat, new, count=1):
    FIXES.append((name, pat, new, count, True))


# ---------------- 1. '# ### ' doubles ---------------------------------------
n_d = text.count("# ### ")
text = text.replace("# ### ", "### ")
print(f"[info] '# ### ' normalized: {n_d}")

# ---------------- 2. remaining glued headings (probe-verified bytes) --------
fix("H 2.1", "that is not used in the paper. ### 2.1 Email as a Multimodal Communication Medium",
    "that is not used in the paper.\n\n### 2.1 Email as a Multimodal Communication Medium\n\n")

# '### ### 2.5 Attention and Cross-Modal Attention' + glued lead sentence
fix("H 2.5", "### ### 2.5 Attention and Cross-Modal Attention\n\nAttention allows one vector set Q to produce",
    "### 2.5 Attention and Cross-Modal Attention\n\nAn attention mechanism allows one vector set Q to produce")

# 2.2 / 2.3: headings glued at line end (same line as prose)
fix("H 2.2", "(Section 3.3). ### 2.2 Spam, Phishing, and the Modern Threatscape\n",
    "(Section 3.3).\n\n### 2.2 Spam, Phishing, and the Modern Threatscape\n\n")
fix("H 2.3", "evaluation strategy. ### 2.3 Content Representations for Text\n",
    "evaluation strategy.\n\n### 2.3 Content Representations for Text\n\n")

# 2.4: full glue with lead sentence
fix("H 2.4", "### 2.4 Content Representations for Images Visual representations have followed",
    "### 2.4 Content Representations for Images\n\nVisual representations have followed")

# 2.6: '#' level + debris subline
fix("H 2.6", "# 2.6 Conditional Computation and Early Exits\n\n2.1. Conditional computation Standard neural networks",
    "### 2.6 Conditional Computation and Early Exits\n\nStandard neural networks")

# 3.6: '#' level + glued + inline-list compressed
fixre("H 3.6",
      r"# 3\.6 Gaps in Surveyed Literature Four specific gaps emerge from Sections 3\.1–3\.5, and the paper is organized to address each: 1\. Cross-modal interaction in email spam studies is limited to a few specialized formalisms \(if any\) \[4\] \[27\] - none is the dynamic, token-level, bidirectional cross-attention proven in vision-language architectures \[5\], which has not appeared in the surveyed email-spam literature\. 2\. Unconditional visual encoding is expensive: multimodal pipelines encode both modalities for every message \[4\] even though real corpora are text-dominated \[1\], \[7\] — paying vision cost where it cannot matter\. ",
      "### 3.6 Summary of Gaps\n\nFour specific gaps emerge from Sections 3.1–3.5, and the paper is organized to address each:\n\n1. Cross-modal interaction in email spam studies is limited to a few specialized formalisms (if any) [4], [27] - none is the dynamic, token-level, bidirectional cross-attention proven in vision-language architectures [5], which has not appeared in the surveyed email-spam literature.\n2. Unconditional visual encoding is expensive: multimodal pipelines encode both modalities for every message [4] even though real corpora are text-dominated [1], [7] — paying vision cost where it cannot matter.\n")

# 4. Problem Formulation bare line + '#' subsections -> proper levels
fix("H 4", "\n4. Problem Formulation\n\n# 4.1 Task Definition",
    "\n## 4. Problem Formulation\n\n### 4.1 Task Definition")

# 5.2: glued at line end
fix("H 5.2", "decision space. ### 5.2 Text Encoder\n",
    "decision space.\n\n### 5.2 Text Encoder\n\n")
# 5.3: glued at line end
fix("H 5.3", "updates occur. ### 5.3 Vision Encoder\n",
    "updates occur.\n\n### 5.3 Vision Encoder\n\n")
# 5.4: glued + capitalized 'projector' + inline where-clause
fix("H 5.4", "### 5.4 Modality projector The projector maps each modality into the shared D-dimensional latent space (D = 256): [Equation 9]",
    "### 5.4 Modality Projector\n\nThe projector maps each modality into the shared $d_{model}$-dimensional latent space ($d_{model} = 256$):\n\n[Equation 9]")
# 5.5: '#' level
fix("H 5.5", "# 5.5 Bidirectional Cross-Attention", "### 5.5 Bidirectional Cross-Attention")
# 5.7: bare glued line
fix("H 5.7", "5.7 Shared Classifier and Early-Exit Mechanism The shared classifier maps the $d_{model}$-dimensional representation",
    "### 5.7 Shared Classifier and Early-Exit Mechanism\n\nThe shared classifier maps the $d_{model}$-dimensional representation")

# 6.2: debris paste -> approved heading
fix("H 6.2",
    "6.2 Number of datasets, sets and set leakage3.2.1. Sets3.2.2.1. Leakage3.2.2. Data sets3.2.2.4. Sequence and set setsThere are five datasets included in the dataset:12,1234 as well as the training, validation, and testing datasets.12,12,12,2,12,2,3,12,123.12.16.5,12,2,4.12,124.1.4,23,4.15,22,22.2.12,3.23,42,52,1.3,4A fundamental distinction of the series is that the mixed data sets and the train, validation, and test data are (to varying degrees) distributed – i.e., not randomly distributed.12,12,12,2,12,2,3,4Distribution of the data sets (usage within the training, validation, and test sets).12,12,1253.1,2,1,2,1,26,3,3,34,2,6.2.2.2.6.2.2.8.8.2.3.9.9.2.3.10.10.2.3.11.11.2.1.3.2.2.4.3.2.4.3.2.4.3.2.4.3.2.4.3.2.4.3.2.1.14.14.15.8.\nTable 1 shows the structure of the processed corpus.",
    "### 6.2 Dataset Composition, Splits, and Leakage Control\n\nTable 1 shows the structure of the processed corpus.")

# 9.1: unbolded labels + 'effected' + misattributed subset wording
fix("H 9.1 a",
    "\nExtreme multimodal scarcity. There are a mere 11 emails in the primary SpamAssassin set, all of which are multimodal. Scores on the primary test set are effected significantly by single prediction, and cannot be assumed to generalize to any other domain.",
    "\n**Extreme multimodal scarcity.** Only 11 emails in the primary SpamAssassin subset are multimodal. Scores on this multimodal subset are affected significantly by single predictions, and cannot be assumed to generalize to any other domain.")
fix("H 9.1 b", "\nSingle corpus. All experiments were conducted on the SpamAssassin corpus.",
    "\n**Single corpus.** All experiments were conducted on the SpamAssassin corpus.")
# 9.2: unbolded labels + hyphenation
fix("H 9.2 a", "\nFrozen encoders. DistilBERT and MobileViT are frozen, they were not fine-tuned on the domain data.",
    "\n**Frozen encoders.** DistilBERT and MobileViT are frozen; they were not fine-tuned on the domain data.")
fix("H 9.2 b", "\nFusion method. The proposed multimodal representation is (element-wise averaging) fused after crossattention;",
    "\n**Fusion method.** The proposed multimodal representation is (element-wise averaging) fused after cross-attention;")

# 10: glued heading + corrupted claim wording
fixre("H 10",
      r"\n10\. Conclusion and future work This paper presented the conditional multimodal email spam detection architecture DCAT combining bidirectional cross-attention, deterministic routing, and optional early-exit computation evaluated on a natural multimodal pair of corpora \(SpamAssassin\), where the defining property is multimodal scarcity \(11/6,046 emails\) under a text-only majority \(99\.4%\)\.",
      "\n## 10. Conclusion and Future Work\n\nThis paper presented DCAT, a conditional multimodal email spam detection architecture combining bidirectional cross-attention, deterministic routing, and optional early-exit computation, evaluated on a naturally paired corpus (SpamAssassin) whose defining property is multimodal scarcity (11 of 6,046 emails) under a text-only majority (99.4%).")

# ---------------- 3. equation-body repairs ----------------------------------
# Eq 7: body deleted -> pristine
fix("E7 restore", "[Equation 7] where the input is truncated or padded to 256 tokens",
    "[Equation 7]\n\n$$\\mathbf{H}_{text} = \\text{DistilBERT}(\\mathbf{x}_{text}). $$\n\nwhere the input is truncated or padded to 256 tokens")
# Eq 8: body deleted -> pristine
fix("E8 restore", "[Equation 8] $\\mathbf{H}_{img}$ contains $S$ spatial tokens",
    "[Equation 8]\n\n$$\\mathbf{H}_{img} = \\text{MobileViT}(\\mathbf{x}_{img}). $$\n\n$\\mathbf{H}_{img}$ contains $S$ spatial tokens")
# Eq 4: lead 'Where:' -> 'The unweighted training objective is' + 'Where' -> 'where'
fixre("E4 lead", r"\[Equation 4\]\n\nWhere: \$\$", "[Equation 4]\n\n$$")
fixre("E4 where", r"(\$\$\\mathcal\{L\} = .*?\$\$)\n\nWhere \$", r"\1\n\nwhere $")

# ---------------- 4. value/fact repairs -------------------------------------
# gap3 '1800' debris
fixre("X gap3 1800",
      r"3\. Class imbalance in the cited studies is wrongly ignored by some systems and, more tolerably, unmentioned by all \[1\], \[2\], even though the domain literature \[1\] \[7\] clear mentions that individual messages about 1800 text tokens to 1 email visual \"token\.\"\s*",
      "3. Class imbalance in the multimodal subset is under-treated. Multimodal spam evaluations do not report imbalance-corrected training or subset-level significance, although the ham/spam imbalance is documented in the domain literature [1], [2].\n")
# 8.2 sentence reassembly
fix("X 8.2 reassembly",
    "On the multimodal test subset, of Full-DCAT to the multimodal test subset is a 0.4968→0.8317 improvement over the baseline DCAT-No-XAttn (Table 3). This large improvement directed in the \"opposite\" direction from the proposed design goal was the critical benchmark driving the story of the study.",
    "On the multimodal test subset, DCAT-No-XAttn reports Macro-F1 0.8317 compared with 0.4968 for Full-DCAT (Table 3) — the largest architecture-linked difference in the study — and it runs in the opposite direction from the design's intent. This large, counter-directional difference was the critical benchmark driving the story of the study.")
# 8.4 4.46% fabrication
fix("X 8.4 4.46",
    "because only 4.46% of the messages in the total corpus are multimodal, the overall fraction of GPU FLOPS saved per-messages in the evaluation workload is 0.63%.",
    "because only a small fraction of the corpus is multimodal, the resulting average FLOP reduction over the evaluated workload is 0.63%.")
# 2.4 ResNet/MobileNet spacing
fix("F 2.4 names", "Res Net [17] introduced residual pathways to enable even deeper models, and Mobile Nets [18]",
    "ResNet [17] introduced residual pathways to enable even deeper models, and MobileNets [18]")
# 6.3 ResNet-18
fix("F 6.3 names", "Res Net-18", "ResNet-18")

# ---------------- 5. apply + report -----------------------------------------
log = []
failed = []
for name, old, new, expected, is_re in FIXES:
    if is_re:
        text, n = re.subn(old, lambda m, _n=new: _n, text, flags=re.S)
    else:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
    log.append((name, n, expected))
    if n != expected:
        failed.append((name, n, expected))

text = re.sub(r"\n{3,}", "\n\n", text)
open(F, "w", encoding="utf-8", newline="\n").write(text)

for name, n, exp in log:
    status = "OK " if n == exp else "FAIL"
    print(f"[{status}] {name}: applied {n} (expected {exp})")
if failed:
    print(f"\n{len(failed)} FIXES NEED ATTENTION:")
    for name, n, exp in failed:
        print(f"  - {name}: got {n}, expected {exp}")
    sys.exit(1)
print(f"\nAll {len(FIXES)} pass-2 fixes applied. Wrote {F} ({len(text.split())} words)")
