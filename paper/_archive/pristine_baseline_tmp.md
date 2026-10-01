# HUMAN EDITING STATUS

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

# DCAT: A Dynamic Cross-Attention Transformer for Conditional Multimodal Email Spam Detection

**Preetham S**
*(Guide: Dr. Prathima Mabel)*



## Abstract

Email spam remains one of the most persistent security problems in electronic communication, and a growing share of unwanted mail carries its persuasive or malicious payload in images as well as text. Multimodal spam detectors therefore pair a text encoder with an image encoder, but two structural properties of real email corpora are largely unaddressed: the overwhelming majority of messages are text-only, and genuinely multimodal messages are extremely scarce. This paper presents DCAT (Dynamic Cross-Attention Transformer), a conditional multimodal architecture for email spam detection that combines bidirectional cross-attention between projected text and image representations with deterministic modality routing and an optional early-exit classifier that avoids unnecessary vision computation. On the full test set, Full-DCAT achieves a three-seed mean Macro-F1 of 0.9862, compared with 0.9869 for a reimplementation of a published multimodal baseline and 0.9871 for Late Fusion; the differences are small, and the corpus is 99.4% text-only. On the 11-message multimodal test subset, Full-DCAT does not outperform Late Fusion (McNemar p = 1.0000), while DCAT-No-XAttn reaches Macro-F1 0.8317 versus 0.4968 for Full-DCAT; neither difference is statistically significant at α = 0.05 given the subset's size. Five-fold cross-validation yields a mean multimodal Macro-F1 of 0.7077 for Full-DCAT and 0.5453 for Late Fusion, with higher variance for Full-DCAT (0.2639 versus 0.1222). Weighted-DCAT raises multimodal Macro-F1 from 0.6253 to 0.7478, with pooled out-of-fold McNemar tests of p < 10⁻⁴⁴ against unweighted Full-DCAT and p < 10⁻⁵ against Late Fusion. The early-exit mechanism skips vision computation for 4.45% of multimodal emails and reduces average FLOPs by 0.63% on the evaluated workload. The results indicate that architectural expressiveness alone does not translate into gains when paired training examples are extremely scarce and the corpus is dominated by text-only messages, and that the training objective can matter more than the fusion mechanism.

**Keywords:** multimodal spam detection · cross-attention · email classification · conditional computation · modality routing · DistilBERT · MobileViT · multimodal fusion · deep learning



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## 1. Introduction
Email is the backbone of asynchronous digital communication, and unsolicited bulk email — spam — has accompanied it throughout its history as one of the most persistent cybersecurity problems facing individuals and organizations [1]. Spam is not a static phenomenon: campaigns adapt their content to survive filters, and a growing body of work documents the use of images — promotional banners, phishing screenshots, brand graphics, and text rendered as graphics — to carry part of the spam signal that text-only filters cannot see [2], [3]. When the information that distinguishes spam from legitimate mail lives partly in an image, a detector that reads only text is structurally blind to it.

Multimodal spam detection introduces conditions that ordinary text classification does not face. A real email corpus is heterogeneous in a very specific way: most messages are text-only, a few pair text with one or more images, and an even smaller number carry their relevant content primarily in images. This heterogeneity creates two coupled problems. First, a model that runs a vision encoder on every message performs unnecessary visual computation for the text-only majority. Second, a model that learns interactions *between* modalities needs enough paired examples to estimate those interactions reliably — precisely the examples that natural corpora provide in the smallest numbers.

prior multimodal spam-detection systems typically encode text and images independently and combine them through concatenation or other late-fusion mechanisms [4], with attention-based and gating-based fusion explored in adjacent multimodal literature [5]. These designs differ in where and how information is exchanged between modalities, but they share two assumptions that natural email violates: that every message warrants both encoders, and that paired data is plentiful enough to train interaction-heavy fusion.

This paper presents DCAT (Dynamic Cross-Attention Transformer), a conditional multimodal architecture for email spam detection designed around the actual structure of email corpora. DCAT combines three mechanisms. First, *bidirectional cross-attention*: text and image representations are projected into a shared latent space, where each modality attends to the other before pooling, so that a text feature's representation can depend on the associated image and vice versa. Second, *deterministic modality routing*: based on content extracted during preprocessing, each email is assigned to TEXT, IMAGE, MULTIMODAL, or EMPTY, and only the encoders required by that category are invoked — a text-only message never triggers the vision pathway. Third, an *optional early exit*: for multimodal messages, a text-only auxiliary classifier is evaluated first, and only if it is not confident (probability between 0.05 and 0.95) is the full multimodal pathway executed.

The evaluation is designed to test these design choices under natural conditions rather than idealized ones. It uses a naturally paired corpus extracted from the SpamAssassin public corpus, three random seeds, explicit ablations of the cross-attention module and the class-weighting objective, analysis of full-corpus versus multimodal-subset performance, five-fold cross-validation with pooled out-of-fold statistical comparisons, and efficiency measurements covering parameters, FLOPs, latency, and vision skip rate.

The contributions of this paper are as follows:

- A conditional multimodal email spam detection architecture that combines bidirectional cross-attention with deterministic modality routing and optional early-exit computation.
- A controlled evaluation on naturally paired multimodal email data using three random seeds and explicit architectural and imbalance ablations.
- An analysis of the difference between performance on the full corpus and performance on the much smaller multimodal subset.
- An imbalance ablation comparing unweighted and class-weighted training.
- Efficiency measurements covering parameter counts, FLOPs, latency, and vision skip rate.

The remainder of the paper is organized as follows. Section 2 provides the background needed to read the method: the structure of email as a multimodal medium, the spam and phishing threat landscape, content representations for text and images, attention and cross-attention, and conditional computation. Section 3 reviews related work by approach family and states the research gap. Section 4 formulates the problem. Section 5 describes the DCAT architecture. Section 6 specifies the experimental methodology. Section 7 reports results organized around research questions. Section 8 discusses what the results mean. Section 9 details limitations and threats to validity, and Section 10 concludes with future work.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## 2. Background
This section establishes the concepts the rest of the paper builds on. Each subsection ends where the method or evaluation will pick it up; no background material is included that is not used later.

### 2.1 Email as a Multimodal Communication Medium

The classifier developed in this paper makes decisions over message *content* — which parts of an email constitute text, and which constitute images. That content is only well defined because email itself is formally structured. The MIME standard (Multipurpose Internet Mail Extensions) defines an email message as a structured object: a set of headers followed by a body that may contain multiple typed parts [6]. A single message can therefore simultaneously carry a plain-text body, an HTML rendering of that body, inline images, and attached files — each a distinct part with its own media type. Parsing tools traverse this *MIME tree* to extract the parts; the plain text and HTML parts yield the message's textual content, while image parts (inline or attached) yield its visual content.

This structure is what makes email *natively multimodal*: the modalities are not constructed artificially by a researcher but are present, or absent, in each message as it was actually sent. It also implies that any multimodal email classifier must first perform content extraction — deciding, deterministically, which parts of each message constitute meaningful text and meaningful images. Section 6.1 describes the extraction pipeline used in this work, and the corpus used throughout preserves this original MIME structure [7].

Three message types result from this structure and matter throughout the paper. A *text-only* message has meaningful text but no meaningful image; an *image-only* message has a meaningful image but no meaningful text; a *multimodal* message has both. Natural corpora contain all three in very different proportions — a fact with direct consequences for both computation (Section 2.6) and learning (Section 3.3).

### 2.2 Spam, Phishing, and the Modern Threat Landscape

Spam is conventionally understood as unsolicited bulk email — messages sent in volume for commercial or deceptive purposes without the recipient's consent [1]. *Phishing* is a related but distinct category: deceptive messages engineered to impersonate trusted entities in order to steal credentials or induce fraudulent actions [3]. The two overlap heavily in practice — a phishing message is usually also spam — and modern detection research treats them as points on a continuum of unwanted mail [3]. What matters for this work is that both categories increasingly exploit the visual channel: promotional graphics and brand imagery in bulk marketing, and rendered logos, fake login forms, and screenshots in deceptive mail [2]. Text rendered inside an image is invisible to text filters, and visual branding can carry an impersonation claim that plain text avoids. Consequently, spam and phishing cannot be fully characterized as text-classification problems.

A second property of the spam domain shapes this paper's evaluation methodology: *dataset shift*. Spam corpora age quickly because spammer strategies evolve in response to filters, so a model's performance is tied to the distribution of the corpus it was evaluated on, and findings may not transfer across corpora or time periods [1]. This motivates the transparent, multi-protocol evaluation strategy adopted in Sections 6 and 7.

### 2.3 Content Representations for Text

This subsection traces how text came to be represented by the encoder DCAT adopts; Section 2.4 does the same for images. The representation of text for machine learning has developed through several generations. Classical spam filtering relied on sparse lexical features — bag-of-words and TF-IDF vectors — consumed by linear or probabilistic classifiers [1]. Dense *word embeddings* replaced one-hot lexical symbols with learned continuous vectors that capture distributional similarity [8]. Convolutional neural networks then enabled learned feature extraction directly from character-level [9] and word-level [10] sequences, and recurrent architectures — notably Long Short-Term Memory networks — modeled longer-range sequential dependencies [11].

The current generation is built on the Transformer [12], which dispenses with recurrence entirely and processes a token sequence through stacked layers of *self-attention*: every token attends to every other token, with attention weights computed from learned query, key, and value projections (Section 2.5 gives the operative form). Pre-trained Transformer language models such as BERT [13] and RoBERTa [14] learn deep bidirectional contextual representations from large unlabeled corpora and transfer them to downstream tasks. DistilBERT [15] is a distilled version of BERT that retains most of its language capability with substantially fewer parameters and lower inference cost — the property that makes it practical as a frozen text encoder applied to large numbers of email messages, as in this work. Section 5.2 uses DistilBERT-base-uncased, a six-layer Transformer with 768-dimensional hidden representations.

### 2.4 Content Representations for Images

Visual representations followed a parallel trajectory. Deep convolutional networks established that hierarchical feature learning applies to images: VGG demonstrated the value of depth with uniform small convolutions [16], ResNet introduced residual connections that made very deep networks trainable [17], and MobileNets showed that accuracy suitable for many tasks could be achieved at mobile-friendly computational budgets [18]. CNN-based image-spam detection predates and motivates this line: visual patterns such as colors, shapes, and rendered text overlays carry a genuine spam signal [2].

Vision Transformers (ViT) subsequently showed that an image, cut into fixed-size patches and treated as a token sequence, can be classified by a pure Transformer when pre-trained at scale [19]. MobileViT combines the two families: it embeds convolutional local processing within a Transformer-style global representation, producing a light-weight, general-purpose encoder suitable for resource-constrained settings [20]. This paper uses MobileViT-small [20], accessed through the `timm` PyTorch Image Models library [21], which also supplies the image preprocessing pipeline (resize, normalization) that must match the pre-trained encoder's expected input distribution — an interface contract between data pipeline and model that recurs in Section 6.1. As with text, Section 5.3 specifies the exact configuration used.

