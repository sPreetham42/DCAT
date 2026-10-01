# Repairs HUMAN_EDITABLE_MANUSCRIPT.md into REGENERATED_SOURCE.md.
# Author's voice preserved; accidental editing damage surgically fixed;
# approved structure (NEW_PAPER_OUTLINE hierarchy) restored.
# Every fix is asserted to apply exactly the expected number of times.
import re
import sys

SRC = "HUMAN_EDITABLE_MANUSCRIPT.md"
OUT = "REGENERATED_SOURCE.md"

text = open(SRC, encoding="utf-8").read()

# ---------------------------------------------------------------- extraction
# Keep paper proper: from title through reference [33]; drop editing-status
# header and fact-check appendix (not part of the paper).
start = text.index("# DCAT: A Dynamic Cross-Attention Transformer")
end_ref33 = text.index("[33] I. Loshchilov")
text = text[start:text.index("\n", end_ref33)]
# strip editing-guidance comments
text = re.sub(r"<!-- HUMAN EDITING:.*?-->", "", text, flags=re.S)

FIXES = []
def fix(name, old, new, count=1):
    FIXES.append((name, old, new, count, False))

def fixre(name, pat, new, count=1):
    FIXES.append((name, pat, new, count, True))

# =============================== A. STRUCTURE ===============================
# glued heading/prose splits and heading-level normalization
fix("H 1", "# 1. Introduction Email is the foundation",
    "## 1. Introduction\n\nEmail is the foundation")
fix("H 2", "2. Background This section presents",
    "## 2. Background\n\nThis section presents")
fix("H 2.1", "### 2.1 Email as a Multimodal Communication Medium The classifier built",
    "### 2.1 Email as a Multimodal Communication Medium\n\nThe classifier built")
fix("H 2.2", "and learning (Section 3.3). ### 2.2 Spam, Phishing, and the Modern Threatscape Spam is defined",
    "and learning (Section 3.3).\n\n### 2.2 Spam, Phishing, and the Modern Threatscape\n\nSpam is defined")
fix("H 2.3", "multi-protocol evaluation strategy. ### 2.3 Content Representations for Text This subsection traces",
    "multi-protocol evaluation strategy.\n\n### 2.3 Content Representations for Text\n\nThis subsection traces")
fix("H 2.4", "Section 5.3 describes the model used. ### 2.4 Content Representations for Images Visual representations",
    "Section 5.3 describes the model used.\n\n### 2.4 Content Representations for Images\n\nVisual representations")
fix("H 2.5", "Section 5.3 describes the model used.", "Section 5.3 describes the model used.", 0)  # placeholder no-op
FIXES.pop()  # remove no-op
fix("H 2.5a", "224 x 224 resize). Data source: stages 1-4 of Section 6.1.",
    "224 x 224 resize). Data source: stages 1-4 of Section 6.1.", 0)
FIXES.pop()
# 2.5 heading is glued with its first sentence: "### 2.5 Attention and Cross-Modal Attention allows one vector set..."
fix("H 2.5", "2.5 Attention and Cross-Modal Attention allows one vector set Q to produce",
    "### 2.5 Attention and Cross-Modal Attention\n\nAn attention mechanism allows one vector set Q to produce")
fix("H 2.6", "### 2.6 Conditional Computation and Early Exits\n\n2.1. Conditional computation Standard neural networks",
    "### 2.6 Conditional Computation and Early Exits\n\nStandard neural networks")
fix("H 3", "3. Related work The background and related work sections of this paper answer different questions: What mechanisms does this paper construct on? ",
    "## 3. Related Work\n\nBackground and related work answer different questions: what mechanisms does this paper build on? ")
fix("H 3 intro b", "What mechanisms have other systems built on?\n\nHow was that work constructed on?\n\nWhat is the specific question this paper asks?\n\nBackground and related work are broken into three approach families; no single system anchors this paper. All numbers are full-test unless explicitly broken out: no identical-theory pair underpins our work.",
    "What mechanisms have other systems built on? What is the specific question this paper asks?\n\nWork is grouped into approach families; no single system anchors this paper.")
fix("H 3.1", "3.1 Text-based spam detection Scored pattern rules",
    "### 3.1 Text-Based Spam Detection\n\nScored pattern rules")
fix("H 3.2", "3.2 Image-based spam detection Image-spam detection treats",
    "### 3.2 Image-Based Spam Detection\n\nImage-spam detection treats")
fix("H 3.3", "3.3 Multimodal spam detection and fusion Multimodal spam detectors fuse",
    "### 3.3 Multimodal Spam Detection and Fusion\n\nMultimodal spam detectors fuse")
fix("H 3.4", "3.4 Conditional computation Early-exit architectures introduce",
    "### 3.4 Conditional Computation in Classification Systems\n\nEarly-exit architectures introduce")
fix("H 3.5 tail", "on pooled out-of-sample predictions.3.6 Gaps in Surveyed Literature Three gaps",
    "on pooled out-of-sample predictions.\n\n### 3.6 Summary of Gaps\n\nThree gaps")
fix("H 3.5", "3.5 Evaluation practice in settings of modality imbalance between available sources of evidence complicates evaluation practice:",
    "### 3.5 Evaluation Practice in Modality-Imbalanced Settings\n\nModality imbalance between available sources of evidence complicates evaluation practice:")
fix("H 4", "4. Problem Formulation\n\n### 4.1 Task Definition",
    "## 4. Problem Formulation\n\n### 4.1 Task Definition")
fix("H 4.2", "# 4.2 Modality Routing", "### 4.2 Modality Routing")
fix("H 4.3", "# 4.3 Conditional Computation Paths", "### 4.3 Conditional Computation Paths")
fix("H 4.4", "# 4.4 Learning Objective", "### 4.4 Learning Objective")
fix("H 5", "5. The DCAT Architecture ### 5.1 Architecture overview DCAT consists of 5 components:",
    "## 5. The DCAT Architecture\n\n### 5.1 Architecture Overview\n\nDCAT consists of five components:")
fix("H 5.2", "### 5.2 Text encoder The text encoder is DistilBERT-base-uncased [15], a 6-layer Transformer",
    "### 5.2 Text Encoder\n\nThe text encoder is DistilBERT-base-uncased [15], a six-layer Transformer")
fix("H 5.3", "### 5.3 Vision encoder The vision encoder is MobileViT-small [20], accessed via the `timm` library [21]. Images are resized to 224 x 224 pixels before encoding. \n\nWith normalized image tensor, it produces spatial feature representations:",
    "### 5.3 Vision Encoder\n\nThe vision encoder is MobileViT-small [20], accessed via the `timm` library [21]. Images are resized to $224 \\times 224$ pixels before encoding. With normalized image tensor $\\mathbf{x}_{img}$, it produces spatial feature representations:")
fix("H 5.6", "# 5.6 Pooling and Fusion", "### 5.6 Pooling and Fusion")
fix("H 6", "6. Experimental Methodology\n\n# 6.1 Corpus and Preprocessing",
    "## 6. Experimental Methodology\n\n### 6.1 Corpus and Preprocessing")
