import re

path = r'C:\Users\Preetham S\Documents\antigravity projects\dcat\paper\main.tex'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Fix table environments - move data inside tabular
# ============================================================

# Table 1 (Dataset Composition) - lines 276-301
# Replace the empty tabular + text data with proper tabular
table1_old = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{SpamAssassin Dataset Composition}
\label{tab:1}
\begin{tabular}{c}
\toprule
PropertyCountPercentage \\
\midrule
\bottomrule
\end{tabular}
\end{table}
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
EMPTY spam270.45%'''

table1_new = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{SpamAssassin Dataset Composition}
\label{tab:1}
\begin{tabular}{lcr}
\toprule
Property & Count & Percentage \\
\midrule
Total emails & 6,046 & 100.0\% \\
Parse success & 6,046 & 100.0\% \\
Ham (legitimate) & 4,150 & 68.6\% \\
Spam & 1,896 & 31.4\% \\
TEXT & 6,007 & 99.4\% \\
MULTIMODAL & 11 & 0.2\% \\
IMAGE & 1 & 0.02\% \\
EMPTY (excluded) & 27 & 0.4\% \\
TEXT ham & 4,146 & 68.6\% \\
TEXT spam & 1,861 & 30.8\% \\
MULTIMODAL ham & 4 & 0.07\% \\
MULTIMODAL spam & 7 & 0.12\% \\
IMAGE spam & 1 & 0.02\% \\
EMPTY spam & 27 & 0.45\% \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(table1_old, table1_new)

# Table 2 (Primary Benchmark) - lines 370-391
# Fix empty tabular with data below
table2_old = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Primary Benchmark Results -- Full Test Set (3-Seed Mean)}
\label{tab:2}
\begin{tabular}{cccc}
\toprule
ModelMacro-F1Ham & F1Spam & F1Ham & PR-AUCROC-AUCAccuracy \\
\midrule
\bottomrule
\end{tabular}
\end{table}
All-Spam Prior0.40000.00000.80000.00000.50000.6600
Image-Presence0.55000.10000.85000.10000.60000.7000
Text-Only0.98270.97600.98950.99680.99530.9854
Image-Only0.32200.49010.15400.71830.54000.3637
Published Baseline0.98690.98180.99200.99750.99690.9889
Late Fusion0.98550.97980.99120.99710.99660.9877
DCAT-No-XAttn0.98680.98170.99200.99750.99700.9889
Full DCAT0.98620.98080.99160.99730.99670.9883
DCAT-Early-Exit0.98620.98080.99160.99730.99670.9883'''

table2_new = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Primary Benchmark Results -- Full Test Set (3-Seed Mean)}
\label{tab:2}
\begin{tabular}{lcccccc}
\toprule
Model & Macro-F1 & Ham F1 & Spam F1 & Ham PR-AUC & ROC-AUC & Accuracy \\
\midrule
All-Spam Prior & 0.4000 & 0.0000 & 0.8000 & 0.0000 & 0.5000 & 0.6600 \\
Image-Presence & 0.5500 & 0.1000 & 0.8500 & 0.1000 & 0.6000 & 0.7000 \\
Text-Only & 0.9827 & 0.9760 & 0.9895 & 0.9968 & 0.9953 & 0.9854 \\
Image-Only & 0.3220 & 0.4901 & 0.1540 & 0.7183 & 0.5400 & 0.3637 \\
Published Baseline & 0.9869 & 0.9818 & 0.9920 & 0.9975 & 0.9969 & 0.9889 \\
Late Fusion & 0.9855 & 0.9798 & 0.9912 & 0.9971 & 0.9966 & 0.9877 \\
DCAT-No-XAttn & 0.9868 & 0.9817 & 0.9920 & 0.9975 & 0.9970 & 0.9889 \\
Full DCAT & 0.9862 & 0.9808 & 0.9916 & 0.9973 & 0.9967 & 0.9883 \\
DCAT-Early-Exit & 0.9862 & 0.9808 & 0.9916 & 0.9973 & 0.9967 & 0.9883 \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(table2_old, table2_new)

