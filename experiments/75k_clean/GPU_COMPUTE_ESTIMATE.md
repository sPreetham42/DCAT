# GPU Compute & Storage Estimate

*Note: All runtimes are approximate estimates based on standard throughput on a single NVIDIA A100 (40GB) or V100 (32GB) GPU. These are not precise benchmarked runtimes.*

## Dataset Parameters
- **Total Training Examples:** ~58,000 (80% of 73k)
- **Validation Examples:** ~7,300 (10% of 73k)
- **Batch Size:** 32 (estimated safe threshold for DistilBERT + MobileViT + Cross-Attn)
- **Batches per Epoch:** ~1,800
- **Expected Epochs:** 5 - 10 (early stopping enabled)

## Estimated Timings (Per Deep Model)

| Model | Est. Time per Epoch | Est. Total Wall-Clock | Storage (Checkpoint) | Storage (Predictions) |
|---|---|---|---|---|
| M2: Text-only (DistilBERT) | ~15 min | ~1.5 - 2 hours | ~270 MB | ~1 MB (CSV/JSON) |
| M3: Image-only (MobileViT) | ~12 min | ~1 - 1.5 hours | ~30 MB | ~1 MB |
| M4: Late Fusion | ~25 min | ~2 - 3 hours | ~300 MB | ~1 MB |
| M5: DCAT-No-XAttn | ~30 min | ~2.5 - 3.5 hours | ~350 MB | ~1 MB |
| M6: Full DCAT | ~35 min | ~3 - 4.5 hours | ~380 MB | ~1 MB |

## Total Sweep Estimate
Executing the full Seed 42 matrix (M1-M6, plus C1-C2) sequentially on a single GPU will require approximately **10 to 15 hours of wall-clock time**. 

## Total Storage Estimate
- **Model Checkpoints:** ~1.5 GB per full matrix sweep.
- **Log/Prediction Artifacts:** < 50 MB total.

## Prediction Storage Requirements
To calculate paired statistical significance tests (McNemar's test and Bootstrap Confidence Intervals) on the conditioned multimodal subset, the system MUST save the raw test-set predictions (prob/logits array mapped to exactly the `email_id`). Storing these raw CSV/JSON logs is trivial in terms of storage footprint but completely critical for scientific reproducibility.
