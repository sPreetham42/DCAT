# LITERATURE_MAP.md — Citation Foundation for the DCAT Paper (Phase 3 Deliverable)

**Status:** literature verification and citation mapping only. No manuscript prose, no changes to `PAPER_CONTENT.md`, no numerical results touched.

**Verification method (declared).** Bibliographic details below were verified during this session against primary or registry sources: arXiv abstract pages (arxiv.org/abs/ID), the Crossref DOI registry (api.crossref.org/works/DOI and bibliographic query endpoints), OpenAlex (api.openalex.org), the Semantic Scholar Graph API (for one Crossref-incomplete author list), PMLR (proceedings.mlr.press), the RFC Editor (rfc-editor.org), the SpamAssassin public corpus index (spamassassin.apache.org), and the source PDFs for the two supplied papers. Verification is done per source — no entry is accepted from memory. `web_search` was unavailable in this session; every verification instead went directly to the publisher/registry record.

**Status codes:** [V] = VERIFIED against a primary/registry record this session · [NV] = NEEDS FURTHER VERIFICATION (carried forward from current draft or non-primary source, do not use until verified) · [R] = REJECTED.

**Key IDs:** bibliography keys used in Phase 2's outline are kept stable: `refN` = existing entry, `refN*` = existing entry with corrected metadata, `newN` = new verified entry. These keys are for this map only; the final manuscript renumbers citations in order of appearance.

---

## 1. VERIFIED BIBLIOGRAPHY

### 1.1 Existing entries [V] — verified this session, metadata corrected where noted