fix("H 6.2", "6.2 Number of datasets, sets and set leakage3.2.1. Sets3.2.2.1. Leakage3.2.2. Data sets3.2.2.4. Sequence and set setsThere are five datasets included in the dataset:12,1234 as well as the training, validation, and testing datasets.12,12,12,2,12,2,3,12,123.12.16.5,12,2,4.12,124.1.4,23,4.15,22,22.2.12,3.23,42,52,1.3,4A fundamental distinction of the series is that the mixed data sets and the train, validation, and test data are (to varying degrees) distributed – i.e., not randomly distributed.12,12,12,2,12,2,3,4Distribution of the data sets (usage within the training, validation, and test sets).12,12,1253.1,2,1,2,1,26,3,3,34,2,6.2.2.2.6.2.2.8.8.2.3.9.9.2.3.10.10.2.3.11.11.2.1.3.2.2.4.3.2.4.3.2.4.3.2.4.3.2.4.3.2.4.3.2.1.14.14.15.8.\nTable 1 shows the structure of the processed corpus.",
    "### 6.2 Dataset Composition, Splits, and Leakage Control\n\nTable 1 shows the structure of the processed corpus.")
fix("H 6.5", "# 6.5 Evaluation Metrics", "### 6.5 Evaluation Metrics")
fix("H 6.6", "# 6.6 Statistical Evaluation", "### 6.6 Statistical Evaluation")
fix("H 6.7", "# 6.7 Efficiency Evaluation", "### 6.7 Efficiency Evaluation")
fix("H 6.8", "# 6.8 Error-Analysis Protocol", "### 6.8 Error-Analysis Protocol")
fix("H 7", "7. Results\n\nWith that settled in Section 6, now it is just what the measures reveal.",
    "## 7. Results\n\nWith that settled in Section 6, what remains is what the measures reveal.")
fix("H 7.1", "# 7.1 Full-Test-Set Benchmark", "### 7.1 Full-Test-Set Benchmark")
fix("H 7.3", "# 7.3 Cross-Attention Ablation", "### 7.3 Cross-Attention Ablation")
fix("H 7.5", "The imbalance ablation is the only comparison in this study with statistically decisive differences. 7.5 Multimodal Robustness: Five-Fold Cross-Validation Research question: is the multimodal signal stable? A five-fold cross-validation of the larger evaluation subset described in the experiment artifacts (Table 5).",
    "The imbalance ablation is the only comparison in this study with statistically decisive differences.\n\n### 7.5 Multimodal Robustness: Five-Fold Cross-Validation\n\n*Research question: is the multimodal signal stable?*\n\nFive-fold cross-validation is performed on the larger evaluation subset described in the experiment artifacts (Table 5).")
fix("H 8", "8. Discussion This section interprets the evidence of Section 7.\n\nObserved results are distinguished from their plausible interpretations; speculation is distinguished from explicit claims. 8.1 Why the Full-Test Metric Barely Moves The observed result is",
    "## 8. Discussion\n\nThis section interprets the evidence of Section 7. Observed results are distinguished from their plausible interpretations; speculation is distinguished from explicit claims.\n\n### 8.1 Why the Full-Test Metric Barely Moves\n\nThe observed result is")
fix("H 8.2", "Section 8.2 interprets. \n\n8.2 Signal, Scarcity, and Sensitivity in the Multimodal Subset The single-measure contribution",
    "Section 8.2 interprets.\n\n### 8.2 The Multimodal Subset: Signal, Scarcity, and Sensitivity\n\nOn the multimodal test subset,")
fix("H 8.3", "8.3 Class Weighting Changes 75 more than Architecture Changes The training-objective ablation",
    "### 8.3 Class Weighting Changes More than Architecture Does\n\nThe imbalance ablation")
fix("H 8.4", "8.4 Efficiency: Theory versus Measured Overhead The early exit mechanism",
    "### 8.4 Efficiency: Theoretical Savings versus Measured Overhead\n\nThe early-exit mechanism")
fix("H 8.5", "8.5 What Does DCAT Establish and Not?\n\nTogether, the protocols",
    "### 8.5 What DCAT Does and Does Not Establish\n\nRead together, the protocols")
fix("H 9", "9. Limitations and Threats to Validity\n\n# 9.1 Dataset Limitations",
    "## 9. Limitations and Threats to Validity\n\n### 9.1 Dataset Limitations")
fix("H 9.2", "# 9.2 Architecture Limitations", "### 9.2 Architecture Limitations")
fix("H 9.3", "# 9.3 Evaluation Limitations", "### 9.3 Evaluation Limitations")
fix("H 9.4", "# 9.4 Threats to Validity", "### 9.4 Threats to Validity")
fix("H 10", "10. Conclusion and future work This paper presented the conditional multimodal email spam detection architecture DCAT combining bidirectional cross-attention, deterministic routing, and optional early-exit computation evaluated on a natural multimodal pair of corpora (Spam Assassin), where the defining property is multimodal scarcity (11/6,046 emails) under a text-only majority (99.4%).",
    "## 10. Conclusion and Future Work\n\nThis paper presented DCAT, a conditional multimodal email spam detection architecture combining bidirectional cross-attention, deterministic routing, and optional early-exit computation, evaluated on a naturally paired corpus (SpamAssassin) whose defining property is multimodal scarcity (11 of 6,046 emails) under a text-only majority (99.4%).")

# ========================= B. FABRICATED CONTENT REMOVAL ====================
fixre("X gentrification", r"It should be noted that certain areas or districts in the city.*?long experienced disinvestment\)\.\s*", "")
fixre("X econometrics", r"The relationship between the variables could be linear.*?essential as including relevant variables\.\s*", "")
fixre("X EFS", r"\[2\] The new EFS is the first state-based.*?Department of Postsecondary Education \(DPS\)\.\s*", "")
fixre("X thermo", r"Hopefully, in another reorganisation scenario.*?only the second process\.\s*", "")
fixre("X thermo2", r"The two cycles are combined and merged on one g\..*?the answer to both should be the same\.\s*", "")
fix("X hosp", " Human annotator of this work: Timothy Hosp. No competing interests.", "")
fixre("X 1800 gap2", r"even when corpus analysis shows the text content outnumbers email's visual content by a factor of 1800:1 \[7\], \[1\] - wasting vision effort needlessly\.",
      "even though real corpora are text-dominated [1], [7] — paying vision cost where it cannot matter.")
fixre("X gap3", r"3\. Class imbalance in the cited studies is wrongly ignored.*?1800 text tokens to 1 email visual \"\.token\.\"\"",
      "3. Class imbalance in the multimodal subset is under-treated. Multimodal spam evaluations do not report imbalance-corrected training or subset-level significance, although the ham/spam imbalance is documented in the domain literature [1], [2]")
fix("X gap3 tail", "3. Class imbalance in the multimodal subset is under-treated. Multimodal spam evaluations do not report imbalance-corrected training or subset-level significance, although the ham/spam imbalance is documented in the domain literature [1], [2], even though the domain literature [1] [7] clear mentions",
    "3. Class imbalance in the multimodal subset is under-treated. Multimodal spam evaluations do not report imbalance-corrected training or subset-level significance, although the ham/spam imbalance is documented in the domain literature [1], [2], even though the domain literature [1], [7] clearly documents")
fix("X gap1 hedge", "none is the dynamic, token-level, bidirectional cross-attention dominant in vision-language architectures [5], too new to have appeared in email spam.",
    "none is the dynamic, token-level, bidirectional cross-attention proven in vision-language architectures [5], which has not appeared in the surveyed email-spam literature.")