### 2.5 Attention and Cross-Modal Attention

An *attention mechanism* allows a model to compute a weighted combination of elements from one representation, where the weights depend on the content of another. In the canonical formulation [12], a set of queries Q interacts with a set of keys K and values V: each query is compared against every key, the similarities are normalized by a softmax, and the resulting weights mix the values. For scaled dot-product attention,

[Equation 1]

$$\text{Attention}(Q, K, V) = \text{Softmax}\!\left( \frac{QK^{T}}{\sqrt{d_k}} \right) V, $$

where $d_k$ is the per-head key dimension. Multi-head attention runs several such operations in parallel with separate projections and concatenates the results, letting different heads attend to different relationships. Attention of this form first demonstrated its value in sequence-to-sequence translation, where it learned soft alignments between source and target words [22], and in vision, where it learned to fix a captioning model's gaze on salient image regions [23].

*Self-attention* computes Q, K, and V from the same sequence — this is the mechanism inside the encoders of Sections 2.3 and 2.4. *Cross-attention* instead takes the queries from one sequence and the keys and values from another, so each element of the first acquires a representation conditioned on the second. When the two directions are computed and fused — sequence A attending to B and B attending to A — the mechanism is *bidirectional*. Bidirectional attention flow was introduced for machine comprehension to obtain query-aware context representations without early summarization [24], and the vision-language literature generalized cross-attention into two-stream architectures: ViLBERT processes image and text in separate streams that interact through co-attentional Transformer layers [5], LXMERT learns cross-modality encoder representations [25], and CLIP aligns the two modalities contrastively rather than through token-level attention [26]. In a bidirectional cross-attention layer, the representation of one modality becomes a function of the content of the other — the property DCAT exploits in Section 5.5. This contrasts with *late fusion*, in which each modality is processed independently until its pooled representation is combined with the other, and with *gating-based fusion*, in which learned multiplicative gates decide how modalities influence a shared unit [27].

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

### 2.6 Conditional Computation and Early Exits
Standard neural networks execute the same computation for every input. *Conditional computation* relaxes this: the amount or structure of computation varies with the input [28]. One established mechanism is the *early exit*: intermediate classifiers are attached to intermediate representations, and an input whose prediction is already confident leaves the network early, skipping the remaining layers [29]. Another is *dynamic routing*: a learned policy selects, per input, which blocks of the network to execute, as in SkipNet's dynamically routed convolutional networks [30].

Email classification admits a particularly simple and interpretable form of conditional computation. The *modality structure* of each message is known before any neural computation runs: a text-only email does not need a vision encoder, and an image-only email does not need a text encoder. Routing on this deterministic signal costs nothing to learn and cannot misroute. For the multimodal minority, a stronger form is available: a text-only auxiliary classifier can be evaluated first, and the expensive vision pathway invoked only when the text evidence alone is not confident — an early-exit application in which the exit *avoids a whole encoder* rather than a few layers. The trade-off is that evaluating the auxiliary classifier and branching is itself work, so realized savings depend on the workload, a point the efficiency results of Section 7.7 quantify.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## 3. Related Work
Background and related work answer different questions. Section 2 defined the concepts and mechanisms this paper builds on; this section examines how those mechanisms have been applied to spam detection, situates DCAT among the families of prior approaches, and closes with the specific gap it addresses. Work is grouped by approach family; no single system is an anchor for this paper.

### 3.1 Text-Based Spam Detection

Rule-based filtering, exemplified by SpamAssassin's scored pattern rules [7], dominated early spam defense and remains in production use. Classical machine-learning classifiers — Naive Bayes, support vector machines, random forests — over bag-of-words and TF-IDF features form the second generation [1]. Deep learning introduced learned feature extraction: character-level [9] and word-level [10] convolutional classifiers, and LSTM-based sequential models [11]. Transformer-based encoders — BERT [13], RoBERTa [14], and the efficient DistilBERT [15] — provide the current state of text-based email classification, and their strong performance on text-dominated corpora (confirmed in our own evaluation, Section 7.1) is the baseline reality any multimodal system must confront.

### 3.2 Image-Based Spam Detection

Image-spam detection treats the image as a primary evidence channel. CNN-based approaches identify visual spam patterns — colors, shapes, text overlays — directly from image content [2]. Modern general-purpose encoders such as VGG [16], ResNet [17], and MobileNet [18] supply the feature-extraction backbone for such systems. Image-only classification nevertheless remains a weak primary signal: images are ambiguous without their associated text, and legitimate mail contains visually similar content such as company logos and marketing graphics — a limitation our Image-Only variant quantifies in Section 7.1.

### 3.3 Multimodal Spam Detection and Fusion

Multimodal spam systems combine the two evidence channels. The standard architecture encodes text and image independently and fuses late: MMTD, a multilingual multimodal spam detector, combines a text encoder and an image encoder over text and document images before fusion [4]. Attention- and gating-based mechanisms bring interaction into the fusion stage: gated multimodal units learn how modalities influence a shared representation [27], and the vision-language architectures described in Section 2.5 — ViLBERT's co-attention [5], LXMERT's cross-modality encoders [25], CLIP's contrastive alignment [26] — demonstrate token-level cross-modal interaction in other domains.

Two corpus-level facts, however, separate email from the vision-language settings where these mechanisms matured. First, naturally occurring email is overwhelmingly text-only; multimodal examples are rare, and the multimodal subset may be too small to estimate complex cross-modal interactions reliably. Second, standard multimodal pipelines spend vision computation on every message regardless of need. Neither property is specific to any one published system; they follow from the corpus structure that the spam literature itself documents [1], [2], [4].

### 3.4 Conditional Computation in Classification Systems

Early-exit architectures attach intermediate classifiers and let confident inputs skip remaining layers [29]; dynamic-routing networks learn per-input execution policies over computational blocks [30]; and the field is surveyed comprehensively by Han et al. [28], who identify sample-wise dynamic architectures as a distinct family. Email's modality structure offers a deterministic, zero-cost routing signal that these general mechanisms do not exploit: the required encoders are known from the message's MIME content before inference begins. Applying input-conditional *modality selection* to email spam detection — routing on content structure and adding an early exit that can skip an entire encoder — is the specific conditional-computation configuration this paper evaluates; to our knowledge, this combination has not previously been applied to email spam detection.

### 3.5 Evaluation Practice in Modality-Imbalanced Settings

Modality imbalance stresses evaluation methodology itself. A model can post a strong full-corpus metric while performing poorly on the multimodal subset that defines its distinctive capability; with very few multimodal samples, metrics such as F1 can swing substantially with a handful of prediction changes. The spam literature's dataset-shift concerns compound this: corpus composition drives results [1]. These observations motivate the evaluation protocol used here — reporting full-test and multimodal-subset metrics separately, adding five-fold cross-validation for the multimodal analysis, and testing paired model differences with McNemar's test [31] on pooled out-of-fold predictions.

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

### 3.6 Summary of Gaps
Four specific gaps emerge from Sections 3.1–3.5, and the paper is organized to address each:

1. **Cross-modal interaction is underexplored for email spam.** Published multimodal spam systems fuse modalities after independent encoding [4] or through gating [27]; bidirectional token-level cross-attention of the kind proven in vision-language architectures [5] has not been applied to email spam in the surveyed literature.
2. **Unconditional visual computation ignores corpus structure.** Multimodal pipelines encode both modalities for every message [4], although real corpora are text-dominated [1], [7] — paying vision cost where it cannot matter.
3. **Class imbalance in the multimodal subset is under-treated.** Multimodal spam evaluations do not report imbalance-corrected training or subset-level significance, although the ham/spam imbalance is documented in the domain literature [1], [2].
4. **Evaluation rarely separates corpus-level from subset-level views.** Full-test metrics, multimodal-subset metrics, cross-validation stability, and paired significance tests are seldom reported together, although Section 3.5 shows each captures a different failure mode.

DCAT is designed as the conjunction of these four observations: bidirectional cross-attention (gap 1), deterministic modality routing with early exit (gap 2), a class-weighting ablation (gap 3), and a multi-protocol evaluation with statistical testing (gap 4).



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## 4. Problem Formulation
### 4.1 Task Definition

Let an email message $m$ consist of textual content $t$ — the email body, subject line, and any other extracted textual information — and, optionally, one or more images $\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$ embedded inline or attached. The task is binary classification: predict

[Equation 2]

$$y \in \{0, 1\}, \qquad y = 0 \text{ (ham, legitimate email)}, \quad y = 1 \text{ (spam)}. $$

### 4.2 Modality Routing

Based on content extracted during preprocessing, every email is deterministically assigned to one of four modality categories. Let the Boolean flags $has\_text$ and $has\_image$ indicate whether meaningful text (at least 10 characters after cleaning) and at least one meaningful image (passing the size and quality filters of Section 6.1) are present. The routing rule is

[Equation 3]

$$\text{modality}(m) = \begin{cases} \text{MULTIMODAL}, & \text{if } has\_text \wedge has\_image, \\ \text{TEXT}, & \text{if } has\_text \wedge \neg has\_image, \\ \text{IMAGE}, & \text{if } \neg has\_text \wedge has\_image, \\ \text{EMPTY}, & \text{otherwise.} \end{cases} $$

EMPTY messages — neither meaningful text nor a meaningful image — are discarded from training and evaluation. The routing decision is deterministic: it employs no learned classifier, no probability threshold, and no learned heuristic. Determinism is deliberate. The modality structure of a message is fully determined by its content, so a learned router could only add error, cost, and opacity to a decision that content structure already answers.

### 4.3 Conditional Computation Paths

DCAT implements three active computation paths:

- **TEXT path:** text encoder → projection → mean pooling → shared classifier. The vision encoder is not invoked.
- **IMAGE path:** image encoder → projection → mean pooling → shared classifier. The text encoder is not invoked.
- **MULTIMODAL path:** text encoder → projection → optional early exit via the text-only classifier → if not exited, image encoder → projection → bidirectional cross-attention → mean pooling → fusion → shared classifier.

The paths share all trainable components (projector, cross-attention, classifiers); only the *sequence* of operations differs by modality. Figure 1 illustrates the three paths and the early-exit branch.

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

### 4.4 Learning Objective
The model is trained with binary cross-entropy over $N$ training examples:

[Equation 4]

$$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log \sigma(\hat{z}_i) + (1 - y_i) \log \left( 1 - \sigma(\hat{z}_i) \right) \right], $$

where $\hat{z}_i$ is the predicted logit for email $i$, $\sigma(\cdot)$ is the sigmoid function, and $y_i$ is the ground-truth label. Because the training distribution is ham-dominant (Section 6.2), the weighted variant used by Weighted-DCAT multiplies the positive-class term by $w_{pos}$:

[Equation 5]

$$\mathcal{L}_{weighted} = -\frac{1}{N} \sum_{i=1}^{N} \left[ w_{pos}\, y_i \log \sigma(\hat{z}_i) + (1 - y_i) \log \left( 1 - \sigma(\hat{z}_i) \right) \right], $$

with the positive-class weight defined as

[Equation 6]

$$w_{pos} = \frac{N_{ham}}{N_{spam}}. $$

This weighting compensates for the ham-dominant class distribution used during training; its empirical effect is measured by the imbalance ablation of Section 7.4.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## 5. The DCAT Architecture
### 5.1 Architecture Overview

DCAT consists of five components:

1. **Text Encoder (DistilBERT):** encodes email text into token-level contextual embeddings.
2. **Vision Encoder (MobileViT):** encodes email images into spatial visual feature maps.
3. **Modality Projector:** maps both encoder outputs into a shared latent space of dimension $d_{model} = 256$, using linear projections followed by Layer Normalization.
4. **Bidirectional Cross-Attention:** exchanges information between text and image representations in the shared latent space.
5. **Shared Classifier:** maps fused or unimodal representations to a spam/ham prediction.

[FIGURE 1 — DCAT OVERALL ARCHITECTURE]

**Caption:** DCAT architecture overview. Deterministic modality routing assigns each email to the TEXT, IMAGE, MULTIMODAL, or EMPTY category; only the required encoders are invoked. For MULTIMODAL emails, a text-only auxiliary classifier may exit early and classify without vision; otherwise bidirectional cross-attention exchanges information between the projected streams before pooling and fusion. Frozen components are shown in blue; trainable components in orange.

**Placement & purpose:** Section 5.1 (after the architecture-overview paragraph). Purpose: show the actual DCAT pipeline — deterministic router, modality-specific encoders, projectors, bidirectional cross-attention, pooling/fusion, shared classifier, and the early-exit branch from the text-only auxiliary classifier. Data source: methodology of Sections 4 and 5 (Eqs. 2, 3, 7-21).

**Note:** final graphics are produced in the LaTeX project (`latex/figures/`, vector sources); the specifications above are the approved rendering contract for regeneration.

The design rationale follows from Sections 2 and 4. The encoders are frozen pre-trained models, so trainable capacity concentrates in the projection, interaction, and classification components — only 2,008,578 of 73,309,090 parameters (2.74%) are trainable (Section 5.8). The projector exists because the two encoders emit representations in different spaces (768-dimensional text tokens versus spatial visual feature maps); cross-attention requires a common space in which queries from one modality can be compared against keys from the other. The classifier is *shared* across all three paths so that every path's representation is mapped into the same decision space.

### 5.2 Text Encoder

The text encoder is DistilBERT-base-uncased [15], a six-layer Transformer with 768-dimensional hidden representations. Given tokenized input $\mathbf{x}_{text}$, it produces token-level hidden states

[Equation 7]

$$\mathbf{H}_{text} = \text{DistilBERT}(\mathbf{x}_{text}). $$

The input is truncated or padded to 256 tokens; an attention mask marks padding positions so that masked tokens do not contribute to attention or pooling, and $B$ denotes the batch size. All encoder parameters are frozen during training: the encoder acts as a fixed feature extractor, and no encoder gradient updates occur.

### 5.3 Vision Encoder

The vision encoder is MobileViT-small [20], accessed through the `timm` library [21]. Images are resized to $224 \times 224$ pixels before encoding. With normalized image tensor $\mathbf{x}_{img}$, the encoder produces spatial feature representations

[Equation 8]

$$\mathbf{H}_{img} = \text{MobileViT}(\mathbf{x}_{img}). $$

$\mathbf{H}_{img}$ contains $S$ spatial tokens; for the evaluated configuration the feature map corresponds to a $15 \times 15$ spatial grid. Like the text encoder, the vision encoder is frozen during training.

### 5.4 Modality Projector

The projector maps each modality's features into the shared $d_{model}$-dimensional latent space ($d_{model} = 256$):

[Equation 9]

$$\mathbf{Z}_{text} = \text{LayerNorm}\!\left( \mathbf{H}_{text} \mathbf{W}_{text} + \mathbf{b}_{text} \right), $$

[Equation 10]

$$\mathbf{Z}_{img} = \text{LayerNorm}\!\left( \mathbf{H}_{img} \mathbf{W}_{img} + \mathbf{b}_{img} \right), $$

with projection matrices

[Equation 11]

$$\mathbf{W}_{text} \in \mathbb{R}^{768 \times d_{model}}, \qquad \mathbf{W}_{img} \in \mathbb{R}^{D_{img} \times d_{model}}, $$

where $D_{img}$ is the MobileViT feature dimension and $d_{model} = 256$. The projections are trainable; they are the first stage at which the two modalities inhabit a common space. Layer Normalization after the linear projection stabilizes the scale of both projected streams before they interact, which matters because the two encoders were pre-trained with different internal distributions.

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

### 5.5 Bidirectional Cross-Attention
The cross-attention module consists of $N_{xattn} = 2$ identical layers, each performing information exchange in both directions, following the co-attention structure of ViLBERT [5] and the scaled dot-product formulation of Eq. (1).

For text-to-image attention, queries are derived from the text stream and keys and values from the image stream:

[Equation 12]

$$\mathbf{Q}_{text} = \mathbf{Z}_{text} \mathbf{W}_{Q,text}, \qquad \mathbf{K}_{img} = \mathbf{Z}_{img} \mathbf{W}_{K,img}, \qquad \mathbf{V}_{img} = \mathbf{Z}_{img} \mathbf{W}_{V,img}, $$

[Equation 13]

$$\mathbf{Z}_{img \rightarrow text} = \text{Softmax}\!\left( \frac{\mathbf{Q}_{text} \mathbf{K}_{img}^{T}}{\sqrt{d_k}} \right) \mathbf{V}_{img}. $$

Each text token's representation is thus recomputed as a content-dependent mixture of image tokens: which image regions matter to a given text token is learned, not fixed. For image-to-text attention the roles reverse:

[Equation 14]

$$\mathbf{Q}_{img} = \mathbf{Z}_{img} \mathbf{W}_{Q,img}, \qquad \mathbf{K}_{text} = \mathbf{Z}_{text} \mathbf{W}_{K,text}, \qquad \mathbf{V}_{text} = \mathbf{Z}_{text} \mathbf{W}_{V,text}, $$

[Equation 15]

$$\mathbf{Z}_{text \rightarrow img} = \text{Softmax}\!\left( \frac{\mathbf{Q}_{img} \mathbf{K}_{text}^{T}}{\sqrt{d_k}} \right) \mathbf{V}_{text}. $$

The two streams are then updated with residual connections:

[Equation 16]

$$\mathbf{Z}_{text}^{out} = \mathbf{Z}_{text} + \text{MLP}\!\left( \mathbf{Z}_{img \rightarrow text} \right), $$

[Equation 17]

$$\mathbf{Z}_{img}^{out} = \mathbf{Z}_{img} + \text{MLP}\!\left( \mathbf{Z}_{text \rightarrow img} \right). $$

[FIGURE 2 — CROSS-ATTENTION BLOCK]

**Caption:** One bidirectional cross-attention layer. Each stream's queries attend to the other stream's keys and values (Eqs. 12-15); the attended representation is added back to its own stream through a residual MLP update (Eqs. 16-17). Layer Normalization is applied before each sub-layer (Pre-LN). The layer is repeated N_xattn = 2 times with h = 4 heads and per-head dimension d_k = 64.

**Placement & purpose:** Section 5.5 (after the bidirectional cross-attention equations). Purpose: make the Q/K/V relationships between the two streams concrete and consistent with Eqs. 12-17. Data source: methodology of Section 5.5 (Eqs. 12-17) and the hyperparameters of Appendix B.

**Note:** final graphics are produced in the LaTeX project (`latex/figures/`, vector sources); the specifications above are the approved rendering contract for regeneration.

Multi-head attention uses $h = 4$ heads with per-head dimension $d_k = 64$. The layer uses Pre-LayerNorm (Pre-LN) design — Layer Normalization applied *before* each sub-layer rather than after — which has been shown to improve Transformer training stability [32]. The residual additions in Eqs. (16)–(17) preserve each stream's original representation, so cross-attention refines rather than replaces the unimodal features; this interacts with the fusion design below.

### 5.6 Pooling and Fusion

Sequence-level representations are reduced by mean pooling. For the text representation, $\mathbf{z}_{text} = \text{MeanPool}(\mathbf{Z}_{text})$; for the image representation, $\mathbf{z}_{img} = \text{MeanPool}(\mathbf{Z}_{img})$. Mean pooling over the attention mask lets variable-length messages (and masked padding) contribute proportionally.

The multimodal representation is obtained by element-wise averaging of the cross-attention outputs:

[Equation 18]

$$\mathbf{z}_{fused} = \frac{\mathbf{z}_{text}^{out} + \mathbf{z}_{img}^{out}}{2}. $$

The fused representation is $d_{model}$-dimensional — not twice the feature dimension, as concatenation-based late fusion would produce. Element-wise averaging keeps the multimodal and unimodal representations in the same space, which is what allows a single shared classifier to serve all three paths.

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

### 5.7 Shared Classifier and Early-Exit Mechanism
The shared classifier maps the $d_{model}$-dimensional representation to a single logit, and it is implemented identically for all three computation paths:

[Equation 19]

$$p(y = 1 \mid m) = \sigma\!\left( \text{MLP}_{cls}(\mathbf{H}_{fused}) \right), $$

where $\mathbf{H}_{fused}$ is the fused multimodal representation or the corresponding pooled unimodal representation.

For MULTIMODAL emails, DCAT optionally evaluates a text-only auxiliary classifier before invoking the vision encoder. The pooled text representation is passed to

[Equation 20]

$$p_{aux}(y = 1 \mid t) = \sigma\!\left( \text{MLP}_{aux}(\mathbf{H}_{unimodal}) \right), $$

and the exit rule is

[Equation 21]

$$\text{exit if } p_{aux} \geq 0.95 \;\;(\text{classify spam}) \quad \text{or} \quad p_{aux} \leq 0.05 \;\;(\text{classify ham}). $$

For values between the two thresholds, the complete multimodal pathway is executed: text → vision → cross-attention → fusion → shared classifier. The auxiliary classifier is separate from the main shared classifier and is trained jointly with the model, so learning the main task simultaneously calibrates the exit. The symmetric 0.95/0.05 thresholds require near-certainty before skipping vision; their effect on the workload is measured in Section 7.7, and their fixed value is examined in Section 9.2.

### 5.8 Training Procedure

The evaluated configuration is:

- **Optimizer:** AdamW [33] with learning rate $1 \times 10^{-4}$ and default weight decay.
- **Scheduler:** cosine annealing.
- **Loss:** binary cross-entropy with logits (Eq. 4), with optional positive-class weighting (Eqs. 5–6) for Weighted-DCAT.
- **Precision:** FP16 mixed precision using PyTorch automatic mixed precision (AMP).
- **Batch size:** 64. **Epochs:** 1.
- **Encoder freezing:** DistilBERT and MobileViT are frozen; projection, cross-attention, and classifier parameters are trainable.
- **Hardware:** an NVIDIA GPU with CUDA support.
- **Reproducibility:** deterministic seeding across Python, NumPy, and PyTorch.

Full-DCAT contains 73,309,090 total parameters, of which 2,008,578 are trainable — 2.74% of the model. The trainable set comprises the projector, the cross-attention blocks, and the classifiers; freezing the encoders is what makes single-epoch training on this corpus feasible and keeps the trainable component comparable in scale to the fusion variants it is compared against.

### 5.9 Inference Pipeline

At inference time:

1. The deterministic router assigns the email to TEXT, IMAGE, MULTIMODAL, or EMPTY (EMPTY is discarded).
2. Only the encoder or encoders required by the selected modality are invoked.
3. For MULTIMODAL emails, the auxiliary classifier is evaluated (Eq. 20).
4. If early exit is not triggered, the image is encoded and bidirectional cross-attention is applied.
5. The resulting representation is passed to the shared classifier.
6. The sigmoid probability is thresholded at 0.5 to produce the binary prediction.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## 6. Experimental Methodology
### 6.1 Corpus and Preprocessing

The corpus used throughout the paper originates from the SpamAssassin public email corpus [7], which provides naturally occurring email messages that retain their original MIME structure — plain-text emails, HTML messages, inline images, and image attachments. MIME preservation is what makes the deterministic modality extraction of Section 4.2 possible. The raw corpus occupies about 16 GB on disk; the processed subset used for primary evaluation contains 6,046 emails. The corpus was selected because it provides naturally occurring mail, preserves the MIME structure needed for deterministic modality extraction, and has been used in previous spam-detection studies.

Preprocessing operates on raw `.eml` files through four deterministic stages:

1. **MIME parsing.** Each `.eml` file is parsed with Python's `email` package, traversing the MIME tree to extract plain text, HTML content, and image content. HTML is reduced to visible text using BeautifulSoup with the lxml parser; image parts are decoded to raw bytes; non-fatal parsing issues are logged.
2. **Content filtering and quality control.** Text is retained when at least 10 characters remain after whitespace stripping. Images must be at least $20 \times 20$ pixels and at least 1024 bytes; images failing these filters are discarded and their drop reasons recorded. When multiple meaningful images are present, the largest image by byte size is selected, with pixel area as tie-breaker.
3. **Image processing.** Selected images are resized to $224 \times 224$ pixels using bicubic interpolation, converted to RGB, and normalized through the `timm` preprocessing pipeline [21] to match the pre-trained MobileViT encoder's expected input distribution.
4. **Text tokenization.** Email text is tokenized with the DistilBERT tokenizer using `max_length = 256`, `truncation = longest_first`, and `padding = max_length`; input IDs and attention masks are generated.

[FIGURE 3 — PREPROCESSING FLOW]

**Caption:** Preprocessing and data-flow diagram. Raw .eml files pass through the four deterministic stages of Section 6.1 (MIME parsing; content filtering with the size and quality thresholds annotated; image processing; text tokenization) before deterministic modality assignment. EMPTY messages are discarded from training and evaluation.

**Placement & purpose:** Section 6.1 (after the four preprocessing stages). Purpose: show the pipeline from raw input to model-ready modalities with the exact thresholds annotated (>=10 chars text; >=20x20 px and >=1024 bytes image; 224x224 resize). Data source: Section 6.1 stages 1-4.

**Note:** final graphics are produced in the LaTeX project (`latex/figures/`, vector sources); the specifications above are the approved rendering contract for regeneration.

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

### 6.2 Dataset Composition, Splits, and Leakage Control
Table 1 reports the composition of the processed corpus.

**Table 1. SpamAssassin dataset composition (processed subset, 6,046 emails)**

| Property | Count | Percentage |
|---|---:|---:|
| Total emails | 6,046 | 100.0% |
| Parse success | 6,046 | 100.0% |
| Ham (legitimate) | 4,150 | 68.6% |
| Spam | 1,896 | 31.4% |
| TEXT | 6,007 | 99.4% |
| MULTIMODAL | 11 | 0.2% |
| IMAGE | 1 | 0.02% |
| EMPTY (excluded) | 27 | 0.4% |
| TEXT ham | 4,146 | 68.6% |
| TEXT spam | 1,861 | 30.8% |
| MULTIMODAL ham | 4 | 0.07% |
| MULTIMODAL spam | 7 | 0.12% |
| IMAGE spam | 1 | 0.02% |
| EMPTY spam | 27 | 0.45% |

Text-only messages make up 99.4% of the processed corpus; only 11 of 6,046 emails are multimodal (4 ham, 7 spam), one email is IMAGE, and 27 are EMPTY and excluded from training and evaluation. The ham/spam split is 4,150 versus 1,896 messages — a 2.19:1 ham-to-spam ratio — so the corpus is moderately imbalanced rather than approximately balanced. This composition is the empirical premise of the whole study: the full-test metric is dominated by text classification, and the multimodal subset is tiny by construction.

The default split uses 70% training, 15% validation, and 15% test data with a fixed random seed of 42, and stratification preserves the ham/spam proportions across splits. The split process enforces that no email appears in more than one subset, and sender-based and campaign-based leakage controls are applied where the corresponding identifiers are available. Appendix C documents one lineage entry generated under an alternative 10% primary-test configuration; the primary tables use the 70/15/15 configuration throughout.

The leakage analysis checks five forms of duplication and overlap: exact text duplicates across splits; exact image duplicates across splits; perceptual image duplicates using perceptual hashing; near-duplicate text pairs using Jaccard similarity; and sender and campaign identifier overlap. Exact textual and hash-based deduplication was applied to the full dataset. The perceptual leakage procedure was implemented and executed as a pilot over a limited subset because of its computational cost; the resulting evidence therefore supports the deduplication checks applied to the full data, while the perceptual audit should not be interpreted as an exhaustive verification of every image pair.

### 6.3 Model Variants

Eight variants are evaluated, each serving a defined diagnostic role:

1. **All-Spam Prior** — predicts spam for every input; a class-prior sanity floor.
2. **Modality Indicator** — uses only the modality type as the input feature; tests how much signal the modality label alone carries.3. **Text-Only** — activates only the text pathway; the text-dominated corpus's reference model.
4. **Image-Only** — activates only the image pathway; quantifies the standalone visual signal.
5. **Late Fusion** — concatenates mean-pooled DistilBERT and MobileViT representations before classification; the standard independent-encoding fusion design.
6. **DCAT-No-XAttn** — removes cross-attention and averages independently pooled text and image representations; isolates the interaction mechanism from the shared-space design.
7. **Full-DCAT** — the complete bidirectional cross-attention architecture (Section 5).
8. **DCAT-Early-Exit** — Full-DCAT with the auxiliary early-exit mechanism enabled.

In addition, a published multimodal baseline is included as a reimplementation of a late-fusion architecture using DistilBERT for text and ResNet-18 for images [4]. It enters this study as one controlled configuration among the variants — same corpus, splits, and protocol — not as an external benchmark.

### 6.4 Ablation Design

Three ablations isolate the paper's research questions, each tied to a gap from Section 3.6:

- **Cross-attention ablation** (gap 1): compares Late Fusion, DCAT-No-XAttn, and Full-DCAT on the multimodal subset — a progression from no interaction, to shared-space averaging, to full bidirectional cross-attention.
- **Imbalance ablation** (gap 3): compares Full-DCAT trained with unweighted BCE against Weighted-DCAT with $w_{\text{spam}} = N_{\text{ham}} / N_{\text{spam}}$ (Eqs. 5–6).
- **Early-exit ablation** (gap 2): compares Full-DCAT and DCAT-Early-Exit using latency, FLOPs, and vision skip rate.

### 6.5 Evaluation Metrics

The evaluation reports Macro-F1 (the unweighted mean of ham-F1 and spam-F1), Ham F1, Spam F1, Ham PR-AUC (the precision-recall area for the ham class), ROC-AUC (overall discrimination between the two classes), and Accuracy (the proportion of correctly classified emails). For multimodal analysis, the same metrics are recomputed using only messages assigned to the MULTIMODAL category (MM-Macro-F1 denotes multimodal Macro-F1). Macro-F1 is used as the headline metric because it weights the two classes equally and is therefore sensitive to majority-class collapse — a failure mode that Section 7.2 shows is real in this setting.

### 6.6 Statistical Evaluation

Paired model comparisons use McNemar's test [31] with continuity correction: the test uses the predictions made by both models on the same examples and evaluates the discordant prediction counts. Two settings are used: (1) the multimodal test subset, containing approximately 11 samples; and (2) pooled out-of-fold predictions from the five-fold cross-validation experiment, containing 7,867 samples. The small multimodal test subset limits the statistical power of comparisons based on those 11 examples; the pooled setting exists precisely to obtain a better-powered comparison.

### 6.7 Efficiency Evaluation

Efficiency is evaluated using total and trainable parameter counts; approximate FLOPs per forward pass; average per-sample latency; P95 latency; the vision skip rate for early exit; and FLOP reduction relative to Full-DCAT. The per-sample and total-time measurements are reported separately throughout because they use different measurement procedures.

### 6.8 Error-Analysis Protocol

Error analysis examines full-test and multimodal confusion matrices for the main model variants, considering false positives, false negatives, and examples misclassified by one model but not another. Per-sample error records are stored in `artifacts/error_analysis/dcat_errors.csv` and `artifacts/error_analysis/late_fusion_errors.csv`, and they are the traceability basis for the error discussion in Section 7.9.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## 7. Results
The protocol of Section 6 fixed what was measured and how; this section reports what the measurements show. Results are organized around the research questions stated at the head of each subsection. Every number below is reproduced from the evaluation artifacts; where the source artifacts contain conflicting values, the conflict is stated rather than resolved.

### 7.1 Full-Test-Set Benchmark

*Research question: which representations carry the corpus's class signal, and how do the fusion designs compare when the full test set dominates the metric?*

**Table 2. Primary benchmark — full test set (three-seed means, seeds 42/43/44)**