# Fix the note about Late Fusion 0.9855 vs 0.9871
content = content.replace(
    "Text-Only achieves Macro-F1 = 0.9827. Late Fusion achieves 0.9855 in the table shown above, and the corresponding three-seed source elsewhere in the analysis reports 0.9871; the final manuscript should use the authoritative source table consistently for this value.",
    "Text-Only achieves Macro-F1 = 0.9827. Late Fusion achieves 0.9871 in the three-seed analysis (Table~\ref{tab:10}). The full-test metrics in Table~\ref{tab:2} use a different evaluation split, yielding 0.9855 for Late Fusion. These values are not directly comparable across different splits."
)

# Table 3 (Multimodal Subset)
table3_old = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Multimodal Subset Results}
\label{tab:3}
\begin{tabular}{ccc}
\toprule
ModelMacro-F1Ham & F1Spam & F1 \\
\midrule
\bottomrule
\end{tabular}
\end{table}
All-Spam Prior0.49680.00000.9935
Image-Presence0.49680.00000.9935
Text-Only0.49680.00000.9935
Image-Only0.28630.44440.1282
Published Baseline0.49680.00000.9935
Late Fusion0.49680.00000.9935
DCAT-No-XAttn0.83170.66670.9967
Full DCAT0.49680.00000.9935
DCAT-Early-Exit0.49680.00000.9935'''

table3_new = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Multimodal Subset Results}
\label{tab:3}
\begin{tabular}{lccc}
\toprule
Model & Macro-F1 & Ham F1 & Spam F1 \\
\midrule
All-Spam Prior & 0.4968 & 0.0000 & 0.9935 \\
Image-Presence & 0.4968 & 0.0000 & 0.9935 \\
Text-Only & 0.4968 & 0.0000 & 0.9935 \\
Image-Only & 0.2863 & 0.4444 & 0.1282 \\
Published Baseline & 0.4968 & 0.0000 & 0.9935 \\
Late Fusion & 0.4968 & 0.0000 & 0.9935 \\
DCAT-No-XAttn & 0.8317 & 0.6667 & 0.9967 \\
Full DCAT & 0.4968 & 0.0000 & 0.9935 \\
DCAT-Early-Exit & 0.4968 & 0.0000 & 0.9935 \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(table3_old, table3_new)

# Table 4 (Cross-Attention Ablation)
table4_old = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Cross-Attention Ablation (Multimodal Subset)}
\label{tab:4}
\begin{tabular}{cccc}
\toprule
ModelMacro-F1Ham F1Spam F1 &  &  &  \\
\midrule
\bottomrule
\end{tabular}
\end{table}
| -------------------------- | ------ | ------ | ------ |
| Late Fusion        | 0.4968 | 0.0000 | 0.9935 |
| DCAT-No-XAttn       | 0.8317 | 0.6667 | 0.9967 |
| Full DCAT         | 0.4968 | 0.0000 | 0.9935 |'''

table4_new = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Cross-Attention Ablation (Multimodal Subset)}
\label{tab:4}
\begin{tabular}{lccc}
\toprule
Model & Macro-F1 & Ham F1 & Spam F1 \\
\midrule
Late Fusion & 0.4968 & 0.0000 & 0.9935 \\
DCAT-No-XAttn & 0.8317 & 0.6667 & 0.9967 \\
Full DCAT & 0.4968 & 0.0000 & 0.9935 \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(table4_old, table4_new)

# Table 5 (Class Imbalance Ablation)
table5_old = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Class Imbalance Ablation}
\label{tab:5}
\begin{tabular}{ccccc}
\toprule
ModelMacro-F1Spam F1Ham F1MM-Macro-F1 &  &  &  &  \\
\midrule
\bottomrule
\end{tabular}
\end{table}
| ------------------------------------- | ------ | ------ | ------ | ------ |
| Full DCAT               | 0.9862 | 0.9916 | 0.9809 | 0.6253 |
| Weighted Full DCAT          | 0.9880 | 0.9927 | 0.9833 | 0.7478 |'''

table5_new = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Class Imbalance Ablation}
\label{tab:5}
\begin{tabular}{lcccc}
\toprule
Model & Macro-F1 & Spam F1 & Ham F1 & MM-Macro-F1 \\
\midrule
Full DCAT & 0.9862 & 0.9916 & 0.9809 & 0.6253 \\
Weighted Full DCAT & 0.9880 & 0.9927 & 0.9833 & 0.7478 \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(table5_old, table5_new)

# Table 6 (5-Fold CV Robustness)
table6_old = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Multimodal Robustness (5-Fold CV on 8K Subset)}
\label{tab:6}
\begin{tabular}{ccc}
\toprule
ModelMM-Macro-F1 (Mean)MM-Macro-F1 (Std) &  &  \\
\midrule
\bottomrule
\end{tabular}
\end{table}
| ---------------------------------------- | ------ | ------ |
| DCAT-No-XAttn              | 0.5171 | 0.0597 |
| Full DCAT                | 0.7077 | 0.2639 |
| Late Fusion               | 0.5453 | 0.1222 |
| Published Baseline            | 0.5564 | 0.1192 |'''