fix("X gap4 conj", "DCAT addresses each of these gaps: the combinations of cross-attention (gap 1), early exit (gap 2), class-weighting (gap 3), and multi-protocol evaluation (gap 4).",
    "DCAT addresses each of these gaps: bidirectional cross-attention (gap 1), deterministic modality routing with early exit (gap 2), a class-weighting ablation (gap 3), and a multi-protocol evaluation with statistical testing (gap 4).")
fix("X 3intro families", "Background and related work are broken into three approach families; no single system anchors this paper.",
    "Background and related work are organized into approach families; no single system anchors this paper.")
fix("X 3.6 count", "Three gaps below are revealed in Sections 3.1-3.5, and the paper is organized to address each:",
    "Four specific gaps emerge from Sections 3.1–3.5, and the paper is organized to address each:")

# ===================== C. VALUE / FACT CORRUPTION REPAIRS ===================
# Equation 1 (scrambled by paste) -> pristine form
fixre("E1 block", r"\[Equation 1\] \[2\].*?---V, \[3\]",
      "[Equation 1]\n\n$$\\text{Attention}(Q, K, V) = \\text{Softmax}\\!\\left( \\frac{QK^{T}}{\\sqrt{d_k}} \\right) V, $$")
fix("E1 where", "where d is the number of dimensions in Q and K, which are identical.",
    "where $d_k$ is the per-head key dimension.")
# Equation 2: author's prose collapsed the equation; restore the numbered display
fix("E2 block", "[Equation 2]\n\nWhere $y \\in \\{0, 1\\},$ $y=0$ is ham and legitimate email, and $y=1$ is spam.",
    "[Equation 2]\n\n$$y \\in \\{0, 1\\}, \\qquad y = 0 \\text{ (ham, legitimate email)}, \\quad y = 1 \\text{ (spam)}. $$")
# Equation 3: author's version inserted stray articles and lost math form
fixre("E3 block", r"\[Equation 3\]\n\nModality\(m\) = .*?\\end\{cases\}\s*",
      "[Equation 3]\n\n$$\\text{modality}(m) = \\begin{cases} \\text{MULTIMODAL}, & \\text{if } has\\_text \\wedge has\\_image, \\\\ \\text{TEXT}, & \\text{if } has\\_text \\wedge \\neg has\\_image, \\\\ \\text{IMAGE}, & \\text{if } \\neg has\\_text \\wedge has\\_image, \\\\ \\text{EMPTY}, & \\text{otherwise.} \\end{cases} $$\n\n")
# Equation 5: author's version lost LaTeX log/sigma formatting
fixre("E5 block", r"\[Equation 5\]\n\nWeighted \(Positive\):.*?\\sigma\(\\hat\{z\}_i\)\)\] \$\$",
      "[Equation 5]\n\n$$\\mathcal{L}_{weighted} = -\\frac{1}{N} \\sum_{i=1}^{N} \\left[ w_{pos}\\, y_i \\log \\sigma(\\hat{z}_i) + (1 - y_i) \\log \\left( 1 - \\sigma(\\hat{z}_i) \\right) \\right], $$")
# Equations 9-11: bodies deleted -> restore pristine
fix("E9-11 block", "[Equation 9] [Equation 10] with projection matrices where the projections are trainable; they are the first stage at which the two modalities inhabit a common space.",
    "[Equation 9]\n\n$$\\mathbf{Z}_{text} = \\text{LayerNorm}\\!\\left( \\mathbf{H}_{text} \\mathbf{W}_{text} + \\mathbf{b}_{text} \\right), $$\n\n[Equation 10]\n\n$$\\mathbf{Z}_{img} = \\text{LayerNorm}\\!\\left( \\mathbf{H}_{img} \\mathbf{W}_{img} + \\mathbf{b}_{img} \\right), $$\n\nwith projection matrices\n\n[Equation 11]\n\n$$\\mathbf{W}_{text} \\in \\mathbb{R}^{768 \\times d_{model}}, \\qquad \\mathbf{W}_{img} \\in \\mathbb{R}^{D_{img} \\times d_{model}}, $$\n\nwhere $D_{img}$ is the MobileViT feature dimension and $d_{model} = 256$. The projections are trainable; they are the first stage at which the two modalities inhabit a common space.")
# remove the debris paragraph that had displaced Eqs. 9-11
fixre("X projector debris", r"\[Equations 11, 12\] The projected representations are of size.*?Spatial projector described in \[6\]\.\s*", "")
# Equation 12: restore bold K/V (formatting consistency with Q)
fix("E12 bold", "$$\\mathbf{Q}_{text} = \\mathbf{Z}_{text} \\mathbf{W}_{Q,text} \\qquad K_{img} = \\mathbf{Z}_{img} \\mathbf{W}_{K,img} \\qquad V_{img} = \\mathbf{Z}_{img} \\mathbf{W}_{V,img}$$",
    "$$\\mathbf{Q}_{text} = \\mathbf{Z}_{text} \\mathbf{W}_{Q,text}, \\qquad \\mathbf{K}_{img} = \\mathbf{Z}_{img} \\mathbf{W}_{K,img}, \\qquad \\mathbf{V}_{img} = \\mathbf{Z}_{img} \\mathbf{W}_{V,img}, $$")
# Equation 13 stray period
fix("E13 period", "\\mathbf{V}_{img}. $$.", "\\mathbf{V}_{img}. $$")
# Equation 14 region: debris sentence + lost equation body
fixre("E14 region", r"\[Equation 14\]\n\nAnd andare, respectively, the query image, key text, and value text were obtained by These yielded the query image, key text, and value text representation\. Were obtained by \(18\) \(19\) \(20\)",
      "[Equation 14]\n\n$$\\mathbf{Q}_{img} = \\mathbf{Z}_{img} \\mathbf{W}_{Q,img}, \\qquad \\mathbf{K}_{text} = \\mathbf{Z}_{text} \\mathbf{W}_{K,text}, \\qquad \\mathbf{V}_{text} = \\mathbf{Z}_{text} \\mathbf{W}_{V,text}, $$")
# Equation 15: author's unicode degeneration -> pristine LaTeX
fixre("E15 block", r"\[Equation 15\]\n\nZ\(text → img\) = Softmax\(Z\(QimgK\(text\)T\)/√dK\)Z\(Vtext\)\.",
      "[Equation 15]\n\n$$\\mathbf{Z}_{text \\rightarrow img} = \\text{Softmax}\\!\\left( \\frac{\\mathbf{Q}_{img} \\mathbf{K}_{text}^{T}}{\\sqrt{d_k}} \\right) \\mathbf{V}_{text}. $$")
fix("X 5.5 debris", "All too simple solution, suppose, that answered your problems? The two streams are then added with residual connections:",
    "The two streams are then added with residual connections:")
# 5.5 first sentence: 2 layers each bidirectional (not one per direction)
fix("C 5.5 layers", "The cross-attention module has a total of $N_{xattn} = 2$ identical layers, one for each of the directions of information flow, sharing the co-attention design of [5] and the scaled dot-product approach of Eq. (1).",
    "The cross-attention module has a total of $N_{xattn} = 2$ identical layers, each performing information exchange in both directions, sharing the co-attention design of [5] and the scaled dot-product approach of Eq. (1).")
