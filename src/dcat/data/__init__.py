"""Data layer for DCAT: the normalized email contract, preprocessing, dataset
writers, validation, exploration, and leakage audit."""

from __future__ import annotations

from dcat.data.modalities import Modality, modality_from_flags
from dcat.data.records import (
    EmailRecord,
    ImageDisposition,
    ImageRecord,
    ParserOutput,
    RawImage,
)

__all__ = [
    "EmailRecord",
    "ImageDisposition",
    "ImageRecord",
    "Modality",
    "ParserOutput",
    "RawImage",
    "modality_from_flags",
]
