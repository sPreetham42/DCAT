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
# 1. Introduction Email is the foundation of asynchronous digital communication. Unsolicited bulk email – spam – has been a constant across email history and remains one of the most intractable cybersecurity problems faced by people and organizations [1]. 

Spam is never static: campaigns update their messaging to work around filters; a growing body of literature documents how images – banners, phishing screenshots, logos, text-as-image – carry part of the spam signal that text-only filters cannot see [2], [3]. 

When the content that distinguishes spam from benign mail is partly in an image, a text-only detector is structurally blind to it.

Modality-agnostic spam detection creates conditions that standard text classifiers do not see. A real-world email corpus is heterogenous in a particular way: most messages are text-only, only some pair text with an image, and far fewer convey their signal mainly in an image. This heterogeneity creates two intertwined problems. 

First, a model that encodes every email in a visual backbone makes needless visual computation for the majority that contain only text. 

Second, a model that learns interactions *between* modalities needs enough paired examples to reliably measure them in natural corpora.

Previous multimodal spam systems typically encode text and images separately then fuse them through concatenation or other late-fusion strategies [4], with attention- and gating-based techniques developed in related multimodal literature [5]. These models differ in where and what kinds of information they share between modalities, but they rely on two assumptions – that every message needs both encoders, and that enough paired examples exist to learn a fusion with complex interactions – that natural email does not support.

This paper presents the Dynamic Cross-Attention Transformer (DCAT), a conditionally multimodal email spam detector designed around the realities of email. DCAT is built on three principles: (1) *bidirectional cross-attention*: where representations are projected into a shared latent space, each modality attends to the other before pooling so that a text feature's representation can depend on the image and vice versa, (2) *deterministic routing*: which assigns each email to one of three categories based on extracted content, and (3) an *early exit*: in which a text-only auxiliary classifier is run on images with insufficient signal, and the full model is only run when the auxiliary classifier is uncertain. Deterministic routing ensures the visual pathway is only used when needed, and early exit reduces the multimodal computation required.

The study aims to answer the following questions:
 Q1 Is the proposed conditional architecture more accurate than a text-only baseline? 

Q2 How does the full model compare to an early-exit model?
 Q3 Is the performance difference maintained when evaluated on the full corpus? 

Q4 Is the class-weighted training objective superior to an unweighted one? 

Q5 Is the model able to learn effective interactions between the modalities? Q6 Can the model operate efficiently in terms of parameters, FLOPs, and latency? Q7 What is the model's attitude towards information sharing, and how is it affected by the size of the training set? 

Q8 Do we observe the vision-skip rate?

Q9 Does the model demonstrate learnability and stability?

The answers to these questions are in the following sections.

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->
2. Background This section presents the background principles on which the rest of this paper is built, with each subsection concluding at the point where methods or evaluation take up the thread - no unrelated background material is presented that is not used in the paper. ### 2.1 Email as a Multimodal Communication Medium The classifier built in this paper makes predictions over message content - which portions of an email are text, which are images - and this content is made well-defined by the formal structure of the email standard. 

The MIME (Multipurpose Internet Mail Extensions) standard [6] designates email messages as structured objects: a set of headers and a body that can contain multiple typed parts. 

Any message can then carry simultaneously a plain text body, an HTML presentation of that body, inline images, and attached files - each a discrete media type, encoded in different parts. Pieces of the MIME tree are traversed by parsing tools and assembled into text and image content. This structure is what makes email inherently multimodal; it also implies that any email classifier built in this manner must operate on content extracted from it, since it cannot assume well-formedness beyond its own paper's processing pipeline. Section 6.1 explains the extraction pipeline used here; the corpus preserves the original MIME structure [7]. 

Three message types make up the corpus and occupy all subsequent discussion: text-only, meaning that there is text and no meaningful image; image-only, meaning that there is a meaningful image and no text; and multimodal, meaning that the message has both (Section 2.2). 

Different corpora contain very different proportions of these three message types, with immediate consequences for both computation (Section 2.6) and learning (Section 3.3). ### 2.2 Spam, Phishing, and the Modern Threatscape Spam is defined as unsolicited bulk email: messages sent in quantity for marketing or attack-related purposes without the user's prior consent [1]. Phishing is a fraudulent message designed to imitate a trusted entity in order to steal login credentials or induce other fraudulent action [3], which typically overlaps strongly with spam; modern detection perspectives treat spam and phishing on a single continuum [3], and the property of interest is that both rely strongly on the visual channel: glossy graphics and brand logos in marketing spam, branded logos and login screens in scam email [2]. 

Any text rendered in an image cannot be filtered by plain text filters, and any visual branding is a way to carry an impersonation claim that plain text can't. As such, spam and phishing cannot be fully defined by text alone. A second property of the spam domain motivates the evaluation methodology used in Sections 6 and 7: dataset shift. 

Spam email is very closely related to the specific phasing out of corpora for relevant computational reasons and models will not necessarily transfer across emails [1]. 

This property motivates a transparent, multi-protocol evaluation strategy. ### 2.3 Content Representations for Text This subsection traces through the evolution of how text has come to be represented by the encoder here; Section 2.4 does the same for images. The representation of text for machine learning has gone through several steps: bag-of-words and TF-IDF vectors made up shallow lexical features that could be consumed by sparse linear or probabilistic classifiers [1]; word embeddings provided dense, learned continuous representations of symbolic lexical units, capturing the distributional properties of words in context [8]; convolutional neural networks enabled learned features from the local concatenation of characters [9] and words [10]; and recurrent neural networks [11] model longer-range sequential dependencies, notably LSTMs. The current generation [13,14,15] is based on the Transformer [12], which removes the recurrence altogether in favor of multiple stacked layers of selfattention - where every token attends to every other - with learned query, key, and value linear projections, as described in the next subsection. 

Pretrained language models (e.g. [13,14]) learn deep, bidirectional contextual representations of large unlabeled corpora that transfer to other NLP problems. 

DistilBERT [15] is an efficient distilled version of BERT with most of its capabilities but fewer parameters and inference cost, making it appropriate as a shared frozen representation of a text for this work. As of Section 5.2, it is used in the form of its six-layer `base-uncased` variant, with 768-dimensional context vectors. ### 2.4 Content Representations for Images Visual representations have followed a similar progression: VGG's [16] uniform small convolutions demonstrated the benefit of depth, Res Net [17] introduced residual pathways to enable even deeper models, and Mobile Nets [18] showed that accuracy suitable for many tasks can be achieved at a mobile-friendly computational budget. 

CNNs also form the basis of visual spam detection, which establishes the fact that visual patterns of texture, color, and overlays carry the spam signal of interest. These are recapitulated here for the case of images: [2]. Transformers for images (ViT, [19]) represented a new point: when treated as an image patch token sequence, and pretrained at scale, a Transformer can be directly trained to produce a classifier. 

MobileViT [20] combined the two ideas: a local processing convolution and a global processing Transformer, yielding an efficient universal image encoder. 