fix("C 5.5 mh", "Multi-head Attention We use $h=4$ heads with dimensions $d_{k} = 64$ per head.",
    "Multi-head attention: we use $h = 4$ heads with dimensions $d_{k} = 64$ per head.")
# 5.3: SHS debris -> pristine spatial-grid sentence
fix("C 5.3 SHS", "where SHS = 15x15 for the evaluated configuration. Like the text encoder, the vision encoder is frozen during training.",
    "$\\mathbf{H}_{img}$ contains $S$ spatial tokens; for the evaluated configuration the feature map corresponds to a $15 \\times 15$ spatial grid. Like the text encoder, the vision encoder is frozen during training.")
# 5.1 component list reassembly (author's fragments, proper list form)
fixre("S 5.1 list", r"1\. Text encoder \(DistilBERT \[15\]\) encodes email text into token-level contextual embeddings 2\. \n\nVision encoder \(MobileViT \[20\]\) encodes email images into spatial visual feature maps 3\. \n\nModality projector maps both encoder outputs into a shared latent space of dimension = 256 \(d\) by linear projections followed by Layer Normalization 4\. Bidirectional cross-attention exchanges information between text and image representations in the shared latent space 5\. Shared classifier maps the fused or unimodal shared representations into a spam/ham prediction \[FIGURE 1 - DCAT OVERALL ARCHITECTURE\] Caption: DCAT architecture overview\. Deterministic modality routing assigns each email to the TEXT, IMAGE, MULTIMODAL, or EMPTY category, where only the required encoders are invoked\. \n\nFor MULTIMODAL emails a text-only auxiliary classifier may exit early and classify without vision, otherwise bidirectional cross-attention exchanges information between the projected streams before pooling and fusion\. \n\nFrozen components are shown in blue, trainable components in orange\. Placement & purpose: Section 5\.1 \(after the architecture-overview paragraph\)\. Purpose: show the actual DCAT pipeline - deterministic router, modality-specific encoders, projectors, bidirectional cross-attention, pooling/fusion, shared classifier, and the early-exit branch from the text-only auxiliary classifier\. \n\nData source: methodology of Sections 4 and 5 \(Eqs\. 2, 3, 7-21\)\. Note: final graphics are produced in the LaTeX project \(`latex/figures/`, vector sources\); the specifications above are the approved rendering contract for regeneration\. ",
      "1. **Text encoder (DistilBERT [15]):** encodes email text into token-level contextual embeddings.\n2. **Vision encoder (MobileViT [20]):** encodes email images into spatial visual feature maps.\n3. **Modality projector:** maps both encoder outputs into a shared latent space of dimension $d_{model} = 256$, using linear projections followed by Layer Normalization.\n4. **Bidirectional cross-attention:** exchanges information between text and image representations in the shared latent space.\n5. **Shared classifier:** maps fused or unimodal shared representations into a spam/ham prediction.\n\n[FIGURE 1 - DCAT OVERALL ARCHITECTURE]\n\n**Caption:** DCAT architecture overview. Deterministic modality routing assigns each email to the TEXT, IMAGE, MULTIMODAL, or EMPTY category, where only the required encoders are invoked. For MULTIMODAL emails a text-only auxiliary classifier may exit early and classify without vision, otherwise bidirectional cross-attention exchanges information between the projected streams before pooling and fusion. Frozen components are shown in blue, trainable components in orange.\n\n**Placement & purpose:** Section 5.1 (after the architecture-overview paragraph). Purpose: show the actual DCAT pipeline - deterministic router, modality-specific encoders, projectors, bidirectional cross-attention, pooling/fusion, shared classifier, and the early-exit branch from the text-only auxiliary classifier. Data source: methodology of Sections 4 and 5 (Eqs. 2, 3, 7-21).\n\n**Note:** final graphics are produced in the LaTeX project (`latex/figures/`, vector sources); the specifications above are the approved rendering contract for regeneration.\n")
# 5.1 rationale paragraph: rejoin author's split
fix("S 5.1 rationale", "The design rationale follows from Sections 2 and 4. \n\nThe encoders are frozen pre-trained models",
    "The design rationale follows from Sections 2 and 4. The encoders are frozen pre-trained models")
# 5.4 remainder (after restored Eqs 9-11): author's LayerNorm sentence retained; remove displaced text
fixre("S 5.4 tail", r"Layer normalization after the linear projection stabilizes the scale of both projected streams before they interact, which matters because the two encoders were pre-trained with different internal distributions\. \n\nD img is the MobileViT feature dimension \(960\)[^\n]*",
      "Layer normalization after the linear projection stabilizes the scale of both projected streams before they interact, which matters because the two encoders were pre-trained with different internal distributions.")
# Figure 2 spec reassembly
fixre("S fig2", r"\[FIGURE 2 - CROSS-ATTENTION BLOCK\]\n\nFigure 3 Caption: One bidirectional cross-attention layer\. Queries of each stream attend to keys and values of the other stream \(Eqs\. 12-15\)\. \n\nThe attended representation of the other stream is added back to its own stream via a residual MLP update \(Eqs\. \n\n16-17\)\. Layer Normalization is applied before each sub-layer \(Pre-LN\)\. The layer is repeated N_xattn = 2 times with h = 4 heads and per-head dimension d_k = 64\.\n\nAdaptations & anectdotes Placement & purpose: Section 5\.5 \(following the bidirectional cross-attention equations\)\. Purpose: to give weight to the \(intimidating\) Q/K/V relationships between streams and remain consistent with Eqs\. 12-17\. Data source: method of Section 5\.5 \(Eqs\. 12-17\) and the hyperparameters of Appendix B\.\n\nNote: final graphics are built in the LaTeX project \(`latex/figures/`, sources in vector\), the above requirements constitute the agreed rendering contract upon regenerations\.",
      "[FIGURE 2 - CROSS-ATTENTION BLOCK]\n\n**Caption:** One bidirectional cross-attention layer. Queries of each stream attend to the keys and values of the other stream (Eqs. 12-15); the attended representation is added back to its own stream via a residual MLP update (Eqs. 16-17). Layer Normalization is applied before each sub-layer (Pre-LN). The layer is repeated $N_{xattn} = 2$ times with $h = 4$ heads and per-head dimension $d_k = 64$.\n\n**Placement & purpose:** Section 5.5 (following the bidirectional cross-attention equations). Purpose: to give weight to the Q/K/V relationships between streams and remain consistent with Eqs. 12-17. Data source: method of Section 5.5 (Eqs. 12-17) and the hyperparameters of Appendix B.\n\n**Note:** final graphics are built in the LaTeX project (`latex/figures/`, sources in vector), the above requirements constitute the agreed rendering contract upon regenerations.")
# 5.7 lead sentence + H_fused gloss
fix("C 5.7 lead", "The shared classifier is (d_{model})-dimensional to 1-dimensional, implemented the same way on each path:",
    "The shared classifier maps the $d_{model}$-dimensional representation to a single logit, implemented the same way on each path:")
fix("C 5.7 Hfused", "- $\\mathbf{H}_{fused}$ is a multimodal fused representation, or one of the pools of a unimodal representation.",
    "- $\\mathbf{H}_{fused}$ is the fused multimodal representation or the corresponding pooled unimodal representation.")
