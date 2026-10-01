# REFERENCE_STYLE_BLUEPRINT.md

**Purpose.** This document converts the Phase 1 analysis of two published reference papers into a reusable structural and stylistic blueprint. It is authoritative **only** for structure, organization, narrative flow, and presentation conventions. It is **not** a source of scientific facts for the DCAT paper — all research facts come from `PAPER_CONTENT.md`.

**Papers analyzed.**

| Role in this analysis | Actual bibliographic identity |
|---|---|
| Compact journal paper (5 sections, 15 pp.) | Lohith J J, Anusree Manoj K, Guru Nanma P, Pooja Srinivasan (2023). *TP-Detect: trigram-pixel based vulnerability detection for Ethereum smart contracts*. **Multimedia Tools and Applications**, 82(14), 36379–36393. DOI: 10.1007/s11042-023-15042-4. |
| Extended journal paper (4 sections, 44 pp.) | Lohith J J, Kunwar Singh, Bharatesh Chakravarthi (2023/2024). *Digital forensic framework for smart contract vulnerabilities using ensemble models*. **Multimedia Tools and Applications**, 83(18), 51469–51512. DOI: 10.1007/s11042-023-17308-3. |

Throughout this file they are referred to as **the compact paper** (TP-Detect) and **the extended paper** (ensemble/forensic framework).

---

## 1. Bibliographic identity

### 1.1 Compact paper — "TP-Detect"

| Field | Value |
|---|---|
| Title | TP-Detect: trigram-pixel based vulnerability detection for Ethereum smart contracts |
| Authors | Lohith J J, Anusree Manoj K, Guru Nanma P, Pooja Srinivasan |
| Affiliation | Computer Science and Engineering, B.M.S. College of Engineering, Bull Temple Road, Bangalore 560019, Karnataka, India |
| Corresponding author | Pooja Srinivasan (email in footnote); all author emails listed in footnotes |
| Venue | Multimedia Tools and Applications (Springer) |
| Year / volume / pages | 2023, vol. 82, pp. 36379–36393 (15 pp.) |
| DOI | 10.1007/s11042-023-15042-4 |
| Dates | Received 11 May 2022 / Revised 2 Sep 2022 / Accepted 27 Feb 2023 / Published online 30 Mar 2023 |
| License | Author(s), under exclusive licence to Springer Science+Business Media, LLC, part of Springer Nature |
| Producer metadata | LaTeX with hyperref; Acrobat Distiller; single-column Springer layout (~439.6 × 666.5 pt page) |
| Back matter | Data Availability statement; Declarations (Competing interests); Publisher's Note; copyright/licence statement |

### 1.2 Extended paper — "Digital forensic framework"

| Field | Value |
|---|---|
| Title | Digital forensic framework for smart contract vulnerabilities using ensemble models |
| Authors | Lohith J J, Kunwar Singh, Bharatesh Chakravarthi |
| Affiliations | Dept. of CSE, National Institute of Technology, Tiruchirapalli 620015, Tamilnadu, India; School of Computing and Augmented Reality, Ira A. Fulton Schools of Engineering, Arizona State University, Tempe AZ 85281, USA |
| Corresponding author | Bharatesh Chakravarthi (ASU); author emails in footnotes |
| Venue | Multimedia Tools and Applications (Springer) |
| Year / volume / pages | Issue-dated 2024 (vol. 83), pp. 51469–51512 (44 pp.); accepted 25 Sep 2023; published online 13 Nov 2023 |
| DOI | 10.1007/s11042-023-17308-3 |
| Dates | Received 6 Mar 2023 / Revised 21 Sep 2023 / Accepted 25 Sep 2023 / Published online 13 Nov 2023 |
| License | Author(s), under exclusive licence to Springer Science+Business Media, LLC, part of Springer Nature |
| Producer metadata | LaTeX with hyperref; Acrobat Distiller; same single-column Springer layout |
| Back matter | Data Availability statement; Declarations (Conflict of Interest); Publisher's Note; licence statement |

**Relationship.** The extended paper cites the compact paper in its related-work subsection, showing how a later paper integrates an earlier one as one citation among many — never as a structural anchor. This is exactly the pattern DCAT should follow: any "base" lineage becomes ordinary related-work citation.

---

## 2. Structural blueprint

### 2.1 Side-by-side section hierarchy (as published)

