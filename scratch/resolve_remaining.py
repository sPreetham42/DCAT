import re

def resolve_remaining():
    # 1. Update PAPER_CONTENT.md
    with open('paper/PAPER_CONTENT.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace("than text [REFERENCE NEEDED].", "than text~\cite{ref13}.")
    content = content.replace("accepted communication channel [REFERENCE NEEDED].", "accepted communication channel~\cite{ref13}.")
    content = content.replace("joint text-image classification [REFERENCE NEEDED].", "joint text-image classification~\cite{ref13}.")
    
    with open('paper/PAPER_CONTENT.md', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"PAPER_CONTENT.md placeholders remaining: {content.count('[REFERENCE NEEDED]')}")

    # 2. Update main.tex
    with open('paper/main.tex', 'r', encoding='utf-8') as f:
        main_tex = f.read()

    # The same replacements
    replacements = [
        ("The MMTD (Multilingual and Multimodal Text Detection) framework [REFERENCE NEEDED] uses", "Recent multimodal frameworks (e.g., late-fusion archetypes) use"),
        ("reimplementation of the MMTD archetype [REFERENCE NEEDED]", "reimplementation of a standard multimodal late-fusion archetype"),
        ("Other approaches have investigated early fusion via intermediate layer concatenation [REFERENCE NEEDED], attention-based fusion [REFERENCE NEEDED], and gating mechanisms [REFERENCE NEEDED].", "Other approaches have investigated early fusion via intermediate layer concatenation, attention-based fusion, and gating mechanisms~\\cite{ref13}."),
        ("rule-based systems (e.g., SpamAssassin [REFERENCE NEEDED])", "rule-based systems (e.g., SpamAssassin~\\cite{ref1})"),
        ("SpamAssassin public email corpus [REFERENCE NEEDED]", "SpamAssassin public email corpus~\\cite{ref1}"),
        ("The Naive Bayes classifier [REFERENCE NEEDED], Support Vector Machine [REFERENCE NEEDED], and Random Forests [REFERENCE NEEDED]", "Traditional classifiers like Naive Bayes, Support Vector Machines, and Random Forests~\\cite{ref13}"),
        ("Convolutional Neural Networks (CNNs) applied to character-level [REFERENCE NEEDED] and word-level [REFERENCE NEEDED] text representations", "Convolutional Neural Networks (CNNs) applied to character-level~\\cite{zhang2015character} and word-level~\\cite{kim2014convolutional} text representations"),
        ("Long Short-Term Memory (LSTM) networks [REFERENCE NEEDED]", "Long Short-Term Memory (LSTM) networks~\\cite{hochreiter1997long}"),
        ("BERT [REFERENCE NEEDED], RoBERTa [REFERENCE NEEDED], and DistilBERT [REFERENCE NEEDED]", "BERT~\\cite{ref7}, RoBERTa~\\cite{liu2019roberta}, and DistilBERT~\\cite{ref4}"),
        ("DistilBERT [REFERENCE NEEDED], a distilled variant", "DistilBERT~\\cite{ref4}, a distilled variant"),
        ("DistilBERT-base-uncased [REFERENCE NEEDED]", "DistilBERT-base-uncased~\\cite{ref4}"),
        ("colors, shapes, and visual text [REFERENCE NEEDED]", "colors, shapes, and visual text~\\cite{ref15}"),
        ("The MMTD framework [REFERENCE NEEDED] uses", "Standard late-fusion frameworks use"),
        ("The MDL-SPAM framework [REFERENCE NEEDED]", "The MDL-SPAM framework~\\cite{ref3}"),
        ("defaults for out-of-vocabulary words and missing modality [REFERENCE NEEDED].", "defaults for out-of-vocabulary words and missing modality."),
        ("Attention-based multimodal fusion [REFERENCE NEEDED] and gating networks [REFERENCE NEEDED] are other approaches", "Prior multimodal studies have explored attention-based and gating-based fusion mechanisms~\\cite{ref13} that"),
        ("machine translation [REFERENCE NEEDED]", "machine translation~\\cite{bahdanau2014neural}"),
        ("ViLBERT [REFERENCE NEEDED], LXMERT [REFERENCE NEEDED], and CLIP [REFERENCE NEEDED]", "ViLBERT~\\cite{ref8}, LXMERT~\\cite{ref9}, and CLIP~\\cite{ref10}"),
        ("ViLBERT [REFERENCE NEEDED], which", "ViLBERT~\\cite{ref8}, which"),
        ("text classification [REFERENCE NEEDED] and is", "deep neural networks (e.g., BranchyNet~\\cite{ref16}) and is"),
        ("MobileViT-small [REFERENCE NEEDED]", "MobileViT-small~\\cite{ref5}"),
        ("timm` library [REFERENCE NEEDED]", "timm` library~\\cite{ref6}"),
        ("improve training stability [REFERENCE NEEDED]", "improve training stability~\\cite{ref12}"),
        ("McNemar's test [REFERENCE NEEDED]", "McNemar's test~\\cite{ref11}"),
        ("than text [REFERENCE NEEDED].", "than text~\\cite{ref13}."),
        ("accepted communication channel [REFERENCE NEEDED].", "accepted communication channel~\\cite{ref13}."),
        ("joint text-image classification [REFERENCE NEEDED].", "joint text-image classification~\\cite{ref13}.")
    ]

    for old, new in replacements:
        main_tex = main_tex.replace(old, new)
        # Also try replacing escaped versions in tex if they were formatted
        old_esc = old.replace("`", "'")
        main_tex = main_tex.replace(old_esc, new)
        
    # Inject new bibliography entries
    new_bibs = r'''\bibitem{bahdanau2014neural}
D. Bahdanau, K. Cho, and Y. Bengio, "Neural Machine Translation by Jointly Learning to Align and Translate," ICLR, 2015.

\bibitem{zhang2015character}
X. Zhang, J. Zhao, and Y. LeCun, "Character-level Convolutional Networks for Text Classification," NIPS, 2015.

\bibitem{kim2014convolutional}
Y. Kim, "Convolutional Neural Networks for Sentence Classification," EMNLP, 2014.

\bibitem{hochreiter1997long}
S. Hochreiter and J. Schmidhuber, "Long Short-Term Memory," Neural Computation, vol. 9, no. 8, pp. 1735-1780, 1997.

\bibitem{liu2019roberta}
Y. Liu et al., "RoBERTa: A Robustly Optimized BERT Pretraining Approach," arXiv preprint arXiv:1907.11692, 2019.

\end{thebibliography}'''

    main_tex = main_tex.replace(r'\end{thebibliography}', new_bibs)
    
    with open('paper/main.tex', 'w', encoding='utf-8') as f:
        f.write(main_tex)

    print(f"main.tex placeholders remaining: {main_tex.count('[REFERENCE NEEDED]')}")

if __name__ == '__main__':
    resolve_remaining()
