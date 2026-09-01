"""Validate that the Hydra/OmegaConf configuration tree is well-formed.

These tests load the YAML files directly with OmegaConf (without bootstrapping
the full Hydra app, which requires a run entry point). They assert structure,
not runtime behavior.
"""

from __future__ import annotations

from pathlib import Path

import yaml

CONFIGS_ROOT = Path(__file__).resolve().parents[1] / "configs"


def _load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def test_all_expected_config_files_exist():
    expected = [
        "config.yaml",
        "model/dcat.yaml",
        "model/distilbert.yaml",
        "model/mobilevit.yaml",
        "data/dataset.yaml",
        "training/base.yaml",
        "training/finetune.yaml",
        "experiments/late_fusion.yaml",
        "experiments/early_fusion.yaml",
        "experiments/cross_attention.yaml",
        "experiments/dcat.yaml",
        "benchmark/inference.yaml",
        "router/thresholds.yaml",
    ]
    for rel in expected:
        assert (CONFIGS_ROOT / rel).is_file(), f"Missing expected config: {rel}"


def test_dcat_model_config_has_shared_dim():
    cfg = _load(CONFIGS_ROOT / "model" / "dcat.yaml")
    assert cfg["shared_dim"] in {128, 256, 384, 512}


def test_dcat_cross_attention_defaults():
    cfg = _load(CONFIGS_ROOT / "model" / "dcat.yaml")["cross_attention"]
    assert cfg["layers"] == 2
    assert cfg["heads"] == 4
    assert cfg["d_model"] == 256
    assert cfg["d_ff"] == 1024
    assert cfg["dropout"] == 0.1
    assert cfg["pre_norm"] is True


def test_router_thresholds_positive():
    cfg = _load(CONFIGS_ROOT / "router" / "thresholds.yaml")
    for key in ("min_image_width", "min_image_height", "min_image_bytes"):
        assert cfg[key] > 0


def test_root_config_composes_expected_defaults():
    cfg = _load(CONFIGS_ROOT / "config.yaml")
    defaults = [d for d in cfg.get("defaults", [])]
    assert "model/dcat.yaml" in defaults
    assert "data/dataset.yaml" in defaults
    assert "router/thresholds.yaml" in defaults