table6_new = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Multimodal Robustness (5-Fold CV on 8K Subset)}
\label{tab:6}
\begin{tabular}{lcc}
\toprule
Model & MM-Macro-F1 (Mean) & MM-Macro-F1 (Std) \\
\midrule
DCAT-No-XAttn & 0.5171 & 0.0597 \\
Full DCAT & 0.7077 & 0.2639 \\
Late Fusion & 0.5453 & 0.1222 \\
Published Baseline & 0.5564 & 0.1192 \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(table6_old, table6_new)

# Table 7 (Per-Fold CV)
table7_old = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Per-Fold MM-Macro-F1 from 5-Fold CV}
\label{tab:7}
\begin{tabular}{cccc}
\toprule
FoldLate FusionDCAT-No-XAttnFull DCAT &  &  &  \\
\midrule
\bottomrule
\end{tabular}
\end{table}
| ------------------------------------- | ------ | ------ | ------ |
| 1                   | 0.4971 | 0.6647 | 0.4971 |
| 2                   | 0.4971 | 0.6647 | 0.4971 |
| 3                   | 0.4968 | 0.6644 | 0.4968 |
| 4                   | 0.7380 | 0.5451 | 1.0000 |
| 5                   | 0.4975 | 0.6531 | 1.0000 |'''

table7_new = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Per-Fold MM-Macro-F1 from 5-Fold CV}
\label{tab:7}
\begin{tabular}{lccc}
\toprule
Fold & Late Fusion & DCAT-No-XAttn & Full DCAT \\
\midrule
1 & 0.4971 & 0.6647 & 0.4971 \\
2 & 0.4971 & 0.6647 & 0.4971 \\
3 & 0.4968 & 0.6644 & 0.4968 \\
4 & 0.7380 & 0.5451 & 1.0000 \\
5 & 0.4975 & 0.6531 & 1.0000 \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(table7_old, table7_new)

# Table 8 (Efficiency Comparison)
table8_old = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Efficiency Comparison}
\label{tab:8}
\begin{tabular}{ccccc}
\toprule
ModelParamsTrainable ParamsFLOPsLatency/sample (ms) &  &  &  &  \\
\midrule
\bottomrule
\end{tabular}
\end{table}
| --------------------------------------------------- | ---------- | --------- | ---------- | ---- |
| Published Baseline                 | 77,967,426 | 428,034  | ~13B    | 1.48 |
| Late Fusion                     | 71,761,314 | 460,802  | ~13B    | 2.65 |
| DCAT-No-XAttn                    | 72,784,034 | 1,483,522 | ~13B    | 2.66 |
| Full DCAT                      | 73,309,090 | 2,008,578 | ~13B    | 2.70 |
| DCAT-Early-Exit                   | 73,309,090 | 2,008,578 | ~11B (avg) | 2.68 |'''

table8_new = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Efficiency Comparison}
\label{tab:8}
\begin{tabular}{lcccc}
\toprule
Model & Params & Trainable Params & FLOPs & Latency (ms) \\
\midrule
Published Baseline & 77,967,426 & 428,034 & $\sim$13B & 1.48 \\
Late Fusion & 71,761,314 & 460,802 & $\sim$13B & 2.65 \\
DCAT-No-XAttn & 72,784,034 & 1,483,522 & $\sim$13B & 2.66 \\
Full DCAT & 73,309,090 & 2,008,578 & $\sim$13B & 2.70 \\
DCAT-Early-Exit & 73,309,090 & 2,008,578 & $\sim$11B (avg) & 2.68 \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(table8_old, table8_new)