| Model | Macro-F1 | Ham F1 | Spam F1 | Ham PR-AUC | ROC-AUC | Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| All-Spam Prior | 0.4000 | 0.0000 | 0.8000 | 0.0000 | 0.5000 | 0.6600 |
| Modality Indicator | 0.5500 | 0.1000 | 0.8500 | 0.1000 | 0.6000 | 0.7000 |
| Text-Only | 0.9827 | 0.9760 | 0.9895 | 0.9968 | 0.9953 | 0.9854 |
| Image-Only | 0.3220 | 0.4901 | 0.1540 | 0.7183 | 0.5400 | 0.3637 |
| Published Baseline | 0.9869 | 0.9818 | 0.9920 | 0.9975 | 0.9969 | 0.9889 |
| Late Fusion | 0.9871 | 0.9820 | 0.9921 | 0.9972 | 0.9965 | 0.9890 |
| DCAT-No-XAttn | 0.9867 | 0.9815 | 0.9919 | 0.9972 | 0.9964 | 0.9887 |
| Full-DCAT | 0.9862 | 0.9808 | 0.9916 | 0.9973 | 0.9967 | 0.9883 |
| DCAT-Early-Exit | 0.9867 | 0.9814 | 0.9919 | 0.9975 | 0.9968 | 0.9887 |

*Source: `results/tables/final_results.csv` (three-seed means from seeds 42, 43, and 44).*

Text-Only achieves Macro-F1 0.9827. Full-DCAT achieves 0.9862, compared with 0.9869 for the Published Baseline and 0.9867 for DCAT-No-XAttn; the difference between Full-DCAT and Late Fusion is small on the full test set. One reporting note, resolved during the publication-readiness audit: the Late Fusion row above is the three-seed mean (0.9871), verified against the designated source table and the per-seed master record; the earlier draft had carried 0.9855 for this row, a transcription error against its own designated source, which also left Table 2 inconsistent with the seed-level analysis in Section 7.8. The two tables now agree. At this performance level, all text-bearing models differ by thousandths of a Macro-F1 point.

Image-Only achieves Macro-F1 0.3220 — below the All-Spam Prior value of 0.4000. Given that meaningful image content is present in only a small fraction of the corpus, image-only training is based on substantially less data than text-only training. The two sanity priors behave as designed: the All-Spam Prior scores 0.4000 Macro-F1 (reflecting the 2.19:1 class imbalance), and the Modality Indicator reaches 0.5500, showing that the modality label alone carries some signal but far less than content.

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

### 7.2 Multimodal-Subset Results
*Research question: what happens on the 11 multimodal emails?*

**Table 3. Multimodal subset results**

| Model | Macro-F1 | Ham F1 | Spam F1 |
|---|---:|---:|---:|
| All-Spam Prior | 0.4968 | 0.0000 | 0.9935 |
| Modality Indicator | 0.4968 | 0.0000 | 0.9935 |
| Text-Only | 0.5584 | 0.1633 | 0.9535 |
| Image-Only | 0.4968 | 0.0000 | 0.9935 |
| Published Baseline | 0.4968 | 0.0000 | 0.9935 |
| Late Fusion | 0.4968 | 0.0000 | 0.9935 |
| DCAT-No-XAttn | 0.8317 | 0.6667 | 0.9967 |
| Full-DCAT | 0.4968 | 0.0000 | 0.9935 |
| DCAT-Early-Exit | 0.4968 | 0.0000 | 0.9935 |

The multimodal subset contains very few samples, and some models predict all or almost all samples as spam. Late Fusion, Full-DCAT, Image-Only, and the All-Spam Prior all have Macro-F1 0.4968 with Ham F1 0.0000 — majority-class collapse. Text-Only reaches 0.5584, the only unimodal model with nonzero ham recall (Ham F1 0.1633), and DCAT-No-XAttn is the strongest, with Macro-F1 0.8317 and Ham F1 0.6667.

One provenance note is required. Table 3 reproduces the archived multimodal evaluation table (`results/tables/main_results_multimodal.csv`, corroborated by `results/tables/modality_analysis.csv`). The source analysis's own summary of this subsection lists Text-Only at 0.4968/0.0000/0.9935 (majority-collapsed) and Image-Only at 0.2863/0.4444/0.1282, values that match neither archived table. The summary values therefore appear to describe a different (unrecoverable) aggregation or configuration, and the archived table — the designated source for these metrics — is reported here. This conflict is disclosed rather than silently reconciled.

One data-quality caveat is preserved from the source analysis, with its arithmetic clarified during the publication-readiness audit: the All-Spam Prior accuracy reported for this subset is 0.9871. That value is consistent with a 155-sample multimodal evaluation set containing 2 ham and 153 spam messages (153/155 = 0.9871; Spam-F1 = 306/308 = 0.9935) rather than with the 11-message subset described by the corpus counts (4 ham, 7 spam). The manuscript therefore uses the authoritative sample-level counts (4 ham, 7 spam) for prevalence and treats the subset-level metrics as produced by the archived evaluation configuration, whose subset composition is not recoverable from the available artifacts.

### 7.3 Cross-Attention Ablation

*Research question: does bidirectional cross-attention help on multimodal inputs?*

The cross-attention ablation compares the same three models as the multimodal analysis: Late Fusion (no interaction, concatenation-based), DCAT-No-XAttn (shared space, averaged representations), and Full-DCAT (bidirectional cross-attention) — a progression from no interaction to full bidirectional interaction. On the 11-message multimodal test subset, all three report identical majority-collapsed values (Macro-F1 0.4968, Ham F1 0.0000, Spam F1 0.9935) except DCAT-No-XAttn, whose Macro-F1 of 0.8317 (Ham F1 0.6667) was reported in Table 3 and is the only non-collapsed interaction-capable result in the study.

McNemar's test gives p = 1.0000 for Full-DCAT versus Late Fusion, and p = 0.2482 for Full-DCAT versus DCAT-No-XAttn. Neither comparison reaches the α = 0.05 threshold. With approximately 11 multimodal test samples, these comparisons have limited statistical power: Full-DCAT is statistically indistinguishable from Late Fusion here, and the apparent advantage of the simpler DCAT-No-XAttn over Full-DCAT is not statistically significant either.

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

### 7.4 Class-Imbalance Ablation
*Research question: does class weighting matter more than architecture?*

**Table 4. Class-imbalance ablation**

| Model | Macro-F1 | Spam F1 | Ham F1 | MM-Macro-F1 |
|---|---:|---:|---:|---:|
| Full-DCAT | 0.9862 | 0.9916 | 0.9809 | 0.6253 |
| Weighted Full-DCAT | 0.9880 | 0.9927 | 0.9833 | 0.7478 |

Weighted-DCAT increases full-test Macro-F1 from 0.9862 to 0.9880 and multimodal Macro-F1 from 0.6253 to 0.7478. The corresponding pooled out-of-fold McNemar comparisons give p = 2.49 × 10⁻⁴⁵ for Weighted-DCAT versus Full-DCAT, and p = 3.34 × 10⁻⁶ for Weighted-DCAT versus Late Fusion — both far below α = 0.05 on 7,867 pooled out-of-fold samples. The imbalance ablation is the only comparison in the study with statistically decisive differences.

### 7.5 Multimodal Robustness: Five-Fold Cross-Validation

*Research question: is the multimodal signal stable?*

Five-fold cross-validation is performed on the larger evaluation subset described in the experiment artifacts (Table 5).

**Table 5. Multimodal robustness (five-fold CV on 8K subset)**

| Model | MM-Macro-F1 (mean) | MM-Macro-F1 (std) |
|---|---:|---:|
| DCAT-No-XAttn | 0.5171 | 0.0597 |
| Full-DCAT | 0.7077 | 0.2639 |
| Late Fusion | 0.5453 | 0.1222 |
| Published Baseline | 0.5564 | 0.1192 |

Full-DCAT has the highest reported mean MM-Macro-F1 at 0.7077; its standard deviation of 0.2639 is also the highest among the listed models. The per-fold results (Section 7.6) show large changes between folds, including folds in which Full-DCAT reached 1.0000 and folds in which it was close to the All-Spam Prior level. The small amount of multimodal data in the evaluation protocol limits how strongly these fold-level differences can be generalized.

### 7.6 Per-Fold Behavior

*Research question: where does the variance come from?*

**Table 6. Per-fold MM-Macro-F1 from five-fold CV**

| Fold | Late Fusion | DCAT-No-XAttn | Full-DCAT |
|---:|---:|---:|---:|
| 1 | 0.4971 | 0.6647 | 0.4971 |
| 2 | 0.4971 | 0.6647 | 0.4971 |
| 3 | 0.4968 | 0.6644 | 0.4968 |
| 4 | 0.7380 | 0.5451 | 1.0000 |
| 5 | 0.4975 | 0.6531 | 1.0000 |

*Source: `artifacts/weighted_cv/cv_results.csv`.* The fold-level values above are reproduced from the recorded analysis; the archived cross-validation artifacts record the same models' means under a different fold numbering, so the per-fold ordering could not be independently re-derived from the repository.

The fold-level values vary substantially. Full-DCAT reaches 1.0000 in folds 4 and 5, while folds 1–3 remain near the All-Spam Prior level. The variation is consistent with a metric that is highly sensitive to the composition of a small multimodal evaluation set: the same model is perfect in some folds and majority-collapsed in others, depending on which handful of multimodal messages lands in the fold's evaluation split.

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

### 7.7 Efficiency Results
*Research question: what does conditional computation actually save?*

**Table 7. Efficiency comparison**

| Model | Params | Trainable params | FLOPs | Latency/sample (ms) |
|---|---:|---:|---:|---:|
| Published Baseline | 77,967,426 | 428,034 | ~13B | 1.48 |
| Late Fusion | 71,761,314 | 460,802 | ~13B | 2.65 |
| DCAT-No-XAttn | 72,784,034 | 1,483,522 | ~13B | 2.66 |
| Full-DCAT | 73,309,090 | 2,008,578 | ~13B | 2.70 |
| DCAT-Early-Exit | 73,309,090 | 2,008,578 | ~11B (avg) | 2.68 |

DCAT has approximately four times as many trainable parameters as Late Fusion — 2.01M versus 0.46M — with the additional parameters primarily associated with the cross-attention blocks and classifier. Total FLOPs remain close to 13B for the four always-on variants because the frozen encoders dominate the computational cost. DCAT-Early-Exit is listed at approximately 11B FLOPs on average over the full workload; the source artifact annotates this cell "(avg, 90% text-only)", indicating an average taken over the corpus's text-only majority, and this convention differs from the measured 12.7B in Table 8, which reflects the early exit's marginal effect on the multimodal portion of the workload. The two figures are estimates under different averaging conventions and are not directly comparable. The Published Baseline has the lowest reported per-sample latency at 1.48 ms, while Full-DCAT and DCAT-Early-Exit report 2.70 ms and 2.68 ms, respectively.

**Table 8. Early-exit efficiency details (full test set)**

| Metric | Full-DCAT | DCAT-Early-Exit | Diff |
|---|---:|---:|---:|
| Total latency | 59.9 ms | 74.7 ms | +24.82% |
| P95 latency | 60.3 ms | 113.6 ms | +88.39% |
| Total FLOPs | 12.8B | 12.7B | −0.63% |
| Vision skip rate | 0.00% | 4.45% | +4.45% |