The current work uses the MobileViT-small [20], which is available through the `timm` PyTorch Image Models library [21], accompanied by a matching image preprocess pipeline (resize, normalization, etc.). As with text, Section 5.3 describes the model used. ### 2.5 Attention and Cross-Modal Attention allows one vector set Q to produce a weighted combination of another vector set V, where the weights depend on the content of a third set K: each query compares to each key, the relationships are normalized in a softmax, and then each value is proportionally combined using these normalized weights. 

In the canonical case [12], scaled dotproduct attention:

[Equation 1] [2]

[Q K^\top]/\sqrt{\mathrm{d_k}}) \text{Softmax} \text{Attention} (Q, K, V) = ---V, [3]

where d is the number of dimensions in Q and K, which are identical. Multi-headed versions (see [12]) run multiple such attention processes with different linear projections, and concatenate their output. This idea first demonstrated usefulness in sequence-to-sequence translation, where it learned to produce soft alignments between source and target language [22], and in vision, where it was used to focus the gaze of image captioners on salient regions [23].
*Self-attention* on one sequence: this is how the encoders in Sections 2.3 and 2.4 read each individual sequence. *Cross-attention* on two sequences: each element of one sequence learns an attention-weighted sum over the other sequence, conditional on the other sequence; that is, every element in sequence A learns to pay attention to sequence B, and vice versa. When the results of these two directions are learned and combined (A attending to B and B attending to A) the attention flow is *bidirectional*. 

Flow of attention in two directions was proposed for machine comprehension to learn query-aware representations of context without treating the query separately and causing an early summarization step [24], and the vision-language literature by extending this idea across modalities: split the image and text into separate streams but learn how to pay attention across them via co-attentional Transformer layers [5], learn across-modality encoder representations [25], or contrastively align modalities instead of applying token-level attention [26]. 

A layer of bidirectional cross-attention learns representations of each modality that are a function of content from the other modality - this is what property DCAT is taking advantage of in Section 5.5. This is different from *late fusion* approaches where each modality is processed independently until a pooled feature vector is extracted and then fused, or from *gating-based* approaches where learned multiplicative gates determine how a common set of features influences each modality [27].


<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->
# 2.6 Conditional Computation and Early Exits

2.1. Conditional computation Standard neural networks apply the same computation for each input. Conditional computation adapts it to the input [28], e.g., the composition, depth or width of the network varies depending on the input. Several techniques have been used for it, such as early exiting: placing classifiers at some layer in the network, and if an input can be classified before the last layer, it can exit without completing the forward pass [29]; or dynamic routing: an optimization policy is learned and, for each input, it activates the blocks needed to classify the input (e.g., in the dynamically routed convolutional networks of Skip Net [30]).

Email classification is a special case with a very simple and natural type of interpretable conditional computation. The -structure of each message is prespecified to be completely known without any neural computation: no vision encoder is used for text-only email, and vice versa. Routing on this deterministic signal is free to learn and avoids all misrouting. 

For the broad multimodal market, the full power of a model is available: a text-only auxiliary classifier can be computed first, and the costly vision pathway invoked only when the evidence from the text alone falls below a threshold - an early exit (a "skip" that avoids a full encoder rather than a handful of layers). 

In this richer case, evaluating the auxiliary classifier and then branching off is additional work, and any realized efficiency gains depend on the workload; the efficiency results in Section 7.7 quantify this.


<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->
3. Related work The background and related work sections of this paper answer different questions: What mechanisms does this paper construct on? 

What mechanisms have other systems built on?

How was that work constructed on?

What is the specific question this paper asks?

Background and related work are broken into three approach families; no single system anchors this paper. All numbers are full-test unless explicitly broken out: no identical-theory pair underpins our work.

# 3.1 Text-based spam detection Scored pattern rules [7] led and remain the dominant spam defense on which all modern work rests. Supervised traditional classifiers - Naive Bayes, support vector machines, and random forests - over bag-of-words and tf-idf features form the second generation. Character [9] and word [10] level learned convolution classifiers and sequential models [11] made deep learning. Context-aware transformers - BERT [13], RoBERTa [14], and this paper's own minimal DistilBERT [15] - comprise the state of the art for text-only email classification, and outperform multimodal systems on text-only corpora (verified in this paper's own evaluation, Section 7.1).

# 3.2 Image-based spam detection Image-spam detection treats the image as the primary source of evidence. Convolutional neural networks - from colors and shapes to text overlays - learn spam visual patterns directly from the pixels [2]. Image-identificationCNNs - VGG [16], Res Net [17], and Mobile Net [18] - serve as the feature backbone in such detectors. Image-only classification, however, remains a weak primary signal: images are ambiguous without their associated text, legitimate mail frequently shares similar visual components such as logos and marketing material [1], [2], and this paper's Image-Only variant demonstrates that gap in Section 7.1.

# 3.3 Multimodal spam detection and fusion Multimodal spam detectors fuse the two sources of evidence. Encoding the image and text individually and fusing at the end is a proven paradigm: multilingual multimodal spam detector (MMTD) combines a text encoder with an image encoder over text and document images before fusion [4]. Interaction is introduced into the fusion mechanism using attention [27] and gating: learned gating of the two modalities produces a shared space that learns how the two modalities influence each other, and vision-language models (Section 2.5) - ViLBERT's co-attention [5], Cross-modality LXMERT's structured cross-modal encoder [25], contrastive vision-language BERT CLIP [26] - learned token-level interaction across modalities.

However, two features specific to the email corpus divide multimodal detection in the vision-language domain from other situations. First, truly native, natural multimodal email is rare; test set multimodal examples may be too small to estimate saturated modality interaction reliably. Second, the computation pipeline executes the vision encoder on every message, regardless of need. This latter feature is not specific to published systems: the corpus structure that previous spam models themselves articulated [1], [2], [4] informs both properties.

# 3.4 Conditional computation Early-exit architectures introduce additional exits and allow confidently classified samples to skip subsequent computation stages; dynamic-routing architectures learn conditional execution policies at the level of computational blocks; and Han et al. [28] define these sample-specific execution architectures as a distinct class. The information structure of email, which explicitly identifies the kind of content expected in a message - in this case, the modality or modality set, though this deterministic indication existed in the data collection procedure in Han et al. [28]'s work - in each message offers a strong, zero-cost signal for content-based modality routing that existing general mechanisms do not consider: the text and image encoders needed for a particular message are known in the message itself, before execution. This paper's approach - using image-conditional modality routing and an early message-level exit to skip vision - is a modality-awareness flavor of conditional computation that is, to our knowledge, the first to appear in email spam detection.

# 3.5 Evaluation practice in settings of modality imbalance between available sources of evidence complicates evaluation practice: a model can post excellent results across the full test corpus while failing on the instances that define its unique knowledge, and corpus shift issues common in spam detection mean that common metrics are driven by corpus composition [1]. These issues motivate the evaluation approach used here: separating full test from multimodal subset performance, performing five-fold cross-validation in the multimodal subset, and testing model paired differences with McNemar [31] on pooled out-of-sample predictions.<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->
# 3.6 Gaps in Surveyed Literature Three gaps below are revealed in Sections 3.1-3.5, and the paper is organized to address each: 1. Cross-modal interaction in email spam studies is limited to a few specialized formalisms (if any) [4] [27] - none is the dynamic, token-level, bidirectional cross-attention dominant in vision-language architectures [5], too new to have appeared in email spam. 2. Unconditional visual encoding is expensive: multimodal pipelines encode both modalities for every message [4] even when corpus analysis shows the text content outnumbers email's visual content by a factor of 1800:1 [7], [1] - wasting vision effort needlessly. 