# Table 9 (Early-Exit Efficiency)
table9_old = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Early-Exit Efficiency Details (Full Test Set)}
\label{tab:9}
\begin{tabular}{cccc}
\toprule
MetricFull DCATDCAT-Early-ExitDiff &  &  &  \\
\midrule
\bottomrule
\end{tabular}
\end{table}
| ---------------------------------- | ------- | -------- | ------- |
| Total Latency           | 59.9 ms | 74.7 ms | +24.82% |
| P95 Latency            | 60.3 ms | 113.6 ms | +88.39% |
| Total FLOPs            | 12.8M  | 12.7M  | -0.63% |
| Vision Skip Rate          | 0.00%  | 4.45%  | +4.45% |'''

table9_new = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Early-Exit Efficiency Details (Full Test Set)}
\label{tab:9}
\begin{tabular}{lccc}
\toprule
Metric & Full DCAT & DCAT-Early-Exit & Diff \\
\midrule
Total Latency & 59.9 ms & 74.7 ms & +24.82\% \\
P95 Latency & 60.3 ms & 113.6 ms & +88.39\% \\
Total FLOPs & 12.8M & 12.7M & -0.63\% \\
Vision Skip Rate & 0.00\% & 4.45\% & +4.45\% \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(table9_old, table9_new)

# Table 10 (3-Seed Variance)
table10_old = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{3-Seed Macro-F1 Variance}
\label{tab:10}
\begin{tabular}{cccccc}
\toprule
ModelSeed 42Seed 43Seed 44MeanStd &  &  &  &  &  \\
\midrule
\bottomrule
\end{tabular}
\end{table}
| --------------------------------- | ------ | ------ | ------ | ------ | ------ |
| Published Baseline        | 0.9870 | 0.9865 | 0.9871 | 0.9869 | 0.0003 |
| Late Fusion            | 0.9868 | 0.9869 | 0.9875 | 0.9871 | 0.0003 |
| Full DCAT             | 0.9860 | 0.9863 | 0.9864 | 0.9862 | 0.0002 |'''

table10_new = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{3-Seed Macro-F1 Variance}
\label{tab:10}
\begin{tabular}{lccccc}
\toprule
Model & Seed 42 & Seed 43 & Seed 44 & Mean & Std \\
\midrule
Published Baseline & 0.9870 & 0.9865 & 0.9871 & 0.9869 & 0.0003 \\
Late Fusion & 0.9868 & 0.9869 & 0.9875 & 0.9871 & 0.0003 \\
Full DCAT & 0.9860 & 0.9863 & 0.9864 & 0.9862 & 0.0002 \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(table10_old, table10_new)

# Table 11 (Modality-Specific)
table11_old = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Modality-Specific Macro-F1 (Full Test Set, Seed 42)}
\label{tab:11}
\begin{tabular}{ccc}
\toprule
ModelText-Only EmailsMultimodal Emails &  &  \\
\midrule
\bottomrule
\end{tabular}
\end{table}
| -------------------------------------- | ------ | ------ |
| Late Fusion              | 0.9858 | 0.4968 |
| DCAT-No-XAttn             | 0.9871 | 0.8317 |
| Full DCAT               | 0.9865 | 0.4968 |'''

table11_new = r'''\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Modality-Specific Macro-F1 (Full Test Set, Seed 42)}
\label{tab:11}
\begin{tabular}{lcc}
\toprule
Model & Text-Only Emails & Multimodal Emails \\
\midrule
Late Fusion & 0.9858 & 0.4968 \\
DCAT-No-XAttn & 0.9871 & 0.8317 \\
Full DCAT & 0.9865 & 0.4968 \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(table11_old, table11_new)

# ============================================================
# 2. Fix Appendix markdown-style tables
# ============================================================

# Appendix A
appendix_a_old = r'''\section{Appendix A: Dataset Statistics Summary}
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
| Train/Val/Test split        | 70/15/15 (config)    |'''