# 5.7 equations: put display math on its own line after the label
fix("F E19", "[Equation 19]$$p(y = 1 \\mid m)", "[Equation 19]\n\n$$p(y = 1 \\mid m)")
fix("F E20", "[Equation 20]$$p_{aux}(y = 1 \\mid t)", "[Equation 20]\n\n$$p_{aux}(y = 1 \\mid t)")
fix("F E21", "[Equation 21]$$\\text{exit if } p_{aux}", "[Equation 21]\n\n$$\\text{exit if } p_{aux}")
# 5.7 path arrows lost
fix("F 5.7 arrows", "the entire multimodal path is performed: text vision cross-attention fusion shared classifier.",
    "the entire multimodal path is performed: text → vision → cross-attention → fusion → shared classifier.")
# 5.8: meaning inversion repair (encoders are frozen, not the trainable set)
fix("C 5.8 inversion", "The trainable component consists of the projection layer, the cross-attention layers, and the classifiers; it is this component that needs to be frozen to train single-epoch on this corpus, and that maintains a similar size to the fusion variants it is compared against.",
    "The trainable component consists of the projection layer, the cross-attention layers, and the classifiers; freezing the encoders is what makes single-epoch training on this corpus feasible, and it keeps the trainable component of similar size to the fusion variants it is compared against.")
fix("H 5.8", "5.8 Training Procedure The training setup used is:",
    "### 5.8 Training Procedure\n\nThe training setup used is:")
# 5.9 inference list: logically scrambled -> restore approved procedure
fixre("S 5.9 list", r"5\.9 Inference Pipeline At inference time, the process is:\n\n- The deterministic router assigns the email to either the TEXT, IMAGE, MULTIMODAL, or EMPTY modality \(EMPTY is dropped\)\.- Only the encoder\(s\) corresponding to the assigned modality are run\.- If IMAGE or MULTIMODAL, run the image encoder and perform the visual cross-attention\.- If MULTIMODAL, compute the auxiliary classifier \(Eq\. 20\)\.- Run the vision encoder \(if not already\) and perform the text image cross-attention\.- Compute the shared classifier output\.- Threshold the sigmoid output at 0\.5 for the label\.",
      "### 5.9 Inference Pipeline\n\nAt inference time, the process is:\n\n1. The deterministic router assigns the email to TEXT, IMAGE, MULTIMODAL, or EMPTY (EMPTY is discarded).\n2. Only the encoder or encoders required by the selected modality are invoked.\n3. For MULTIMODAL emails, the auxiliary classifier is evaluated (Eq. 20).\n4. If early exit is not triggered, the image is encoded and bidirectional cross-attention is applied.\n5. The resulting representation is passed to the shared classifier.\n6. The sigmoid probability is thresholded at 0.5 to produce the binary prediction.")
# 4.3 paths: arrows lost + scrambled MULTIMODAL item + debris
fix("S 4.3 paths", "- **TEXT path:** text encoder projection mean pooling shared classifier. Do not call the vision encoder.\n- IMAGE path: image encoder projection mean pooling shared classifier Note: text encoder is not used.\n- 4.26MULTIMODAL path: text encoder projection optional early exit if not exited, text-only classifier if exited, image encoder projection. Bidirectional cross-attention mean pooling fusion shared classifier.",
    "- **TEXT path:** text encoder → projection → mean pooling → shared classifier. Do not call the vision encoder.\n- **IMAGE path:** image encoder → projection → mean pooling → shared classifier. Note: the text encoder is not used.\n- **MULTIMODAL path:** text encoder → projection → optional early exit via the text-only classifier → if not exited, image encoder → projection → bidirectional cross-attention → mean pooling → fusion → shared classifier.")
# 4.1: restore set-brace math + keep author's phrasing
fix("F 4.1 braces", "and is accompanied by one or more images {I_1, I_2,..., I_K} embedded inline or as attachments.",
    "and is accompanied by one or more images $\\{I_1, I_2, \\ldots, I_K\\}$ embedded inline or as attachments.")
# 4.2: "one of three categories" -> four (DCAT routes to four)
fix("C 1 three categories", "which assigns each email to one of three categories based on extracted content",
    "which assigns each email to one of four categories based on extracted content")
fix("C 1 early exit", "an *early exit*: in which a text-only auxiliary classifier is run on images with insufficient signal, and the full model is only run when the auxiliary classifier is uncertain.",
    "an *early exit*: in which a text-only auxiliary classifier is evaluated first on the message's text, and the full multimodal pathway is executed only when that classifier is uncertain.")
fix("C 1 modality-agnostic", "Modality-agnostic spam detection creates conditions that standard text classifiers do not see.",
    "Multimodal spam detection creates conditions that standard text classifiers do not see.")
fix("C 1 heterogenous", "A real-world email corpus is heterogenous in a particular way:",
    "A real-world email corpus is heterogeneous in a particular way:")
# 2.2: garbled dataset-shift sentence -> pristine meaning
fix("C 2.2 shift", "Spam email is very closely related to the specific phasing out of corpora for relevant computational reasons and models will not necessarily transfer across emails [1].",
    "Spam corpora age quickly because spammer strategies evolve in response to filters, so a model's performance is tied to the distribution of the corpus it was evaluated on, and findings may not transfer across corpora or time periods [1].")
# 2.1: mangled content-extraction sentence
fix("C 2.1 extraction", "it also implies that any email classifier built in this manner must operate on content extracted from it, since it cannot assume well-formedness beyond its own paper's processing pipeline.",
    "it also implies that any multimodal email classifier must first perform deterministic content extraction, deciding which parts of each message constitute meaningful text and meaningful images.")
# 3.1: broken sentence + name spacing
fix("C 3.1 made", "Character [9] and word [10] level learned convolution classifiers and sequential models [11] made deep learning.",
    "Character-level [9] and word-level [10] learned convolution classifiers and sequential models [11] brought in deep learning.")
fix("F 3.2 names", "Image-identificationCNNs - VGG [16], Res Net [17], and Mobile Net [18] - serve as the feature backbone",
    "Image-identification CNNs - VGG [16], ResNet [17], and MobileNet [18] - serve as the feature backbone")
fix("F 3.3 clip", "contrastive vision-language BERT CLIP [26] - learned token-level interaction across modalities.",
    "and CLIP's contrastive vision-language alignment [26] - learned token-level interaction across modalities.")
fix("C 3.4 image-conditional", "This paper's approach - using image-conditional modality routing and an early message-level exit to skip vision -",
    "This paper's approach - using content-conditional modality routing and an early message-level exit to skip vision -")
# 6.1: stage fixes
fix("C 6.1 lead", "Preprocessing takes the raw.eml files and does through four deterministic phases:",
    "Preprocessing operates on raw `.eml` files through four deterministic stages:")
fix("C 6.1 stage1", "1. **MIME parsing.** For each.eml file, parse with the email package, walk the MIME tree to get plain text, HTML, and images. Use Beautiful Soup and the lxml parser to reduce HTML to visible text; decode image parts to raw bytes; and ignore any non-fatal parsing errors.",
    "1. **MIME parsing.** For each `.eml` file, parse with the email package, walk the MIME tree to get plain text, HTML, and images. Use Beautiful Soup and the lxml parser to reduce HTML to visible text; decode image parts to raw bytes; non-fatal parsing issues are logged.")
fix("C 6.1 stage2 label", "2. **Filtering and Quality Filtering:** Texts with less than 10 characters",
    "2. **Content filtering and quality control.** Texts with less than 10 characters")