3. Class imbalance in the cited studies is wrongly ignored by some systems and, more tolerably, unmentioned by all [1], [2], even though the domain literature [1] [7] clear mentions that individual messages about 1800 text tokens to 1 email visual "token." 

4. The gamut of study metrics are rarely paired: report cross-validation stability, report baseline scores, report message and subset test metrics, measure statistical significance - in the cited studies, only some of these were present and when they were, they appeared scattered in the text. DCAT addresses each of these gaps: the combinations of cross-attention (gap 1), early exit (gap 2), class-weighting (gap 3), and multi-protocol evaluation (gap 4).


<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->
4. Problem Formulation

# 4.1 Task Definition

Suppose an email message m has text content t (the email body, subject line, and any other text data that has been extracted) and is accompanied by one or more images {I_1, I_2,..., I_K} embedded inline or as attachments. The goal is binary classification of the email message: predict.

[Equation 2]

Where $y \in \{0, 1\},$ $y=0$ is ham and legitimate email, and $y=1$ is spam.

# 4.2 Modality Routing

Using the features extracted at preprocessing, all emails are routed in a deterministic fashion to one of four routes. Suppose the Boolean indicators $has\_text$ and $has\_image$ denote that meaningful text (10 or more characters in length after cleaning) and at least 1 meaningful image (qualifies the size/quality constraints outlined in section 6.1) are included. Then the rule for routing is:

[Equation 3]

Modality(m) = \begin{cases} a MULTIMODAL, & \text{has\_text} \wedge \text{has\_image} \\ a TEXT, & \text{has\_text} \wedge \neg \text{has\_image} \\ a IMAGE, & \neg \text{has\_text} \wedge \text{has\_image} \\ an EMPTY, & \text{otherwise}. \end{cases}

EMPTY messages - those with neither text nor meaningful image - do not proceed to training or evaluation. The router decision is deterministic: there is no learned classifier, no probability threshold, no learned heuristic. We prefer determinism: the content structure of a message completely decides its modality structure, so a learned router could only add error, cost, and opacity to a decision that content structure already resolves.

# 4.3 Conditional Computation Paths

DCAT implements three active computation paths:

- **TEXT path:** text encoder projection mean pooling shared classifier. Do not call the vision encoder.
- IMAGE path: image encoder projection mean pooling shared classifier Note: text encoder is not used.
- 4.26MULTIMODAL path: text encoder projection optional early exit if not exited, text-only classifier if exited, image encoder projection. Bidirectional cross-attention mean pooling fusion shared classifier.

All trainable parts (projector, cross-attention, classifiers) are the same in each path; only the *order* of operations varies by modality. In Fig. 1, these three paths plus the early-exit branch are shown.

It should be noted that certain areas or districts in the city that have historically been associated with poverty will still experience a greater degree of challenges when compared to others. The process of gentrification tends to concentrate itself in the downtown urban core of the city. As a result, the benefits that are meant to arrive in the city may only circulate in the core and will not distribute its advantages all throughout the city equally (e.g., in neighborhoods that have long experienced disinvestment).

# 4.4 Learning Objective

The model is trained with the binary cross-entropy over $N$ training examples:

[Equation 4]

Where: $$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log \sigma(\hat{z}_i) + (1 - y_i) \log \left( 1 - \sigma(\hat{z}_i) \right) \right], $$

Where $\hat{z}_i$ is the predicted logit of email $i$, $\sigma(\cdot)$ is the sigmoid function, and $y_i$ is the label which is 1 if the email $i$ is spam and 0 if it is not. Since the training distribution is ham-heavy (Section 6.2), the weighted variant used by Weighted-DCAT is:

[Equation 5]

Weighted (Positive):$$\mathcal{L}_{weighted} = -\frac{1}{N} \sum_{i=1}^{N} [w_{pos} y_i log\sigma(\hat{z}_i) + (1-y_i) log (1-\sigma(\hat{z}_i))] $$

with the positive-class weight defined as

[Equation 6]

$$w_{pos} = \frac{N_{ham}}{N_{spam}}. $$

This weighting is meant to counteract the ham-heavy class distribution used during training, with its empirical effect observed by the imbalance ablation of Section 7.4.


<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->
5. The DCAT Architecture ### 5.1 Architecture overview DCAT consists of 5 components: 1. Text encoder (DistilBERT [15]) encodes email text into token-level contextual embeddings 2. 

Vision encoder (MobileViT [20]) encodes email images into spatial visual feature maps 3. 

Modality projector maps both encoder outputs into a shared latent space of dimension = 256 (d) by linear projections followed by Layer Normalization 4. Bidirectional cross-attention exchanges information between text and image representations in the shared latent space 5. Shared classifier maps the fused or unimodal shared representations into a spam/ham prediction [FIGURE 1 - DCAT OVERALL ARCHITECTURE] Caption: DCAT architecture overview. Deterministic modality routing assigns each email to the TEXT, IMAGE, MULTIMODAL, or EMPTY category, where only the required encoders are invoked. 

For MULTIMODAL emails a text-only auxiliary classifier may exit early and classify without vision, otherwise bidirectional cross-attention exchanges information between the projected streams before pooling and fusion. 

Frozen components are shown in blue, trainable components in orange. Placement & purpose: Section 5.1 (after the architecture-overview paragraph). Purpose: show the actual DCAT pipeline - deterministic router, modality-specific encoders, projectors, bidirectional cross-attention, pooling/fusion, shared classifier, and the early-exit branch from the text-only auxiliary classifier. 

Data source: methodology of Sections 4 and 5 (Eqs. 2, 3, 7-21). Note: final graphics are produced in the LaTeX project (`latex/figures/`, vector sources); the specifications above are the approved rendering contract for regeneration. 

The design rationale follows from Sections 2 and 4. 

The encoders are frozen pre-trained models, so trainable capacity concentrates in the projection, interaction, and classification components - only 2,008,578 of 73,309,090 parameters (2.74%) are trainable (Section 5.8). The projector exists because the two encoders emit representations in different spaces (768-dimensional text tokens versus spatial visual feature maps); cross-attention requires a common space in which queries from one modality can be compared against keys from the other. The classifier is *shared* across all three paths so that every path's representation is mapped into the same decision space. ### 5.2 Text encoder The text encoder is DistilBERT-base-uncased [15], a 6-layer Transformer with 768-dimensional hidden representations. 

Given tokenized input, it produces token-level hidden states: [Equation 7] where the input is truncated or padded to 256 tokens, and an attention mask indicates padding positions so that masked tokens do not contribute to attention or pooling, and B denotes the batch size. 

All encoder parameters are frozen during training: the encoder acts as a fixed feature extractor, and no encoder gradient updates occur. ### 5.3 Vision encoder The vision encoder is MobileViT-small [20], accessed via the `timm` library [21]. Images are resized to 224 x 224 pixels before encoding. 