The vision skip rate is 4.45%, and the corresponding average FLOP reduction is 0.63%. The total-time measurement shows an increase of 24.82% for the early-exit variant, while the per-sample measurement in Table 7 changes from 2.70 ms to 2.68 ms. These values come from different measurement procedures and should not be combined into a single latency claim. The measured overhead of evaluating the auxiliary classifier and handling the conditional branch offsets the theoretical computational reduction in the total-time experiment.

### 7.8 Seed Variance and Modality-Specific Performance

*Research question: how stable are the headline numbers?*

**Table 9. Three-seed Macro-F1 variance**

| Model | Seed 42 | Seed 43 | Seed 44 | Mean | Std |
|---|---:|---:|---:|---:|---:|
| Published Baseline | 0.9870 | 0.9865 | 0.9871 | 0.9869 | 0.0003 |
| Late Fusion | 0.9868 | 0.9869 | 0.9875 | 0.9871 | 0.0003 |
| Full-DCAT | 0.9860 | 0.9863 | 0.9864 | 0.9862 | 0.0002 |

Across the three seeds, the standard deviation is at most 0.0003 for these models. Late Fusion has the highest mean among the three (0.9871), followed by the Published Baseline (0.9869) and Full-DCAT (0.9862); the differences between the means are small.

**Table 10. Modality-specific Macro-F1 (full test set, seed 42)**

| Model | Text-only emails | Multimodal emails |
|---|---:|---:|
| Late Fusion | 0.9858 | 0.4968 |
| DCAT-No-XAttn | 0.9871 | 0.8317 |
| Full-DCAT | 0.9865 | 0.4968 |

On the TEXT modality, the reported models have Macro-F1 values of 0.9858 or higher. The IMAGE modality contains only one sample, so any associated metric is highly sensitive to that single prediction. On the MULTIMODAL subset, DCAT-No-XAttn reports 0.8317 while Full-DCAT and Late Fusion report 0.4968 — the same ordering the multimodal analyses of Sections 7.2–7.4 exhibit, now isolated from the text-dominated remainder of the corpus.

### 7.9 Confusion-Matrix Results

*Research question: where do the remaining errors concentrate?*

Figure 4 reports the archived confusion matrix for DCAT in the weighted-primary configuration (panel a), the configuration in which the class-weighting analysis of Section 7.4 was performed, together with a Macro-F1 comparison across the evaluated variants on the multimodal subset (panel b, values from Table 3). In the weighted-primary configuration, the DCAT confusion matrix contains 57 false positives and 25 false negatives on the full test set; false positives impose costs on legitimate mail, false negatives represent missed spam, and the per-sample error records of Section 6.8 allow both to be traced to individual messages. The panel is intended to make the contrast between corpus-level and subset-level behavior directly visible.

[FIGURE 4 — RESULTS VISUALIZATION PANEL]

**Caption:** Results visualization. (a) Confusion matrix of DCAT in the weighted-primary configuration on the full test set (n = 7,351; 57 false positives, 25 false negatives). (b) Multimodal Macro-F1 for all evaluated variants on the multimodal subset, reproducing the values of Table 3 (ASP: All-Spam Prior; MI: Modality Indicator; Text: Text-Only; Image: Image-Only; PB: Published Baseline; LF: Late Fusion; NoXAttn: DCAT-No-XAttn; DCAT: Full-DCAT; EE: DCAT-Early-Exit). Majority-collapsed variants sit at 0.4968; DCAT-No-XAttn reaches 0.8317.

**Placement & purpose:** Section 7.9 (Confusion-Matrix Results). Purpose: make the contrast between corpus-level and subset-level behavior directly visible. Data source: (a) artifacts/experiments/weighted_primary/results.json (confusion matrix [[2196, 57], [25, 5073]], n = 7,351); (b) Table 3 values.

**Note:** final graphics are produced in the LaTeX project (`latex/figures/`, vector sources); the specifications above are the approved rendering contract for regeneration.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## 8. Discussion
This section interprets the evidence of Section 7. Observed results are distinguished from their reasonable interpretations; speculation is labeled as such.

### 8.1 Why the Full-Test Metric Barely Moves

The observed result is a 0.0009 Macro-F1 gap between Full-DCAT (0.9862) and Late Fusion (0.9871) on the full test set, with seed-level standard deviations of at most 0.0003 (Tables 2 and 9). Three corpus-level facts explain this. First, the corpus is 99.4% text-only, so the cross-attention module — the only architectural difference between Full-DCAT and DCAT-No-XAttn — is exercised on roughly 0.2% of the data; its contribution is concentrated in a small fraction of examples. Second, the multimodal subset contains only 11 emails, which provides limited training signal for estimating cross-modal interactions; the additional trainable parameters of the cross-attention module may be sensitive to the specific multimodal examples available during training. Third, the shared classifier is trained primarily on text-dominated batches, so multimodal representations must be mapped into a decision space shaped mainly by text-only examples. These conditions plausibly explain why the more expressive cross-attention architecture does not improve the full-test metric; they are interpretations consistent with the observed pattern, not established causes. Whether the added interaction capacity helps under these conditions is an empirical question; Sections 7.1–7.4 measure it directly, and Section 8.2 interprets the outcome.

### 8.2 The Multimodal Subset: Signal, Scarcity, and Sensitivity

On the multimodal test subset, DCAT-No-XAttn reports Macro-F1 0.8317 compared with 0.4968 for Full-DCAT (Table 3) — the largest architecture-linked difference in the study — and it runs in the opposite direction from the design's intent. The simpler variant averages independently pooled text and image representations rather than applying cross-attention. Two interpretations are consistent with the evidence. With only 11 primary multimodal examples, the estimate is highly sensitive to individual predictions. And the additional parameters and learned interactions in Full-DCAT may be difficult to estimate from the available multimodal training data, whereas DCAT-No-XAttn's representation preserves the two modalities separately until averaging and may be less sensitive to the limited signal.

The statistical result disciplines both readings: the McNemar comparison between Full-DCAT and DCAT-No-XAttn is not significant at α = 0.05 (p = 0.2482). The observed Macro-F1 difference should therefore be treated as a result specific to this small evaluation rather than as evidence of a general advantage for removing cross-attention. What the subset does establish unambiguously is the failure mode it exposes: every fully trained interaction-capable model that collapsed, collapsed to majority-class prediction (Ham F1 = 0.0000), the exact pattern the Macro-F1 headline metric is chosen to expose.

### 8.3 Class Weighting Changes More than Architecture Does

The imbalance ablation isolates a training-objective effect: changing the class weighting changes the predictions substantially on the pooled evaluation. Weighted-DCAT improves multimodal Macro-F1 from 0.6253 to 0.7478 and full-test Macro-F1 from 0.9862 to 0.9880, and the pooled out-of-fold McNemar comparisons are statistically significant for both Weighted-DCAT versus Full-DCAT (p = 2.49 × 10⁻⁴⁵) and Weighted-DCAT versus Late Fusion (p = 3.34 × 10⁻⁶). Within this experiment, the change in the loss function produces a larger multimodal improvement than the difference between the cross-attention and simpler fusion variants. The result does not establish that class weighting is universally dominant, but it provides direct evidence that class imbalance materially affects the evaluated multimodal task — evidence for gap 3 of Section 3.6.

### 8.4 Efficiency: Theoretical Savings versus Measured Overhead

The early-exit mechanism skips the vision encoder for 4.45% of the multimodal cases in the evaluated workload; because only a small fraction of the corpus is multimodal, the resulting average FLOP reduction is 0.63%. The two latency measurements tell different stories: the per-sample measurement (Table 7) is essentially unchanged (2.70 ms → 2.68 ms), while the total-time measurement (Table 8) shows a 24.82% increase in total latency and an 88.39% increase in P95 latency. The measurements should not be combined into a single latency claim. The total-time measurement shows that conditional-execution overhead — evaluating the auxiliary classifier and handling the branch — can outweigh the computational saving under this workload. A corpus with a larger proportion of multimodal messages would provide a different workload for the same mechanism; that case was not evaluated here; the savings scale with multimodal prevalence, not with the mechanism itself.

### 8.5 What DCAT Does and Does Not Establish

Read together, the protocols provide different views of the architecture, and the paper's claims are bounded accordingly. What the evidence supports: DCAT matches the strongest baselines on the full test set (Macro-F1 0.9862 versus 0.9869–0.9871) with a small, seed-stable gap; its cross-validation mean multimodal Macro-F1 is the highest reported (0.7077 versus 0.5453 for Late Fusion) but with much larger fold-to-fold variance (Section 7.6); class weighting produces the only statistically decisive improvements; and the early exit achieves small, workload-dependent savings at a measured overhead cost. What the evidence does not support: a claim that cross-attention improves full-test performance under this corpus and protocol — the full-test results show no advantage for cross-attention over the published late-fusion baseline, and the multimodal-subset advantage of the simpler variant is statistically inconclusive. The honest summary is that architectural expressiveness did not pay under multimodal scarcity, while the training objective did. The corpus is 99.4% text-only, and these conclusions should not be generalized to email corpora with substantially higher proportions of image-containing messages.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## 9. Limitations and Threats to Validity
### 9.1 Dataset Limitations

**Extreme multimodal scarcity.** Only 11 emails in the primary SpamAssassin subset are multimodal. Metrics calculated on this subset are sensitive to individual predictions and should not be extrapolated to other domains.
**Single corpus.** All experiments use the SpamAssassin corpus; performance on other email datasets is not evaluated.
**No OCR.** The pipeline does not extract text rendered inside images. Image-based spam that places its primary text content inside a graphic therefore loses that information before classification.
**Single-image limitation.** Only the largest meaningful image is processed for messages containing multiple images; other visual content is not exposed to the model.

### 9.2 Architecture Limitations

**Frozen encoders.** DistilBERT and MobileViT remain frozen during training; domain-specific fine-tuning was not evaluated.
**Simple fusion strategy.** The multimodal representation uses element-wise averaging after cross-attention; other fusion mechanisms were not evaluated.
**Fixed early-exit thresholds.** The thresholds are fixed at 0.95 and 0.05; the effect of changing them was not studied.

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

### 9.3 Evaluation Limitations
**Small multimodal test set.** The primary multimodal test subset contains approximately 11 emails; multimodal metrics and McNemar comparisons are sensitive to a small number of examples.
**Single training epoch.** All models are trained for one epoch; longer training schedules could produce different optimization behavior, particularly for the cross-attention parameters.
**No adversarial evaluation.** The model is not evaluated against deliberately constructed adversarial spam.
**Efficiency measurement uncertainty.** The reported per-sample and total-time measurements differ, and the original detailed source artifact for the total-time comparison is no longer available in the repository. In addition, the efficiency table mixes two FLOPs figures with different averaging conventions (a workload-average estimate for the early-exit variant and a marginal measured value for the comparison), which cannot be converted into one another from the available artifacts.

