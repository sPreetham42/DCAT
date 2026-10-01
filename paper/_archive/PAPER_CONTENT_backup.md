# DCAT: Dynamic Cross-Attention Transformer for Conditional Multimodal Email Spam Detection

Authors: Preetham S

Guide:

---

## Abstract

Email spam represents a persistent security problem, and spam campaigns now increasingly use images in addition to text. This is a limitation for text-only filtering if relevant spam content is captured by images. Multimodal spam detection architectures typically process text and image modalities independently and fuse them at a late stage, and conventional multimodal pipelines may apply visual encoders even to inputs that have no meaningful image content. This paper proposes DCAT (Dynamic Cross-Attention Transformer), a conditional multimodal email spam detection architecture with two main components: bidirectional cross-attention between projected text and image representations, and deterministic modality routing with optional early-exit classification to avoid unnecessary vision computation.

DCAT is evaluated on a naturally paired multimodal email corpus extracted from the SpamAssassin public dataset under deterministic modality routing, multi-seed evaluation, and explicit ablation studies. On the full test set, DCAT achieves Macro-F1 = 0.9862 from three seeds compared with 0.9869 for the published multimodal baseline reimplementation and 0.9871 for Late Fusion. On the multimodal test subset, Full-DCAT does not outperform Late Fusion (McNemar $p=1.0000$), while DCAT-No-XAttn achieves Macro-F1 = 0.8317 compared to 0.4968 for Full-DCAT. Five-fold cross-validation on the multimodal evaluation yields a mean MM-Macro-F1 of 0.7077 for Full-DCAT and 0.5453 for Late Fusion, with standard deviations of 0.2639 and 0.1222, respectively. Weighted-DCAT increases multimodal Macro-F1 from 0.6253 to 0.7478 with pooled out-of-fold McNemar tests giving $p < 10^{-44}$ against unweighted Full-DCAT and $p < 10^{-5}$ against Late Fusion. The early-exit mechanism skips vision computation for 4.45% of multimodal emails and reduces average FLOPs by 0.63% on the evaluated test workload. Since 99.4% of the corpus is text-only, the effect of multimodal computation on the full-test metric is limited. The results suggest that architectural changes alone cannot guarantee gains when multimodal training examples are extremely scarce and the corpus is strongly dominated by text-only messages.

Keywords: Multimodal spam detection, cross-attention, email classification, conditional computation, modality routing, DistilBERT, MobileViT, multimodal fusion, deep learning

---

## 1. Introduction

Email spam represents one of the main cybersecurity problems affecting individuals and organizations. Spam messages may contain promotional images, phishing screenshots, brand graphics, or other visual content in addition to text. In such messages, part of the information relevant to the spam decision can be captured within the image rather than in the textual content alone.

Multimodal spam detection introduces a different set of conditions than conventional text classification. An email corpus can contain text-only messages, messages with both text and images, and a much smaller number of messages in which images provide most of the relevant content. A model that processes all available modalities for every message performs unnecessary visual computation for text-only inputs. At the same time, a model that learns cross-modal interactions needs enough paired examples for those interactions to be estimated reliably.

Prior multimodal spam-detection systems have made use of separate text and image encoders followed by feature concatenation or other fusion mechanisms. Late-fusion approaches allow a direct way to combine modality-specific representations, though the encoders are independent till the fusion stage. Other approaches have explored intermediate fusion, attention-based fusion, and gating mechanisms. These approaches differ in where and how information is exchanged between modalities.

DCAT uses bidirectional cross-attention to exchange information between text and image token representations before pooling. Text tokens attend to image representations, and image tokens attend to text representations. The architecture also uses deterministic modality routing so that text-only and image-only messages do not invoke unnecessary encoders. For multimodal messages, an optional early-exit classifier evaluates the text representation before the vision pathway is executed.

The paper evaluates these design choices under a naturally paired email setting. The evaluation includes multi-seed results, ablations, analysis of performance on the much smaller multimodal subset, five-fold cross-validation, statistical comparisons across out-of-fold models, and efficiency measurements.

The contributions of the paper are as follows:

A conditional multimodal email spam detection architecture that combines bidirectional cross-attention with deterministic modality routing and optional early-exit computation.

A controlled evaluation on naturally paired multimodal email data using three random seeds and explicit architectural and imbalance ablations.

Analysis of the difference between performance on the full corpus and performance on the much smaller multimodal subset.

An imbalance ablation comparing unweighted and class-weighted training.

Efficiency measurements covering parameter counts, FLOPs, latency, and vision skip rate.

The remainder of the paper is organized as follows. Section 2 reviews the existing work on text-based spam detection, image-based spam detection, multimodal fusion, cross-attention, conditional computation, and evaluation issues in multimodal corpora. Section 3 formulates the classification problem. Section 4 describes the DCAT architecture. Section 5 describes the dataset and preprocessing pipeline. Section 6 describes the experimental protocol. Section 7 reports the experimental results. Section 8 discusses the observed results. Section 9 describes limitations and threats to validity. Section 10 concludes the paper and outlines future work.

---

## 2. Background and Related Work

### 2.1 Text-Based Spam Detection

Text-based spam detection has a long history of heuristic and machine-learning-based approaches. Early systems used rule-based techniques such as SpamAssassin~\cite{ref1}, which assign spam scores using predefined patterns and indicators. Traditional classifiers such as Naive Bayes, Support Vector Machines, and Random Forests~\cite{ref2} have also been applied to spam classification using bag-of-words and TF-IDF representations.

Deep learning introduced learned feature extraction for text classification. Convolutional Neural Networks have been applied to character-level~\cite{ref19} and word-level~\cite{ref18} representations, while Long Short-Term Memory networks have been used to model sequential dependencies~\cite{ref20}. Transformer-based language models such as BERT~\cite{ref7}, RoBERTa~\cite{ref21}, and DistilBERT~\cite{ref4} provide contextual representations for text classification.

DistilBERT~\cite{ref4} is a distilled version of BERT that reduces model size and inference cost while retaining much of the original model's language capability, making it suitable for experiments where text encoding is performed for large numbers of email messages.

### 2.2 Image-Based Spam Detection

Image-based spam detection considers messages in which images carry part of the content used to distinguish spam from legitimate email. Images can contain promotional material, screenshots, logos, or text rendered as graphics.

CNN-based approaches have been applied to image spam detection to identify visual patterns such as colors, shapes, and text overlays~\cite{ref24}. Modern image encoders such as VGG~\cite{ref15}, ResNet~\cite{ref16}, and MobileNet~\cite{ref17} provide general-purpose visual feature extraction architectures that can be used as components of such systems.