**Compact paper — 5 top-level sections, max depth 3:**

```
Abstract (~250 words, one paragraph)
Keywords (5, "·"-separated)
1 Introduction                       (4–5 long paragraphs + bulleted
                                      contribution list + roadmap para)
2 Related work
  2.1 Detection of vulnerabilities in smart contracts   (tool-by-tool, one para each)
  2.2 Machine learning and blockchain                    (method-by-method)
3 Methodology                        (overview para + pipeline figure first)
  3.1 Collection and preprocessing of smart contracts
  3.2 Dataset
    3.2.1 Trigram feature extraction
    3.2.2 Pixel value extraction
    3.2.3 Merging of datasets
  3.3 Training                        (models + multi-label strategies)
4 Results                            (split protocol, metrics, eqs. (1)–(3),
                                      own-results table+bar figure, comparison table)
5 Conclusion                         (recap, benefits, future work)
Data availability / Declarations / References (57)
```

**Extended paper — 4 top-level sections, max depth 3, tutorial-style long intro:**

```
Abstract (~280 words, one paragraph)
Keywords (6, "·"-separated)
1 Introduction                       (1.1–1.9 subsections: background tutorial,
                                      security flaws, motivation, contribution,
                                      organization, related work (1.6–1.7),
                                      vulnerability taxonomy (1.8), challenges (1.9))
2 Methodology
  2.1 Stage-1 (NLP preprocessing/features; Algorithm 1; architecture figure)
  2.2 Data preparation
    2.2.1 About dataset
    (2.2.x) Preprocessing of data (bullet steps: conversion, regex, tokenization,
           stop words, lemmatization)
  2.3 Smart contract vulnerabilities (six classes, each with code Listing +
      attack-scenario paragraph)
  2.4 Feature engineering strategies (2.4.1 TF-IDF, 2.4.2 Word2Vec,
      2.4.3 CBOW, 2.4.4 Skip-Gram; dimension counts for every feature set)
  2.5 Imbalance handling (SMOTE; 2.5.1 Feature validation = k-fold CV)
  2.6 Stage-2 (ensemble: 2.6.1–2.6.5 one subsection per classifier,
      each ending in confusion-matrix figure refs)
3 Results and discussions
  (metric definitions as numbered equations (1)–(10) interleaved with figures)
  (per-model confusion matrices, ROC, metric bar charts; one big results table
   spanning 4 pages, best values highlighted)
4 Conclusion
Data availability / Declarations / References (81)
```

### 2.2 Structural patterns worth adopting

- **Title pattern:** short system name + colon + functional descriptor ("what it does" + "on what"). No question titles, no subtitles beyond one colon.
- **Abstract (both):** single paragraph, ~250–300 words; arc = domain motivation → task → proposed method → dataset/setup → headline numbers → comparative closing claim. Numbers appear in the abstract.
- **Keywords:** 5–6, ordered general→specific, Springer "·" style.
- **Introduction:**
  - Funnel: broad domain (with citations) → specific platform/technology → the practical problem → why ML/AI is apt → the concrete gap → contributions → roadmap.
  - The compact paper uses un-subsectioned paragraphs + a bulleted contribution list + an explicit "Organization of the paper" paragraph. The extended paper uses numbered intro subsections (1.1–1.9) including motivation and contribution subsections.
  - **Lesson:** either is acceptable; DCAT should use the *un-subsectioned* intro with an explicit bulleted contribution list and a roadmap paragraph (cleaner, more common in top venues).