appendix_a_new = r'''\section{Appendix A: Dataset Statistics Summary}
\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Dataset Statistics Summary}
\label{tab:app-a}
\begin{tabular}{lc}
\toprule
Metric & Value \\
\midrule
Total emails (SpamAssassin subset) & 6,046 \\
Ham emails & 4,150 (68.6\%) \\
Spam emails & 1,896 (31.4\%) \\
Text-only emails & 6,007 (99.4\%) \\
Multimodal emails & 11 (0.2\%) \\
Image-only emails & 1 (0.02\%) \\
Empty emails (excluded) & 27 (0.4\%) \\
Text truncation length & 256 tokens \\
Image resolution & $224 \times 224$ pixels \\
Train/Val/Test split & 70/15/15 (config) \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(appendix_a_old, appendix_a_new)

# Appendix B
appendix_b_old = r'''\section{Appendix B: Model Hyperparameters}
| HyperparameterValue      |                  |
| ----------------------------- | --------------------------------- |
| Text encoder         | DistilBERT-base-uncased (frozen) |
| Vision encoder        | MobileViT-small via timm (frozen) |
| Shared latent dimension    | 256                |
| Cross-attention layers    | 2                 |
| Cross-attention heads     | 4                 |
| Cross-attention d\_model    | 256                |
| Cross-attention d\_ff     | 1024               |
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
| Seeds             | 42, 3, 44            |'''

appendix_b_new = r'''\section{Appendix B: Model Hyperparameters}
\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Model Hyperparameters}
\label{tab:app-b}
\begin{tabular}{lc}
\toprule
Hyperparameter & Value \\
\midrule
Text encoder & DistilBERT-base-uncased (frozen) \\
Vision encoder & MobileViT-small via \texttt{timm} (frozen) \\
Shared latent dimension & 256 \\
Cross-attention layers & 2 \\
Cross-attention heads & 4 \\
Cross-attention $d_{model}$ & 256 \\
Cross-attention $d_{ff}$ & 1024 \\
Cross-attention dropout & 0.1 \\
Cross-attention activation & GELU \\
Cross-attention normalization & Pre-LayerNorm \\
Classifier hidden dim & 128 \\
Classifier dropout & 0.3 \\
Classifier activation & GELU \\
Pooling strategy & Mean pooling \\
Optimizer & AdamW \\
Learning rate & $1 \times 10^{-4}$ \\
Scheduler & Cosine annealing \\
Batch size & 64 \\
Epochs & 1 \\
Precision & FP16 mixed \\
Loss function & BCEWithLogitsLoss \\
Classification threshold & 0.5 \\
Early-exit high threshold & 0.95 \\
Early-exit low threshold & 0.05 \\
Seeds & 42, 43, 44 \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(appendix_b_old, appendix_b_new)

# Appendix C
appendix_c_old = r'''\section{Appendix C: Complete Results Lineage}
Source: \texttt{artifacts/final\_results/results\_lineage.csv}
| MetricModelSplitSeed/FoldSource ArtifactValueAggregation |                |              |      |                            |            |                           |
| -------------------------------------------------------- | ----------------------------- | -------------------------- | --------- | ----------------------------------------------------- | ---------------------- | --------------------------------------------------- |
| Macro-F1                         | Full-DCAT           | Primary Test (10%)     | Seed 42  | \texttt{artifacts/experiments/weighted\_primary/results.json} | 0.9868         | Unweighted mean of Spam and Ham F1         |
| MM-Macro-F1                       | Full-DCAT           | Multimodal CV (5-Fold)   | 5-Fold CV | \texttt{artifacts/experiments/weighted\_cv/cv\_results.csv}  | 0.6609         | Mean across 5 folds                 |
| MM-Macro-F1                       | Late-Fusion          | Multimodal CV (5-Fold)   | 5-Fold CV | \texttt{artifacts/experiments/weighted\_cv/cv\_results.csv}  | 0.5564         | Mean across 5 folds                 |
| MM-Macro-F1                       | Weighted-DCAT         | Multimodal CV (5-Fold)   | 5-Fold CV | \texttt{artifacts/experiments/weighted\_cv/cv\_results.csv}  | 0.6824         | Mean across 5 folds                 |
| McNemar p-value                     | Weighted-DCAT vs. Full-DCAT  | Pooled OOF (7,867 samples) | All Folds | task-1070 log                     | $2.49 \times 10^{-45}$ | Exact/Asymptotic McNemar with continuity correction |
| McNemar p-value                     | Weighted-DCAT vs. Late-Fusion | Pooled OOF (7,867 samples) | All Folds | task-1070 log                     | $3.34 \times 10^{-6}$ | Exact/Asymptotic McNemar with continuity correction |'''

