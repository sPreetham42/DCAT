import re

with open('paper/PAPER_CONTENT.md', encoding='utf-8') as f:
    text = f.read()

# Discussion 8.3 - 8.5 Replacements
d_text_old = r'''### 8.3 The Dominance of Text in Email Spam Detection

The results consistently demonstrate that text is the overwhelmingly dominant modality for spam detection in the SpamAssassin corpus. The Text-only model achieves 0.9827 Macro-F1, and all multimodal models achieve at most 0.0044 additional improvement (Late Fusion 0.9871 - Text-Only 0.9827 = 0.0044).

This finding has practical implications: for most real-world email filtering deployments, text-based models may suffice, and the computational cost of maintaining vision encoders may not be justified by the marginal performance improvement. However, this conclusion is specific to the SpamAssassin corpus and may not hold for email corpora with higher multimodal content ratios (e.g., marketing emails, phishing campaigns with image-heavy payloads).

### 8.4 The Promise of Class-Weighted Training

The imbalance ablation provides the most encouraging result: Weighted-DCAT improves multimodal Macro-F1 from 0.6253 to 0.7478, with highly significant McNemar p-values ($p < 10^{-44}$ vs. Full-DCAT, p < 10^{-5} vs. Late Fusion). This suggests that the primary barrier to multimodal performance is not the architectural design but rather the training objective's failure to account for the severe class imbalance within the multimodal subset.

The practical recommendation is that class-weighted loss should be considered a standard component of any multimodal spam detection system operating on naturally imbalanced email corpora.

### 8.5 Efficiency Trade-offs

The efficiency analysis demonstrates that the early-exit mechanism provides marginal computational savings in practice. The 4.45% vision skip rate is constrained by the extreme text-dominance of the corpus: since 99.4% of emails are text-only (and thus never reach the multimodal pathway), the early-exit can only affect the remaining 0.6% of emails. Even if 100% of multimodal emails were early-exited, the total FLOP reduction would be less than 1%.

The early-exit mechanism would be more impactful in email corpora with higher multimodal ratios, or in domains where multimodal content is more prevalent (e.g., social media, e-commerce product reviews).'''

d_text_new = r'''### 8.3 Text-Dominated Corpus

Text is the dominant modality for spam detection in the SpamAssassin corpus. The Text-only model achieves 0.9827 Macro-F1, while multimodal models provide at most a 0.0044 increase (Late Fusion 0.9871 - Text-Only 0.9827 = 0.0044). For deployments resembling this corpus distribution, text-based models achieve near-equivalent performance without the computational cost of maintaining vision encoders. This dynamic is specific to the SpamAssassin corpus and its 99.4% text-only distribution; performance requirements may differ for email corpora with higher image-heavy payloads.

### 8.4 Effect of Class Weighting

The imbalance ablation shows that Weighted-DCAT increases multimodal Macro-F1 from 0.6253 to 0.7478, with statistically significant McNemar p-values ($p < 10^{-44}$ vs. Full-DCAT, $p < 10^{-5}$ vs. Late Fusion) on the pooled OOF predictions. These results indicate that addressing the severe class imbalance via the training objective provides a larger gain than cross-attention architectural changes for this task. Class-weighted loss functions address the natural distribution imbalance of email corpora directly.

### 8.5 Efficiency Trade-offs

The early-exit mechanism achieves a 4.45% vision skip rate, bounded by the fact that only 0.6% of emails in the dataset proceed to the multimodal pathway initially. This yields a theoretical FLOP reduction of 0.63%. Conversely, the batch total-time latency measurement reports a 24.82% latency increase for the early-exit configuration. This demonstrates that the overhead of evaluating the auxiliary classifier and branching logic negates the theoretical FLOP savings on this highly text-dominated corpus.'''

text = text.replace(d_text_old, d_text_new)

# Abstract and Intro stylistic replacements
text = text.replace('an honest reporting of results, both when the proposed architecture does not achieve improvement over simpler baselines, and an analysis of the data distribution issues which lead to these results.',
                    'an evaluation of results against simple baselines and an analysis of the data distribution characteristics that constrain architectural improvements.')

text = text.replace('An honest reporting of results', 'An evaluation of results')

text = text.replace('This work provides an honest evaluation of conditional multimodal architectures',
                    'This work evaluates conditional multimodal architectures')

# Fix equation math block error if it persists
text = text.replace(r'where _{$\hat{z}_i$} is the logit output for email _{$t$0}, _{$t$1} is the sigmoid function, and _{$t$2} is the ground-truth label.',
                    r'where $\hat{z}_i$ is the logit output for email $m$, $\sigma$ is the sigmoid function, and $y_i$ is the ground-truth label.')

text = text.replace(r'positive class weight _{$t$3}:', r'positive class weight $w_{pos}$: \n\n```math\n\mathcal{L}_{weighted} = -\frac{1}{N} \sum_{i=1}^{N} \left[ w_{pos} \cdot y_i \log \sigma(\hat{z}_i) + (1 - y_i) \log(1 - \sigma(\hat{z}_i)) \right]\n```\n')

text = text.replace(r'_{$t$4}', '')
text = text.replace(r'where _{$t$5} to counteract', r'where $w_{pos} = \frac{N_{ham}}{N_{spam}}$ to counteract')

# Remove duplicate sentence in 7.7
text = text.replace('vision skip rate indicates that only a small fraction of multimodal emails have text predictions confident enough to be early-exited. The 0.63% FLOP reduction is therefore also small. While the per-sample latency (Table 8) shows a slight per-sample latency improvement (2.70ms to 2.68ms), the total-time measurement (Table 9) shows a 24.82% increase in latency for the early-exit variant. This discrepancy is caused by the overhead of the early-exit classifier evaluation and the conditional branching logic in PyTorch, which together negate the theoretical FLOP savings on this highly text-dominated corpus.', '')

# Clean up any leftover duplicate text
text = text.replace(r'| Vision Skip Rate | 0.00% | 4.45% | +4.45% |', r'| Vision Skip Rate | 0.00% | 4.45% | +4.45% |' + '\n\nThe 4.45% vision skip rate indicates that only a small fraction of multimodal emails have text predictions confident enough to be early-exited. The 0.63% FLOP reduction is therefore also small. While the per-sample latency (Table 8) shows a slight per-sample latency improvement (2.70ms to 2.68ms), the total-time batch measurement shows an increase (from 59.9ms to 74.7ms) for the early-exit variant. This discrepancy is caused by the overhead of the early-exit classifier evaluation and the conditional branching logic in PyTorch, which together negate the theoretical FLOP savings on this highly text-dominated corpus.')

with open('paper/PAPER_CONTENT.md', 'w', encoding='utf-8') as f:
    f.write(text)