fix("F 6.1 stage labels", "3. Image processing. Chosen images are resized",
    "3. **Image processing.** Chosen images are resized")
fix("F 6.1 stage4", "4. Text tokenization. Email text is tokenized",
    "4. **Text tokenization.** Email text is tokenized")
# Figure 3 spec reassembly
fixre("S fig3", r"\[FIGURE 3 - PREPROCESSING FLOW\]\n\n\*\*Caption:\*\* Preprocessing and data-flow diagram\. Raw\.eml files undergo the four deterministic stages of Section 6\.1 \(MIME parsing; content filtering with size and quality thresholds annotated; image processing; text tokenization\) prior to deterministic modality assignment\. EMPTY messages are eliminated from the training and assessment process\.\n\n\*\*Placement & purpose:\*\* After 4 preprocessing steps \(Section 6\.1\)\. Purpose: Demonstrate the flow of data from raw input to prepared modalities for input to our models, with the specific thresholds annotated \(>= 10 chars text, >=20×20 px and >=1024 bytes image, 224×224 resize\)\. Data source: stages 1-4 of Section 6\.1\.\n\n\*\* Note: final graphics are produced in the latex project \(`latex/figures/`, vector sources\); the above specifications are the approved ones\.",
      "[FIGURE 3 - PREPROCESSING FLOW]\n\n**Caption:** Preprocessing and data-flow diagram. Raw `.eml` files undergo the four deterministic stages of Section 6.1 (MIME parsing; content filtering with size and quality thresholds annotated; image processing; text tokenization) prior to deterministic modality assignment. EMPTY messages are eliminated from the training and assessment process.\n\n**Placement & purpose:** After the 4 preprocessing steps (Section 6.1). Purpose: demonstrate the flow of data from raw input to prepared modalities for input to our models, with the specific thresholds annotated (>= 10 chars text, >= 20×20 px and >= 1024 bytes image, 224×224 resize). Data source: stages 1-4 of Section 6.1.\n\n**Note:** final graphics are produced in the latex project (`latex/figures/`, vector sources); the above specifications are the approved ones.")
# 6.2 leakage list: repair 1185 debris
fix("C 6.2 leakage", "The leakage analysis tests for five kinds of duplication and overlap: exact textual duplicate pair, among the 1185 splits; exact image duplicate pair among the 1185 splits; perceptual image duplicate pair among the 1185 splits, and using perceptual hash; Jaccard near-duplicate text pairs; sender, campaign name overlap. Exact textual and hash-based deduplication was performed on the entire dataset; the perceptual leakage test was performed on a pilot sample of the data due to the high cost; the evidence from this test therefore confirms the workings of the deduplication tests on the entire data, but should not be considered an exhaustive check of all image pairs.",
    "The leakage analysis tests for five kinds of duplication and overlap: exact textual duplicate pairs across splits; exact image duplicate pairs across splits; perceptual image duplicate pairs across splits, using perceptual hashing; Jaccard near-duplicate text pairs; and sender and campaign name overlap. Exact textual and hash-based deduplication was performed on the entire dataset; the perceptual leakage test was performed on a pilot sample of the data due to the high cost; the evidence from this test therefore supports the deduplication checks applied to the entire data, but should not be considered an exhaustive check of all image pairs.")
fix("C 6.2 balanced", "so the corpus is on the mid-side of the normal ham-to-spam representation rather than idling around balanced.",
    "so the corpus is moderately imbalanced rather than approximately balanced.")
# 6.3: ResNet name
fix("F 6.3 resnet", "a reimplementation of a late-fusion architecture based on DistilBERT for text and Res Net-18 for images [4].",
    "a reimplementation of a late-fusion architecture based on DistilBERT for text and ResNet-18 for images [4].")
# 6.6: redundant gloss + garbled tail
fix("C 6.6 gloss", "(1) the multimodal test subset (~11 samples; analogous to a 11-sample test set) and (2) the pooled out-of-fold predictions from the five-fold cross-validation experiment (~7,867 samples). The multimodal test set sample size is too small to make statistical claims using those 11 examples, and the pooled setting is used exclusively to make that statement.",
    "(1) the multimodal test subset (~11 samples) and (2) the pooled out-of-fold predictions from the five-fold cross-validation experiment (~7,867 samples). The multimodal test set sample size is too small to make statistical claims using those 11 examples; the pooled setting exists precisely to obtain a better-powered comparison.")
# 6.8: case + debris
fix("C 6.8 case", "Error analysis Displays full-test", "Error analysis displays full-test")
# 7.1: RQ wording + dangling Late Fusion + 5e-4 + section ref
fix("C 7.1 rq", "*Research question: What are the class signals found in the representations and how do the fusion designs compare when the entire test set outweighs the metric?*",
    "*Research question: what are the class signals found in the representations, and how do the fusion designs compare when the full test set dominates the metric?*")
fix("C 7.1 lf", "Text-Only: achieves Macro-F1 0.9827. Full-DCAT: 0.9862 versus 0.9869 Published Baseline, 0.9867 DCAT-No-XAttn, Late Fusion. On the full test set the difference is small.",
    "Text-Only achieves Macro-F1 0.9827. Full-DCAT: 0.9862 versus 0.9869 for the Published Baseline, 0.9867 for DCAT-No-XAttn, and 0.9871 for Late Fusion; on the full test set the difference is small.")
fix("C 7.1 5e4", "At this level of performance, all text models are within one-thousandth of one another (5e-4).",
    "At this level of performance, all text models are within thousandths of one another (on the order of 10⁻³).")
fix("F 7.1 secref", "which was inconsistent with the seed-level analysis in 7.8.",
    "which was inconsistent with the seed-level analysis in Section 7.8.")
# 7.2: mini-header glue + precision fixes + provenance wording
fix("C 7.2 header glue", "Multimodal Low Number Samples and Majority-class Collapse The Multimodal subset has so few samples that Late Fusion, Full-DCAT, Image-Only, and the All-Spam Prior all predict mostly spam, with Macro-F1 0.4968, Ham F1 0.0000.",
    "The multimodal subset has so few samples that Late Fusion, Full-DCAT, Image-Only, and the All-Spam Prior all predict mostly spam, with Macro-F1 0.4968 and Ham F1 0.0000 — majority-class collapse.")
fix("C 7.2 textonly", "Text-Only delivers the only non-zero ham recall of a unimodal model, with 0.5584, while DCAT-No-XAttn is dominant overall, with Macro-F1 0.8317, Ham F1 0.6667.",
    "Text-Only reaches 0.5584, the only unimodal model with nonzero ham recall (Ham F1 0.1633), while DCAT-No-XAttn is dominant overall, with Macro-F1 0.8317 and Ham F1 0.6667.")
fix("C 7.2 fig3->tab3", "One provenance note is needed. Figure 3 reproduces the archived multimodal evaluation table",
    "One provenance note is needed. Table 3 reproduces the archived multimodal evaluation table")
fix("C 7.2 synopsis", "(The source analysis own synopsis of this subsection gives Text-Only at 0.4968/0.0000/0.9935 (majority-collapsed) and Image-Only at 0.2863/0.4444/0.1282, values inconsistent with either archived table.)",
    "(The source analysis's own synopsis of this subsection gives Text-Only at 0.4968/0.0000/0.9935 (majority-collapsed) and Image-Only at 0.2863/0.4444/0.1282, values that match neither archived table.)")