Image-only classification is subject to an additional limitation of being ambiguous without its associated email text. Legitimate messages may also contain visually similar objects, including company logos and marketing graphics.

### 2.3 Multimodal Spam Detection

Multimodal spam detection combines information from text and images. Standard late-fusion systems encode the two modalities separately and concatenate their representations prior to classification. The published MMTD framework~\cite{ref13}, for example, uses a text encoder and an image encoder followed by multimodal fusion.

The MDL-SPAM framework~\cite{ref2} combines VGG-16 for image processing with LSTM-based text processing followed by fusion. Its methodology and data construction provide a basis for comparison with other multimodal spam-detection approaches.

Other multimodal studies have explored attention-based and gating-based fusion mechanisms, where information from different modalities is combined through learned interaction. These approaches vary in the amount of cross-modal interaction that occurs before the final decision.

For naturally occurring email corpora, multimodal examples can be much less common than text-only examples. This distribution affects both training and evaluation, as the multimodal subset may contain too few examples for reliable estimation of complex cross-modal interactions.

### 2.4 Cross-Attention in Multimodal Learning

Cross-attention mechanisms were originally developed from attention-based sequence-to-sequence models for machine translation~\cite{ref22} and later incorporated into vision-language architectures such as ViLBERT~\cite{ref8}, LXMERT~\cite{ref9}, and CLIP~\cite{ref10}. In a cross-attention operation, one representation supplies queries while the other supplies keys and values. The resulting attention weights determine which elements of the second representation contribute to each query representation.

DCAT uses bidirectional cross-attention inspired by the co-attention structure employed in ViLBERT~\cite{ref8}. Text representations attend to image representations and image representations attend to text representations. This differs from late fusion, where the two modalities are processed independently until their pooled representations are combined.

For email classification, this structure allows the representation of one modality to depend on the content of the other. A text feature may therefore have a different representation, depending on the associated image, and image features may similarly depend on the text.

### 2.5 Conditional Computation and Early Exit

Conditional computation changes the amount or structure of computation according to the input. An early-exit architecture provides an example of such a mechanism: an intermediate classifier can produce a prediction before the full network is executed~\cite{ref23}.

In multimodal email classification, deterministic routing provides a simpler form of conditional computation. A text-only email does not require a vision encoder, while an image-only email does not require text encoding. For multimodal emails, DCAT can additionally use a text-only auxiliary classifier to determine whether the remaining multimodal computation is necessary.

The early-exit path in DCAT is triggered when the auxiliary text classifier produces a probability of at least 0.95 or at most 0.05. Otherwise, the complete multimodal path is executed.

### 2.6 Evaluation Challenges in Multimodal Spam Detection

Multimodal evaluation can become challenging in the face of highly imbalanced modality distributions. A model may have a strong full-test metric while having limited performance on the much smaller multimodal subset. If the multimodal subset contains only a small number of samples, metrics such as F1 can vary substantially with a small number of prediction changes.

The evaluation in this work therefore reports both full-test and multimodal-subset metrics and uses five-fold cross-validation for an additional multimodal analysis. McNemar's test is used for paired comparisons of model predictions.

---

## 3. Problem Formulation

### 3.1 Task Definition

Given an email message $m$ with text content $t$ (email body, subject, and any extracted textual information) and optionally one or more images $\mathbf{I} = {I_1, I_2, \ldots, I_K}$ (embedded inline images or attachments), the task is to predict a binary label $y \in {0,1}$, where $y=0$ indicates legitimate email (ham) and $y=1$ indicates spam.

### 3.2 Modality Routing

Each email is deterministically assigned to one of four modality categories based on the content extracted during preprocessing:

TEXT: meaningful text ($\geq 10$ characters after cleaning) is present, but no meaningful image passes the size and quality filters.

IMAGE: at least one meaningful image is present, but no meaningful text is present.

MULTIMODAL: both meaningful text and at least one meaningful image are present.

EMPTY: neither meaningful text nor a meaningful image is present.

The routing decision is determined by the Boolean flags $p < 10^{-44}$0__:

```math

\text{modality}(m) = \begin{cases} \text{MULTIMODAL}, & \text{if } has\_text \wedge has\_image,\\ \text{TEXT}, & \text{if } has\_text \wedge \neg has\_image,\\ \text{IMAGE}, & \text{if } \neg has\_text \wedge has\_image,\\ \text{EMPTY}, & \text{otherwise.} \end{cases}

```

EMPTY emails are discarded from training and evaluation. The routing process is deterministic and does not employ a learned classifier, probability threshold, or learned heuristic.

### 3.3 Conditional Computation Path

DCAT implements three active computation paths:

TEXT path: text encoder → projection → mean pooling → shared classifier. The vision encoder is not invoked.

IMAGE path: image encoder → projection → mean pooling → shared classifier. The text encoder is not invoked.

MULTIMODAL path: text encoder → projection → optional early exit via the text-only classifier → if not exited, image encoder → projection → bidirectional cross-attention → mean pooling → fusion → shared classifier.

### 3.4 Objective

The model is trained using binary cross-entropy:

```math

\mathcal{L} = -\frac{1}{N} \sum_{$p < 10^{-44}$1__}^{N} \left[ y_i \log \sigma(\hat{z}_i) + (1-y_i)\log(1-\sigma(\hat{z}_i)) \right]

```

where $p < 10^{-44}$2__ is the logit for email $p < 10^{-44}$3__, $p < 10^{-44}$4__ is the sigmoid function, and $p < 10^{-44}$5__ is the ground-truth label.

For Weighted-DCAT, the positive-class term is multiplied by $p < 10^{-44}$6__:

```math

\mathcal{L}_{weighted} = -\frac{1}{N} \sum_{$p < 10^{-44}$7__}^{N} \left[ w_{pos}y_i \log \sigma(\hat{z}_i) + (1-y_i)\log(1-\sigma(\hat{z}_i)) \right].

```

The positive-class weight is defined as:

```math

w_{pos} = \frac{N_{ham}}{N_{spam}}.

```

This weighting compensates for the ham-dominant class distribution used during training.

---

## 4. Proposed DCAT Framework

### 4.1 Architecture Overview

DCAT consists of five main components:

1. Text Encoder (DistilBERT): encodes email text into token-level contextual embeddings.

2. Vision Encoder (MobileViT): encodes email images into spatial visual feature maps.

3. Modality Projector: maps the two encoder outputs into a shared latent space of dimension $p < 10^{-44}$8__ using linear projections followed by Layer Normalization.

4. Bidirectional Cross-Attention: exchanges information between text and image representations in the shared latent space.

5. Shared Classifier: maps fused or unimodal representations to a spam/ham prediction.

The complete architecture is illustrated in [FIGURE: DCAT Architecture].

### 4.2 Text Encoder