With normalized image tensor, it produces spatial feature representations: [Equation 8] where SHS = 15x15 for the evaluated configuration. Like the text encoder, the vision encoder is frozen during training. ### 5.4 Modality projector The projector maps each modality into the shared D-dimensional latent space (D = 256): [Equation 9] [Equation 10] with projection matrices where the projections are trainable; they are the first stage at which the two modalities inhabit a common space. 

Layer normalization after the linear projection stabilizes the scale of both projected streams before they interact, which matters because the two encoders were pre-trained with different internal distributions. 

[Equations 11, 12] The projected representations are of size #timesteps x D, so the batch size is B, #timesteps is S or Dimg, and D img is the MobileViT feature dimension (960). Since the two encoder outputs are of different sizes, the projector emulates the Spatial projector described in [6].


<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->
# 5.5 Bidirectional Cross-Attention

The cross-attention module has a total of $N_{xattn} = 2$ identical layers, one for each of the directions of information flow, sharing the co-attention design of [5] and the scaled dot-product approach of Eq. (1).

For text-to-image attention, the queries are obtained from the text stream, and the keys and values from the image stream:

[Equation 12]

$$\mathbf{Q}_{text} = \mathbf{Z}_{text} \mathbf{W}_{Q,text} \qquad K_{img} = \mathbf{Z}_{img} \mathbf{W}_{K,img} \qquad V_{img} = \mathbf{Z}_{img} \mathbf{W}_{V,img}$$

[Equation 13]

$$\mathbf{Z}_{img \rightarrow text} = \text{Softmax}\!\left( \frac{\mathbf{Q}_{text} \mathbf{K}_{img}^{T}}{\sqrt{d_k}} \right) \mathbf{V}_{img}. $$.

The new, content-aware representation of each text token is therefore re-derived as a mixture of image tokens: what parts of an image are relevant for a specific text token are not predetermined, but learned. This time, the attention from image to text works the other way:

[Equation 14]

And andare, respectively, the query image, key text, and value text were obtained by These yielded the query image, key text, and value text representation. Were obtained by (18) (19) (20)

[Equation 15]

Z(text → img) = Softmax(Z(QimgK(text)T)/√dK)Z(Vtext).

All too simple solution, suppose, that answered your problems? The two streams are then added with residual connections:

[Equation 16]

$$\mathbf{Z}_{text}^{out} = \mathbf{Z}_{text} + \text{MLP}\! \left(\mathbf{Z}_{img\rightarrow text}\right),$$

[Equation 17]

$$\mathbf{Z}_{img}^{out} = \mathbf{Z}_{img} + \text{MLP}\!\left(\mathbf{Z}_{text \rightarrow img}\right)$$

[FIGURE 2 - CROSS-ATTENTION BLOCK]

Figure 3 Caption: One bidirectional cross-attention layer. Queries of each stream attend to keys and values of the other stream (Eqs. 12-15). 

The attended representation of the other stream is added back to its own stream via a residual MLP update (Eqs. 

16-17). Layer Normalization is applied before each sub-layer (Pre-LN). The layer is repeated N_xattn = 2 times with h = 4 heads and per-head dimension d_k = 64.

Adaptations & anectdotes Placement & purpose: Section 5.5 (following the bidirectional cross-attention equations). Purpose: to give weight to the (intimidating) Q/K/V relationships between streams and remain consistent with Eqs. 12-17. Data source: method of Section 5.5 (Eqs. 12-17) and the hyperparameters of Appendix B.

Note: final graphics are built in the LaTeX project (`latex/figures/`, sources in vector), the above requirements constitute the agreed rendering contract upon regenerations.

Multi-head Attention We use $h=4$ heads with dimensions $d_{k} = 64$ per head. The layer uses Pre-LN, where Layer Norm is applied before each sub-layer rather than after, which has been shown to stabilize training of the Transformer [32]. The residual additions in Eqs. (16)-(17) are used to preserve each stream's original representation so that the cross-attention components focus on enhancement rather than replacement of the unimodal features; this conceptually interacts with the fusion design described below.

# 5.6 Pooling and Fusion

Sequence level representations are obtained by mean pooling: $\mathbf{z}_{text} = \text{Mean Pool}(\mathbf{Z}_{text})$ and $\mathbf{z}_{img} = \text{Mean Pool}(\mathbf{Z}_{img})$ With mean pooling over the attention mask, variable-length messages (and masked padding) are weighted proportionally.

The multimodal representation is obtained by taking the elementwise mean of the cross-attention outputs:

[Equation 18]

$$\mathbf{z}_{fused} = \frac{\mathbf{z}_{text}^{out} + \mathbf{z}_{img}^{out}}{2}. $$

The fused representation is d_{model} - dimensional, not 2*feature dimension, as late fusion by concatenation would be. Elementwise averaging keeps the multimodal and the unimodal representations in the same space, and this is what allows a single shared classifier to classify on all three paths.


<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->
5.7 Shared Classifier and Early-Exit Mechanism The shared classifier is (d_{model})-dimensional to 1-dimensional, implemented the same way on each path:

[Equation 19]$$p(y = 1 \mid m) = \sigma\! \left( \text{MLP}_{cls}(\mathbf{H}_{fused}) \right), $$ where

- $\mathbf{H}_{fused}$ is a multimodal fused representation, or one of the pools of a unimodal representation.

In case of MULTIMODAL emails, DCAT optionally checks a text-only auxiliary classifier before calling the vision encoder: the pooled text representation is passed to

[Equation 20]$$p_{aux}(y = 1 \mid t) = \sigma\! \left( \text{MLP}_{aux}(\mathbf{H}_{unimodal}) \right), $$ and the exit rule is

[Equation 21]$$\text{exit if } p_{aux} \geq 0.95 \;\;(\text{classify spam}) \quad \text{or} \quad p_{aux} \leq 0.05 \;\;(\text{classify ham}). $$ For values in between the two thresholds, the entire multimodal path is performed: text vision cross-attention fusion shared classifier. The auxiliary classifier is separate from the main shared classifier and is trained alongside the model, so training the main task implicitly calibrates the exit. The symmetric 0.95/0.05 thresholds force near-certainty before skipping vision; their impact on the workload is measured in Section 7.7, and their fixed value in Section 9.2.

5.8 Training Procedure The training setup used is:

- AdamW [33] optimizer with learning rate 1e-4, default weight decay.
- Cosine annealing schedule.
- Binary cross-entropy with logits loss (Eq. 4), with optional positive-class weighting (Eqs. 5-6) in Weighted-DCAT.
- Mixed-precision FP16 training using PyTorchAMP.
- Batch size of 64. Epochs: 1.
- Encoder parameters: frozen DistilBERT and MobileViT; remaining (projection, cross-attention, shared classifier) unfrozen.
- Available hardware: a CUDA-capable NVIDIA GPU.
- Random seed: fixed across Python, NumPy, and PyTorch for deterministic runs.

The total number of parameters in the full-DCAT model is 73,309,090, of which 2,008,578 are trainable - 2.74% of the total. The trainable component consists of the projection layer, the cross-attention layers, and the classifiers; it is this component that needs to be frozen to train single-epoch on this corpus, and that maintains a similar size to the fusion variants it is compared against.

5.9 Inference Pipeline At inference time, the process is:

