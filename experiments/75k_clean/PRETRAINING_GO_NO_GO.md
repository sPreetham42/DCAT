# Pre-Training GO / NO-GO Status

## 1. DATA PIPELINE
**Status: READY**
- The repository was exhaustively searched. No hidden source mappings or temporal timestamps exist in the corpus.
- Empty-text image-only emails are correctly canonicalized into singletons to prevent pathological TF-IDF collapsing.

## 2. CLEAN SPLIT
**Status: VALID**
- The split is definitively deterministic using `Seed 42`.
- `INDEPENDENT_SPLIT_VERIFICATION.md` mathematically proves there is zero Train/Val, Train/Test, or Val/Test overlap, and zero cross-split group leakage.
- The boundary is completely frozen via hashes.

## 3. MULTIMODAL TEST POWER
**Status: LIMITED**
- The pre-specified operational Seed 42 resulted in only **3** image-bearing hams in the test set.
- Consequently, the statistical power for the central multimodal claim (`Text vs Text + has_image vs Full DCAT` within the image-bearing subset) is severely underpowered for this exact split. 
- *Methodological note: This split is retained because unbiased construction takes scientific precedence over deliberately re-rolling seeds to achieve a target statistical power.*

## 4. HEADLINE CHECKPOINTS
**Status: REQUIRE RETRAINING**
- Every single historical checkpoint (M1-M6) in the repository is fundamentally contaminated. They were trained on the leaky `union-find` split, rendering them scientifically invalid for headline evaluation on the new frozen dataset.
- `full-dcat_seed42_best.pt` suffers from a proven architecture irreconcilability (1 layer vs 2 layer config).

## 5. GPU TRAINING
**Status: BLOCKED IN CURRENT ENVIRONMENT**
- The execution environment is CPU-only (`Device count: 0`).
- The entire evaluation pipeline is logically frozen and scientifically validated, but physically executing the deep model matrix (DistilBERT, MobileViT, DCAT) over 60,000+ multimodal training records is physically blocked on this specific hardware. 
- The experiment must be handed off to a GPU-capable node.
