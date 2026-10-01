# Data layout

This directory separates **tracked provenance** (small, authoritative) from **large
local-only data** that is deliberately kept out of the active source structure.

## Tracked

| Path | Contents |
|---|---|
| `manifests/leakage_groups.csv` | Leakage-safe split manifest: one group id per sample, produced by `scripts/build_dataset.py`. This is the split the reported results use. |
| `manifests/spamassassin_profile.csv` | Per-message corpus profile (modality, parse status, content hashes). |
| `manifests/manifest.csv` | Tiny **synthetic** manifest written by `scripts/create_dummy_data.py`; for smoke tests only. Not the dataset behind any reported number. |
| `.gitkeep` | Keeps the directory present in Git. |

## Local only (large — not version-controlled)

| Path | Approx. size | Contents |
|---|---|---|
| `raw/` | ~16 GB | Raw corpus, including `image_spam_public.json`. |
| `processed/` | ~780 MB | `email_origin.csv`, `records.parquet`, extracted `images/`. |
| `spamassassin/` | ~52 MB | Public SpamAssassin tarballs and their extraction. |
| `../checkpoints/` | ~7.9 GB | Trained model weights (seeds 42 / 43 / 44). |

All of the above are excluded by `.gitignore`. The metrics derived from them are kept in
`../results/` (tables and figures) and `../artifacts/` (per-analysis evidence).

## Provenance

`artifacts/final_results/results_lineage.csv` maps each reported number to the artifact
and aggregation method that produced it.