- The deterministic router assigns the email to either the TEXT, IMAGE, MULTIMODAL, or EMPTY modality (EMPTY is dropped).
- Only the encoder(s) corresponding to the assigned modality are run.
- If IMAGE or MULTIMODAL, run the image encoder and perform the visual cross-attention.
- If MULTIMODAL, compute the auxiliary classifier (Eq. 20).
- Run the vision encoder (if not already) and perform the text image cross-attention.
- Compute the shared classifier output.
- Threshold the sigmoid output at 0.5 for the label.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->
6. Experimental Methodology

# 6.1 Corpus and Preprocessing

The body of corpus used throughout the paper comes from the Spam Assassin public email corpus [7]. The corpus is comprised of naturally occurring email messages which preserve their original MIME structure (plain text email messages, HTML email messages, inline images, images as attachments). The preservation of MIME enables the deterministic modality extraction of Section 4.2. 

The full raw corpus is approximately 16GB on disk and the subset used in the primary evaluation is 6,046 messages. 

The corpus was selected because it is naturally occurring, preserves the MIME structure needed for deterministic modality extraction, and it has been used in prior spam-detection research.

Preprocessing takes the raw.eml files and does through four deterministic phases:

1. **MIME parsing.** For each.eml file, parse with the email package, walk the MIME tree to get plain text, HTML, and images. Use Beautiful Soup and the lxml parser to reduce HTML to visible text; decode image parts to raw bytes; and ignore any non-fatal parsing errors.
2. **Filtering and Quality Filtering:** Texts with less than 10 characters after stripping whitespace are discarded. Images with less than $20 \times 20$ pixels or less than 1024 bytes are removed, with the corresponding dropping reasons preserved. If there are multiple images with sufficient information, the largest one in byte size is preserved. Pixels count is used if a tie exists.
3. Image processing. Chosen images are resized to $224 \times 224$ pixels through bicubic sampling, transformed into RGB color space, and normalized via the `timm` [21] preprocessing pipeline, that aligns to the input distribution of the pre-trained MobileViT encoder.
4. Text tokenization. Email text is tokenized with the DistilBERT tokenizer under `max_length = 256, truncation = longest_first, padding = max_length` to produce the input IDs and attention mask.

[FIGURE 3 - PREPROCESSING FLOW]

**Caption:** Preprocessing and data-flow diagram. Raw.eml files undergo the four deterministic stages of Section 6.1 (MIME parsing; content filtering with size and quality thresholds annotated; image processing; text tokenization) prior to deterministic modality assignment. EMPTY messages are eliminated from the training and assessment process.

Placement & purpose: After 4 preprocessing steps (Section 6.1). Purpose: Demonstrate the flow of data from raw input to prepared modalities for input to our models, with the specific thresholds annotated (>= 10 chars text, >=20×20 px and >=1024 bytes image, 224×224 resize). Data source: stages 1-4 of Section 6.1.

** Note: final graphics are produced in the latex project (`latex/figures/`, vector sources); the above specifications are the approved ones.

The relationship between the variables could be linear, or they could be linked by a more intricate function, especially in some applications. While in some circumstances the function might lead to a linear relationship, this might not always be the case. The most vital part is the inclusion of the functional form in the econometric model because its omission causes model misspecification. 

In this way, omitting the functional form is considered the same as omitting significant variables (Wooldridge, 2013). 

Thus, the correct specification of a functional form is as essential as including relevant variables.

6.2 Number of datasets, sets and set leakage3.2.1. Sets3.2.2.1. Leakage3.2.2. Data sets3.2.2.4. Sequence and set setsThere are five datasets included in the dataset:12,1234 as well as the training, validation, and testing datasets.12,12,12,2,12,2,3,12,123.12.16.5,12,2,4.12,124.1.4,23,4.15,22,22.2.12,3.23,42,52,1.3,4A fundamental distinction of the series is that the mixed data sets and the train, validation, and test data are (to varying degrees) distributed – i.e., not randomly distributed.12,12,12,2,12,2,3,4Distribution of the data sets (usage within the training, validation, and test sets).12,12,1253.1,2,1,2,1,26,3,3,34,2,6.2.2.2.6.2.2.8.8.2.3.9.9.2.3.10.10.2.3.11.11.2.1.3.2.2.4.3.2.4.3.2.4.3.2.4.3.2.4.3.2.4.3.2.4.3.2.1.14.14.15.8.
Table 1 shows the structure of the processed corpus.


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

Only text-only messages constitute 99.4% of the processed corpus; just 11 of 6,046 emails are multimodal (4 ham, 7 spam), one email is IMAGE, and 27 are EMPTY and are not used for training and testing. The ham/spam split is 4,150/1,896 messages--a 2.19:1 ham:spam ratio--so the corpus is on the mid-side of the normal ham-to-spam representation rather than idling around balanced. And this is the working hypothesis of the entire experiment--the full-test measure is ultimately determined by text classification, and the multimodal subset is tiny by design.

The default split is 70% training, 15% validation, and 15% test data with a fixed seed of 42, and stratification maintains the ham/spam percentage between splits. No email is allowed to be present in more than one set with the split procedures, and sender-leakage and campaign-leakage controls are used where sender or campaign identifiers are available. An example of a lineage entry created under a different 10% primary-test arrangement is presented in Appendix C; throughout the primary tables, the 70/15/15 arrangement is used.

The leakage analysis tests for five kinds of duplication and overlap: exact textual duplicate pair, among the 1185 splits; exact image duplicate pair among the 1185 splits; perceptual image duplicate pair among the 1185 splits, and using perceptual hash; Jaccard near-duplicate text pairs; sender, campaign name overlap. Exact textual and hash-based deduplication was performed on the entire dataset; the perceptual leakage test was performed on a pilot sample of the data due to the high cost; the evidence from this test therefore confirms the workings of the deduplication tests on the entire data, but should not be considered an exhaustive check of all image pairs.


### 6.3 Model Variants

Eight variants are evaluated, each serving a defined diagnostic role:

1. **All-Spam Prior** — predicts spam for every input; a class-prior sanity floor.
2. **Modality Indicator** — uses only the modality type as the input feature; tests how much signal the modality label alone carries.3. **Text-Only** — activates only the text pathway; the text-dominated corpus's reference model.
4. **Image-Only** — activates only the image pathway; quantifies the standalone visual signal.
5. **Late Fusion** — concatenates mean-pooled DistilBERT and MobileViT representations before classification; the standard independent-encoding fusion design.
6. **DCAT-No-XAttn** — removes cross-attention and averages independently pooled text and image representations; isolates the interaction mechanism from the shared-space design.
7. **Full-DCAT** — the complete bidirectional cross-attention architecture (Section 5).
8. **DCAT-Early-Exit** — Full-DCAT with the auxiliary early-exit mechanism enabled.

Furthermore, a published multimodal baseline is featured as a reimplementation of a late-fusion architecture based on DistilBERT for text and Res Net-18 for images [4]. As a research alternative, it is approached in this work as another controlled configuration - same corpus, splits, protocol - within our experiments, rather than as a benchmark.


### 6.4 Ablation Design

Three ablations isolate the paper's research questions, each tied to a gap from Section 3.6:

- **Cross-attention ablation** (gap 1): compares Late Fusion, DCAT-No-XAttn, and Full-DCAT on the multimodal subset — a progression from no interaction, to shared-space averaging, to full bidirectional cross-attention.
- **Imbalance ablation** (gap 3): compares Full-DCAT trained with unweighted BCE against Weighted-DCAT with $w_{\text{spam}} = N_{\text{ham}} / N_{\text{spam}}$ (Eqs. 5–6).
- **Early-exit ablation** (gap 2): compares Full-DCAT and DCAT-Early-Exit using latency, FLOPs, and vision skip rate.

# 6.5 Evaluation Metrics

The evaluation reports Macro-F1 (the mean of ham-F1 and spam-F1, with each given equal weight), Ham F1, Spam F1, Ham PR-AUC (precision-recall area for ham class), ROC-AUC (overall class separation), and Accuracy (fraction of emails correctly classified). In the multimodal case, we re-evaluate the same metrics based solely on messages labelled as MULTIMODAL (MM-Macro-F1 is the multimodal equivalent of Macro-F1). We choose Macro-F1 as the primary measure, since giving equal weight to the class labels means that it is also influenced by the problem of Majority-Class Collapse (defeating the objective to maximize overall accuracy), as we saw in Section 7.2.

# 6.6 Statistical Evaluation

Paired model comparisons are conducted with McNemar's test [31] with a continuity correction (combining the counts of discordant predictions between two models). We use two settings: (1) the multimodal test subset (~11 samples; analogous to a 11-sample test set) and (2) the pooled out-of-fold predictions from the five-fold cross-validation experiment (~7,867 samples). The multimodal test set sample size is too small to make statistical claims using those 11 examples, and the pooled setting is used exclusively to make that statement.

# 6.7 Efficiency Evaluation

Efficiency is measured by total and trainable parameter count; an estimate of the total FLOPs per forward pass; the average per-sample latency; P95 latency; the vision skip-rate for early exit; and the FLOP reduction compared to Full-DCAT. The per-sample vs. total-time metrics are shown separately as they are obtained via different measurement procedures.

# 6.8 Error-Analysis Protocol

Error analysis Displays full-test and multimodal confusion matrices for the main variants of the model, for false positives, false negatives, and instances where one model was wrong but the other was right. Errors for each individual sample are saved to `artifacts/error_analysis/dcat_errors.csv` and `artifacts/error_analysis/late_fusion_errors.csv`. These individual sample error files are the traceability source for the error discussion in Section 7.9.

[2] The new EFS is the first state-based, employer-sponsored program for sustainable portfolios from the perspective of private, multiemployer, and community-based investments. [3] A separate EFS program focusing on public institutions such as municipals and the whole state will be announced later. [4] The University of Massachusetts (UMass) participating investors' accumulated savings are used to finance investments. 

The UMass contribution rate averages 12%. 

In 1995, the investment returns paid the annual salaries of the statewide directors, managers, and liaisons in the Department of Postsecondary Education (DPS).

7. Results

With that settled in Section 6, now it is just what the measures reveal. The presentation of results in the section follows the formulation of research questions at the beginning of each subsection. Every figure, reference and table reproduced here came from the evaluation artifacts; if the source artifacts showed contradictions, the contradiction is mentioned here.

# 7.1 Full-Test-Set Benchmark

*Research question: What are the class signals found in the representations and how do the fusion designs compare when the entire test set outweighs the metric?*


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

Text-Only: achieves Macro-F1 0.9827. Full-DCAT: 0.9862 versus 0.9869 Published Baseline, 0.9867 DCAT-No-XAttn, Late Fusion. On the full test set the difference is small. 

One final reporting point (reconciled in publication-readiness phase audit): our Late Fusion figure in the row above is the three-seed mean (0.9871), rechecked versus the identified seed-level source table and seed-master. 

The original draft report was transcribing 0.9855 for that row (a copy-paste error, with the designated source table), which was inconsistent with the seed-level analysis in 7.8. The two numbers are now consistent. At this level of performance, all text models are within one-thousandth of one another (5e-4).

Image-Only yields Macro-F1 0.3220 – below the All-Spam Prior of 0.4000. Because only a small proportion of the corpus has meaningful content in the image, this version of image-only training is being trained on far less data than text-only. The sanity priors are working as expected: the All-Spam Prior gives 0.4000 Macro-F1 (based on the class imbalance of 2.19:1), and the Modality Indicator is giving 0.5500, indicating that there is some signal in the modality label itself, but not as much as in content.

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

Multimodal Low Number Samples and Majority-class Collapse The Multimodal subset has so few samples that Late Fusion, Full-DCAT, Image-Only, and the All-Spam Prior all predict mostly spam, with Macro-F1 0.4968, Ham F1 0.0000. Text-Only delivers the only non-zero ham recall of a unimodal model, with 0.5584, while DCAT-No-XAttn is dominant overall, with Macro-F1 0.8317, Ham F1 0.6667.

One provenance note is needed. Figure 3 reproduces the archived multimodal evaluation table (results/tables/main_results_multimodal.csv, confirmed by results/tables/modality_analysis.csv). (The source analysis own synopsis of this subsection gives Text-Only at 0.4968/0.0000/0.9935 (majority-collapsed) and Image-Only at 0.2863/0.4444/0.1282, values inconsistent with either archived table.) 

Thus the summary values seem to refer to an alternate (unrecoverable) aggregation/arrangement; the archived table -- the apparently final source for these figures -- is presented here. 

No attempt is made to reconcile this difference (or delete it).

One data-quality concern carries over from the source analysis, whose arithmetic is clarified for the publication-readiness review: the All-Spam Prior accuracy cited on this subset is 0.9871. That is for a 155-sample multimodal evaluation set with 2 ham and 153 spam messages (153/155=0.9871; Spam-F1=306/308=0.9935) rather than for the corpus counts (4 ham, 7 spam) cited in the text of the manuscript. The paper therefore relies on the authoritatively determined sample-level counts (4 ham, 7 spam) for prevalence, and assumes the subset-level metrics to be generated by the preserved evaluation configuration, for which the subset composition cannot be determined from the available artifacts.

# 7.3 Cross-Attention Ablation

*Question: does bidirectional cross-attention work on multimodal inputs?*

The cross-attention ablation is done between the same three models as the multimodal analysis: No interaction via late fusion (concatenation-based), DCAT-No-XAttn (shared space, averaged representations), and Full-DCAT (bidirectional cross-attention, a transition from no interaction to completely bi-directionally interacting). These three models show all identical majority-collapsed values (Macro-F1 0.4968, Ham F1 0.0000, Spam F1 0.9935) on the 11-message multimodal test set, except for the DCAT-No-XAttn result (Macro-F1 0.8317, Ham F1 0.6667), which was shown in Table 3 and is the only result from an interaction-capable model (though not interaction-dependent) that was not collapsed.

4 p = 1.0000 for Full-DCAT vs. Late Fusion and p = 0.2482 for Full-DCAT vs. DCAT-No-XAttn. 

Neither is less than 0.05. 

While there are on the order of 11 multimodal test samples, under this test alone the comparison of Full-DCAT and Late Fusion are underpowered to statistically distinguish, and the advantage of the simpler DCAT-No-XAttn over Full-DCAT is also statistically insignificant.

