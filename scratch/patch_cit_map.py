import re

def patch_cit_map():
    with open('scratch/convert_to_latex.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_cit_map = """    cit_map = [
        r'\\textbf{[[REF_MISSING]]}', # 00: lure content
        r'\\cite{ref2}', # 01: communication channel
        r'\\cite{ref3}', # 02: joint text-image classification
        r'\\textbf{[[REF_MISSING]]}', # 03: MMTD framework intro
        r'\\textbf{[[REF_MISSING]]}', # 04: intermediate layer concatenation
        r'\\textbf{[[REF_MISSING]]}', # 05: attention-based fusion
        r'\\textbf{[[REF_MISSING]]}', # 06: gating mechanisms
        r'\\cite{ref1}', # 07: SpamAssassin
        r'\\textbf{[[REF_MISSING]]}', # 08: Naive Bayes
        r'\\textbf{[[REF_MISSING]]}', # 09: SVM
        r'\\textbf{[[REF_MISSING]]}', # 10: Random Forests
        r'\\textbf{[[REF_MISSING]]}', # 11: character-level
        r'\\textbf{[[REF_MISSING]]}', # 12: word-level
        r'\\textbf{[[REF_MISSING]]}', # 13: LSTM
        r'\\cite{ref7}', # 14: BERT
        r'\\textbf{[[REF_MISSING]]}', # 15: RoBERTa
        r'\\cite{ref4}', # 16: DistilBERT
        r'\\cite{ref4}', # 17: DistilBERT again
        r'\\cite{ref15}', # 18: visual text
        r'\\textbf{[[REF_MISSING]]}', # 19: MMTD framework related work
        r'\\cite{ref3}', # 20: MDL-SPAM
        r'\\cite{ref3}', # 21: missing modality
        r'\\textbf{[[REF_MISSING]]}', # 22: Attention-based multimodal fusion
        r'\\textbf{[[REF_MISSING]]}', # 23: gating networks
        r'\\textbf{[[REF_MISSING]]}', # 24: machine translation
        r'\\cite{ref8}', # 25: ViLBERT
        r'\\cite{ref9}', # 26: LXMERT
        r'\\cite{ref10}', # 27: CLIP
        r'\\cite{ref8}', # 28: ViLBERT co-attention
        r'\\cite{ref16}', # 29: text classification early exit
        r'\\cite{ref4}', # 30: DistilBERT-base-uncased
        r'\\cite{ref5}', # 31: MobileViT-small
        r'\\cite{ref6}', # 32: timm library
        r'\\cite{ref12}', # 33: training stability
        r'\\cite{ref1}', # 34: public email corpus
        r'\\textbf{[[REF_MISSING]]}', # 35: MMTD archetype
        r'\\cite{ref11}', # 36: McNemar test
    ]"""
    
    # Replace the cit_map array in the file
    content = re.sub(r'    cit_map = \[.*?\]', new_cit_map, content, flags=re.DOTALL)
    
    with open('scratch/convert_to_latex.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    patch_cit_map()