- **Related work placement:** compact paper = separate Section 2 after intro, split by approach family (tools vs ML), one paragraph per work, each paragraph: what it does → how → quantitative result → limitation/contrast. Extended paper = folded into the intro (1.6–1.7) plus survey-style tables. **Lesson for DCAT:** separate related-work section, organized by *approach family*, each paragraph self-contained, ending with the aggregate gap — never one-per-paragraph rankings around a single ancestor work.
- **Research gap:** stated *inside* the intro ("Motivation"/"Our contribution") and reinforced at the end of related work via a contrast sentence ("classical methods … however, they are confined to … which eventually impacts overall performance").
- **Contributions:** compact paper = 4 bullets, each one sentence: (i) what is classified, (ii) how the dataset is built, (iii) which models train it, (iv) first-use/novelty claim hedged with "To the best of our knowledge". DCAT should mirror this shape (4–6 bullets, hedged novelty, no over-claiming).
- **Methodology organization:** a **staged pipeline** narrative. Opening paragraph states the N-step approach and points at an overview figure; then one subsection per stage in execution order; each component subsection explains *what → why → how*, with concrete dimensions/sizes (rows, columns, feature counts) at every stage.
- **Named artifact pattern:** the dataset gets a name ("TriPix") and is reused as vocabulary throughout results and conclusion. DCAT should likewise use its named framework (DCAT) and named dataset consistently once introduced.
- **Dataset section:** dedicated subsections for source, preprocessing (explicit bullet list of operations), composition, and merging — with counts everywhere.
- **Training/experimental setup:** compact paper puts split (80/20) + library + metric inside "Results"; extended paper puts training protocol, k-fold CV, and 36-model matrix inside "Methodology". **Lesson for DCAT:** keep a dedicated Experimental Methodology section (setup, variants, metrics, protocol) separate from Results — cleaner than either reference and standard in ML venues.
- **Results organization:** always (a) restate protocol in 1 paragraph, (b) define metrics (numbered equations), (c) own-results table + figure, (d) narrate numbers in prose verbatim, (e) highlight best values, (f) comparison-to-prior-work table with explicit "[our work]" row. For DCAT keep (a)–(e); the prior-work comparison should be a modest, honest table — not the paper's center.
- **Analysis/discussion:** the compact paper merges analysis into Results; the extended paper titles its section "Results and discussions" but really presents. Neither has a true discussion section. **Lesson for DCAT:** a separate Discussion that interprets (why cross-attention helps/hurts where, efficiency trade-offs, corpus characteristics) is an improvement over both references — adopt it.
- **Limitations:** neither paper has a real limitations section (a weakness of both). DCAT should keep its Limitations/Threats-to-Validity section — this is a deliberate improvement over the reference pattern, not a deviation from it.
- **Conclusion:** two paragraphs — (1) recap of what was done + benefits, (2) summary of findings + future work. Never introduces new results.
- **References:** numeric, citation-order (Springer style), 57–81 entries, heavy use of well-known venues; references are integrated as bracketed numbers mid-sentence, not footnoted.
- **Formal back matter:** Data Availability, Declarations/Competing interests, Publisher's Note. These give the "published" feel; DCAT's LaTeX template should carry equivalents.

### 2.3 Narrative progression (both papers)

1. Domain is valuable → 2. domain has a defect → 3. learning methods can find the defect → 4. here is the gap in existing detection practice → 5. our N-step approach (with overview figure) → 6. each step in detail with data sizes → 7. protocol + metrics → 8. numbers, ours first, then comparison → 9. what it means + future work.

Detail budget: intro ≈ 15–20% of body; related work ≈ 15%; methodology ≈ 35–45% (the largest share); results ≈ 20–30%; conclusion ≤ 5%. The extended paper spends nearly half its body on methodology-side material (feature engineering, imbalance handling, per-classifier explanations); this is where its 44 pages legitimately come from.

---

## 3. Presentation blueprint