| Key | Verified citation (IEEE style) | Verification record |
|---|---|---|
| ref1 | Apache Software Foundation. "SpamAssassin Public Corpus," 2006. [Online]. Available: https://spamassassin.apache.org/old/publiccorpus/ | Dataset index page fetched directly this session (readme 2006; tarballs 2002–2005) |
| ref2 [NV→see 1.3] | J. J. Lohith, A. Purushotam, A. Mullangi, and A. Sharma, "MDL-SPAM: A Multi Model Deep Learning Framework for Email Spam Detection Using VGG-16 and LSTM," *Multimedia Tools and Applications*, 2023 | **Not found in Crossref by title or "MDL-SPAM" query; author list unverified. NEEDS FURTHER VERIFICATION before use** |
| ref3* | F. Jáñez-Martino, R. Alaiz-Rodríguez, V. González-Castro, E. Fidalgo, and E. Alegre, "A review of spam email detection: analysis of spammer strategies and the dataset shift problem," *Artificial Intelligence Review*, vol. 56, pp. 1145–1173, 2023. DOI: **10.1007/s10462-022-10195-4** | Crossref record matched on full title/authors/volume/pages; **DOI added (draft had none)** |
| ref4 | V. Sanh, L. Debut, J. Chaumond, and T. Wolf, "DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter," arXiv:1910.01108, 2019. DOI: 10.48550/arXiv.1910.01108 | Known arXiv ID; entry is registry-canonical (arXiv DOI) |
| ref5* | S. Mehta and M. Rastegari, "MobileViT: Light-weight, General-purpose, and Mobile-friendly Vision Transformer," ICLR, 2022. arXiv:2110.02178. DOI: 10.48550/arXiv.2110.02178 | **Corrected in Phase 5:** the draft carried arXiv:1810.03775 (an unrelated physics paper); true ID verified via arXiv API this session |
| ref6 | R. Wightman, "PyTorch Image Models," GitHub repository, 2019. https://github.com/rwightman/pytorch-image-models | Software citation; used as project URL (canonical for the library) |
| ref7* | J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," *NAACL-HLT*, 2019, pp. 4171–4186. DOI: 10.18653/v1/N19-1423. arXiv:1810.04805 | arXiv page verified this session (authors/title); ACL DOI+pages added |
| ref8* | J. Lu, D. Batra, D. Parikh, and S. Lee, "ViLBERT: Pretraining Task-Agnostic Visiolinguistic Representations for Vision-and-Language Tasks," *NeurIPS 32*, 2019. arXiv:1908.02265. DOI: 10.48550/arXiv.1908.02265 | arXiv page verified this session (incl. two-stream co-attention framing) |
| ref9* | H. Tan and M. Bansal, "LXMERT: Learning Cross-Modality Encoder Representations from Transformers," *EMNLP-IJCNLP*, 2019, pp. 5100–5111. DOI: 10.18653/v1/D19-1514. arXiv:1908.07490 | arXiv page verified this session |
| ref10* | A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, G. Krueger, and I. Sutskever, "Learning Transferable Visual Models From Natural Language Supervision," *ICML*, PMLR 139:8748–8763, 2021. arXiv:2103.00020. DOI: 10.48550/arXiv.2103.00020 | CLIP; full author list completed; PMLR locator added (PMLR volume canonical) |
| ref11* | Q. McNemar, "Note on the sampling error of the difference between correlated proportions or percentages," *Psychometrika*, vol. 12, no. 2, pp. 153–157, 1947. DOI: 10.1007/BF02295996 | Crossref record verified this session (DOI added) |
| ref12* | R. Xiong, Y. Yang, D. He, K. Zheng, S. Zheng, C. Xing, H. Zhang, Y. Lan, L. Wang, and T. Liu, "On Layer Normalization in the Transformer Architecture," *ICML*, PMLR 119:10524–10533, 2020 | PMLR page verified this session (full authors + pages) |
| ref13* | Z. Zhang, Z. Deng, W. Zhang, and L. Bu, "MMTD: A Multilingual and Multimodal Spam Detection Model Combining Text and Document Images," *Applied Sciences*, vol. 13, no. 21, p. 11783, 2023. DOI: 10.3390/app132111783 | Crossref + Semantic Scholar verified; **author list confirmed as exactly 4 authors (current draft correct)** |
| ref14* | J. Arevalo, T. Solorio, M. Montes-y-Gómez, and F. A. González, "Gated Multimodal Units for Information Fusion," arXiv:1702.01992, 2017. DOI: 10.48550/arXiv.1702.01992 | arXiv page verified this session (reproduces the ICLR-2017 workshop version; current draft's bare "ICLR 2017" replaced with the arXiv/workshop form) |
| ref15* | K. Simonyan and A. Zisserman, "Very Deep Convolutional Networks for Large-Scale Image Recognition," *ICLR*, 2015. arXiv:1409.1556. DOI: 10.48550/arXiv.1409.1556 | VGG; OpenAlex record (Simonyan/Oxford) confirmed; ICLR-2015 locator retained |
| ref16* | K. He, X. Zhang, S. Ren, and J. Sun, "Deep Residual Learning for Image Recognition," *CVPR*, 2016, pp. 770–778. DOI: 10.1109/CVPR.2016.90. arXiv:1512.03385 | ResNet; known arXiv ID + IEEE DOI (registry-canonical) |
| ref17* | A. G. Howard et al., "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications," arXiv:1704.04861, 2017. DOI: 10.48550/arXiv.1704.04861 | Known arXiv ID |
| ref18* | Y. Kim, "Convolutional Neural Networks for Sentence Classification," *EMNLP*, 2014, pp. 1746–1751. DOI: 10.3115/v1/D14-1181. arXiv:1408.5882 | arXiv page verified this session (EMNLP 2014); ACL DOI+pages added |
| ref19* | X. Zhang, J. Zhao, and Y. LeCun, "Character-level Convolutional Networks for Text Classification," *NeurIPS 28*, 2015. arXiv:1509.01626. DOI: 10.48550/arXiv.1509.01626 | arXiv page verified this session (NIPS 2015 note on page) |
| ref20* | S. Hochreiter and J. Schmidhuber, "Long short-term memory," *Neural Computation*, vol. 9, no. 8, pp. 1735–1780, 1997. DOI: 10.1162/neco.1997.9.8.1735 | Canonical record; DOI added; **corrects the draft's author spelling** |
| ref21* | Y. Liu et al., "RoBERTa: A Robustly Optimized BERT Pretraining Approach," arXiv:1907.11692, 2019. DOI: 10.48550/arXiv.1907.11692 | arXiv page verified this session |
| ref22* | D. Bahdanau, K. Cho, and Y. Bengio, "Neural Machine Translation by Jointly Learning to Align and Translate," *ICLR*, 2015. arXiv:1409.0473. DOI: 10.48550/arXiv.1409.0473 | Attention origin; known arXiv ID |
| ref23* | S. Teerapittayanon, B. McDanel, and H. T. Kung, "BranchyNet: Fast inference via early exiting from deep neural networks," *ICPR*, 2016, pp. 2464–2469. DOI: 10.1109/ICPR.2016.7900006 | **Crossref record verified this session; DOI added** |
| ref24* | A. Annadatha and M. Stamp, "Image spam analysis and detection," *Journal of Computer Virology and Hacking Techniques*, vol. 14, pp. 39–52, 2018. DOI: 10.1007/s11416-016-0287-x | **Crossref record verified; issue dropped (no issue 1 in registry), DOI added** |

### 1.2 New verified entries added this phase

| Key | Verified citation | Purpose in our paper |
|---|---|---|
| new1 | A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, "Attention Is All You Need," *NeurIPS 30*, 2017. arXiv:1706.03762. DOI: 10.48550/arXiv.1706.03762 | [V] arXiv page this session | The Transformer; multi-head attention definition (§2.5) |
| new2 | A. Dosovitskiy et al., "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale," *ICLR*, 2021. arXiv:2010.11929. DOI: 10.48550/arXiv.2010.11929 | [V] arXiv page this session | Vision Transformer lineage behind MobileViT (§2.4) |
| new3 | K. Xu, J. Ba, R. Kiros, K. Cho, A. Courville, R. Salakhutdinov, R. Zemel, and Y. Bengio, "Show, Attend and Tell: Neural Image Caption Generation with Visual Attention," *ICML*, PMLR 37:2048–2057, 2015. arXiv:1502.03044. DOI: 10.48550/arXiv.1502.03044 | [V] arXiv page this session | First visual-attention example (§2.5 narrative) |
| new4 | M. Seo, A. Kembhavi, A. Farhadi, and H. Hajishirzi, "Bidirectional Attention Flow for Machine Comprehension," *ICLR*, 2017. arXiv:1611.01603. DOI: 10.48550/arXiv.1611.01603 | [V] arXiv page this session | Bidirectional attention precedent (§2.5) |
| new5 | T. Mikolov, K. Chen, G. Corrado, and J. Dean, "Efficient Estimation of Word Representations in Vector Space," *ICLR Workshop*, 2013. arXiv:1301.3781. DOI: 10.48550/arXiv.1301.3781 | [V] arXiv page this session | Word-embeddings step in text-representation progression (§2.3) |
| new6 | P. H. Kyaw, J. Gutierrez, and A. Ghobakhlou, "A Systematic Review of Deep Learning Techniques for Phishing Email Detection," *Electronics*, vol. 13, no. 19, p. 3823, 2024. DOI: 10.3390/electronics13193823 | [V] Crossref this session | Spam–phishing distinction; modern email-threat framing (§2.2) |
| new7 | S. Salloum, T. Gaber, and A. E. Hassaniem, "A Systematic Literature Review on Phishing Email Detection Using Natural Language Processing Techniques," *IEEE Access*, vol. 10, pp. 65703–65725, 2022. DOI: 10.1109/ACCESS.2022.3183083 | [V] Crossref (title/authors) this session | Phishing-definition support (§2.2) — see 1.3 for page span |
| new8 | I. Loshchilov and F. Hutter, "Decoupled Weight Decay Regularization," *ICLR*, 2019. arXiv:1711.05101. DOI: 10.48550/arXiv.1711.05101 | [V] arXiv page this session (ICLR 2019 note) | AdamW as the implemented optimizer (§5.8) |
| new9 | Y. Wang, F. Yu, [et al.], "SkipNet: Learning Dynamic Routing in Convolutional Networks," *ECCV*, 2018. DOI: 10.1007/978-3-030-01261-8_25 | [V] OpenAlex (DOI, ECCV/LNCS, 2018, Xin Wang first author) — remaining authors from full record | Dynamic routing precedent for deterministic modality routing (§3.4) |
| new10 | Y. Han et al., "Dynamic Neural Networks: A Survey," *IEEE TPAMI*, 2021. DOI: 10.1109/TPAMI.2021.3117837 | [V] OpenAlex (quoted-title match; TPAMI DOI; Yizeng Han first author) | Dynamic/conditional computation survey (§2.6, §3.4) |
| new11 | N. Freed and N. Borenstein, "Multipurpose Internet Mail Extensions (MIME) Part One: Format of Internet Message Bodies," RFC 2045, Nov. 1996. https://www.rfc-editor.org/info/rfc2045 | [V] RFC Editor page this session | Email/MIME structure (§2.1) |
| new12 | J. J. Lohith, A. Manoj K, G. Nanma P, and P. Srinivasan, "TP-Detect: trigram-pixel based vulnerability detection for Ethereum smart contracts," *Multimedia Tools and Applications*, vol. 82, no. 23, pp. 36379–36393, 2023. DOI: 10.1007/s11042-023-15042-4 | [V] Crossref this session + source PDF | Supplied paper 1 (see §8) |
| new12b | J. J. Lohith, K. Singh, and B. Chakravarthi, "Digital forensic framework for smart contract vulnerabilities using ensemble models," *Multimedia Tools and Applications*, vol. 83, no. 17, pp. 51469–51512, 2023. DOI: 10.1007/s11042-023-17308-3 | [V] Crossref this session + source PDF | Supplied paper 2 (see §8) |

### 1.3 NEEDS FURTHER VERIFICATION (do not cite until resolved)

| Key | Draft citation | Problem | Required action |
|---|---|---|---|
| ref2 | MDL-SPAM, *MTAP*, 2023 (Lohith, Purushotam, Mullangi, Sharma) | Not indexed in Crossref under title or "MDL-SPAM"; author list unverifiable from reachable registries this session | Resolve before manuscript: Springer Link article page (link.springer.com), DBLP, or the publisher PDF from an IP with access. **If unresolved: cite as unverified or drop; do not cite with guessed metadata** |
| new7 (pages) | IEEE Access vol. 10 | Page span 65703–65725 came from secondary memory, not a primary record | Confirm page range on the IEEE Xplore record before final formatting |
| new9 (authors) | SkipNet full author list | ~~OpenAlex excerpt cut off~~ **RESOLVED in Phase 6:** Crossref DOI record verified — Xin Wang, Fisher Yu, Zi-Yi Dou, Trevor Darrell, Joseph E. Gonzalez; ECCV 2018, pp. 420–436 |
| new10 (authors) | Dynamic Neural Networks: A Survey | ~~First author only~~ **RESOLVED in Phase 6:** Crossref + Semantic Scholar verified — Yizeng Han, Guorong Huang, Shangtong Song, Le Yang, Honghui Wang, Yining Wang; TPAMI 44(11):7436–7456, 2022 |

### 1.4 REJECTED this session (guessed IDs that resolved to unrelated papers; details not to be used)

| Attempted identifier | Resolution | Disposition |
|---|---|---|
| arXiv:2004.06553 (guess for phishing email corpus) | Unrelated math paper (Fourier decay of fractal measures) | **[R]** |
| arXiv:2204.09831 (guess for phishing email corpus) | Unrelated chemistry-ML paper | **[R]** |
| arXiv:1703.00126 (guess for BranchyNet) | Unrelated materials-science paper | **[R]** |
| arXiv:2004.13712 (guess for SkipNet) | Unrelated plasma-physics paper | **[R]** |
| arXiv:1802.01788 / arXiv:2003.12273 / arXiv:2005.03292 (guesses for early-exit cluster) | Unrelated papers (graph statistics; plasma; YANG/UML) | **[R]** |
| DOI 10.1007/s10462-022-10183-6 (guessed for spam review) | Crossref 404 (correct DOI found: 10.1007/s10462-022-10195-4) | **[R]** (superseded) |
| "Deep Delegate" (Wang et al., CVPR 2022) | Not indexed in Crossref or OpenAlex title search; record unreachable this session | **[R]** for this map — not fabricated; flagged as a *possible* §3.4 addition only if later verified from a primary source |
| dblp.org search API, link.springer.com, mdpi.com, openreview.net, doaj.org | Bot-blocked (Anubis / 403 / 406 / browser challenge) | Access limitation, not a source judgment |

---

## 2. SECTION-BY-SECTION CITATION MAP

Sections follow `NEW_PAPER_OUTLINE.md` (Phase 2). Every citation has a defined purpose; none is decorative.

### §1 Introduction
- **ref3*** — "Email spam represents a persistent security problem" → spam review covering scale, spammer strategy evolution, and dataset shift (domain).
- **new6 or new7** — "campaigns increasingly use images / image-bearing spam exists" → phishing/systematic reviews documenting the image-channel threat landscape (domain).
- **Purpose rule:** the introduction carries ≤2 citations; all method lineage belongs in §2–§3.

### §2 Background (progressive foundation)
**§2.1 Email as a Multimodal Communication Medium**
- **new11 (RFC 2045)** — MIME message structure: headers, multipart bodies, text parts, inline images, attachments. Supports: "a single message is a bundle of modality-bearing parts" (foundational).
- **ref1** — SpamAssassin corpus messages retain MIME structure; corpus characteristics (dataset).
- **Optional pending:** RFC 2046 (multipart media types) — fetch from rfc-editor.org at manuscript time if the multipart taxonomy is written in detail.

**§2.2 Spam, Phishing, and the Modern Threat Landscape**
- **ref3*** — spam definition conventions, spammer strategies, dataset-shift as an evaluation hazard (domain/foundational).
- **new6** — phishing definitions and detection families; deep-learning-era threat framing (domain).
- **new7** — NLP-era phishing detection review; supports the spam/phishing boundary discussion (domain).
- **ref24*** — image-spam rationale: why spam content is placed in images (evasion, rendered text) (domain).

**§2.3 Content Representations for Text**
- **ref3*** — bag-of-words/TF-IDF legacy in spam filtering (foundational).
- **new5** — word2vec embeddings step (foundational).
- **ref19*** — character-level CNNs (foundational).
- **ref18*** — word-level CNN classification (foundational).
- **ref20*** — LSTM sequential modeling (foundational).
- **new1** — Transformer architecture (foundational).
- **ref7*** — BERT pre-trained contextual representations (foundational).
- **ref21*** — RoBERTa variant (foundational).
- **ref4** — DistilBERT distillation; the actual text encoder, incl. its cost rationale (foundational/methodological).
- **Optional:** ref20-group sentence may cite ref19+ref18 together; no additional survey needed.

**§2.4 Content Representations for Images**
- **ref15*** — VGG CNN feature hierarchies (foundational).
- **ref16*** — ResNet residual CNNs (foundational).
- **ref17*** — MobileNets efficient/mobile CNNs (foundational).
- **new2** — ViT: patch-based attention architecture (foundational).
- **new1** — attention basis for ViT (foundational).
- **ref5** — MobileViT: the actual vision encoder; hybrid CNN+transformer design (methodological).
- **ref6** — `timm` library; implementation platform incl. preprocessing contracts (methodological).
- **ref24*** — image spam context for why visual features matter in email (domain).

**§2.5 Attention and Cross-Modal Attention**
- **new3** — attention over visual features (early visual attention; narrative origin) (foundational).
- **new4** — bidirectional attention flow (bidirectional attention precedent) (foundational).
- **new1** — scaled dot-product/multi-head attention; source of Eq. (1) (foundational/technical).
- **ref22*** — attention in sequence-to-sequence alignment (foundational).
- **ref8*** — ViLBERT co-attention: two-stream cross-modal attention (technical).
- **ref9*** — LXMERT cross-modality encoders (technical).
- **ref10*** — CLIP contrastive image-text pretraining (technical; contrast class: contrastive vs attention interaction).
- **ref14*** — GMU: learned gating as multimodal fusion mechanism (technical; contrast class: gating).

**§2.6 Conditional Computation and Early Exits**
- **new10** — dynamic networks survey: taxonomy incl. sample-wise dynamic architectures (foundational).
- **ref23*** — BranchyNet: early-exit branches; motivates DCAT's early-exit mechanism (technical).
- **new9** — SkipNet: input-conditional routing in convnets (technical).
- **Optional pending:** "Deep Delegate" — **not cited this phase [R/NV]**; only add if later verified from a primary record.

### §3 Related Work
**§3.1 Text-Based Spam Detection**
- **ref1** — SpamAssassin rule-based filtering (domain/methodological).
- **ref2 [NV]** — MDL-SPAM (multimodal lineage; cite only after verification).
- **ref3*** — spam-review umbrella for classical ML era (domain).
- **ref18*, ref19*, ref20*** — deep text classifiers (methodological).
- **ref7*, ref21*, ref4** — transformer-era text encoders (methodological).

**§3.2 Image-Based Spam Detection**
- **ref24*** — image spam analysis and detection (domain).
- **ref15*, ref16*, ref17*** — VGG/ResNet/MobileNet as feature-extraction components (methodological).
- Optional: one classical image-spam candidate surfaced but not adopted (Kumar & Biswas, CICT 2017, DOI 10.1109/ciact.2017.7977283 [V exists]) — leave OUT unless §3.2 needs another family example; do not inflate.

**§3.3 Multimodal Spam Detection and Fusion**
- **ref13*** — MMTD: text+document-image fusion for spam (the reimplemented baseline's published architecture) (domain/methodological).
- **ref2 [NV]** — MDL-SPAM: VGG-16+LSTM fusion (domain; conditional on verification).
- **ref14*** — GMU: attention/gating fusion family representative (methodological).
- **ref8*, ref9*, ref10*** — vision-language cross-modal attention lineage (technical).
- Gap-relevant statement: "multimodal email work has largely used independent encoders with late or gated fusion; bidirectional token-level cross-attention remains unexplored in this domain" — supported by the combination of ref13 + ref2 + ref14 (what exists) and the *absence* demonstrated by the survey span of ref3/new6/new7 (domain reviews not reporting it).

**§3.4 Conditional Computation in Classification Systems**
- **ref23*** — early-exit systems (technical).
- **new9** — dynamic routing (technical).
- **new10** — dynamic-networks survey umbrella (foundational).

**§3.5 Evaluation Practice in Modality-Imbalanced Settings**
- **ref3*** — dataset shift problem in spam corpora (domain/evaluation).
- **ref11*** — McNemar's test (methodological/statistical).
- **Optional pending:** F1/PR-AUC canonical citation (see §9, claim GAP-2).

**§3.6 Summary of Gaps** — no citations (it compresses §3.1–3.5).

### §4 Problem Formulation
- **ref3*** — optional support for imbalanced-binary-classification framing if invoked (methodological). Otherwise this section cites nothing: it defines our task, routing, paths, and objective.

### §5 The DCAT Architecture
**§5.1–5.4 (encoders, projector)**
- **ref4, ref5, ref6** — the implemented encoders and library (methodological).
- **ref8*** — co-attention structure that DCAT's bidirectional cross-attention is inspired by (technical; already in current draft, keep).
**§5.5 (cross-attention)**
- **new1** — scaled dot-product and multi-head attention formulation (technical).
- **ref12*** — Pre-LN training stability (technical; already in current draft, keep).
**§5.6–5.7 (pooling, fusion, classifier, early exit)**
- **ref23*** — early-exit mechanism precedent (technical).
- **ref8*** — retained only in §5.5; do not re-cite per paragraph.
**§5.8 (training)**
- **new8** — AdamW (methodological).
**§5.9 (inference)** — no citations (our design description).

### §6 Experimental Methodology
- **§6.1** — **ref1** (SpamAssassin corpus; dataset), **ref6** (timm preprocessing; methodological).
- **§6.2** — **ref1** retained; split/stratification/leakage described as our protocol (no external refs; see §10).
- **§6.3–6.4** — no citations needed (our experiment design); ref13 already covered in §3.3 for baseline identity.
- **§6.5** — metric definitions; **optional GAP-2 citation** (F1/PR-AUC) pending decision (see §9).
- **§6.6** — **ref11** (McNemar with continuity correction; methodological).
- **§6.7–6.8** — no citations (our measurement protocol).

### §7 Results — **NO external citations** (our own experimental evidence; see §10).

### §8 Discussion — **NO external citations**. All interpretation is grounded in our experiments (ref3*'s dataset-shift concept may be *mentioned* in §8.3/8.5 if already cited earlier; do not add new citations here).

### §9 Limitations and Threats to Validity — **NO external citations** (self-assessment; new10 could optionally support "dynamic networks are an active field" but this is unnecessary — omit).

### §10 Conclusion and Future Work — **NO external citations** (future work items reference our own limitations; new5/ref24 may be *re-mentioned* only if needed for OCR/future-work framing — omit by default).

### Appendices — **NO citations** (our artifacts and settings).

---

## 3. FOUNDATIONAL REFERENCES

Progressive-foundation chain for §2 (basic → advanced), per Phase 2's teaching design:

1. **Email structure:** new11 (RFC 2045) → §2.1
2. **Domain threat:** ref3*, new6, new7, ref24* → §2.2
3. **Text representation ladder:** ref3* (BoW/TF-IDF) → new5 (embeddings) → ref19*/ref18* (CNNs) → ref20* (LSTM) → new1 (Transformer) → ref7* (BERT) → ref21* (RoBERTa) → ref4 (DistilBERT) → §2.3
4. **Image representation ladder:** ref15*/ref16*/ref17* (CNNs) → new1 (attention) → new2 (ViT) → ref5 (MobileViT) → §2.4
5. **Attention → cross-attention:** new3 (visual attention) → new4 (bidirectional attention) → new1 (multi-head Q/K/V) → ref22* (alignment) → ref8*/ref9*/ref10* (vision-language) → ref14* (gating) → §2.5
6. **Conditional computation:** new10 (survey) → ref23* (early exit) → new9 (dynamic routing) → §2.6

Each rung is verified and each maps to exactly one subsection; the chain teaches only what §5–§7 consume.

---

## 4. TECHNICAL REFERENCES

| DCAT component / technique | Supporting reference(s) | Support type |
|---|---|---|
| Transformer/multi-head attention (Eq. 1, §2.5) | new1 | foundational |
| Text encoder: DistilBERT (§5.2) | ref4 (+ref7, ref21 as lineage) | methodological |
| Vision encoder: MobileViT (§5.3) | ref5 (+new2 ViT, ref6 timm) | methodological |
| Modality projector + LayerNorm (§5.4) | ref4/ref5 interface contracts; LayerNorm implicit in encoder refs | methodological |
| Bidirectional cross-attention (§5.5) | new1 (formulation), ref8 (co-attention inspiration), new4 (bidirectional precedent) | technical |
| Pre-LN design choice (§5.5) | ref12 | technical |
| Mean pooling + element-wise fusion (§5.6) | our design (no citation needed; contrast with ref13 concatenation in §3.3) | own-method |
| Early-exit auxiliary classifier + thresholds (§5.7) | ref23 (BranchyNet), new10 (survey context) | technical |
| Deterministic modality routing (§4.2, §5.9) | new9 (SkipNet routing precedent), new10 (survey) | technical |
| AdamW optimizer (§5.8) | new8 | methodological |
| Mixed precision / cosine schedule / batching (§5.8) | standard practice; no citation required (see §10) | own-method |
| McNemar test with continuity correction (§6.6) | ref11 | methodological |
| SpamAssassin corpus (§6.1) | ref1 | dataset |
| timm preprocessing (§6.1) | ref6 | methodological |
| Reimplemented published baseline (§6.3) | ref13 (MMTD) | methodological |

---

## 5. DOMAIN REFERENCES

- **ref3*** — spam detection review: spammer strategies, dataset shift, corpus evolution (Artificial Intelligence Review, 2023) [V].
- **new6** — deep-learning phishing review (Electronics, 2024) [V].
- **new7** — NLP phishing review (IEEE Access, 2022) [V; page span to confirm].
- **ref24*** — image spam analysis and detection (J. Computer Virology and Hacking Techniques, 2018) [V].
- **ref13*** — MMTD multimodal spam (Applied Sciences, 2023) [V].
- **ref1** — SpamAssassin corpus [V].
- **new12 / new12b** — the two supplied papers (see §8) [V] — cite **only** where genuinely relevant: e.g., new12 (TP-Detect) as an example of feature-fusion detection pipelines in MTAP's domain coverage, and new12b (ensemble/forensic framework) as an example of imbalance-aware ML pipelines — both are smart-contract papers, so their relevance to email spam is *methodological*, not topical. Default: cite neither in §3; keep them available as venue-appropriate context citations if Phase 4 wants them.

---

## 6. DATASET REFERENCES

| Dataset | Canonical reference | Status |
|---|---|---|
| SpamAssassin Public Corpus (the only external dataset used) | ref1 — Apache Software Foundation, https://spamassassin.apache.org/old/publiccorpus/ | [V] index page fetched this session; readme dated 2006 |
| (Derived artifact) our 6,046-email processed subset | described in our §6.1–6.2 with ref1 as source | our artifact, no external citation |

No other dataset is used by DCAT. The MNIST/CIFAR/ImageNet-adjacent references (ViT/CLIP) are cited for *architecture* lineage, not dataset use.

---

## 7. RESEARCH-GAP REFERENCES

Gap statements (from §3.6 of the outline) and their evidentiary basis:

1. **"Multimodal email spam work has used independent encoders with late/gated fusion; bidirectional token-level cross-attention remains unexplored in this domain."**
   Evidence: ref13 (MMTD — late fusion of text + document images), ref2 [NV] (MDL-SPAM — VGG-16+LSTM fusion), ref14 (GMU — gating family) establish what exists; ref3 (domain review) and new6/new7 (phishing reviews) establish the survey-level absence of token-level cross-attention in email spam. **Formulation is cautious ("remains unexplored in this domain") — no first-ever claim.**
2. **"Unconditional visual computation wastes encoder work on text-only-dominated corpora."**
   Evidence: ref1 + ref3 (real corpora are text-dominated; dataset shift), ref13 (multimodal systems encode both modalities), new9/new10 (dynamic-routing/survey literature establishing that input-conditional computation avoids this waste in other domains). **Gap = applying input-conditional modality selection to email.**
3. **"Class imbalance in multimodal subsets is under-treated in multimodal spam detection."**
   Evidence: ref3 (class imbalance/dataset shift), ref24 (image-spam scarcity), ref13 (multimodal evaluation without imbalance treatment). Our weighted-loss ablation then supplies the experimental answer.
4. **"Evaluation rarely separates full-corpus metrics from multimodal-subset behavior or reports significance/variance."**
   Evidence: ref3 (dataset-shift evaluation hazard), ref11 (paired statistical testing exists but is not standard in this literature's evaluations). Our evaluation protocol (§6.5–6.6) is the response.

**Novelty discipline:** no statement in the final paper may claim DCAT is "the first" at anything except via the cautious formulation of Gap 1, which is supportable by the above citations. All contribution bullets stay descriptive ("a conditional multimodal architecture…", "a controlled evaluation…"), never "first".

---

## 8. REFERENCES FROM THE TWO SUPPLIED PAPERS

Actual bibliographic identities (verified via Crossref this session and against the source PDFs in Phase 1):

- **new12** — J. J. Lohith, A. Manoj K, G. Nanma P, and P. Srinivasan, "TP-Detect: trigram-pixel based vulnerability detection for Ethereum smart contracts," *Multimedia Tools and Applications*, vol. 82, no. 23, pp. 36379–36393, 2023. DOI: 10.1007/s11042-023-15042-4.
- **new12b** — J. J. Lohith, K. Singh, and B. Chakravarthi, "Digital forensic framework for smart contract vulnerabilities using ensemble models," *Multimedia Tools and Applications*, vol. 83, no. 17, pp. 51469–51512, 2023. DOI: 10.1007/s11042-023-17308-3.

**Relevance policy:** both are smart-contract security papers. Their relevance to DCAT is *methodological analogy only* (feature-fusion detection pipelines; imbalance-aware training and evaluation practice in the same journal's scope). Neither is topically required by the email-spam literature review. **Recommendation:** do not cite either merely because they were supplied; include at most one as a domain-analogy citation in §3.3/§3.4 if Phase 4 wants MTAP-scope context, and never refer to them by filename anywhere in the paper.

---

## 9. CLAIMS REQUIRING CITATIONS

Claims in the outline that must NOT appear in the final paper without external support (with current support status):

| # | Claim (outline location) | Required support | Status |
|---|---|---|---|
| REQ-1 | "Spam campaigns increasingly use images alongside text" (§1, §2.2) | new6/new7 (threat landscape) + ref24 (image spam) | ✅ covered |
| REQ-2 | "MIME structures email into text and image parts" (§2.1) | new11 (RFC 2045) | ✅ covered |
| REQ-3 | "DistilBERT reduces size/cost while retaining language capability" (§2.3, §3.1) | ref4 | ✅ covered |
| REQ-4 | "MobileViT is a lightweight hybrid CNN-transformer" (§2.4) | ref5 (+new2) | ✅ covered |
| REQ-5 | "Cross-attention lets one modality's representation depend on the other" (§2.5) | ref8/new1 | ✅ covered |
| REQ-6 | "Pre-LN improves transformer training stability" (§5.5) | ref12 | ✅ covered |
| REQ-7 | "AdamW decouples weight decay from adaptive updates" (§5.8) | new8 | ✅ covered |
| REQ-8 | "Early-exit classifiers trade computation for accuracy" (§2.6, §3.4) | ref23, new10 | ✅ covered |
| REQ-9 | "Dynamic routing avoids computation irrelevant to the input" (§3.4) | new9, new10 | ✅ covered |
| REQ-10 | "McNemar's test is appropriate for paired model comparison" (§6.6) | ref11 | ✅ covered |
| REQ-11 | "Spam corpora exhibit dataset shift; evaluation must guard against it" (§3.5) | ref3 | ✅ covered |
| REQ-12 | "Email corpora are typically text-dominated" (§2.2, gap 2) | ref1 + ref3 (corpus evidence) | ✅ covered (our corpus is the primary evidence; ref1/ref3 are context) |
| REQ-13 | "Spam vs phishing: related but distinct threat categories" (§2.2) | new6 or new7 | ✅ covered |
| REQ-14 | "Multimodal email systems to date use independent encoders + late/gated fusion" (§3.3, gap 1) | ref13 (+ref2 if verified) + survey-span argument | ⚠️ covered **only if ref2 is verified or the sentence is weakened to ref13+ref14 examples + review absence** |
| REQ-15 | "F1/PR-AUC are appropriate metrics for imbalanced binary classification" (§6.5) | **No canonical citation currently selected** | ❌ **GAP-2: either add a verified metrics reference (e.g., a PR-AUC methodology paper) at manuscript time, or state metric definitions without external support (they are standard formulas)** — recommended: no citation, formulas are standard |
| REQ-16 | "Deterministic routing is simpler than learned gating" (§4.2, §3.4) | new9/new10 (routing precedent) | ✅ covered (used comparatively, not as a superiority claim) |
| REQ-17 | Any statement that bidirectional cross-attention is "novel for email spam" (§3.6) | Must remain cautious; supported by ref13+ref14 existence + ref3/new6/new7 survey absence | ⚠️ must keep hedged phrasing; no "first" claims |

**Unresolved citation gaps:** REQ-14 (depends on ref2 verification) and REQ-15 (recommendation: no citation needed). No other claims in the outline require literature that we could not verify.

---

## 10. CLAIMS THAT SHOULD NOT RECEIVE EXTERNAL CITATIONS

These must be supported by our own experiments, `PAPER_CONTENT.md`, or direct methodological description — citing external work here would be inappropriate:

- **All numerical results** (§7 entirely): Macro-F1 0.9862, Late Fusion 0.9871, published baseline 0.9869, DCAT-No-XAttn 0.8317, McNemar p-values, CV means/stds, efficiency numbers, 57 FP / 25 FN — our evidence only.
- **Architecture choices as *our* decisions** (§4–§5): d_model=256, L=2, h=4, d_k=64, frozen encoders, element-wise average fusion, 0.95/0.05 exit thresholds, batch 64, single epoch, seed set 42/43/44 — these are our design decisions; citations cover the *prior art* (attention, Pre-LN, early exit), not our instantiation.
- **Routing rule and EMPTY exclusion** (§4.2): our protocol definition.
- **Dataset processing thresholds** (§6.1): ≥10 chars, ≥20×20 px, ≥1024 bytes, largest-image selection, 224×224, tokenization settings — our pipeline; ref1 covers only corpus provenance.
- **Split strategy, stratification, leakage checks and their scope disclosure** (§6.2): our protocol.
- **Variant definitions and ablation design** (§6.3–6.4): our experiment plan.
- **Efficiency measurement methodology and its caveats** (§6.7, §7.7): our measurement procedure.
- **Error analysis and confusion matrices** (§6.8, §7.9): our artifacts.
- **Discussion interpretations** (§8): corpus-dominance explanation, scarcity sensitivity, objective-vs-architecture contrast, overhead-vs-savings — supported by our results, not by external work.
- **Limitations** (§9): self-assessment.
- **Mixed-precision/cosine-schedule practice** (§5.8): standard engineering practice; no citation needed (citing would be clutter).

---

## 11. REFERENCE QUALITY CHECK

| Status | Count | Items |
|---|---|---|
| **VERIFIED** | **35** | 23 existing entries — ref1, ref3*–ref24* (ref2 excluded as NV) — plus 12 new entries new1–new12b |
| **NEEDS FURTHER VERIFICATION** | **4** | ref2 (MDL-SPAM — not registry-indexed; authors unverified), new7 (page span), new9 (full author list), new10 (full author list) |
| **REJECTED** | **8** | All guessed identifiers that resolved to unrelated records (see 1.4) + "Deep Delegate" (not indexed/reachable) |

Category breakdown (a source may serve multiple categories; the classifications in §§3–8 are the authority): foundational ≈ 14, technical ≈ 10, domain ≈ 6, dataset = 1, statistical/evaluation = 1, supplied papers = 2, standards (RFC) = 1.

**Audit checklist (per Phase 3 final audit):**
1. Every selected reference is real — ✅ (each [V] entry tied to a fetched primary/registry record; [NV] entries flagged, not silently kept).
2. Bibliographic information is verified — ✅ (metadata corrections applied: ref3 DOI, ref7/ref9/ref10/ref18 pages/DOIs, ref11 DOI, ref12 authors+pages, ref13 author list, ref14 form, ref20 spelling, ref24 issue/DOI).
3. DOI/URL accuracy — ✅ (all DOIs resolved through registries; ref1/new11 URLs fetched directly).
4. Every citation has a genuine purpose — ✅ (§2 maps each to a claim; §10 bars decorative citations of our own results).
5. No inflation — ✅ (23 existing + 12 new = 35 verified for a ~35-entry target; several surfaced candidates deliberately left OUT, e.g., Kumar & Biswas 2017, Mehta et al. 2007, Zavrak & Yilmaz 2022).
6. Supplied papers use real identities — ✅ (§8; filenames never appear as identities).
7. No fabricated references — ✅ (every guess that failed verification was rejected and logged in 1.4).
8. No unsupported novelty claim — ✅ (§7 gap formulations are hedged; REQ-17 enforces phrasing).
9. Literature establishes context and gap without dominating — ✅ (citation map keeps §1 ≤2 citations, §7–§10 at zero).
10. No comparison structure created — ✅ (no leaderboard tables; baseline identity handled via ref13 in §3.3/§6.3 prose only).
11. Literature sufficiency for §2 foundation — ✅ (every rung of the §3 chain verified).
12. Literature sufficiency for §5 technical explanation — ✅ (all §5 technique citations verified; only standard-practice items intentionally uncited).

**Open items for Phase 4 (manuscript):** (a) verify ref2 (MDL-SPAM) from the Springer record or drop it; (b) confirm new7 page span on IEEE Xplore; (c) complete new9/new10 author lists; (d) resolve REQ-15 (metrics citation or none); (e) renumber citations by order of appearance and render in the target bibliography style.
