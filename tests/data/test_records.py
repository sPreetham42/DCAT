"""Unit tests for the typed data records (EmailRecord, ImageRecord, etc.)."""

from __future__ import annotations

import pytest

from dcat.data import (
    EmailRecord,
    ImageDisposition,
    ImageRecord,
    Modality,
    ParserOutput,
    RawImage,
)


class TestImageRecord:
    def test_defaults_are_sane(self):
        rec = ImageRecord(image_id="img-1")
        assert rec.width == 0
        assert rec.height == 0
        assert rec.filtered is False
        assert rec.selected is False

    def test_negative_dimension_rejected(self):
        with pytest.raises(ValueError):
            ImageRecord(image_id="x", width=-1)

    def test_filtered_requires_reason(self):
        with pytest.raises(ValueError):
            ImageRecord(image_id="x", filtered=True)

    def test_filtered_with_reason_ok(self):
        rec = ImageRecord(image_id="x", filtered=True, filter_reason="too_small")
        assert rec.filter_reason == "too_small"


class TestRawImage:
    def test_byte_size_from_data(self):
        raw = RawImage(image_id="i", data=b"\x00\x01\x02", content_type="image/png")
        assert raw.byte_size == 3

    def test_cid_and_disposition(self):
        raw = RawImage(
            image_id="i",
            data=b"x",
            content_type="image/png",
            disposition=ImageDisposition.INLINE,
            cid="abc@cid",
        )
        assert raw.cid == "abc@cid"
        assert raw.disposition == ImageDisposition.INLINE


class TestEmailRecord:
    def _valid(self, **kw):
        defaults = dict(
            email_id="e1",
            label=0,
            has_text=True,
            has_meaningful_image=False,
            modality=Modality.TEXT,
        )
        defaults.update(kw)
        return EmailRecord(**defaults)

    def test_consistent_multimodal(self):
        rec = EmailRecord(
            email_id="e1",
            label=1,
            has_text=True,
            has_meaningful_image=True,
            modality=Modality.MULTIMODAL,
        )
        assert rec.modality is Modality.MULTIMODAL

    def test_modality_consistency_enforced(self):
        with pytest.raises(ValueError, match="inconsistent"):
            self._valid(has_meaningful_image=True, modality=Modality.TEXT)

    def test_label_must_be_binary_or_none(self):
        with pytest.raises(ValueError, match="label"):
            self._valid(label=2)

    def test_none_label_allowed(self):
        rec = self._valid(label=None)
        assert rec.label is None

    def test_empty_modality(self):
        rec = EmailRecord(email_id="e", modality=Modality.EMPTY)
        assert rec.has_text is False
        assert rec.images == ()


class TestParserOutput:
    def test_defaults(self):
        out = ParserOutput(email_id="e1")
        assert out.subject is None
        assert out.images == ()
        assert out.errors == ()

    def test_carries_raw_images(self):
        raw = RawImage(image_id="i", data=b"x", content_type="image/png")
        out = ParserOutput(email_id="e", images=(raw,))
        assert out.images[0].image_id == "i"
