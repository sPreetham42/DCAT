# Image-Level Leakage Control Audit

## Current Deduplication Mechanism
The current group-disjoint split relies exclusively on a text-based TF-IDF sparse similarity matrix (cosine similarity $\ge 0.90$).

## Image Deduplication Status
An audit of the `records.parquet` dataset specifically examining the `images_json` column revealed the following:
- `exact_hash`: `null`
- `perceptual_hash`: `null`

Because the processed dataset lacks pre-computed perceptual or exact cryptographic image hashes, the current connected-component grouping algorithm is **completely blind to image reuse**.

## Vulnerabilities
This creates a critical leakage vulnerability for the multimodal claim. If a spam campaign uses the exact same spam payload image (e.g., a rasterized text advertisement) but embeds it within a hundred different randomly generated text templates (to evade text-based spam filters), the TF-IDF algorithm will assign these emails to completely separate groups. 
Those groups will be randomly distributed across the Train and Test splits, resulting in exact-duplicate images leaking into the test set.

## Conclusion
**DO NOT claim that the multimodal test set is fully leakage-controlled.**
The text modality is controlled, but the image modality is not. To repair this, an implementation of an image perceptual-hash mechanism (e.g., `imagehash` phash) must be computed for all image paths, and exact matches must form explicit edges within the connected-component graph.