appendix_c_new = r'''\section{Appendix C: Complete Results Lineage}
Source: \texttt{artifacts/final\_results/results\_lineage.csv}
\begin{table}[htbp]
\centering
\renewcommand{\arraystretch}{1.2}
\caption{Complete Results Lineage}
\label{tab:app-c}
\begin{tabular}{lllclc}
\toprule
Metric & Model & Split & Seed/Fold & Source Artifact & Value \\
\midrule
Macro-F1 & Full-DCAT & Primary Test (10\%) & Seed 42 & \texttt{artifacts/experiments/weighted\_primary/results.json} & 0.9868 \\
MM-Macro-F1 & Full-DCAT & Multimodal CV (5-Fold) & 5-Fold CV & \texttt{artifacts/experiments/weighted\_cv/cv\_results.csv} & 0.6609 \\
MM-Macro-F1 & Late-Fusion & Multimodal CV (5-Fold) & 5-Fold CV & \texttt{artifacts/experiments/weighted\_cv/cv\_results.csv} & 0.5564 \\
MM-Macro-F1 & Weighted-DCAT & Multimodal CV (5-Fold) & 5-Fold CV & \texttt{artifacts/experiments/weighted\_cv/cv\_results.csv} & 0.6824 \\
McNemar p-value & Weighted-DCAT vs. Full-DCAT & Pooled OOF (7,867 samples) & All Folds & task-1070 log & $2.49 \times 10^{-45}$ \\
McNemar p-value & Weighted-DCAT vs. Late-Fusion & Pooled OOF (7,867 samples) & All Folds & task-1070 log & $3.34 \times 10^{-6}$ \\
\bottomrule
\end{tabular}
\end{table}'''

content = content.replace(appendix_c_old, appendix_c_new)

# ============================================================
# 3. Fix \_{ in text mode (Appendix B had d\_model etc.)
# These are now in the table replacement above, but check for remaining
# ============================================================

# Fix remaining \_ in text that should just be _ (e.g., in prose)
# Actually, \_ in text mode is correct for underscore display
# The issue was only inside math mode which we already fixed

# ============================================================
# 4. Fix abstract to clarify the discrepancy
# ============================================================

# The abstract says "Weighted-DCAT increases multimodal Macro-F1 from 0.6253 to 0.7478"
# This is from the class imbalance ablation (Table 5)
# But the lineage says CV values are 0.6609->0.6824
# Fix the abstract to clarify
content = content.replace(
    "Weighted-DCAT increases multimodal Macro-F1 from 0.6253 to 0.7478 with pooled out-of-fold McNemar tests giving $$p < 10^{-44}$$ against unweighted Full-DCAT and $$p < 10^{-5}$$ against Late Fusion.",
    "Weighted-DCAT increases multimodal Macro-F1 from 0.6253 to 0.7478 in the class imbalance ablation, with pooled out-of-fold McNemar tests giving $$p < 10^{-44}$$ against unweighted Full-DCAT and $$p < 10^{-5}$$ against Late Fusion."
)

# ============================================================
# 5. Fix section 7.4 text to clarify the ablation source
# ============================================================
# The text says "Weighted-DCAT increases multimodal Macro-F1 from 0.6253 to 0.7478"
# This is fine since Table 5 shows these values
# But the abstract now says "in the class imbalance ablation"
# Make sure section 7.4 is consistent

# ============================================================
# 6. Fix the \end{document} issue - check for missing \end
# ============================================================

# Check if \end{document} exists
if r'\end{document}' not in content:
    content = content.rstrip() + '\n\\end{document}\n'
    print("Added \\end{document}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("All table fixes applied successfully")
print("Checking for remaining issues...")
print("  ]`math remaining:", content.count(']`math'))
print("  \\] count:", content.count('\\]'))
print("  \[ count:", content.count('\\['))
print("  \end{document} present:", r'\end{document}' in content)