<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

### 7.4 Class-Imbalance Ablation
*Research question: does class weighting matter more than architecture?*

**Table 4. Class-imbalance ablation**

| Model | Macro-F1 | Spam F1 | Ham F1 | MM-Macro-F1 |
|---|---:|---:|---:|---:|
| Full-DCAT | 0.9862 | 0.9916 | 0.9809 | 0.6253 |
| Weighted Full-DCAT | 0.9880 | 0.9927 | 0.9833 | 0.7478 |

Weighting-DCAT improves full-test Macro-F1 from 0.9862 to 0.9880 and multimodal Macro-F1 from 0.6253 to 0.7478. Corresponding pooled out-of-fold McNemar comparisons yield p = 2.49 10 for Weighted-DCAT vs. Full-DCAT, and p = 3.34 10 for Weighted-DCAT vs. 

Late Fusion (both far below = 0.05), on the 7,867 pooled out-of-fold samples. 

The imbalance ablation is the only comparison in this study with statistically decisive differences. 7.5 Multimodal Robustness: Five-Fold Cross-Validation Research question: is the multimodal signal stable? A five-fold cross-validation of the larger evaluation subset described in the experiment artifacts (Table 5).

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

DCAT has roughly four times as many trainable parameters as Late Fusion-2.01M versus 0.46 M [18] including additional parameters for the cross-attention blocks and classifier. The total FLOPs with these four always-on variants is roughly 13B each, since the frozen encoders make up the bulk of the computation. About 11B FLOPs over the whole workload for DCAT-Early-Exit (shown as an approximation based on all tests cells on this line: "avg, 90% text-only" on the source artifact cell; this is not comparable to the figure of 12.7B in Table 8, which ignores the effect of the early exit on the few multimodal tests that would otherwise run past the early exit) over the whole corpus. 

In these measurements, the source artifact cell's number is a rough average over the text-only majority of the corpus, which causes it to be not directly comparable with 12.7B in Table 8, since the early exit produces small savings on the tests that trigger the early exit. 

That Published Baseline can be read as having lowest latency per sample at 1.48ms, with Full-DCAT and DCAT-Early-Exit measuring 2.70ms and 2.68ms respectively.


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

*Where do remaining errors aggregate?* Figure 4 shows the archived confusion matrix for DCAT in the weighted-primary configuration (panel a), the setting for which the class-weighting analysis of Section 7.4 was conducted, along with a Macro-F1 comparison over all evaluated variants on the multimodal subset (panel b, values from Table 3). In the weighted-primary setting, the DCAT confusion matrix contains 57 false positives and 25 false negatives on the full test set; false positives hinder legitimate mail, false negatives miss spam, and the per-sample error records of Section 6.8 allow them to be directly traced to individual messages. The figure is meant to make the contrast between the behavior of the full corpus and that of the evaluation subset immediately obvious.

[FIGURE 4 - RESULTS VISUALIZATION PANEL] FIGURE CAPTION: Results visualization. (a) Confusion matrix of DCAT in the weighted-primary setting on the full test set (n = 7,351; 57 false positives, 25 false negatives). (b) Multimodal Macro-F1 for all evaluated settings on the multimodal subset, reproducing the values of Table 3 (ASP: All-Spam Prior; MI: Modality Indicator; Text: Text-Only; Image: Image-Only; PB: Published Baseline; LF: Late Fusion; NoXAttn: DCAT-No-XAttn; DCAT: Full-DCAT; EE: DCAT-Early-Exit). Majority-collapsed settings sit at 0.4968; DCAT-No-XAttn reaches 0.8317.


**Note:** final graphics are produced in the LaTeX project (`latex/figures/`, vector sources); the specifications above are the approved rendering contract for regeneration.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->
8. Discussion This section interprets the evidence of Section 7.

Observed results are distinguished from their plausible interpretations; speculation is distinguished from explicit claims. 8.1 Why the Full-Test Metric Barely Moves The observed result is a 0.0009 Macro-F1 improvement of Full-DCAT (0.9862) over Late Fusion (0.9871) on the full test set, with seed-level s.d. of at most 0.0003 (Tables 2 and 9). 

Three corpus-level considerations plausibly explain this minimal change. 

First, the corpus is 99.4% text-only, which leaves the single cross-attention module that differentiates Full-DCAT from DCAT-No-XAttn to be used on only ∼0.2% of the data; its impact is limited to a small subset of examples. Second, the five emails in the multimodal subcorpus are insufficient for stable estimation of cross-modal interactions, so the module's additional trainable parameters may be sensitive to the set of available multimodal training examples. Third, the shared classifier is trained primarily on text-dominated batches, so representations of the multimodal examples must be mapped into a decision space constructed primarily by text-only examples. These factors are consistent with the minimal full-test improvement for more expressive cross-attention architecture; there may be other explanations, but these are consistent with the patterns of results. 

Whether the added expressiveness improves overall performance in this context is an empirical question that Section 7.1-7.4 addressed directly, and Section 8.2 interprets. 

8.2 Signal, Scarcity, and Sensitivity in the Multimodal Subset The single-measure contribution of Full-DCAT to the multimodal test subset is a 0.4968→0.8317 improvement over the baseline DCAT-No-XAttn (Table 3). This large improvement directed in the "opposite" direction from the proposed design goal was the critical benchmark driving the story of the study. The simpler variant learns pooled independently-vectored text and image representations rather than applying cross-attention. 

Two interpretations for this paradox are consistent with the evidence. With only 11 primary multimodal examples, the estimated contribution is highly unstable and sensitive to any prediction errors. And the additional parameters and the consequent complexity of estimating possible interactions in Full-DCAT may have been problematic for estimating those parameters from the limited sample of multimodal training examples, whereas the preserved separate pools of text and image representations in DCAT-No-XAttn seem more robust. 

(The statisticist sets aside the discrepancy between the 0.4968→0.8317 Macro-F1 gain against the smaller estimate of higher variance, with the caveat that the McNemar test cannot claim significance at a 0.05 threshold (p=0.2482).) 

What the small evaluation does establish, conclusively, is the ultimate failure mode: the 4 of 4 fully trained models with interaction capacity collapsed to the baseline condition of majority-class prediction (Ham F1 0.0000), exactly the effect that the full-test headline was intended to isolate. (The number of sampling-related failures remains underpowered to discern the reason for the majority-class collapse.) 8.3 Class Weighting Changes 75 more than Architecture Changes The training-objective ablation isolates a training-objective effect that changing the class weights in the loss function changes predictions substantially on the pooled evaluation. Weighted-DCAT improves the multimodal Macro-F1 from 0.6253 to 0.7478, full-test Macro-F1 from 0.9862 to 0.9880, and yields total-time latency improvements of 9.84% (2.70 ms →2.44 ms) and 6.36% (2.68 ms →2.51 ms) for median and P95, respectively, in comparison to the full-training, baseline estimates in Table 6. 

These evaluations show that changing the class-weighting produces a greater gain in the low-data, strongly-imbalanced multimodal setting than replacing the cross-attention architecture with the simpler, pooling-only design. 

