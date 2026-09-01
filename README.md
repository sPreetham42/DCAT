# DCAT — Dynamic Cross-Attention Transformer

**Conditional multimodal email-spam detection combining cross-modal feature interaction with modality-aware computation.**

DCAT is a research project that audits and extends **MDL-SPAM: A Multi Model Deep Learning Framework for Email Spam Detection Using VGG-16 and LSTM**. The audited paper has serious methodological flaws (disjoint text/image data, independently shuffled fusion probabilities, hardcoded `0.5` for missing modalities, and a tiny two-element fusion input through an unnecessarily large dense network). DCAT is designed to address them with a clean, reproducible, and falsifiable experimental framework.

---

## Research Contribution

> A conditional multimodal email-spam detection architecture that combines cross-modal feature interaction with modality-aware computation, specifically designed for the heterogeneous structure of email.

**We make no claim that cross-attention itself is novel.** The contribution is the *architectural combination*, evaluated honestly.

### Research Objectives (hypotheses to be tested)

- **H1 (computational):** Conditional modality routing reduces computational cost under realistic email modality distributions while maintaining classification performance.
- **H2 (representational):** Cross-modal feature interaction improves multimodal spam classification over conventional fusion (late fusion / early concatenation) on *genuinely paired* multimodal emails.

Results may falsify either hypothesis. No expected improvements are manufactured.

### Two research gaps addressed

1. **Gap 1:** Independent unimodal processing + late fusion does not explicitly model cross-modal feature interactions between email text and visual content.
2. **Gap 2:** Multimodal systems waste computation by invoking expensive modality encoders when the corresponding modality is absent.

---

## Frozen Architectural Principles

Do not redesign these unless a genuine correctness problem is found:

1. **Deterministic MIME preprocessing** — Python `email` package + BeautifulSoup + Pillow.
2. **Deterministic modality routing** — TEXT / IMAGE / MULTIMODAL routes based on actual extracted content.
3. **Conditional computation** — the missing modality encoder is *never run*; no `0.5` injection; no dummy evidence vectors; no three separate classifiers. The classifier head is **shared**.
4. **Text encoder** — Hugging Face DistilBERT (`max_length=256` configurable), token-level hidden states `[B, T, 768]`.
5. **Vision encoder** — pretrained lightweight MobileViT (via `timm`), pre-pooling spatial features `[B, V, Dv]` (token count verified at runtime, never assumed).
6. **Shared latent projection** — default `shared_dim = 256` (configurable: 128/256/384/512).
7. **Bidirectional cross-attention** (multimodal only) — 2 layers, 4 heads, d_model=256, d_ff=1024, Pre-LayerNorm, residuals, GELU, dropout=0.1.
8. **Mean pooling** — all paths produce `[B, shared_dim]` before the shared classifier.
9. **Shared classifier** — `LayerNorm → Linear(256,128) → GELU → Dropout(0.3) → Linear(128,1)`, `BCEWithLogitsLoss` for training.
10. **Multiple images** — supported by the data model; selection isolated behind a pluggable interface (initial baseline: top-1 largest meaningful image).

**Explicitly deferred:** OCR, FastAPI/Go serving, ONNX/TensorRT, LangChain/LangGraph, Kafka/Redis/PostgreSQL, learned routing, contrastive pretraining, microservices.

---

## Project Stack

| Category | Tools |
|---|---|
| Language | Python 3.12 |
| ML | PyTorch, Hugging Face Transformers, timm |
| Preprocessing | Pillow, BeautifulSoup4, lxml |
| Config | Hydra, OmegaConf |
| Experiment tracking | MLflow |
| Hyperparams | Optuna |
| Data versioning | DVC, Parquet, PyArrow |
| Data manipulation | NumPy, Polars/Pandas, scikit-learn, SciPy |
| Testing | pytest |
| Serving (later) | FastAPI, Pydantic (deferred) |
| Production gateway (later) | Go (deferred) |

---

## Repository Layout

```
dcat/
├── configs/            # Hydra configuration
│   ├── config.yaml     # root config (composition)
│   ├── model/          # dcat, distilbert, mobilevit
│   ├── data/           # dataset
│   ├── training/       # base, finetune
│   ├── experiments/    # late_fusion, early_fusion, cross_attention, dcat
│   ├── benchmark/      # inference
│   └── router/         # modality thresholds
├── src/dcat/           # core package
│   ├── data/           # data contract, datasets, DVC, leakage audit
│   ├── preprocessing/  # MIME parser, HTML, image, modality router
│   ├── models/         # encoders, projection, cross-attention, classifier, DCAT
│   ├── training/       # trainers, optimizers, schedulers, seed manager
│   ├── evaluation/     # metrics, baselines, benchmarking
│   ├── inference/      # inference pipeline
│   └── scripts/        # CLI entry points (env check, dataset validation, etc.)
├── tests/              # pytest suites (unit, tensor-shape, integration)
├── scripts/            # standalone runnable scripts
├── data/               # raw/processed data (gitignored)
├── notebooks/          # exploration notebooks
└── docs/               # research notes and docs
```

---

## Implementation Roadmap

The roadmap is implemented strictly in order. Tests and a Git checkpoint follow every milestone. See `docs/ROADMAP.md` for details.

| # | Milestone | Status |
|---|---|---|
| 1 | Repository foundation (scaffold, config, env verification) | **current** |
| 2 | Dataset contract (typed models) | |
| 3 | Deterministic MIME parser | |
| 4 | Modality detector / router | |
| 5 | Image preprocessing | |
| 6 | HTML processing | |
| 7 | Dataset validation | |
| 8 | Dataset exploration | |
| 9 | Leakage audit | |
| 10 | Standalone text encoder (DistilBERT) | |
| 11 | Standalone vision encoder (MobileViT) | |
| 12 | Projection layers | |
| 13 | Cross-attention module | |
| 14 | Shared classification head | |
| 15 | Assemble conditional DCAT | |
| 16+ | Training pipeline, baselines, experiments | |

---

## Setup

### Requirements

- Python 3.12
- NVIDIA GPU with CUDA (target: RTX 4050 6 GB VRAM)

### Installation

```bash
python -m venv .venv
source .venv/Scripts/activate          # Windows (Git Bash)
# or: .venv\Scripts\activate            Windows (cmd/PowerShell)

pip install -e ".[dev]"
```

> On a fresh machine, install the `torch` / `torchvision` CUDA wheels *before* the rest if the default PyPI wheel does not match your CUDA version:
>
> ```bash
> pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
> ```

### Verify the environment

```bash
python -m dcat.scripts.env_check
# or the console script:
dcat-env
```

This prints Python version, PyTorch version, CUDA availability, GPU name/memory, and a matrix of every installed dependency.

### Run the tests

```bash
pytest
```

### Run the linters / formatter

```bash
ruff check src tests
black --check src tests
```

---

## Hardware Constraints

- **GPU:** NVIDIA RTX 4050 — 6 GB VRAM
- **RAM:** 16 GB

The training system is designed accordingly: CUDA, FP16 mixed precision, gradient accumulation, controlled batch-size selection, optional gradient checkpointing. Initial image size `224×224`, text length `256`.

---

## Reproducibility

Every MLflow run records: git commit, dataset version, seed, full configuration, total/trainable parameters, training time, and validation metrics. A seed manager covers Python, NumPy, and PyTorch (CPU + CUDA).

---

## License

MIT (research project — no warranty).
