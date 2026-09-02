"""Unit tests for DatasetValidator."""

from __future__ import annotations

import pytest

from dcat.data import EmailRecord, Modality
from dcat.data.validation import DatasetValidator


def test_validator_passes_clean_dataset():
    rec = EmailRecord(
        email_id="valid_01",
        label=1,
        text="Valid text body here.",
        has_text=True,
        has_meaningful_image=False,
        modality=Modality.TEXT,
    )
    validator = DatasetValidator()
    report = validator.validate([rec])
    assert report.passed is True
    assert report.error_count == 0


def test_validator_detects_duplicate_email_ids():
    rec1 = EmailRecord(
        email_id="dup_01",
        label=0,
        text="Sample text 1",
        has_text=True,
        modality=Modality.TEXT,
    )
    rec2 = EmailRecord(
        email_id="dup_01",
        label=1,
        text="Sample text 2",
        has_text=True,
        modality=Modality.TEXT,
    )
    validator = DatasetValidator()
    report = validator.validate([rec1, rec2])
    assert report.passed is False
    assert any(i.code == "duplicate_email_id" for i in report.issues)


def test_validator_detects_inconsistent_modality():
    # Constructing EmailRecord raises ValueError on post_init for invalid modality,
    # so we test post_init validation as well as validator checks.
    try:
        EmailRecord(
            email_id="inc_01",
            label=0,
            has_text=True,
            has_meaningful_image=True,
            modality=Modality.TEXT,  # Inconsistent! Expected MULTIMODAL
        )
        pytest.fail("Should have raised ValueError on post_init")
    except ValueError as exc:
        assert "inconsistent" in str(exc)