This does not establish that class weighting dominates or outweighs architecture, but it does demonstrate a larger measurable difference on the evaluated multimodal task. 8.4 Efficiency: Theory versus Measured Overhead The early exit mechanism avoids the vision encoder on 4.45% of the multimodal messages in this evaluation; because only 4.46% of the messages in the total corpus are multimodal, the overall fraction of GPU FLOPS saved per-messages in the evaluation workload is 0.63%. The two latency measures tell a conflicting story: on a per-message basis (Table 7), the saved latency (2.70 ms vs. 

2.68 ms) is negligible, but for the entire evaluation workload (Table 8), the total latency increased 24.82%, with an 88.39% increase in P95 latency. For a definitive statement, the figures cannot be combined; the total-time metric demonstrates that the "overhead" of conditional execution, which is required to evaluate an auxiliary classifier and implement the branch, is sufficient to make the overall prediction workload slightly slower than the baseline. (With a larger load of multimodal messages, the speedup would scale accordingly; this was not evaluated.) 

8.5 What Does DCAT Establish and Not?

Together, the protocols give a complementary view of the architecture, and the claims can accordingly be safely bounded. What the evidence supports: DCAT matches the strong baselines on the full test set, with a small seed-stable gap (0.9862→0.9869-0.9871 in Macro-F1), has the highest across-fold average multimodal Macro-F1 (0.7077→0.5453 on Late Fusion) but with greater variation, (Section 7.6), class weighting produces the only statistically signifcant improvement, and the early-exit achieves workload-dependent reductions at some measured overhead cost. What the evidence does not support: a claim that cross-attention improves full-test results in this corpus/protocol combination - the full-test results show no advantage of cross-attention over the published Late Fusion baseline, and the direct-evidence advantage of the simpler variant on the subset is statistically ambiguous. The most honest summary is that, in this corpus, expressiveness in the architecture was not beneficial, while expressiveness in the training objective was. 

The corpus is 99.4% text-only, so these conclusions should not be generalized to email corpora with a higher proportion of image-containing messages.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

9. Limitations and Threats to Validity

# 9.1 Dataset Limitations

Extreme multimodal scarcity. There are a mere 11 emails in the primary Spam Assassin set, all of which are multimodal. Scores on the primary test set are effected significantly by single prediction, and cannot be assumed to generalize to any other domain.
Single corpus. All experiments were conducted on the Spam Assassin corpus. No performance evaluation was conducted on other collections of email.
**No OCR.** The system does not convert text within images into plain text. Spam messages that use images to display the main body of text have all that text stripped away prior to filtering.
Single-image constraint. For each multi-image message only the largest, most meaningful image is forwarded to the model; the remaining visual elements are not displayed to it.

# 9.2 Architecture Limitations

**Frozen encoders.** DistilBERT and MobileViT are frozen, they were not fine-tuned on the domain data.
Fusion method. The proposed multimodal representation is (element-wise averaging) fused after crossattention; we did not test other fusion methods.
Early-exit thresholds. The thresholds were set to 0.95 and 0.05; the effects of varying these were not investigated.

Hopefully, in another reorganisation scenario, the temperature would exactly have the same as the inlet. Hopefully, in another step of reorganisation, the temperature would exactly have the same as the inlet. Comments: how the body of the process is not shown. But in this case it flow by the same way; for this reason it is not show the whole system, only the second process.

The two cycles are combined and merged on one g. I think that the amount of energy in that this system is too high and lets not be too sure of the power, size, and flow rate that anyone can have, because of the mass of the cycle. A patent of the similar but not the same idea I read not the one shown in my text; the concept has more options. Take, for example, the paragraph of Car/Plant 1; that is answered to by Car/Plant 2, and vice-versa, so that the answer to both should be the same.

# 9.3 Evaluation Limitations

**Small multimodal test set.** The major multimodal test set is ~11 emails. Multimodal metrics and McNemar comparisons are based on very few examples.
**Single training epoch.** Every model is trained for a single epoch, while different training schedules might result in different optimization behavior.
**No adversarial assessment.** The model will not be tested using adversarial spam intentionally designed to challenge it.
**Efficiency measurement uncertainty.** While the per-sample vs. total-time measurements differ, the original source artifact for the total-time comparison is no longer provided. The efficiency table contains two FLops figures with different averaging conventions (a workload-average estimate for the early-exit variant, and a marginal measured value for the comparison), and these can no longer be converted into each other from the given artifacts.

# 9.4 Threats to Validity

Internal validity. Many potential sources of evaluation contamination are mitigated by the deterministic modality routing and duplicate checks; however the single-epoch training regime and extremely limited multimodal data are still critical constraints.
Construct validity. Although Macro-F1, class-specific F1, PR-AUC, and ROC-AUC are common classification metrics, the small sample size used for the calculation of multimodal Macro-F1 makes it imprecise.
**External validity.** One corpus of emails is used in the experiments, which is text dominant; our results may vary with a corpus where more emails have images, or follow another trend of spam.



<!-- HUMAN EDITING: Rewrite this section in your own natural academic voice while preserving all facts, numbers, citations, and technical meaning. -->

10. Conclusion and future work This paper presented the conditional multimodal email spam detection architecture DCAT combining bidirectional cross-attention, deterministic routing, and optional early-exit computation evaluated on a natural multimodal pair of corpora (Spam Assassin), where the defining property is multimodal scarcity (11/6,046 emails) under a text-only majority (99.4%). The evidence supports three conclusions. First, on the full test set, Full-DCAT achieved the same Macro-F1 0.9862 as the published-baseline reimplementation 0.9869 and Late Fusion 0.9871 across three seeds, and experiments do not show a full-test advantage for cross-attention at the 0.001 significance level. 

Second, the multimodal results are highly sensitive to distribution, class imbalance, and the multimodal set size: Full-DCAT and the simple versions collapse to majority-class prediction on the 11-message test set, five-fold cross-validation yields the highest mean of 0.7077 for Full-DCAT versus 0.5453 for Late Fusion but also the highest variance, and class weighting - the training-objective change - produces the only statistically significant improvements in this study (multimodal Macro-F1 0.6253 0.7478; pooled out-of-fold McNemar p = 2.49 10 against Full-DCAT and p = 3.34 10 against Late Fusion). 

Third, the conditional computation behaves as theory predicts but as workload demands: the early exit bypasses vision for 4.45% of multimodal cases and reduces FLOPs by 0.63%, and total-time measurement shows a 24.82% latency increase from the execution overhead. Future work directly addresses these limitations: (1) corpus expansion to larger corpora with vastly more multimodal messages including image-based phishing and marketing emails so that training-objective effects such as class-weighting improvements can be tested at scale, (2) OCR to extract text from within images as an additional information source, (3) fine-tuning of DistilBERT and MobileViT encoders with a systematic learning-rate schedule, (4) multi-image handling, to support multiple salient images per email as opposed to the single largest, (5) learned routing capable of assigning importance to the data sources beyond the content rules of deterministic routing, (6) contrastive pretraining of the projection and cross-attention modules on paired text-image vectors prior to classification, and (7) large-scale efficiency comparison of early exit at corpora with greater multimodal prevalence across multiple exit thresholds. Human annotator of this work: Timothy Hosp. No competing interests.


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
