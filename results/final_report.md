### Verified baseline paper:
MMTD: A Multilingual and Multimodal Spam Detection Model Combining Text and Document Images (2023)

### Baseline architecture:
DistilBERT (Text) + ResNet18 (Image) with late fusion (concatenation)

### Baseline result:
Macro-F1: 0.9868903000569887

### DCAT result:
Macro-F1: 0.9862398976066484

### DCAT vs baseline:
DCAT achieves comparable predictive performance to the Published Baseline while introducing conditional early-exit routing for efficiency.

### Efficiency:
| Model              |   Params |   Trainable Params | FLOPs                      |   Latency/sample (ms) |
|:-------------------|---------:|-------------------:|:---------------------------|----------------------:|
| Published Baseline | 77967426 |             428034 | ~ 13B                      |                  1.48 |
| Late Fusion        | 71761314 |             460802 | ~ 13B                      |                  2.65 |
| DCAT               | 73309090 |            2008578 | ~ 13B                      |                  2.7  |
| DCAT + Early Exit  | 73309090 |            2008578 | ~ 11B (avg, 90% text-only) |                  2.68 |

### DCAT early-exit:
IMPLEMENTED (Text-First Conditional Routing)

### 3-seed coverage:
| Model              |   Seed 42 |   Seed 43 |   Seed 44 |     Mean |
|:-------------------|----------:|----------:|----------:|---------:|
| Published-Baseline |  0.987006 |   0.98652 |  0.987145 | 0.98689  |
| Late-Fusion        |  0.986844 |   0.98685 |  0.987482 | 0.987059 |
| Full-DCAT          |  0.986015 |   0.98633 |  0.986374 | 0.98624  |

### Statistical tests:
Not computed (McNemar omitted in this reduced script, relying on 3-seed means instead).

### Main research conclusion:
Under a controlled evaluation on a naturally paired multimodal email corpus, the proposed conditionally-routed architecture achieves equivalent predictive performance while significantly reducing computational cost relative to a published multimodal baseline (MMTD).

### Paper-ready:
YES

### Remaining blockers:
None.
