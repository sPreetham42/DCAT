# DCAT Implementation Roadmap

This document tracks the incremental build of DCAT. Each milestone ends with **tests passing**, a **git diff review** (no accidental files/secrets), and a **meaningful Git checkpoint**.

> **Guiding principle:** Do not jump into the neural model. Build the data and preprocessing foundations first, and only train once the dataset leakage audit passes.

---

## Phase 0 — Foundations

### Milestone 1 — Repository foundation (CURRENT)
- [x] Project scaffold (`src/`, `tests/`, `configs/`, `scripts/`, `data/`, `notebooks/`, `docs/`)
- [x] Python environment + dependency management (`pyproject.toml`)
- [x] Linting/formatting config (ruff, black, mypy)
- [x] pytest configuration
- [x] Hydra + OmegaConf configuration tree
- [x] MLflow configuration
- [x] `.gitignore`
- [x] README
- [x] Environment verification script
- [ ] Initial tests pass
- [ ] Git checkpoint

## Phase 1 — Data contract & preprocessing

### Milestone 2 — Dataset contract
- [ ] Typed `EmailRecord`, `ImageRecord`, modality types, parser output
- [ ] Unit tests

### Milestone 3 — MIME parser
- [ ] Deterministic parsing with Python `email` + BeautifulSoup + Pillow
- [ ] Tests: text/plain, text/html, text+html, inline/CID/attachment images, multiple images, tracking pixel, malformed MIME, empty body, Unicode, large attachment, nested multipart
- [ ] No ML dependencies required by the parser

### Milestone 4 — Modality detector/router
- [ ] TEXT / IMAGE / MULTIMODAL routing based on actual content
- [ ] Configurable thresholds
- [ ] Deterministic; unit tests

### Milestone 5 — Image preprocessing
- [ ] Decode/validate, dimension checks, filtering, resizing, normalization
- [ ] Stable image metadata; tests

### Milestone 6 — HTML processing
- [ ] Visible-text extraction + limited structural metadata
- [ ] Tests; not a handcrafted spam feature system

### Milestone 7 — Dataset validation
- [ ] Schema / required-field / label / image-decode / modality / file-reference checks
- [ ] Machine-readable + human-readable reports

### Milestone 8 — Dataset exploration
- [ ] Distributions (spam/ham, modality, modality×label, lengths, image sizes, counts, sender/campaign)

### Milestone 9 — Leakage audit
- [ ] Exact + perceptual image hashes, text similarity, URL overlap, sender/campaign overlap
- [ ] Cross-split contamination artifact
- [ ] **No serious training until audit passes**

## Phase 2 — Core model components

- M10 — DistilBERT text encoder (shapes, masking)
- M11 — MobileViT vision encoder (pre-pooling features, actual shapes)
- M12 — Shared latent projections (`TextProjection`, `VisionProjection`)
- M13 — Bidirectional cross-attention (shapes, masking, gradient flow, determinism, no-NaN)
- M14 — Shared classification head (BCEWithLogitsLoss)
- M15 — Assemble conditional DCAT (three routes tested)

## Phase 3 — Training & experiments

- M16 — Reproducible training pipeline (freeze → finetune, mixed precision, gradient accumulation, clipping, early stopping, best-checkpoint)
- M17 — Model summary (params by component, FLOPs benchmark)
- M18 — Baselines: DistilBERT-only, MobileViT-only, late fusion, early/filter concatenation, static cross-attention, DCAT dynamic routing
- M19 — H1/H2 experimental evaluation (F1, PR-AUC, latency, throughput, FLOPs, memory, encoder invocation rate)

---

## Configuration Tree

```
configs/
├── config.yaml             # root composition
├── model/
│   ├── dcat.yaml           # shared latent dim, head
│   ├── distilbert.yaml     # max_length etc.
│   └── mobilevit.yaml      # model name, image size
├── data/
│   └── dataset.yaml
├── training/
│   ├── base.yaml
│   └── finetune.yaml
├── experiments/
│   ├── late_fusion.yaml
│   ├── early_fusion.yaml
│   ├── cross_attention.yaml
│   └── dcat.yaml
├── benchmark/
│   └── inference.yaml
└── router/
    └── thresholds.yaml
```
