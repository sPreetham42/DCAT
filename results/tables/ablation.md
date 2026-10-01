# Cross-Attention Ablation Study

Does removing cross-attention change performance?

Evaluating strictly on the multimodal test subset:

| Model | Macro-F1 | Ham F1 | Spam F1 |
|---|---|---|---|
| Late Fusion | 0.4968 | 0.0000 | 0.9935 |
| DCAT-No-XAttn | 0.8317 | 0.6667 | 0.9967 |
| DCAT | 0.4968 | 0.0000 | 0.9935 |

### Statistical Significance (McNemar's Test on MM Subset)
- DCAT vs Late Fusion: p-value = 1.0000
- DCAT vs DCAT-No-XAttn: p-value = 0.2482

Conclusion: Based on the test, there is no statistically significant difference in performance when removing the explicit cross-attention mechanism for this specific naturally-paired dataset distribution.