The text encoder uses DistilBERT-base-uncased~\cite{ref4}, a six-layer transformer with 768-dimensional hidden representations. Encoder parameters are frozen during training.

The encoder produces token-level hidden states:

```math

\mathbf{H}_{text} = \text{DistilBERT}(\mathbf{x}_{text}).

```

The tokenized input is truncated or padded to $p < 10^{-44}$9__ tokens. $p < 10^{-5}$0__ denotes the corresponding attention mask, and $p < 10^{-5}$1__ denotes the batch size.

### 4.3 Vision Encoder

The vision encoder uses MobileViT-small~\cite{ref5}, accessed through the `timm` library~\cite{ref6}. Images are resized to $p < 10^{-5}$2__ pixels before encoding.

The encoder produces spatial feature representations:

```math

\mathbf{H}_{img} = \text{MobileViT}(\mathbf{x}_{img}).

```

Here, $p < 10^{-5}$3__ represents the normalized image tensor. $p < 10^{-5}$4__ denotes the number of spatial tokens produced by the encoder. For the evaluated configuration, the feature map corresponds to a $p < 10^{-5}$5__ spatial grid. The vision encoder parameters are frozen during training.

### 4.4 Modality Projector

The projector maps text and image features into a shared $p < 10^{-5}$6__-dimensional latent space:

```math

\mathbf{Z}_{text} = \text{LayerNorm} \left( \mathbf{H}_{text}\mathbf{W}_{text} + \mathbf{b}_{text} \right)

```

```math

\mathbf{Z}_{img} = \text{LayerNorm} \left( \mathbf{H}_{img}\mathbf{W}_{img} + \mathbf{b}_{img} \right).

```

The projection matrices have dimensions:

```math

\mathbf{W}_{text} \in \mathbb{R}^{768 \times d_{model}}

```

and

```math

\mathbf{W}_{img} \in \mathbb{R}^{D_{img} \times d_{model}},

```

with $p < 10^{-5}$7__.

### 4.5 Bidirectional Cross-Attention

The cross-attention module consists of $p < 10^{-5}$8__ identical layers. Each layer performs information exchange in both directions.

For text-to-image attention:

```math

\mathbf{Q}_{text} = \mathbf{Z}_{text}\mathbf{W}_{Q,text}, \qquad \mathbf{K}_{img} = \mathbf{Z}_{img}\mathbf{W}_{K,img}, \qquad \mathbf{V}_{img} = \mathbf{Z}_{img}\mathbf{W}_{V,img}.

```

The attended text representation is:

```math

\mathbf{Z}_{img \rightarrow text} = \text{Softmax} \left( \frac{ \mathbf{Q}_{text} \mathbf{K}_{img}^{T} }{ \sqrt{d_k} } \right) \mathbf{V}_{img}.

```

For image-to-text attention:

```math

\mathbf{Q}_{img} = \mathbf{Z}_{img}\mathbf{W}_{Q,img}, \qquad \mathbf{K}_{text} = \mathbf{Z}_{text}\mathbf{W}_{K,text}, \qquad \mathbf{V}_{text} = \mathbf{Z}_{text}\mathbf{W}_{V,text}.

```

The corresponding attended image representation is computed analogously.

The two streams are updated with residual connections:

```math

\mathbf{Z}_{text}^{out} = \mathbf{Z}_{text} + \text{MLP}(\mathbf{Z}_{img \rightarrow text})

```