fix("C 7.2 designated", "the archived table -- the apparently final source for these figures -- is presented here.",
    "the archived table — the designated source for these figures — is presented here.")
fix("C 7.2 disclosure", "No attempt is made to reconcile this difference (or delete it).",
    "This conflict is disclosed rather than silently reconciled.")
# 7.3: debris '4', grammar
fix("C 7.3 four", "4 p = 1.0000 for Full-DCAT vs. Late Fusion and p = 0.2482 for Full-DCAT vs. DCAT-No-XAttn.",
    "McNemar's test gives p = 1.0000 for Full-DCAT vs. Late Fusion and p = 0.2482 for Full-DCAT vs. DCAT-No-XAttn.")
fix("C 7.3 grammar", "While there are on the order of 11 multimodal test samples, under this test alone the comparison of Full-DCAT and Late Fusion are underpowered to statistically distinguish,",
    "While there are on the order of 11 multimodal test samples, under this test alone the comparison of Full-DCAT and Late Fusion is underpowered to statistically distinguish,")
# 7.4: name + superscripts + split sentence
fix("C 7.4 pvals", "Weighting-DCAT improves full-test Macro-F1 from 0.9862 to 0.9880 and multimodal Macro-F1 from 0.6253 to 0.7478. Corresponding pooled out-of-fold McNemar comparisons yield p = 2.49 10 for Weighted-DCAT vs. Full-DCAT, and p = 3.34 10 for Weighted-DCAT vs. \n\nLate Fusion (both far below = 0.05), on the 7,867 pooled out-of-fold samples.",
    "Weighted-DCAT improves full-test Macro-F1 from 0.9862 to 0.9880 and multimodal Macro-F1 from 0.6253 to 0.7478. Corresponding pooled out-of-fold McNemar comparisons yield p = 2.49 × 10⁻⁴⁵ for Weighted-DCAT vs. Full-DCAT, and p = 3.34 × 10⁻⁶ for Weighted-DCAT vs. Late Fusion (both far below α = 0.05), on the 7,867 pooled out-of-fold samples.")
# 7.7: stray citation + inverted parenthetical + spacing
fix("C 7.7 cite18", "DCAT has roughly four times as many trainable parameters as Late Fusion-2.01M versus 0.46 M [18] including additional parameters for the cross-attention blocks and classifier.",
    "DCAT has roughly four times as many trainable parameters as Late Fusion — 2.01M versus 0.46M — including additional parameters for the cross-attention blocks and classifier.")
fixre("C 7.7 paren", r"\(shown as an approximation based on all tests cells on this line: \"avg, 90% text-only\" on the source artifact cell; this is not comparable to the figure of 12\.7B in Table 8, which ignores the effect of the early exit on the few multimodal tests that would otherwise run past the early exit\) over the whole corpus\.",
      "(the source artifact annotates this cell \"avg, 90% text-only\") over the whole workload.")
# 7.9: figure spec block reassembly
fixre("S fig4", r"\[FIGURE 4 - RESULTS VISUALIZATION PANEL\] FIGURE CAPTION: Results visualization\. \(a\) Confusion matrix of DCAT in the weighted-primary setting on the full test set \(n = 7,351; 57 false positives, 25 false negatives\)\. \(b\) Multimodal Macro-F1 for all evaluated settings on the multimodal subset, reproducing the values of Table 3 \(ASP: All-Spam Prior; MI: Modality Indicator; Text: Text-Only; Image: Image-Only; PB: Published Baseline; LF: Late Fusion; NoXAttn: DCAT-No-XAttn; DCAT: Full-DCAT; EE: DCAT-Early-Exit\)\. Majority-collapsed settings sit at 0\.4968; DCAT-No-XAttn reaches 0\.8317\.",
      "[FIGURE 4 - RESULTS VISUALIZATION PANEL]\n\n**Caption:** Results visualization. (a) Confusion matrix of DCAT in the weighted-primary setting on the full test set (n = 7,351; 57 false positives, 25 false negatives). (b) Multimodal Macro-F1 for all evaluated settings on the multimodal subset, reproducing the values of Table 3 (ASP: All-Spam Prior; MI: Modality Indicator; Text: Text-Only; Image: Image-Only; PB: Published Baseline; LF: Late Fusion; NoXAttn: DCAT-No-XAttn; DCAT: Full-DCAT; EE: DCAT-Early-Exit). Majority-collapsed settings sit at 0.4968; DCAT-No-XAttn reaches 0.8317.")
# 8.1: direction inversion + five->11 emails
fix("C 8.1 direction", "The observed result is a 0.0009 Macro-F1 improvement of Full-DCAT (0.9862) over Late Fusion (0.9871) on the full test set, with seed-level s.d. of at most 0.0003 (Tables 2 and 9).",
    "The observed result is a 0.0009 Macro-F1 gap between Full-DCAT (0.9862) and Late Fusion (0.9871) on the full test set, with seed-level s.d. of at most 0.0003 (Tables 2 and 9).")
fix("C 8.1 eleven", "Second, the five emails in the multimodal subcorpus are insufficient for stable estimation of cross-modal interactions,",
    "Second, the 11 emails in the multimodal subcorpus are insufficient for stable estimation of cross-modal interactions,")
# 8.2: inverted direction + statisticist + 4 of 4
fix("C 8.2 direction", "The single-measure contribution of Full-DCAT to the multimodal test subset is a 0.4968→0.8317 improvement over the baseline DCAT-No-XAttn (Table 3). This large improvement directed in the \"opposite\" direction from the proposed design goal was the critical benchmark driving the story of the study.",
    "On the multimodal test subset, DCAT-No-XAttn reports Macro-F1 0.8317 compared with 0.4968 for Full-DCAT (Table 3) — the largest architecture-linked difference in the study — and it runs in the opposite direction from the design's intent. This large, counter-directional difference was the critical benchmark driving the story of the study.")
fixre("C 8.2 statisticist", r"\(The statisticist sets aside the discrepancy.*?p=0\.2482\)\.\)",
      "(The statistical result disciplines both readings: the McNemar comparison between Full-DCAT and DCAT-No-XAttn is not significant at α = 0.05 (p = 0.2482).)")
fixre("C 8.2 fouroffour", r"the 4 of 4 fully trained models with interaction capacity collapsed to the baseline condition of majority-class prediction \(Ham F1 0\.0000\), exactly the effect that the full-test headline was intended to isolate\. \(The number of sampling-related failures remains underpowered to discern the reason for the majority-class collapse\.\)",
      "every fully trained interaction-capable model that collapsed did so to majority-class prediction (Ham F1 0.0000), exactly the pattern the Macro-F1 headline metric is chosen to expose.")
# 8.3: fabricated latencies -> pristine p-values; 'Table 6' mis-reference removed
fix("C 8.3 latencies", "Weighted-DCAT improves the multimodal Macro-F1 from 0.6253 to 0.7478, full-test Macro-F1 from 0.9862 to 0.9880, and yields total-time latency improvements of 9.84% (2.70 ms →2.44 ms) and 6.36% (2.68 ms →2.51 ms) for median and P95, respectively, in comparison to the full-training, baseline estimates in Table 6.",
    "Weighted-DCAT improves the multimodal Macro-F1 from 0.6253 to 0.7478 and full-test Macro-F1 from 0.9862 to 0.9880; the pooled out-of-fold McNemar comparisons are statistically significant for both Weighted-DCAT versus Full-DCAT (p = 2.49 × 10⁻⁴⁵) and Weighted-DCAT versus Late Fusion (p = 3.34 × 10⁻⁶).")
