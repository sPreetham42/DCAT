"""Unit tests for LeakageAuditor."""

from __future__ import annotations

import io

from PIL import Image

from dcat.data import EmailRecord, Modality
from dcat.data.leakage import LeakageAuditor, compute_image_ahash


def test_leakage_auditor_detects_exact_text_duplicate_cross_split():
    rec_train = EmailRecord(
        email_id="e_train",
        text="Exact duplicate body content across splits.",
        has_text=True,
        modality=Modality.TEXT,
        split="train",
    )
    rec_val = EmailRecord(
        email_id="e_val",
        text="Exact duplicate body content across splits.",
        has_text=True,
        modality=Modality.TEXT,
        split="val",
    )

    auditor = LeakageAuditor()
    report = auditor.audit([rec_train, rec_val])
    assert report.exact_text_duplicates_cross_split == 1
    assert len(report.leakage_pairs) >= 1
    assert report.leakage_pairs[0].leak_type == "exact_text"


def test_perceptual_hash_computation():
    buf = io.BytesIO()
    img = Image.new("RGB", (64, 64), color=(100, 150, 200))
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    ahash = compute_image_ahash(img_bytes)
    assert ahash is not None
    assert len(ahash) == 16