- **Paragraph length:** predominantly 90–150 words; one idea per paragraph; paragraphs never run over ~15 lines. Result-narration paragraphs are shorter and numeric.
- **Information density:** high but concrete — nearly every methodological sentence carries a countable quantity (files, columns, dimensions, fold counts, percentages). Vague intensifiers are rare; numbers do the emphasizing.
- **Academic tone:** impersonal and declarative; "we" is used for actions (we collected, we trained, we observed), never for opinions. No rhetorical questions, no first-person anecdotes, no exclamation.
- **Tense conventions:** past tense for what was done (collected, trained, achieved); present tense for general truths and properties (is immutable, operates by); present for standing claims in abstract's final sentence.
- **Terminology introduction:** every new term is expanded at first mention with acronym in parentheses — "Multilabel k Nearest Neighbours (MLkNN)", "Term frequency–inverse document frequency (TF-IDF)" — then used as acronym thereafter. This is disciplined and consistent; it is a major polish signal.
- **Citation placement:** bracketed numerals attached to the *noun* being credited ("Bitcoin [37]", "the SmartBugs dataset [17]"), at first mention of every tool, dataset, algorithm, and attack. Surveys get grouped citations "[1, 2]". No citation-free claims about prior art; no citations for our own results.
- **Equations:** numbered `(1)…(n)` right-aligned; symbols defined immediately after or inline before; each equation introduced by a sentence stating what it computes; used for metric definitions and one core model formulation. Not every trivial arithmetic step is displayed.
- **Tables:** caption **above**, numbered in citation order; introduced in prose ("Table 1 shows …"); best values highlighted (red/bold); multi-page tables allowed with "continued" headers; columns organized by model/condition, rows by metric or class.
- **Figures:** caption **below**, short noun phrase ("Fig. 1 Complete flow diagram of TP-Detect"), never a full sentence; figures are referenced in order and each is *interpreted* in body text ("Figure 5 quantifies … the comparative analysis of each model's F1-Score"); pipeline diagrams early in methodology, result plots in results.
- **Result narration:** state the number, the condition, and the comparison in one sentence ("The Naive Bayes model achieves F1-scores of 99.38% and 99.44% using Binary Relevance and Classifier Chain respectively"), then one interpretive sentence. Numbers in prose always match the table.
- **Discussion style:** interpretive but brief; contrasts are factual, not rhetorical; weaknesses of alternatives are stated as scope limits ("are confined to addressing feature variations, data imbalance") rather than attacks.
- **Claim qualification:** novelty hedged ("To the best of our knowledge, this … has been used for the first time"); superiority claims always tied to a metric and a comparison set; no absolute claims ("best ever").
- **Contribution presentation:** bullets in intro; re-stated in abstract; re-asserted in conclusion — three-point consistency.
- **Transition style:** mostly explicit and functional ("In this section…", "The rest of the paper is organized as follows", "Considering this fact…", "In the following section how each model has performed…"). Sentences like these open and close sections; paragraphs begin with the section's job, not with summaries of the previous one.
- **Formal publication conventions:** received/accepted dates, corresponding-author footnotes with emails, DOI header, license block, Data Availability, Declarations, Publisher's Note, running heads with journal/volume/page. Together these are what make the artifact feel like a journal paper rather than a report.

---

## 4. What makes them look like real published research

1. **Journal front matter and back matter** — DOI header, dates, author footnotes, Data Availability, Declarations, licence/Publisher's Note.
2. **Named, countable artifacts** — the dataset has a name and every pipeline stage reports concrete dimensions (files, rows, columns, feature counts, fold counts). Nothing is described only qualitatively.
3. **Disciplined terminology introduction** — acronym-at-first-mention for every technical term, then consistent acronym use.
4. **Numbered equations for metrics** with symbol definitions, referenced by number in text.
5. **Float discipline** — every figure/table cited in numeric order, captions in the right position, results highlighted, and interpretation carried by body text rather than captions.
6. **Numbers quoted verbatim in prose** — the results narrative repeats table values, so the prose alone carries the findings.
7. **Hedged, evidence-anchored claims** — novelty and superiority claims are scoped ("among the algorithms tested", "compared to the models used in prior works").
8. **A staged methodology with an overview figure** — the reader always knows where they are in the pipeline.
9. **A contribution list in the introduction** and its three-point echo (abstract → intro → conclusion).
10. **A comparison table with an explicit "[our work]" row** — situates the work without becoming the paper's center.
11. **Consistent citation style** — numeric brackets on every creditable noun; 57–81 references show saturated engagement with the literature.
12. **Single-idea paragraphs** of moderate length — the layout itself signals professional editing.

---

## 5. What NOT to copy

**Adopt (general presentation principles):** the structures, conventions, and stylistic disciplines in §§2–4 — funnel intro + contribution bullets, staged methodology, dedicated setup section, metrics-as-equations, float/caption discipline, hedged claims, formal back matter, naming convention for artifacts, verbatim number narration.

**Do NOT copy (domain/paper-specific):**