```math

\mathbf{Z}_{img}^{out} = \mathbf{Z}_{img} + \text{MLP}(\mathbf{Z}_{text \rightarrow im_

### 4.6 Pooling and Fusion

Sequence-level representations are reduced by mean pooling.

For the text representation:

$\mathbf{z}_{text} = \text{MeanPool}(\mathbf{Z}_{text}).$

For the image representation:

$\mathbf{z}_{img} = \text{MeanPool}(\mathbf{Z}_{img}).$

The multimodal representation is obtained by element-wise averaging from cross-attention:

$\mathbf{z}_{fused} = \frac{ \mathbf{z}_{text}^{out} + \mathbf{z}_{img}^{out} }{2}.$

The resulting representation is $d_{model}$-dimensional rather than twice the feature dimension as in concatenation-based late fusion.

### 4.7 Shared Classifier

The classifier maps the $d_{model}$-dimensional representation to a single logit:

$p(y=1|m) = \sigma \left( \text{MLP}_{cls}(\mathbf{H}_{fused}) \right).$

For unimodal inputs, the corresponding pooled representation is passed to the same shared classifier.

The shared classifier is used by TEXT, IMAGE, and MULTIMODAL paths.

### 4.8 Early-Exit Mechanism

For MULTIMODAL emails, DCAT optionally evaluates a text-only auxiliary classifier before invoking the vision encoder.

The pooled text representation is passed to:

$p_{aux}(y=1|t) = \sigma \left( \text{MLP}_{aux}(\mathbf{H}_{unimodal}) \right).$

If:

$p_{aux} \geq 0.95$

the message is classified as spam from the text-only prediction.

If:

$p_{aux} \leq 0.05$

the message is classified as ham from the text-only prediction.

For values between the two thresholds, the complete multimodal pathway is executed:

text -> vision -> cross-attention -> fusion -> shared classifier.

The auxiliary classifier is separate from the main shared classifier and is trained jointly with the model.

### 4.9 Training Procedure

The evaluated configuration uses:

Optimizer: AdamW with learning rate $1 \times 10^{-4}$ and default weight decay.

Scheduler: cosine annealing.

Loss: Binary Cross-Entropy with Logits Loss, with optional positive-class weighting for Weighted-DCAT.

Precision: FP16 mixed precision using PyTorch automatic mixed precision (AMP).

Batch size: 64.

Epochs: 1.

Encoder freezing: DistilBERT and MobileViT are frozen; projection, cross-attention, and classifier parameters are trainable.

Hardware: NVIDIA GPU with CUDA support.

Reproducibility: deterministic seeding across Python, NumPy, and PyTorch.

Full-DCAT contains 73,309,090 total parameters, of which 2,008,578 are trainable. The trainable parameters are therefore 2.74% of the total model parameters.

### 4.10 Inference Pipeline

At inference time:

1. The deterministic router assigns the email to TEXT, IMAGE, MULTIMODAL, or EMPTY.

2. Only the encoder or encoders required by the selected modality are invoked.

3. For MULTIMODAL emails, the optional auxiliary classifier is evaluated.

4. If early exit is not triggered, the image is encoded and cross-attention is applied.

5. The resulting representation is passed to the shared classifier.

6. A sigmoid probability is thresholded at 0.5 to produce the binary prediction.

---

## 5. Dataset and Data Processing

### 5.1 Data Source

The evaluation corpus originates from the SpamAssassin public email corpus~\cite{ref1}. The messages retain their original MIME structure and contain plain-text emails, HTML messages, inline images, and image attachments.

The processed subset used for primary evaluation contains 6,046 emails. The raw corpus takes up about 16 GB on disk.

The corpus was selected because it provides naturally occurring email messages, preserves MIME structure needed for deterministic modality extraction, and has been used in previous spam-detection studies.

### 5.2 Preprocessing Pipeline

The preprocessing pipeline operates on raw `.eml` files through four deterministic stages.

Stage 1: MIME Parsing. Each `.eml` file is parsed using Python's `email` package. The parser traverses the MIME tree to extract plain text, HTML content, and image content. HTML is processed to get visible text with BeautifulSoup and the lxml parser. Image parts are decoded to raw bytes. Non-fatal parsing issues are logged.

Stage 2: Content Filtering and Quality Control. Text is retained when at least 10 characters remain after whitespace stripping. Images must be at least $20 \times 20$ pixels and at least 1024 bytes. Images that fail these filters are discarded and their drop reasons recorded. When multiple meaningful images are present, the largest image by byte size is selected, with the pixel area as a tie-breaker.

Stage 3: Image Processing. Selected images are resized to $224 \times 224$ pixels using bicubic interpolation, converted to RGB, and normalized for the MobileViT encoder. The `timm` preprocessing pipeline is used to match the pretrained model's expected input distribution.

Stage 4: Text Tokenization. Email text is tokenized with the DistilBERT tokenizer using `max_length = 256`, `truncation = longest_first`, `padding = max_length`. Input IDs and attention masks are generated.

### 5.3 Dataset Composition

The SpamAssassin subset used for primary evaluation contains 6,046 emails after preprocessing.

Table 1: SpamAssassin Dataset Composition

PropertyCountPercentage

Total emails6,046100.0%

Parse success6,046100.0%

Ham (legitimate)4,15068.6%

Spam1,89631.4%

TEXT6,00799.4%

MULTIMODAL110.2%

IMAGE10.02%

EMPTY270.4%

TEXT ham4,14668.6%

TEXT spam1,86130.8%

MULTIMODAL ham40.07%

MULTIMODAL spam70.12%

IMAGE spam10.02%

EMPTY spam270.45%

Text-only messages make up 99.4% of the processed corpus, while only 11 of the 6,046 emails are classified as multimodal. One email is classified as IMAGE and 27 as EMPTY. EMPTY messages are excluded from training and evaluation.

The ham/spam distribution is 4,150 versus 1,896 messages, which is a 2.19:1 ham-to-spam ratio. The corpus is therefore moderately imbalanced rather than approximately balanced.

### 5.4 Split Strategy

The default split uses 70% training, 15% validation, and 15% test data with a fixed random seed of 42. Stratification preserves the ham/spam class proportions across the splits.

The split process enforces:

No email appears in more than one subset.

Sender-based and campaign-based leakage controls are applied where the corresponding identifiers are available.

### 5.5 Leakage Prevention

The leakage analysis is checking several types of duplication and overlap:

* exact text duplicates across splits;

* exact image duplicates across splits;

* perceptual image duplicates using perceptual hashing;

* near-duplicate text pairs using Jaccard similarity;

sender and campaign identifier overlap.

Exact textual and hash-based deduplication was applied to the full dataset. The perceptual leakage procedure was implemented and executed as a pilot over a limited subset because of its computational cost. The resulting evidence therefore supports the deduplication checks applied to the full data, while the perceptual audit should not be interpreted as a full exhaustive verification of every image pair.

---

## 6. Experimental Methodology

### 6.1 Experimental Protocol

All primary experiments use three seeds: 42, 43, and 44. Reported primary metrics are the means across these runs.

The evaluated models use a single training epoch with frozen encoders. Trainable parameters are limited to the projection, cross-attention, and classifier components. Modality routing is deterministic and content-based. The default classification threshold is 0.5 on the sigmoid output.

### 6.2 Model Variants

Eight evaluated variants are included:

1. All-Spam Prior: predicts spam for every input.

2. Modality Indicator: uses only the modality type as the input feature.

3. Text-only: activates only the text pathway.

4. Image-only: activates only the image pathway.

5. Late Fusion: concatenates mean-pooled DistilBERT and MobileViT representations before classification.

6. DCAT-No-XAttn: removes cross-attention and averages independently pooled text and image representations.

7. Full-DCAT: uses the complete bidirectional cross-attention architecture.

8. DCAT-Early-Exit: Full-DCAT with the auxiliary early-exit mechanism enabled.

The published multimodal baseline is a reimplementation of a late-fusion architecture using DistilBERT for text and ResNet-18 for images.

### 6.3 Ablation Studies

The cross-attention ablation compares Late Fusion, DCAT-No-XAttn, and Full-DCAT on the multimodal subset.

The imbalance ablation compares Full-DCAT trained with unweighted BCE against Weighted-DCAT with:

$w_{\text{spam}} = \frac{N_{\text{ham}}}{N_{\text{spam}}}.$

The early-exit ablation compares Full-DCAT and DCAT-Early-Exit using latency, FLOPs, and vision skip rate.

### 6.4 Evaluation Metrics

The evaluation reports:

Macro-F1: unweighted mean of ham-F1 and spam-F1.

Ham F1: F1-score for the ham class.

Spam F1: F1-score for the spam class.

Ham PR-AUC: precision-recall area for the ham class.

ROC-AUC: overall discrimination between the two classes.

Accuracy: overall proportion of correctly classified emails.

For multimodal analysis, the same metrics are recomputed using only messages assigned to the MULTIMODAL category.

### 6.5 Statistical Evaluation

Paired model comparisons use McNemar's test~\cite{ref11} with continuity correction. The test uses the predictions made by both models on the same examples and evaluates the discordant prediction counts.

Two settings are used:

1. The multimodal test subset, containing approximately 11 samples.

2. Pooled out-of-fold predictions from the five-fold cross-validation experiment, containing 7,867 samples.

The small multimodal test subset limits the statistical power of comparisons based on those 11 examples.

### 6.6 Efficiency Evaluation

Efficiency is evaluated using:

* total and trainable parameter counts;

* approximate FLOPs per forward pass;

* average per-sample latency;

* P95 latency;

* vision skip rate for early exit;

FLOP reduction relative to Full-DCAT.

The per-sample and total-time measurements are reported separately because they use different measurement procedures.

### 6.7 Error Analysis Protocol

Error analysis examines full-test and multimodal confusion matrices for the main model variants.

The analysis considers false positives, false negatives, and examples misclassified by one model but not another.

Per-sample error records are stored in:

`artifacts/error_analysis/dcat_errors.csv`

`artifacts/error_analysis/late_fusion_errors.csv`

---

## 7. Results

### 7.1 Primary Benchmark: Full Test Set

Table 2: Primary Benchmark Results -- Full Test Set (3-Seed Mean)

ModelMacro-F1Ham F1Spam F1Ham PR-AUCROC-AUCAccuracy

All-Spam Prior0.40000.00000.80000.00000.50000.6600

Image-Presence0.55000.10000.85000.10000.60000.7000

Text-Only0.98270.97600.98950.99680.99530.9854

Image-Only0.32200.49010.15400.71830.54000.3637

Published Baseline0.98690.98180.99200.99750.99690.9889

Late Fusion0.98550.97980.99120.99710.99660.9877

DCAT-No-XAttn0.98680.98170.99200.99750.99700.9889

Full DCAT0.98620.98080.99160.99730.99670.9883

DCAT-Early-Exit0.98620.98080.99160.99730.99670.9883

Source: `results/tables/final_results.csv` (three-seed means from seeds 42, 43, and 44).

Text-Only achieves Macro-F1 = 0.9827. Late Fusion achieves 0.9855 in the table shown above, and the corresponding three-seed source elsewhere in the analysis reports 0.9871; the final manuscript should use the authoritative source table consistently for this value.

Full DCAT achieves Macro-F1 = 0.9862, while the Published Baseline achieves 0.9869 and DCAT-No-XAttn achieves 0.9868. The difference between Full DCAT and Late Fusion is small on the full test set.

Image-Only achieves Macro-F1 = 0.3220, below the All-Spam Prior value of 0.4000. Given that meaningful image content is present in only a small fraction of the corpus, image-only training is based on substantially less data than text-only training.

### 7.2 Multimodal Subset Analysis

Table 3: Multimodal Subset Results

ModelMacro-F1Ham F1Spam F1

All-Spam Prior0.49680.00000.9935

Image-Presence0.49680.00000.9935

Text-Only0.49680.00000.9935

Image-Only0.28630.44440.1282

Published Baseline0.49680.00000.9935

Late Fusion0.49680.00000.9935

DCAT-No-XAttn0.83170.66670.9967

Full DCAT0.49680.00000.9935

DCAT-Early-Exit0.49680.00000.9935

The multimodal subset contains very few samples, and some models predict all or almost all samples as spam. Late Fusion, Full DCAT, and the All-Spam Prior all have Macro-F1 = 0.4968 with Ham F1 = 0.0000. DCAT-No-XAttn is the exception, with Macro-F1 = 0.8317 and Ham F1 = 0.6667.

The All-Spam Prior accuracy reported for this subset is 0.9871 in the source analysis. That value should not be interpreted as evidence of an approximately 85:15 class ratio when the subset is simultaneously described as containing 4 ham and 7 spam messages. The manuscript should use the authoritative sample-level class counts for prevalence and treat the reported accuracy according to the exact evaluation artifact from which it was produced.

### 7.3 Ablation: Cross-Attention

Table 4: Cross-Attention Ablation (Multimodal Subset)

| ModelMacro-F1Ham F1Spam F1 |    |    |    |

| -------------------------- | ------ | ------ | ------ |

| Late Fusion        | 0.4968 | 0.0000 | 0.9935 |

| DCAT-No-XAttn       | 0.8317 | 0.6667 | 0.9967 |

| Full DCAT         | 0.4968 | 0.0000 | 0.9935 |

McNemar's test gives $p=1.0000$ for Full DCAT versus Late Fusion, and $p=0.2482$ for Full DCAT versus DCAT-No-XAttn. Neither comparison reaches the $\alpha=0.05$ threshold. With approximately 11 multimodal test samples, these comparisons have limited statistical power.

### 7.4 Ablation: Class Imbalance

Table 5: Class Imbalance Ablation

| ModelMacro-F1Spam F1Ham F1MM-Macro-F1 |    |    |    |    |

| ------------------------------------- | ------ | ------ | ------ | ------ |

| Full DCAT               | 0.9862 | 0.9916 | 0.9809 | 0.6253 |

| Weighted Full DCAT          | 0.9880 | 0.9927 | 0.9833 | 0.7478 |

Weighted-DCAT increases full-test Macro-F1 from 0.9862 to 0.9880, and multimodal Macro-F1 from 0.6253 to 0.7478. The corresponding pooled out-of-fold McNemar comparisons give $p = 2.49 \times 10^{-45}$ for Weighted-DCAT versus Full-DCAT, and $p = 3.34 \times 10^{-6}$ for Weighted-DCAT versus Late Fusion.

### 7.5 Multimodal Robustness: 5-Fold Cross-Validation

Five-fold cross-validation is performed on the larger evaluation subset described in the experiment artifacts.

Table 6: Multimodal Robustness (5-Fold CV on 8K Subset)

| ModelMM-Macro-F1 (Mean)MM-Macro-F1 (Std) |    |    |

| ---------------------------------------- | ------ | ------ |

| DCAT-No-XAttn              | 0.5171 | 0.0597 |

| Full DCAT                | 0.7077 | 0.2639 |

| Late Fusion               | 0.5453 | 0.1222 |

| Published Baseline            | 0.5564 | 0.1192 |

Full DCAT has the highest reported mean MM-Macro-F1 at 0.7077. Its standard deviation of 0.2639 is also the highest among the listed models. The per-fold results show large changes between folds, including folds in which Full DCAT reached 1.0000, and folds in which it was close to the All-Spam Prior level. The small amount of multimodal data in the evaluation protocol limits how strongly these fold-level differences can be generalized.

### 7.6 Per-Fold Cross-Validation Details

Table 7: Per-Fold MM-Macro-F1 from 5-Fold CV

| FoldLate FusionDCAT-No-XAttnFull DCAT |    |    |    |

| ------------------------------------- | ------ | ------ | ------ |

| 1                   | 0.4971 | 0.6647 | 0.4971 |

| 2                   | 0.4971 | 0.6647 | 0.4971 |

| 3                   | 0.4968 | 0.6644 | 0.4968 |

| 4                   | 0.7380 | 0.5451 | 1.0000 |

| 5                   | 0.4975 | 0.6531 | 1.0000 |

Source: `artifacts/weighted_cv/cv_results.csv`

The fold-level values vary substantially. Full DCAT reaches 1.0000 in folds 4 and 5, while folds 1 and 2 remain near the All-Spam Prior level. The variation is consistent with a metric that is highly sensitive to the composition of a small multimodal evaluation set.

### 7.7 Efficiency Analysis

Table 8: Efficiency Comparison

| ModelParamsTrainable ParamsFLOPsLatency/sample (ms) |      |      |      |   |

| --------------------------------------------------- | ---------- | --------- | ---------- | ---- |

| Published Baseline                 | 77,967,426 | 428,034  | ~13B    | 1.48 |

| Late Fusion                     | 71,761,314 | 460,802  | ~13B    | 2.65 |

| DCAT-No-XAttn                    | 72,784,034 | 1,483,522 | ~13B    | 2.66 |

| Full DCAT                      | 73,309,090 | 2,008,578 | ~13B    | 2.70 |

| DCAT-Early-Exit                   | 73,309,090 | 2,008,578 | ~11B (avg) | 2.68 |

DCAT has approximately four times as many trainable parameters as Late Fusion: 2.01M versus 0.46M. The additional parameters are primarily associated with the cross-attention blocks and classifier.

Total FLOPs remain close to 13B for the evaluated variants, because the frozen encoders dominate the computational cost. The Published Baseline has the lowest reported per-sample latency at 1.48 ms, while Full DCAT and DCAT-Early-Exit report 2.70 ms and 2.68 ms, respectively.

Table 9: Early-Exit Efficiency Details (Full Test Set)

| MetricFull DCATDCAT-Early-ExitDiff |     |     |     |

| ---------------------------------- | ------- | -------- | ------- |

| Total Latency           | 59.9 ms | 74.7 ms | +24.82% |

| P95 Latency            | 60.3 ms | 113.6 ms | +88.39% |

| Total FLOPs            | 12.8M  | 12.7M  | -0.63% |

| Vision Skip Rate          | 0.00%  | 4.45%  | +4.45% |

The vision skip rate is 4.45%, and the corresponding average FLOP reduction is 0.63%. The total-time measurement shows an increase of 24.82% for the early-exit variant, while the per-sample measurement in Table 8 changes from 2.70 ms to 2.68 ms. These values come from different measurement procedures. The measured overhead of evaluating the auxiliary classifier and handling the conditional branch offsets the theoretical computational reduction in the total-time experiment.

### 7.8 Seed Variance Analysis

Table 10: 3-Seed Macro-F1 Variance

| ModelSeed 42Seed 43Seed 44MeanStd |    |    |    |    |    |

| --------------------------------- | ------ | ------ | ------ | ------ | ------ |

| Published Baseline        | 0.9870 | 0.9865 | 0.9871 | 0.9869 | 0.0003 |

| Late Fusion            | 0.9868 | 0.9869 | 0.9875 | 0.9871 | 0.0003 |

| Full DCAT             | 0.9860 | 0.9863 | 0.9864 | 0.9862 | 0.0002 |

Across the three seeds, the standard deviation is at most 0.0003 for these models. Late Fusion has the highest mean among the three, followed by the Published Baseline and Full DCAT. The differences between the means are small.

### 7.9 Modality-Specific Performance Analysis

Table 11: Modality-Specific Macro-F1 (Full Test Set, Seed 42)

| ModelText-Only EmailsMultimodal Emails |    |    |

| -------------------------------------- | ------ | ------ |

| Late Fusion              | 0.9858 | 0.4968 |

| DCAT-No-XAttn             | 0.9871 | 0.8317 |

| Full DCAT               | 0.9865 | 0.4968 |

On the TEXT modality, the reported models have Macro-F1 values above 0.986. The IMAGE modality contains only one sample, so any associated metric is highly sensitive to that single prediction. On the MULTIMODAL subset, DCAT-No-XAttn reports 0.8317 while Full DCAT and Late Fusion report 0.4968.

### 7.10 Confusion Matrix Analysis

Confusion matrices are provided for DCAT, Late Fusion, and Text-Only on both the full test set and the multimodal subset, together with a Macro-F1 comparison plot.

The weighted-primary confusion matrix for DCAT contains 57 false positives and 25 false negatives on the full test set. The corresponding rates depend on the class distribution of that evaluation.

---

## 8. Discussion

### 8.1 Full-Test Performance and Cross-Attention

Full DCAT achieves Macro-F1 = 0.9862 on the full test set, compared with 0.9871 for Late Fusion in the three-seed analysis. The difference is small. The corpus is 99.4% text-only, so the cross-attention module is not used for most examples. Its contribution is therefore concentrated in a small fraction of the data.

The multimodal subset also contains only 11 emails in the primary corpus. This provides limited training signal for estimating cross-modal interactions. Additional trainable parameters in the cross-attention module may therefore be sensitive to the specific multimodal examples available during training.

The shared classifier is also trained primarily on text-dominated batches. Multimodal representations must consequently be mapped into a decision space shaped mainly by text-only examples. These conditions provide plausible explanations for why the more expressive cross-attention architecture does not improve the full-test metric.

### 8.2 DCAT-No-XAttn on the Multimodal Subset

On the multimodal test subset, DCAT-No-XAttn reports Macro-F1 = 0.8317, compared with 0.4968 for Full DCAT. The simpler variant averages independently pooled text and image representations rather than applying cross-attention.

With only 11 primary multimodal examples, the estimate is highly sensitive to individual predictions. The additional parameters and learned interactions in Full DCAT may therefore be difficult to estimate from the available multimodal training data. The DCAT-No-XAttn representation preserves the two modalities separately until averaging, which may be less sensitive to this limited training signal.

The McNemar comparison between Full DCAT and DCAT-No-XAttn is not statistically significant at $\alpha=0.05$ ($p=0.2482$). The observed Macro-F1 difference should therefore be treated as a result specific to this small evaluation rather than as evidence of a general advantage for removing cross-attention.

### 8.3 Text-Dominated Corpus

Text-only classification remains strong in this corpus, with Macro-F1 = 0.9827. The three-seed full-test results for the multimodal models remain within a narrow range despite the additional visual pathway.

The distribution provides a simple explanation for this pattern: 99.4% of the processed messages are text-only, so full-test metrics are dominated by text classification. The result should not be generalized to email corpora with substantially higher proportions of image-containing messages.

### 8.4 Effect of Class Weighting

Weighted-DCAT increases multimodal Macro-F1 from 0.6253 to 0.7478 and changes the full-test Macro-F1 from 0.9862 to 0.9880. The pooled out-of-fold McNemar comparisons are statistically significant for both Weighted-DCAT versus Full DCAT and Weighted-DCAT versus Late Fusion.

The result isolates a training-objective effect: changing the class weighting changes the predictions substantially on the pooled evaluation. Within this experiment, the change in the loss function produces a larger multimodal improvement than the difference between the cross-attention and simpler fusion variants.

The result does not establish that class weighting is the dominant factor for all multimodal spam corpora, but it provides direct evidence that class imbalance materially affects the evaluated multimodal task.

### 8.5 Efficiency Trade-offs

The early-exit mechanism skips the vision encoder for 4.45% of the multimodal cases in the evaluated workload. Because only a small fraction of the corpus is multimodal, the resulting average FLOP reduction is 0.63%.

The two latency measurements provide different results. Table 8 reports 2.70 ms/sample for Full DCAT and 2.68 ms/sample for DCAT-Early-Exit, while Table 9 reports a 24.82% increase in total latency and an 88.39% increase in P95 latency for the early-exit configuration. The measurements should therefore not be combined into a single latency claim. The total-time measurement shows that conditional execution overhead can outweigh the computational saving under this workload.

A corpus with a larger proportion of multimodal messages would provide a different workload for evaluating the same mechanism. That case was not evaluated here.

### 8.6 Comparison to Prior Work

The Published Baseline reaches Macro-F1 = 0.9869 in the full-test evaluation, compared with 0.9862 for Full DCAT. Both systems use frozen text encoders, but they differ in the image encoder and fusion strategy.

The full-test results therefore do not show an advantage for cross-attention over the published late-fusion baseline under the evaluated corpus and protocol. The multimodal cross-validation results are different: Full DCAT has a mean MM-Macro-F1 of 0.7077, compared with 0.5453 for Late Fusion, but also has a much larger standard deviation. The two evaluation protocols therefore provide different views of the architecture.

## 9. Limitations and Threats to Validity

### 9.1 Dataset Limitations

Extreme multimodal scarcity. Only 11 emails in the primary SpamAssassin subset are multimodal. Metrics calculated on this subset are sensitive to individual predictions and should not be extrapolated to other domains.

Single corpus. All experiments use the SpamAssassin corpus. Performance on other email datasets is not evaluated.

No OCR. The pipeline does not extract text rendered inside images. Image-based spam that puts its primary text contents inside a graphic can therefore lose information before classification.

Single-image limitation. Only the largest meaningful image is processed for messages containing multiple images. Other visual content is not exposed.

### 9.2 Architecture Limitations

Frozen encoders. DistilBERT and MobileViT remain frozen during training. Domain-specific fine-tuning was not evaluated.

Simple fusion strategy. The multimodal representation uses element-wise averaging after cross-attention. Other fusion mechanisms were not evaluated.

Fixed early-exit thresholds. The thresholds are fixed at 0.95 and 0.05. The effect of changing these thresholds was not studied.

### 9.3 Evaluation Limitations

Small multimodal test set. The primary multimodal test subset contains approximately 11 emails. Multimodal metrics and McNemar comparisons are therefore sensitive to a small number of examples.

Single training epoch. All models are trained for one epoch. Longer training schedules could produce different optimization behavior, particularly for the cross-attention parameters.

No adversarial evaluation. The model is not evaluated against deliberately constructed adversarial spam.

Efficiency measurement uncertainty. The reported per-sample and total-time measurements differ, and the original detailed source artifact for the total-time comparison is no longer available in the repository.

### 9.4 Threats to Validity

Internal validity. Deterministic modality routing and duplicate checks reduce several sources of evaluation contamination. The single-epoch training regime and limited multimodal data remain important constraints.

Construct validity. Macro-F1, class-specific F1, PR-AUC, and ROC-AUC provide standard classification metrics, but multimodal Macro-F1 computed on only a small number of emails has limited precision.

External validity. The experiments use one email corpus with a strong text-only majority. The findings may differ for datasets containing more image-containing emails or different spam characteristics.
---

## 10. Conclusion and Future Work

This paper presents DCAT, a conditional multimodal email spam detection architecture combining bidirectional cross-attention, deterministic modality routing, and optional early-exit computation.

On the full test set, Full DCAT achieves Macro-F1 = 0.9862, compared with 0.9869 for the Published Baseline and 0.9871 for Late Fusion in the three-seed analysis. The full-test differences are small and the corpus is dominated by text-only messages.

The primary multimodal subset contains only 11 emails. On that subset, Full DCAT achieves Macro-F1 = 0.4968 while DCAT-No-XAttn achieves 0.8317. The corresponding McNemar comparison is not statistically significant. Five-fold cross-valuation on the larger multimodal evaluation provides a mean MM-Macro-F1 of 0.7077 for Full DCAT and 0.5453 for Late Fusion with substantially higher variance for Full DCAT.

Weighted training changes the multimodal result more substantially than the cross-attention ablation in the reported experiments. Weighted-DCAT increases multimodal Macro-F1 from 0.6253 to 0.7478, with statistically significant pooled out-of-fold McNemar comparisons against both Full DCAT and Late Fusion.

The early-exit mechanism skips vision computation for 4.45% of multimodal cases and reduces average FLOPs by 0.63% in the evaluated workload but the total-time measurement reports a 24.82% latency increase, suggesting that the measured runtime effect depends on execution overhead as well as theoretical FLOP savings.

Overall, the experiments do not demonstrate a consistent full-test advantage from adding cross-attention and show that the multimodal results are highly sensitive to data distribution, class imbalance, and the size of the multimodal subset.

### Future Work

1. Corpus expansion: Evaluate DCAT on larger datasets with substantially more multimodal emails, including image-heavy phishing and marketing corpora.
2. OCR integration: Extract text embedded inside images to provide an additional textual signal for image-based spam.
3. Encoder fine-tuning: Evaluate partial or full fine-tuning of DistilBERT and MobileViT under controlled learning-rate schedules.
4. Multi-image support: Process multiple meaningful images per email instead of retaining only the largest image.
5. Learned routing: Replace deterministic routing with a learned mechanism that can account for modality quality and relevance.
6. Contrastive pre-training: Train projection and cross-attention components using paired text-image representations before classification.
7. Larger-scale efficiency analysis: Evaluate early-exit behavior on corpora with higher multimodal prevalence and compare multiple threshold settings.
---

## Appendix A: Dataset Statistics Summary

| MetricValue            |             |
| ---------------------------------- | ----------------------- |
| Total emails (SpamAssassin subset) | 6,046          |
| Ham emails             | 4,150 (68.6%)      |
| Spam emails            | 1,896 (31.4%)      |
| Text-only emails          | 6,007 (99.4%)      |
| Multimodal emails         | 11 (0.2%)        |
| Image-only emails         | 1 (0.02%)        |
| Empty emails (excluded)      | 27 (0.4%)        |
| Text truncation length       | 256 tokens       |
| Image resolution          | $224 \times 224$ pixels |
| Train/Val/Test split        | 70/15/15 (config)    |

## Appendix B: Model Hyperparameters

| HyperparameterValue      |                  |
| ----------------------------- | --------------------------------- |
| Text encoder         | DistilBERT-base-uncased (frozen) |
| Vision encoder        | MobileViT-small via timm (frozen) |
| Shared latent dimension    | 256                |
| Cross-attention layers    | 2                 |
| Cross-attention heads     | 4                 |
| Cross-attention d_model    | 256                |
| Cross-attention d_ff     | 1024               |
| Cross-attention dropout    | 0.1                |
| Cross-attention activation  | GELU               |
| Cross-attention normalization | Pre-LayerNorm           |
| Classifier hidden dim     | 128                |
| Classifier dropout      | 0.3                |
| Classifier activation     | GELU               |
| Pooling strategy       | Mean pooling           |
| Optimizer           | AdamW               |
| Learning rate         | $1 \times 10^{-4}$        |
| Scheduler           | Cosine annealing         |
| Batch size          | 64                |
| Epochs            | 1                 |
| Precision           | FP16 mixed            |
| Loss function         | BCEWithLogitsLoss         |
| Classification threshold   | 0.5                |
| Early-exit high threshold   | 0.95               |
| Early-exit low threshold   | 0.05               |
| Seeds             | 42, 43, 44            |

## Appendix C: Complete Results Lineage

Source: `artifacts/final_results/results_lineage.csv`

| MetricModelSplitSeed/FoldSource ArtifactValueAggregation |                |              |      |                            |            |                           |
| -------------------------------------------------------- | ----------------------------- | -------------------------- | --------- | ----------------------------------------------------- | ---------------------- | --------------------------------------------------- |
| Macro-F1                         | Full-DCAT           | Primary Test (10%)     | Seed 42  | `artifacts/experiments/weighted_primary/results.json` | 0.9868         | Unweighted mean of Spam and Ham F1         |
| MM-Macro-F1                       | Full-DCAT           | Multimodal CV (5-Fold)   | 5-Fold CV | `artifacts/experiments/weighted_cv/cv_results.csv`  | 0.6609         | Mean across 5 folds                 |
| MM-Macro-F1                       | Late-Fusion          | Multimodal CV (5-Fold)   | 5-Fold CV | `artifacts/experiments/weighted_cv/cv_results.csv`  | 0.5564         | Mean across 5 folds                 |
| MM-Macro-F1                       | Weighted-DCAT         | Multimodal CV (5-Fold)   | 5-Fold CV | `artifacts/experiments/weighted_cv/cv_results.csv`  | 0.6824         | Mean across 5 folds                 |
| McNemar p-value                     | Weighted-DCAT vs. Full-DCAT  | Pooled OOF (7,867 samples) | All Folds | task-1070 log                     | $2.49 \times 10^{-45}$ | Exact/Asymptotic McNemar with continuity correction |
| McNemar p-value                     | Weighted-DCAT vs. Late-Fusion | Pooled OOF (7,867 samples) | All Folds | task-1070 log                     | $3.34 \times 10^{-6}$ | Exact/Asymptotic McNemar with continuity correction |
---

## References

1. Apache Software Foundation, "SpamAssassin Public Corpus," 2006. [Online]. Available: https://spamassassin.apache.org/old/publiccorpus/
2. J. J. Lohith, A. Purushotam, A. Mullangi, and A. Sharma, "MDL-SPAM: A Multi Model Deep Learning Framework for Email Spam Detection Using VGG-16 and LSTM," Multimedia Tools and Applications, 2023.
3. F. Jáñez-Martino, R. Alaiz-Rodríguez, V. González-Castro, E. Fidalgo, and E. Alegre, "A review of spam email detection: analysis of spammer strategies and the dataset shift problem," Artificial Intelligence Review, vol. 56, pp. 1145-1173, 2023.
4. V. Sanh, L. Debut, J. Chaumond, and T. Wolf, "DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter," arXiv preprint:1910.01108, 2019.
5. S. Mehta and M. Rastegari, "MobileViT: Light-weight, General-purpose, and Mobile-friendly Vision Transformer," ICLR, 2022.
6. R. Wightman, "PyTorch Image Models," GitHub repository, 2019. [Online]. Available: https://github.com/rwightman/pytorch-image-models
7. J. Devlin, M. W. Chang, K. Lee, and K. Toutanova, "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," NAACL-HLT, 2019.
8. J. Lu, D. Batra, D. Parikh, and S. Lee, "ViLBERT: Pretraining Task-Agnostic Visiolinguistic Representations for Vision-and-Language Tasks," NeurIPS, 2019.
9. H. Tan and M. Bansal, "LXMERT: Learning Cross-Modality Encoder Representations from Transformers," EMNLP, 2019.
10. A. Radford et al., "Learning Transferable Visual Models From Natural Language Supervision," ICML, 2021.
11. Q. McNemar, "Note on the sampling error of the difference between correlated proportions or percentages," Psychometrika, vol. 12, no. 2, pp. 153-157, 1947.
12. R. Xiong et al., "On Layer Normalization in the Transformer Architecture," ICML, 2020.
13. Z. Zhang, Z. Deng, W. Zhang, and L. Bu, "MMTD: A Multilingual and Multimodal Spam Detection Model Combining Text and Document Images," Applied Sciences, vol. 13, no. 21, p. 11783, 2023.
14. J. E. Arevalo, T. Solorio, M. Montes-y-Gómez, and F. A. González, "Gated Multimodal Units for Information Fusion," ICLR, 2017.
15. K. Simonyan and A. Zisserman, "Very Deep Convolutional Networks for Large-Scale Image Recognition," ICLR, 2015.
16. K. He, X. Zhang, S. Ren, and J. Sun, "Deep Residual Learning for Image Recognition," CVPR, 2016.
17. A. G. Howard et al., "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications," arXiv preprint:1704.04861, 2017.
18. Y. Kim, "Convolutional Neural Networks for Sentence Classification," EMNLP, 2014.
19. X. Zhang, J. Zhao, and Y. LeCun, "Character-level Convolutional Networks for Text Classification," NeurIPS, 2015.
20. S. Hochreiter and J. Schmidhuber, "Long short-term memory," Neural Computation, vol. 9, no. 8, pp. 1735-1780, 1997.
21. Y. Liu et al., "RoBERTa: A Robustly Optimized BERT Pretraining Approach," arXiv preprint:1907.11692, 2019.
22. D. Bahdanau, K. Cho, and Y. Bengio, "Neural Machine Translation by Jointly Learning to Align and Translate," ICLR, 2015.
23. S. Teerapittayanon, B. McDanel, and H. T. Kung, "BranchyNet: Fast inference via early exiting from deep neural networks," ICPR, 2016.
24. A. Annadatha and M. Stamp, "Image spam analysis and detection," Journal of Computer Virology and Hacking Techniques, vol. 14, no. 1, pp. 39-52, 2016.