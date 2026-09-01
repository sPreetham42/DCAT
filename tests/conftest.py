"""Shared pytest fixtures for DCAT.

All tests in this repo should be deterministic in the absence of a GPU: pure
Python / CPU tests must not require CUDA. GPU-gated tests are marked with
``@pytest.mark.gpu`` and are skipped when no device is available.
"""

from __future__ import annotations

import pytest


def _cuda_available() -> bool:
    try:
        import torch

        return bool(torch.cuda.is_available())
    except Exception:  # noqa: BLE001 - torch may not be installed
        return False


@pytest.fixture(scope="session")
def cuda_available() -> bool:
    return _cuda_available()
