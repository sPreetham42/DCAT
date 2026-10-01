# -*- coding: utf-8 -*-
import sys
import codecs

with codecs.open('paper/PAPER_CONTENT.md', 'r', encoding='utf-8') as f:
    text = f.read()

ref_idx = text.find('## References')
if ref_idx != -1:
    text = text[:ref_idx] + '''## References

1. Apache Software Foundation, "SpamAssassin Public Corpus," 2006. [Online]. Available: https://spamassassin.apache.org/old/publiccorpus/
2. J. J. Lohith, A. Purushotam, A. Mullangi, and A. Sharma, "MDL-SPAM: A Multi Model Deep Learning Framework for Email Spam Detection Using VGG-16 and LSTM," Multimedia Tools and Applications, 2023.
3. F. Jáñez-Martino, R. Alaiz-Rodríguez, V. González-Castro, E. Fidalgo, and E. Alegre, "A review of spam email detection: analysis of spammer strategies and the dataset shift problem," Artificial Intelligence Review, vol. 56, pp. 1145–1173, 2023.
4. V. Sanh, L. Debut, J. Chaumond, and T. Wolf, "DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter," arXiv preprint arXiv:1910.01108, 2019.
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
17. A. G. Howard et al., "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications," arXiv preprint arXiv:1704.04861, 2017.
18. Y. Kim, "Convolutional Neural Networks for Sentence Classification," EMNLP, 2014.
19. X. Zhang, J. Zhao, and Y. LeCun, "Character-level Convolutional Networks for Text Classification," NeurIPS, 2015.
20. S. Hochreiter and J. Schmidhuber, "Long short-term memory," Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997.
21. Y. Liu et al., "RoBERTa: A Robustly Optimized BERT Pretraining Approach," arXiv preprint arXiv:1907.11692, 2019.
22. D. Bahdanau, K. Cho, and Y. Bengio, "Neural Machine Translation by Jointly Learning to Align and Translate," ICLR, 2015.
23. S. Teerapittayanon, B. McDanel, and H. T. Kung, "BranchyNet: Fast inference via early exiting from deep neural networks," ICPR, 2016.
24. A. Annadatha and M. Stamp, "Image spam analysis and detection," Journal of Computer Virology and Hacking Techniques, vol. 14, no. 1, pp. 39-52, 2016.

---

## Uncertainty Markers and Verification Items

The following items have been verified for the final submission:

- `[VERIFY EARLY-EXIT METRICS]`: Verified against `artifacts/final_results/efficiency_summary.csv`. The +24.82% latency increase reflects the real-world overhead of conditional branching and early-exit classifier evaluation, which offsets the 0.63% theoretical FLOP reduction.

- `[VERIFY DATASET COUNT]`: Verified against `data/manifests/leakage_groups.csv`. The full repository corpus encompasses 73,500+ samples, but the controlled SpamAssassin subset rigorously evaluated for multimodal performance consists of 6,046 emails.

- `[VERIFY SPLIT RATIO]`: The configuration specifies 70/15/15 for standard training, while the 5-Fold Cross-Validation evaluates on 20% validation folds. 

- `[VERIFY: LEAKAGE AUDIT SCOPE]`: Verified against `artifacts/leakage_audit/leakage_audit.json`. The perceptual leakage audit was executed as a pilot run (2 records) due to computational constraints, demonstrating the methodology. Exact textual and hash-based deduplication was applied to the full dataset.
'''

text = text.replace('and Random Forests~\cite{ref13}', 'and Random Forests~\cite{ref3}')
text = text.replace('gating mechanisms~\cite{ref13}', 'gating mechanisms~\cite{ref14}')
text = text.replace('~\cite{zhang2015character}', '~\cite{ref19}')
text = text.replace('~\cite{kim2014convolutional}', '~\cite{ref18}')
text = text.replace('~\cite{hochreiter1997long}', '~\cite{ref20}')
text = text.replace('~\cite{liu2019roberta}', '~\cite{ref21}')
text = text.replace('~\cite{ref15}', '~\cite{ref24}')
text = text.replace('VGG, ResNet, MobileNet', 'VGG~\cite{ref15}, ResNet~\cite{ref16}, MobileNet~\cite{ref17}')
text = text.replace('~\cite{ref3}', '~\cite{ref2}')
text = text.replace('~\cite{bahdanau2014neural}', '~\cite{ref22}')
text = text.replace('~\cite{ref16}', '~\cite{ref23}')
text = text.replace('baseline (MMTD reimplementation', 'baseline (MMTD~\cite{ref13} reimplementation')
text = text.replace('Published Baseline (MMTD reimplementation)', 'Published Baseline (MMTD~\cite{ref13} reimplementation)')

with codecs.open('paper/PAPER_CONTENT.md', 'w', encoding='utf-8') as f:
    f.write(text)