### 9.4 Threats to Validity

**Internal validity.** Deterministic modality routing and duplicate checks reduce several sources of evaluation contamination; the single-epoch training regime and limited multimodal data remain important constraints.
**Construct validity.** Macro-F1, class-specific F1, PR-AUC, and ROC-AUC are standard classification metrics, but multimodal Macro-F1 computed on only a small number of emails has limited precision.
**External validity.** The experiments use one email corpus with a strong text-only majority; the findings may differ for datasets containing more image-containing emails or different spam characteristics.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## 10. Conclusion and Future Work
This paper presented DCAT, a conditional multimodal email spam detection architecture combining bidirectional cross-attention, deterministic modality routing, and optional early-exit computation, evaluated on a naturally paired SpamAssassin corpus whose defining property is multimodal scarcity (11 of 6,046 emails) under a text-only majority (99.4%).

The evidence supports three conclusions. First, on the full test set, Full-DCAT achieves Macro-F1 0.9862 against 0.9869 for the published-baseline reimplementation and 0.9871 for Late Fusion across three seeds; the differences are small, and the experiments do not demonstrate a consistent full-test advantage from adding cross-attention. Second, the multimodal results are highly sensitive to data distribution, class imbalance, and the size of the multimodal subset: Full-DCAT and the simpler variants collapse to majority-class prediction on the 11-message test subset, five-fold cross-validation yields the highest mean for Full-DCAT (0.7077 versus 0.5453 for Late Fusion) but with the highest variance, and class weighting — the training-objective change — produces the study's only statistically significant improvements (multimodal Macro-F1 0.6253 → 0.7478; pooled out-of-fold McNemar p = 2.49 × 10⁻⁴⁵ against Full-DCAT and p = 3.34 × 10⁻⁶ against Late Fusion). Third, conditional computation behaves as theory predicts but as the workload dictates: the early exit skips vision for 4.45% of multimodal cases and saves 0.63% of FLOPs, while the total-time measurement shows a 24.82% latency increase from execution overhead.

Future work follows directly from the limitations: (1) corpus expansion to larger datasets with substantially more multimodal emails, including image-heavy phishing and marketing corpora, so that training-objective effects such as the class-weighting advantage can be re-examined at scale; (2) OCR integration to extract text embedded inside images as an additional textual signal; (3) encoder fine-tuning of DistilBERT and MobileViT under controlled learning-rate schedules; (4) multi-image support, processing multiple meaningful images per email instead of only the largest; (5) learned routing that can account for modality quality and relevance beyond deterministic content rules; (6) contrastive pre-training of the projection and cross-attention components on paired text-image representations before classification; and (7) larger-scale efficiency analysis of early-exit behavior on corpora with higher multimodal prevalence and across multiple threshold settings.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## Data Availability
The evaluation artifacts are available in the project repository: per-sample error records at `artifacts/error_analysis/dcat_errors.csv` and `artifacts/error_analysis/late_fusion_errors.csv`; cross-validation results at `artifacts/weighted_cv/cv_results.csv`; primary benchmark results at `results/tables/final_results.csv`; and the complete results lineage at `artifacts/final_results/results_lineage.csv`. The SpamAssassin public corpus is publicly available [7].

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## Declarations
**Competing interests.** The author declares no competing interests.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## Appendix A. Dataset and Preprocessing Reference
| Parameter | Value |
|---|---|
| Total emails (SpamAssassin subset) | 6,046 |
| Ham emails | 4,150 (68.6%) |
| Spam emails | 1,896 (31.4%) |
| Text-only emails | 6,007 (99.4%) |
| Multimodal emails | 11 (0.2%) |
| Image-only emails | 1 (0.02%) |
| Empty emails (excluded) | 27 (0.4%) |
| Text truncation length | 256 tokens |
| Image resolution | 224 × 224 pixels |
| Train/Val/Test split | 70/15/15 (primary configuration) |

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## Appendix B. Model Hyperparameters
| Hyperparameter | Value |
|---|---|
| Text encoder | DistilBERT-base-uncased (frozen) |
| Vision encoder | MobileViT-small via timm (frozen) |
| Shared latent dimension | 256 |
| Cross-attention layers | 2 |
| Cross-attention heads | 4 |
| Cross-attention d_model | 256 |
| Cross-attention d_ff | 1024 |
| Cross-attention dropout | 0.1 |
| Cross-attention activation | GELU |
| Cross-attention normalization | Pre-LayerNorm |
| Classifier hidden dim | 128 |
| Classifier dropout | 0.3 |
| Classifier activation | GELU |
| Pooling strategy | Mean pooling |
| Optimizer | AdamW |
| Learning rate | 1 × 10⁻⁴ |
| Scheduler | Cosine annealing |
| Batch size | 64 |
| Epochs | 1 |
| Precision | FP16 mixed |
| Loss function | BCEWithLogitsLoss |
| Classification threshold | 0.5 |
| Early-exit high threshold | 0.95 |
| Early-exit low threshold | 0.05 |
| Seeds | 42, 43, 44 |

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

## Appendix C. Results Lineage and Reproducibility
*Source: `artifacts/final_results/results_lineage.csv`.*

| Metric | Model | Split | Seed/Fold | Source artifact | Value | Aggregation |
|---|---|---|---|---|---:|---|
| Macro-F1 | Full-DCAT | Primary Test (10%) | Seed 42 | `artifacts/experiments/weighted_primary/results.json` | 0.9868 | Unweighted mean of Spam and Ham F1 |
| MM-Macro-F1 | Full-DCAT | Multimodal CV (5-Fold) | 5-Fold CV | `artifacts/experiments/weighted_cv/cv_results.csv` | 0.6609 | Mean across 5 folds |
| MM-Macro-F1 | Late-Fusion | Multimodal CV (5-Fold) | 5-Fold CV | `artifacts/experiments/weighted_cv/cv_results.csv` | 0.5564 | Mean across 5 folds |
| MM-Macro-F1 | Weighted-DCAT | Multimodal CV (5-Fold) | 5-Fold CV | `artifacts/experiments/weighted_cv/cv_results.csv` | 0.6824 | Mean across 5 folds |
| McNemar p-value | Weighted-DCAT vs. Full-DCAT | Pooled OOF (7,867 samples) | All folds | task-1070 log | 2.49 × 10⁻⁴⁵ | Exact/asymptotic McNemar with continuity correction |
| McNemar p-value | Weighted-DCAT vs. Late-Fusion | Pooled OOF (7,867 samples) | All folds | task-1070 log | 3.34 × 10⁻⁶ | Exact/asymptotic McNemar with continuity correction |

*Note.* The lineage table is reproduced as recorded. Its seed-42 primary-test entry (0.9868) and CV means (0.6609 / 0.5564 / 0.6824) differ from the three-seed means of Table 2 and the CV means of Table 6 because the lineage rows document different aggregation settings (a seed-42 primary-test run and an alternative CV configuration); the manuscript's headline tables cite their own authoritative sources as noted beneath each table. The split labels reflect the full raw corpus (approximately 73,500 emails, 10% ≈ 7,351 test emails) rather than the deduplicated 6,046-message evaluation corpus (15% ≈ 907), which explains the label arithmetic. A former discrepancy between the Late Fusion three-seed mean in Table 2 (initially 0.9855) and the seed-level analysis (0.9871) was resolved during the publication-readiness audit as a transcription error against the designated source table; the corrected value is used throughout.



## References

[1] F. Jáñez-Martino, R. Alaiz-Rodríguez, V. González-Castro, E. Fidalgo, and E. Alegre, "A review of spam email detection: analysis of spammer strategies and the dataset shift problem," *Artificial Intelligence Review*, vol. 56, pp. 1145–1173, 2023. DOI: 10.1007/s10462-022-10195-4.

[2] A. Annadatha and M. Stamp, "Image spam analysis and detection," *Journal of Computer Virology and Hacking Techniques*, vol. 14, pp. 39–52, 2018. DOI: 10.1007/s11416-016-0287-x.

[3] P. H. Kyaw, J. Gutierrez, and A. Ghobakhlou, "A systematic review of deep learning techniques for phishing email detection," *Electronics*, vol. 13, no. 19, p. 3823, 2024. DOI: 10.3390/electronics13193823.

[4] Z. Zhang, Z. Deng, W. Zhang, and L. Bu, "MMTD: A multilingual and multimodal spam detection model combining text and document images," *Applied Sciences*, vol. 13, no. 21, p. 11783, 2023. DOI: 10.3390/app132111783.

[5] J. Lu, D. Batra, D. Parikh, and S. Lee, "ViLBERT: Pretraining task-agnostic visiolinguistic representations for vision-and-language tasks," in *NeurIPS 32*, 2019. arXiv:1908.02265.

[6] N. Freed and N. Borenstein, "Multipurpose Internet Mail Extensions (MIME) Part One: Format of Internet Message Bodies," RFC 2045, November 1996. https://www.rfc-editor.org/info/rfc2045.

[7] Apache Software Foundation, "SpamAssassin Public Corpus," 2006. [Online]. Available: https://spamassassin.apache.org/old/publiccorpus/

[8] T. Mikolov, K. Chen, G. Corrado, and J. Dean, "Efficient estimation of word representations in vector space," in *ICLR Workshop*, 2013. arXiv:1301.3781.

[9] X. Zhang, J. Zhao, and Y. LeCun, "Character-level convolutional networks for text classification," in *NeurIPS 28*, 2015. arXiv:1509.01626.

[10] Y. Kim, "Convolutional neural networks for sentence classification," in *EMNLP*, 2014, pp. 1746–1751. DOI: 10.3115/v1/D14-1181.

[11] S. Hochreiter and J. Schmidhuber, "Long short-term memory," *Neural Computation*, vol. 9, no. 8, pp. 1735–1780, 1997. DOI: 10.1162/neco.1997.9.8.1735.

[12] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, "Attention is all you need," in *NeurIPS 30*, 2017. arXiv:1706.03762.

[13] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, "BERT: Pre-training of deep bidirectional transformers for language understanding," in *NAACL-HLT*, 2019, pp. 4171–4186. DOI: 10.18653/v1/N19-1423.

[14] Y. Liu et al., "RoBERTa: A robustly optimized BERT pretraining approach," arXiv:1907.11692, 2019.

[15] V. Sanh, L. Debut, J. Chaumond, and T. Wolf, "DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter," arXiv:1910.01108, 2019.

[16] K. Simonyan and A. Zisserman, "Very deep convolutional networks for large-scale image recognition," in *ICLR*, 2015. arXiv:1409.1556.

