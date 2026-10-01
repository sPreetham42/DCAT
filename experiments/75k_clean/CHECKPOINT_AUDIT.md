# Phase 10: Checkpoint Reuse Decision & Compatibility Audit

This document explicitly verifies the compatibility of all historical checkpoints discovered in the `checkpoints/` directory against the newly constructed, group-disjoint evaluation pipeline (`75k_clean`).

## Audit Methodology
For every checkpoint, we establish:
1. **Architecture:** Whether the structural layers precisely match the current research protocol (`configs/experiments/dcat.yaml`).
2. **Training Data / Split:** Whether the checkpoint was trained on the older mathematically leaky `union-find` split or the new strict TF-IDF group-disjoint split.
3. **Compatibility:** Whether the checkpoint can be scientifically evaluated on the `75k_clean` test set without severe risk of data contamination (leakage).

## Final Classification Matrix

| Filename | Architecture Valid? | Cross-Attn Layers | Training Split Origin | Seed | Classification | Relationship to Clean Test Set |
|---|---|---|---|---|---|---|
| `full-dcat_seed42_best.pt` | **NO** | 1 (Config states 2) | Historical Union-Find | 42 | **INCOMPATIBLE** | Contaminated. The historical union-find split allowed near-duplicates of current test-set items into the historical training phase. |
| `late-fusion_best.pt` | YES | N/A | Historical Union-Find | Unknown | **INCOMPATIBLE** | Contaminated. Trained on leaky split. |
| `text-only_best.pt` | YES | N/A | Historical Union-Find | Unknown | **INCOMPATIBLE** | Contaminated. Trained on leaky split. |
| `image-only_best.pt` | YES | N/A | Historical Union-Find | Unknown | **INCOMPATIBLE** | Contaminated. Trained on leaky split. |
| `dcat-no-cross-attention_best.pt`| YES | 0 | Historical Union-Find | Unknown | **INCOMPATIBLE** | Contaminated. Trained on leaky split. |

## Explicit Known Issue: Architecture Irreconcilability
The historical `full-dcat_seed42_best.pt` structurally contains exactly **1 cross-attention layer**. However, the authoritative research configuration `configs/experiments/dcat.yaml` specifies `model.dcat.cross_attention.layers=2`. The provenance of this checkpoint is scientifically compromised.

## Explicit Checkpoint Reuse Decision
Every historical checkpoint in the `checkpoints/` directory was minted prior to the strict `TF-IDF Cosine Similarity >= 0.90` connected components grouping logic that now defines the `75k_clean` data manifest.

Evaluating these historical checkpoints on the new test set would mean evaluating them on data (near-duplicate campaign variations) they implicitly memorized during their historical training phase. This violates the core scientific mandate of the re-evaluation.

**Conclusion:** 
NO historical checkpoints are `HEADLINE_REUSABLE`. 
ALL historical checkpoints are classified as `INCOMPATIBLE` for producing `FINAL_RESEARCH_SOURCE_OF_TRUTH_75K.md`.

The entire essential model matrix MUST be trained from scratch on the frozen `experiments/75k_clean/manifests/split_manifest.csv`.
