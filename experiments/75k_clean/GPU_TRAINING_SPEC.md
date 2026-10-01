# GPU Training Specification (75K Clean Split)

This specification defines the strictly frozen parameters required to execute the final DCAT evaluation suite on a GPU-capable node. This specification must NOT be altered without invalidating the scientific controls.

## 1. Dataset
- **Exact Path:** `data/processed/records.parquet`
- **Usable Count:** `73,206`
- **Exclusions:** Records where `has_text == False` AND `has_meaningful_image == False` are strictly excluded from the dataloader.

## 2. Split Generation
- **Selected Split:** Group-Disjoint
- **Seed:** `42` (Pre-specified operational seed)
- **Manifest Paths:** 
  - `experiments/75k_clean/manifests/train.json`
  - `experiments/75k_clean/manifests/val.json`
  - `experiments/75k_clean/manifests/test.json`
- **Manifest Validation:** Check against `experiments/75k_clean/SPLIT_MANIFEST_SHA256.txt` before training.
- **Group-Generation Method:** Unigram/Bigram TF-IDF sparse dot product.
- **Similarity Threshold:** `0.90` (Empty-text assigned to forced singletons).

## 3. Preprocessing
- **Exact Pipeline:** Defined in `src/dcat/preprocessing/`
- **Tokenizer Version:** `distilbert-base-uncased` (frozen)
- **Image Preprocessing:** `apple/mobilevit-small` image processor (frozen)
- **Missing-Modality Handling:** 
  - Missing Text -> Empty string `""` -> Tokenized to `[CLS] [SEP]`
  - Missing Image -> Zero-tensor of shape `(3, 256, 256)`

## 4. Required Models
The following model matrix must be fully trained from scratch on Seed 42:

### Control Baselines (Gate 0)
- **Image-presence baseline:** Heuristic. No training. Just `has_image` prior.
- **C1 (Text + has_image):** Text features concatenated with a 1D binary indicator.
- **C2 (Image metadata-only):** Non-pixel metadata (width, height, aspect ratio, file size, MIME type, count). No image tensor input.

### Deep Matrix
- **M1:** TF-IDF + Linear Classifier
- **M2 (Text-only):** DistilBERT.
- **M3 (Image-only):** MobileViT.
- **M4 (Late Fusion):** Decoupled multimodal predictions.
- **M5 (DCAT-No-XAttn):** Concatenated embeddings, no cross-attention layers.
- **M6 (Full DCAT):** Exactly 2 cross-attention layers.

## 5. Seed Policy
- **Primary Seed:** `42` must be used for the initial full matrix sweep.
- **Secondary Seeds:** If compute permits, evaluate `M4`, `M5`, and `M6` on additional random initializations (e.g., 43, 44) to provide standard deviations on the multimodal improvement. DO NOT alter the dataset split seed.

## 6. Required Raw Outputs
For every trained model, the following must be archived:
- `checkpoint.pt`
- Configuration YAML used
- Random Seed used
- Git Commit hash
- Raw test predictions (CSV/JSON mapping `email_id` -> `predicted_logit`, `probability`, `label`)
- Training / Validation loss history logs
- Empirical inference timing data

**CRITICAL:** Do NOT merely save the final F1 score. The statistical significance testing (McNemar/Bootstrap) mathematically requires the exact discordant pair arrays from the raw test predictions.