[17] K. He, X. Zhang, S. Ren, and J. Sun, "Deep residual learning for image recognition," in *CVPR*, 2016, pp. 770–778. DOI: 10.1109/CVPR.2016.90.

[18] A. G. Howard et al., "MobileNets: Efficient convolutional neural networks for mobile vision applications," arXiv:1704.04861, 2017.

[19] A. Dosovitskiy et al., "An image is worth 16x16 words: Transformers for image recognition at scale," in *ICLR*, 2021. arXiv:2010.11929.

[20] S. Mehta and M. Rastegari, "MobileViT: Light-weight, general-purpose, and mobile-friendly vision transformer," in *ICLR*, 2022. arXiv:2110.02178.

[21] R. Wightman, "PyTorch Image Models," GitHub repository, 2019. [Online]. Available: https://github.com/rwightman/pytorch-image-models

[22] D. Bahdanau, K. Cho, and Y. Bengio, "Neural machine translation by jointly learning to align and translate," in *ICLR*, 2015. arXiv:1409.0473.

[23] K. Xu, J. Ba, R. Kiros, K. Cho, A. Courville, R. Salakhutdinov, R. Zemel, and Y. Bengio, "Show, attend and tell: Neural image caption generation with visual attention," in *ICML*, PMLR 37:2048–2057, 2015. arXiv:1502.03044.

[24] M. Seo, A. Kembhavi, A. Farhadi, and H. Hajishirzi, "Bidirectional attention flow for machine comprehension," in *ICLR*, 2017. arXiv:1611.01603.

[25] H. Tan and M. Bansal, "LXMERT: Learning cross-modality encoder representations from transformers," in *EMNLP-IJCNLP*, 2019, pp. 5100–5111. DOI: 10.18653/v1/D19-1514.

[26] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, G. Krueger, and I. Sutskever, "Learning transferable visual models from natural language supervision," in *ICML*, PMLR 139:8748–8763, 2021. arXiv:2103.00020.

[27] J. Arevalo, T. Solorio, M. Montes-y-Gómez, and F. A. González, "Gated multimodal units for information fusion," arXiv:1702.01992, 2017.

[28] Y. Han, G. Huang, S. Song, L. Yang, H. Wang, and Y. Wang, "Dynamic neural networks: A survey," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 44, no. 11, pp. 7436–7456, 2022. DOI: 10.1109/TPAMI.2021.3117837.

[29] S. Teerapittayanon, B. McDanel, and H. T. Kung, "BranchyNet: Fast inference via early exiting from deep neural networks," in *ICPR*, 2016, pp. 2464–2469. DOI: 10.1109/ICPR.2016.7900006.

[30] X. Wang, F. Yu, Z. Dou, T. Darrell, and J. E. Gonzalez, "SkipNet: Learning dynamic routing in convolutional networks," in *ECCV*, 2018, pp. 420–436. DOI: 10.1007/978-3-030-01261-8_25.

[31] Q. McNemar, "Note on the sampling error of the difference between correlated proportions or percentages," *Psychometrika*, vol. 12, no. 2, pp. 153–157, 1947. DOI: 10.1007/BF02295996.

[32] R. Xiong, Y. Yang, D. He, K. Zheng, S. Zheng, C. Xing, H. Zhang, Y. Lan, L. Wang, and T. Liu, "On layer normalization in the Transformer architecture," in *ICML*, PMLR 119:10524–10533, 2020.

[33] I. Loshchilov and F. Hutter, "Decoupled weight decay regularization," in *ICLR*, 2019. arXiv:1711.05101.

---

# HUMAN EDITING FACT-CHECK REFERENCE

This section is NOT part of the paper. After rewriting the prose, verify that
every item below still appears in the manuscript, unchanged.

## Corpus and dataset counts

| Item | Value |
|---|---|
| Processed corpus (primary evaluation) | 6,046 emails |
| Raw corpus on disk | ~16 GB (full raw corpus ≈ 73,500 emails) |
| Ham / spam | 4,150 / 1,896 (2.19:1) |
| TEXT / MULTIMODAL / IMAGE / EMPTY | 6,007 (99.4%) / 11 (0.2%) / 1 (0.02%) / 27 (0.4%) |
| MULTIMODAL composition | 4 ham, 7 spam |
| Split | 70/15/15, seed 42, stratified |
| Primary test set | n = 7,351 (weighted-primary lineage label: "10%") |
| Pooled out-of-fold McNemar samples | 7,867 |
| Multimodal CV evaluation subset | "8K subset" per artifact labeling |

## Headline results (Tables 2, 3)

| Item | Value |
|---|---|
| Full-DCAT full-test Macro-F1 (3-seed mean) | 0.9862 |
| Published Baseline | 0.9869 |
| Late Fusion | 0.9871 |
| DCAT-No-XAttn | 0.9867 |
| DCAT-Early-Exit | 0.9867 |
| Text-Only | 0.9827 |
| Image-Only | 0.3220 |
| All-Spam Prior / Modality Indicator (full test) | 0.4000 / 0.5500 |
| Multimodal Macro-F1: collapse level | 0.4968 (Ham F1 0.0000, Spam F1 0.9935) |
| Multimodal: DCAT-No-XAttn | 0.8317 (Ham F1 0.6667) |
| Multimodal: Text-Only | 0.5584 (Ham F1 0.1633, Spam F1 0.9535) |

## Statistical results

| Item | Value |
|---|---|
| McNemar, Full-DCAT vs Late Fusion (MM subset) | p = 1.0000 |
| McNemar, Full-DCAT vs DCAT-No-XAttn (MM subset) | p = 0.2482 |
| Significance threshold | α = 0.05 |
| McNemar, Weighted-DCAT vs Full-DCAT (pooled OOF, 7,867) | p = 2.49 × 10⁻⁴⁵ |
| McNemar, Weighted-DCAT vs Late Fusion (pooled OOF, 7,867) | p = 3.34 × 10⁻⁶ |
| Seed std (Tables 2/9) | ≤ 0.0003 (Full-DCAT 0.0002; PB and LF 0.0003) |

## Five-fold CV (Tables 5, 6)

| Item | Value |
|---|---|
| Full-DCAT mean / std | 0.7077 / 0.2639 |
| Late Fusion mean / std | 0.5453 / 0.1222 |
| Published Baseline mean / std | 0.5564 / 0.1192 |
| DCAT-No-XAttn mean / std | 0.5171 / 0.0597 |
| Full-DCAT per-fold (Table 6) | 0.4971, 0.4971, 0.4968, 1.0000, 1.0000 |

## Efficiency (Tables 7, 8)

| Item | Value |
|---|---|
| Parameters: Full-DCAT / Late Fusion / Published Baseline | 73,309,090 / 71,761,314 / 77,967,426 |
| Trainable: Full-DCAT / Late Fusion | 2,008,578 (2.01M) / 460,802 (0.46M) |
| FLOPs (always-on variants) | ~13B (estimated) |
| DCAT-Early-Exit FLOPs (Table 7) | ~11B (avg, 90% text-only — different convention, not comparable) |
| Total FLOPs measured (Table 8) | 12.8B → 12.7B (−0.63%) |
| Vision skip rate | 4.45% |
| Total latency | 59.9 ms → 74.7 ms (+24.82%) |
| P95 latency | 60.3 ms → 113.6 ms (+88.39%) |
| Latency/sample | PB 1.48 ms; LF 2.65; NoXAttn 2.66; Full-DCAT 2.70; EE 2.68 ms |

## Class-imbalance ablation (Table 4) and modality view (Table 10)

| Item | Value |
|---|---|
| Weighted-DCAT full-test Macro-F1 | 0.9880 (vs 0.9862) |
| Weighted-DCAT MM-Macro-F1 | 0.7478 (vs 0.6253) |
| Table 10 (seed 42): LF / NoXAttn / Full-DCAT text-only | 0.9858 / 0.9871 / 0.9865 |
| Table 10 multimodal column | 0.4968 / 0.8317 / 0.4968 |

## Confusion matrix (Figure 4a, weighted primary)

| Item | Value |
|---|---|
| DCAT, full test, n = 7,351 | [[2196, 57], [25, 5073]] — 57 FP, 25 FN |

## Architecture and preprocessing constants

| Item | Value |
|---|---|
| Shared latent d_model | 256 |
| Cross-attention layers / heads / d_k | 2 / 4 / 64 |
| Cross-attention d_ff / dropout / activation / norm | 1024 / 0.1 / GELU / Pre-LN |
| Classifier hidden / dropout | 128 / 0.3 |
| Encoders | DistilBERT-base-uncased (frozen), MobileViT-small via timm (frozen) |
| Max token length | 256 |
| Image filter / resize | ≥ 20×20 px, ≥ 1024 bytes; 224×224 bicubic |
| Text filter | ≥ 10 characters |
| Optimizer / LR / batch / epochs | AdamW / 1 × 10⁻⁴ / 64 / 1 |
| Precision / loss / threshold | FP16 mixed / BCEWithLogitsLoss / 0.5 |
| Early-exit thresholds | ≥ 0.95 spam, ≤ 0.05 ham |
| Seeds | 42, 43, 44 |

## Mandatory caveats (must survive editing)

1. **0.9855 → 0.9871 transcription correction** — resolved in the
   publication-readiness audit; disclosed in Section 7.1.
2. **Multimodal evaluation-set distinction** — subset-level metrics come from a
   ~155-sample archived evaluation set (0.9871 = 153/155); prevalence uses the
   sample-level counts (4 ham, 7 spam of 6,046). Disclosed in Section 7.2.
3. **Table 3 provenance** — source analysis's summary (Text-Only collapsed
   0.4968; Image-Only 0.2863/0.4444/0.1282) matches neither archived table;
   archived values reported, conflict disclosed, not reconciled (Section 7.2).
4. **Table 6 fold provenance** — per-fold values reproduced from the recorded
   analysis; fold ordering not independently re-derivable (Section 7.6).
5. **FLOPs conventions** — Table 7's ~11B early-exit figure ("avg, 90%
   text-only") vs Table 8's measured 12.7B are different averaging conventions,
   not comparable (Sections 7.7, 9.3).
6. **Total-time efficiency artifact** — original detailed source artifact no
   longer available; per-sample and total-time measurements differ and must not
   be combined (Section 9.3).
7. **Perceptual-leakage audit scope** — audit was pilot-scope, not a
   corpus-wide perceptual-hash audit (Section 9.4).
8. **Appendix C lineage** — lineage rows use different aggregation settings
   (seed-42 primary 0.9868; CV means 0.6609/0.5564/0.6824) and full-raw-corpus
   split labels (10% ≈ 7,351); headline tables cite their own sources.

## Structural inventory (post-edit targets)

| Item | Count |
|---|---|
| Numbered equations | 21 |
| Tables (10 main + 3 appendix) | 13 |
| Figures | 4 |
| References | 33 ([1]–[33], numbering unchanged) |
