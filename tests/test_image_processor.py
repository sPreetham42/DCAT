"""Unit tests for ImageProcessor."""

from __future__ import annotations

import io

import torch
from PIL import Image

from dcat.data import ImageDisposition, RawImage
from dcat.preprocessing.image_processor import ImageProcessor, ImageProcessorConfig


def _create_test_image_bytes(width: int, height: int, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    img = Image.new("RGB", (width, height), color=(255, 0, 0))
    img.save(buf, format=fmt)
    return buf.getvalue()


def test_image_processor_tracking_pixel_filtering():
    processor = ImageProcessor(
        config=ImageProcessorConfig(min_image_width=20, min_image_height=20, min_image_bytes=100)
    )

    # 1x1 tracking pixel
    small_bytes = _create_test_image_bytes(1, 1)
    raw_small = RawImage(
        image_id="img_track",
        data=small_bytes,
        content_type="image/png",
        disposition=ImageDisposition.INLINE,
    )

    res = processor.process_raw_image(raw_small)
    assert res.record.filtered is True
    assert "below_min" in res.record.filter_reason
    assert res.tensor is None


def test_image_processor_meaningful_image_selection():
    processor = ImageProcessor(
        config=ImageProcessorConfig(min_image_width=20, min_image_height=20, min_image_bytes=10)
    )

    img_bytes = _create_test_image_bytes(100, 100)
    raw = RawImage(
        image_id="img_valid",
        data=img_bytes,
        content_type="image/png",
        disposition=ImageDisposition.ATTACHMENT,
    )

    res = processor.process_raw_image(raw, select=True)
    assert res.record.filtered is False
    assert res.record.selected is True
    assert res.tensor is not None
    assert isinstance(res.tensor, torch.Tensor)
    assert res.tensor.shape == (3, 224, 224)


def test_image_processor_corrupted_bytes_handling():
    processor = ImageProcessor()
    corrupt_raw = RawImage(
        image_id="img_corrupt",
        data=b"not_an_image_header_bytes_1234567890",
        content_type="image/jpeg",
    )

    res = processor.process_raw_image(corrupt_raw)
    assert res.record.filtered is True
    assert "decode_error" in res.record.filter_reason or "byte_size" in res.record.filter_reason
    assert res.tensor is None