| Category | Specifics from the reference papers |
|---|---|
| Domain structures | Smart-contract/blockchain tutorials; vulnerability taxonomies (DASP top-10); blockchain-platform comparison tables; attack-incident tables; per-vulnerability code listings; NLP-for-Solidity framing; 51%-attack / eclipse-attack challenges section |
| Terminology | TriPix dataset, TP-Detect, SolMatrix, Solgraph, SmartiAudit; opcode/trigram/pixel-value vocabulary; multi-label vs multi-class framing tied to their labels |
| Experiments | Binary Relevance vs Classifier Chain training strategies; MLkNN/BRkNN/RF/NB suite; TF-IDF/CBOW/Skip-gram feature-set comparison; 36-model ensemble matrix; 5-fold CV as their headline robustness experiment |
| Claims | "NB outperforms…", "TriPix outperforms models employed in either opcode characteristics or image-based detection", "near 90% accuracy with SMOTE…AUC near 0.7" — none transfer |
| Datasets | SmartBugs (47,587 contracts), SWC Registry, Etherscan scrapes, not-so-smart-contracts |
| Equations | Their precision/recall/F1 block, TF-IDF objective, AGF/AGM/AM/AUCI definitions, Kappa/MCC presentations |
| Comparisons | Their Table 2 (tool-vs-tool) and Table 6 (ensemble-vs-prior-tools with "[our work]" row); Dynamit/Eth2Vec/ESCORT/ContractWard rows |

**Boundary rule.** If a sentence, table row, figure, or equation would only make sense in a blockchain/smart-contract paper, it belongs to the reference papers' domain, not to the presentation system. The *shape* of their comparison table is adoptable; its *content* is not.

---

## 6. DCAT TARGET PAPER PROFILE

The regenerated DCAT paper should read like a **self-contained journal article on conditional multimodal email spam classification**, publishable without any knowledge of any prior project document.

- **Structure:** funnel introduction with explicit contribution bullets and roadmap; separate Related Work organized by approach family (text-based, image-based, multimodal fusion, conditional computation) that ends by stating the gap; Problem Formulation; DCAT Methodology as a staged, figure-anchored pipeline (encoders → projection → bidirectional cross-attention → fusion → classifier → early exit → training); separate Experimental Methodology (dataset and processing, splits and leakage control, variants, metrics, statistical protocol); Results organized around research questions; a true Discussion; Limitations and Threats to Validity; Conclusion; formal back matter.
- **Depth:** comprehensive, not padded. Length comes from (a) teaching exactly the concepts the method needs (email modalities, text/image representation, attention, cross-attention, conditional computation, early exit), (b) fully specified methodology with dimensions and settings, (c) complete result documentation with per-condition numbers, (d) interpretation of every ablation. No repetition, no generic textbook chapters, no literature padding.
- **Narrative:** every section earns the next. By the end of Related Work the reader can state the gap; by the end of Methodology the reader could re-implement DCAT; by the end of Results the reader knows what each component contributes; the Discussion converts findings into meaning; Limitations bound the claims honestly.
- **Technical explanation:** every component gets what → why → how with concrete dimensions (embedding sizes, sequence lengths, image resolutions, parameter counts, latency where measured); terminology introduced acronym-at-first-mention and used consistently; the framework is named (DCAT) and its variants named, then used as stable vocabulary.
- **Academic tone:** impersonal, hedged where evidence is thin ("comparable accuracy", "statistically significant improvement on the multimodal subset"), past tense for actions, present for properties; the well-known honest finding that DCAT matches rather than beats baseline accuracy is presented as an efficiency/scarcity result, never spun as a superiority claim.
- **Figures:** pipeline/architecture figure(s) in methodology; a small number of high-value result figures (efficiency vs accuracy, confusion matrix, per-condition bars if supported); short noun-phrase captions; all interpretation in text.
- **Tables:** dataset composition, variant/configuration table, primary results with best values highlighted, ablation summary, efficiency table, statistical-test summary. Best values marked; every table introduced and narrated in prose.
- **Equations:** numbered and symbol-defined — task/objective in Problem Formulation, cross-attention and fusion in Methodology, exit criterion, and metric definitions. Only what is needed to re-implement or grade the work.
- **Citations:** numeric, bracketed, attached to every creditable claim and tool; 40–70 well-chosen references; the reference papers, where relevant, appear as ordinary related-work citations under their true identities — never as a structural anchor.
- **Results:** protocol restated first; metrics defined; own results before any external comparison; best values highlighted; every number in prose matches its table; comparisons to prior work limited to one honest table.
- **Discussion:** interprets why cross-attention and early exit behave as observed on a text-dominated corpus; explains the multimodal-scarcity setting; ties efficiency gains to the accuracy trade-off; no new results.
- **Overall professionalism:** journal-grade front/back matter, disciplined floats, verbatim number narration, consistent named artifacts, and claims that are always traceable to a table, figure, or equation in the paper. **Comprehensive by teaching, never by padding.**
