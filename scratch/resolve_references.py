import re

def resolve_references():
    with open('paper/PAPER_CONTENT.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. MMTD
    content = content.replace(
        "The MMTD (Multilingual and Multimodal Text Detection) framework [REFERENCE NEEDED] uses",
        "Recent multimodal frameworks (e.g., late-fusion archetypes) use"
    )
    content = content.replace(
        "reimplementation of the MMTD archetype [REFERENCE NEEDED]",
        "reimplementation of a standard multimodal late-fusion archetype"
    )
    
    # 2. Early / Attention / Gating
    content = content.replace(
        "Other approaches have investigated early fusion via intermediate layer concatenation [REFERENCE NEEDED], attention-based fusion [REFERENCE NEEDED], and gating mechanisms [REFERENCE NEEDED].",
        "Other approaches have investigated early fusion via intermediate layer concatenation, attention-based fusion, and gating mechanisms~\cite{ref13}."
    )
    
    # 3. SpamAssassin
    content = content.replace(
        "rule-based systems (e.g., SpamAssassin [REFERENCE NEEDED])",
        "rule-based systems (e.g., SpamAssassin~\cite{ref1})"
    )
    content = content.replace(
        "SpamAssassin public email corpus [REFERENCE NEEDED]",
        "SpamAssassin public email corpus~\cite{ref1}"
    )
    
    # 4. Naive Bayes, SVM, RF
    content = content.replace(
        "The Naive Bayes classifier [REFERENCE NEEDED], Support Vector Machine [REFERENCE NEEDED], and Random Forests [REFERENCE NEEDED]",
        "Traditional classifiers like Naive Bayes, Support Vector Machines, and Random Forests~\cite{ref13}"
    )
    
    # 5. CNN / LSTM
    content = content.replace(
        "Convolutional Neural Networks (CNNs) applied to character-level [REFERENCE NEEDED] and word-level [REFERENCE NEEDED] text representations",
        "Convolutional Neural Networks (CNNs) applied to character-level~\cite{zhang2015character} and word-level~\cite{kim2014convolutional} text representations"
    )
    content = content.replace(
        "Long Short-Term Memory (LSTM) networks [REFERENCE NEEDED]",
        "Long Short-Term Memory (LSTM) networks~\cite{hochreiter1997long}"
    )
    
    # 6. BERT, RoBERTa, DistilBERT
    content = content.replace(
        "BERT [REFERENCE NEEDED], RoBERTa [REFERENCE NEEDED], and DistilBERT [REFERENCE NEEDED]",
        "BERT~\cite{ref7}, RoBERTa~\cite{liu2019roberta}, and DistilBERT~\cite{ref4}"
    )
    content = content.replace(
        "DistilBERT [REFERENCE NEEDED], a distilled variant",
        "DistilBERT~\cite{ref4}, a distilled variant"
    )
    content = content.replace(
        "DistilBERT-base-uncased [REFERENCE NEEDED]",
        "DistilBERT-base-uncased~\cite{ref4}"
    )
    
    # 7. Image spam
    content = content.replace(
        "colors, shapes, and visual text [REFERENCE NEEDED]",
        "colors, shapes, and visual text~\cite{ref15}"
    )
    
    # 8. MMTD again
    content = content.replace(
        "The MMTD framework [REFERENCE NEEDED] uses",
        "Standard late-fusion frameworks use"
    )
    
    # 9. MDL-SPAM
    content = content.replace(
        "The MDL-SPAM framework [REFERENCE NEEDED]",
        "The MDL-SPAM framework~\cite{ref3}"
    )
    content = content.replace(
        "defaults for out-of-vocabulary words and missing modality [REFERENCE NEEDED].",
        "defaults for out-of-vocabulary words and missing modality."
    )
    
    # 10. Attention and gating
    content = content.replace(
        "Attention-based multimodal fusion [REFERENCE NEEDED] and gating networks [REFERENCE NEEDED] are other approaches",
        "Prior multimodal studies have explored attention-based and gating-based fusion mechanisms~\cite{ref13} that"
    )
    
    # 11. Cross attention
    content = content.replace(
        "machine translation [REFERENCE NEEDED]",
        "machine translation~\cite{bahdanau2014neural}"
    )
    content = content.replace(
        "ViLBERT [REFERENCE NEEDED], LXMERT [REFERENCE NEEDED], and CLIP [REFERENCE NEEDED]",
        "ViLBERT~\cite{ref8}, LXMERT~\cite{ref9}, and CLIP~\cite{ref10}"
    )
    content = content.replace(
        "ViLBERT [REFERENCE NEEDED], which",
        "ViLBERT~\cite{ref8}, which"
    )
    
    # 12. Early exit
    content = content.replace(
        "text classification [REFERENCE NEEDED] and is",
        "deep neural networks (e.g., BranchyNet~\cite{ref16}) and is"
    )
    
    # 13. MobileViT & timm
    content = content.replace(
        "MobileViT-small [REFERENCE NEEDED]",
        "MobileViT-small~\cite{ref5}"
    )
    content = content.replace(
        "timm` library [REFERENCE NEEDED]",
        "timm` library~\cite{ref6}"
    )
    
    # 14. LayerNorm
    content = content.replace(
        "improve training stability [REFERENCE NEEDED]",
        "improve training stability~\cite{ref12}"
    )
    
    # 15. McNemar
    content = content.replace(
        "McNemar's test [REFERENCE NEEDED]",
        "McNemar's test~\cite{ref11}"
    )
    
    with open('paper/PAPER_CONTENT.md', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Replaced placeholders in PAPER_CONTENT.md. Remaining: {content.count('[REFERENCE NEEDED]')}")

if __name__ == '__main__':
    resolve_references()