# 8.4: 4.46% fabrication + GPU FLOPS wording + speedup parenthetical
fix("C 8.4 4.46", "The early exit mechanism avoids the vision encoder on 4.45% of the multimodal messages in this evaluation; because only 4.46% of the messages in the total corpus are multimodal, the overall fraction of GPU FLOPS saved per-messages in the evaluation workload is 0.63%.",
    "The early-exit mechanism avoids the vision encoder on 4.45% of the multimodal messages in this evaluation; because only a small fraction of the corpus is multimodal, the resulting average FLOP reduction over the evaluated workload is 0.63%.")
fix("C 8.4 speedup", "(With a larger load of multimodal messages, the speedup would scale accordingly; this was not evaluated.)",
    "(A corpus with a larger proportion of multimodal messages would provide a different workload for the same mechanism; that case was not evaluated here — the savings scale with multimodal prevalence, not with the mechanism itself.)")
# 8.5: arrow misuse + typo
fix("C 8.5 arrows1", "with a small seed-stable gap (0.9862→0.9869-0.9871 in Macro-F1)",
    "with a small seed-stable gap (Macro-F1 0.9862 versus 0.9869–0.9871)")
fix("C 8.5 arrows2", "has the highest across-fold average multimodal Macro-F1 (0.7077→0.5453 on Late Fusion) but with greater variation, (Section 7.6)",
    "has the highest across-fold average multimodal Macro-F1 (0.7077 versus 0.5453 for Late Fusion) but with greater variation (Section 7.6)")
fix("C 8.5 typo", "class weighting produces the only statistically signifcant improvement", "class weighting produces the only statistically significant improvement")
# 9.1: inversion + affected
fix("C 9.1 scarcity", "Extreme multimodal scarcity. There are a mere 11 emails in the primary Spam Assassin set, all of which are multimodal. Scores on the primary test set are effected significantly by single prediction, and cannot be assumed to generalize to any other domain.",
    "**Extreme multimodal scarcity.** Only 11 emails in the primary SpamAssassin subset are multimodal. Scores on this multimodal subset are affected significantly by single predictions, and cannot be assumed to generalize to any other domain.")
fix("F 9.1 labels", "Single corpus. All experiments were conducted on the Spam Assassin corpus.",
    "**Single corpus.** All experiments were conducted on the SpamAssassin corpus.")
fix("F 9.1 labels2", "Single-image constraint. For each multi-image message",
    "**Single-image constraint.** For each multi-image message")
fix("F 9.2 labels", "Fusion method. The proposed multimodal representation",
    "**Fusion method.** The proposed multimodal representation")
fix("F 9.2 labels2", "Early-exit thresholds. The thresholds were set to 0.95 and 0.05;",
    "**Fixed early-exit thresholds.** The thresholds were set to 0.95 and 0.05;")
fix("F 9.2 labels3", "Frozen encoders. DistilBERT and MobileViT are frozen, they were not fine-tuned on the domain data.",
    "**Frozen encoders.** DistilBERT and MobileViT are frozen; they were not fine-tuned on the domain data.")
fix("F 9.4 labels", "Internal validity. Many potential sources",
    "**Internal validity.** Many potential sources")
fix("F 9.4 labels2", "Construct validity. Although Macro-F1", "**Construct validity.** Although Macro-F1")
fix("C 9.3 FLOPs", "The efficiency table contains two FLops figures", "The efficiency table contains two FLOPs figures")
# 10: fabricated significance level + p superscripts + arrow
fix("C 10 same", "Full-DCAT achieved the same Macro-F1 0.9862 as the published-baseline reimplementation 0.9869 and Late Fusion 0.9871 across three seeds, and experiments do not show a full-test advantage for cross-attention at the 0.001 significance level.",
    "Full-DCAT achieves Macro-F1 0.9862 against 0.9869 for the published-baseline reimplementation and 0.9871 for Late Fusion across three seeds; the differences are small, and the experiments do not demonstrate a consistent full-test advantage from adding cross-attention.")
fix("C 10 pvals", "(multimodal Macro-F1 0.6253 0.7478; pooled out-of-fold McNemar p = 2.49 10 against Full-DCAT and p = 3.34 10 against Late Fusion)",
    "(multimodal Macro-F1 0.6253 → 0.7478; pooled out-of-fold McNemar p = 2.49 × 10⁻⁴⁵ against Full-DCAT and p = 3.34 × 10⁻⁶ against Late Fusion)")
# Back matter: restore Data Availability + Declarations (author edit dropped them)
fix("S backmatter", "\n\n\n\n## Appendix A. Dataset and Preprocessing Reference",
    """

## Data Availability

The evaluation artifacts are available in the project repository: per-sample error records at `artifacts/error_analysis/dcat_errors.csv` and `artifacts/error_analysis/late_fusion_errors.csv`; cross-validation results at `artifacts/weighted_cv/cv_results.csv`; primary benchmark results at `results/tables/final_results.csv`; and the complete results lineage at `artifacts/final_results/results_lineage.csv`. The SpamAssassin public corpus is publicly available [7].

## Declarations

**Competing interests.** The author declares no competing interests.

## Appendix A. Dataset and Preprocessing Reference""")
# Q list formatting: strip stray leading spaces; split glued Q5/Q6/Q7
fixre("F Q list", r"\n Q1 Is the proposed", "\n\nQ1 Is the proposed")
fix("F Q glue", "Q5 Is the model able to learn effective interactions between the modalities? Q6 Can the model operate efficiently in terms of parameters, FLOPs, and latency? Q7 What is the model's attitude towards information sharing, and how is it affected by the size of the training set? ",
    "Q5 Is the model able to learn effective interactions between the modalities?\n\nQ6 Can the model operate efficiently in terms of parameters, FLOPs, and latency?\n\nQ7 What is the model's attitude towards information sharing, and how is it affected by the size of the training set?")
# global proper-noun / typo normalizations (formatting-only)
fixre("G SpamAssassin", r"Spam Assassin", "SpamAssassin", 0)  # count-asserted below
FIXES.pop()
n_sa = text.count("Spam Assassin")
text = text.replace("Spam Assassin", "SpamAssassin")

# ---------------------------------------------------------------- apply
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

text = text.replace("Spam Assassin", "SpamAssassin")
# collapse >2 blank lines
text = re.sub(r"\n{3,}", "\n\n", text)
# tidy: single blank line after headings where missing
text = re.sub(r"(?m)^(#{2,3} .+)\n(?=[^\n])", r"\1\n\n", text)

open(OUT, "w", encoding="utf-8", newline="\n").write(text)

print(f"proper-noun SpamAssassin fixes: {n_sa}")
for name, n, exp in log:
    status = "OK " if n == exp else "FAIL"
    print(f"[{status}] {name}: applied {n} (expected {exp})")
if failed:
    print(f"\n{len(failed)} FIXES NEEDS ATTENTION:")
    for name, n, exp in failed:
        print(f"  - {name}: got {n}, expected {exp}")
    sys.exit(1)
print(f"\nAll {len(FIXES)} fixes applied as expected. Wrote {OUT} ({len(text.split())} words)")
