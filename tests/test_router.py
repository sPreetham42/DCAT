"""Unit tests for ModalityRouter."""

from __future__ import annotations

import io

from PIL import Image

from dcat.data import ImageDisposition, Modality, ParserOutput, RawImage
from dcat.preprocessing.router import ModalityRouter, RouterConfig


def _create_image_bytes(w: int, h: int) -> bytes:
    buf = io.BytesIO()
    img = Image.new("RGB", (w, h), color=(0, 255, 0))
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_router_text_only():
    router = ModalityRouter(config=RouterConfig(min_html_text_length=10))
    po = ParserOutput(
        email_id="msg_text",
        text="This is a sufficiently long plain text email body.",
        images=(),
    )

    res = router.route(po)
    assert res.record.modality is Modality.TEXT
    assert res.record.has_text is True
    assert res.record.has_meaningful_image is False
    assert res.selected_image_tensor is None


def test_router_image_only():
    router = ModalityRouter(
        config=RouterConfig(
            min_html_text_length=10, min_image_width=20, min_image_height=20, min_image_bytes=10
        )
    )

    img_bytes = _create_image_bytes(100, 100)
    raw_img = RawImage(
        image_id="img1",
        data=img_bytes,
        content_type="image/jpeg",
        disposition=ImageDisposition.ATTACHMENT,
    )

    po = ParserOutput(
        email_id="msg_img",
        text="Short",  # Below min threshold 10
        images=(raw_img,),
    )

    res = router.route(po)
    assert res.record.modality is Modality.IMAGE
    assert res.record.has_text is False
    assert res.record.has_meaningful_image is True
    assert res.selected_image_tensor is not None
    assert res.selected_image_tensor.shape == (3, 224, 224)


def test_router_multimodal():
    router = ModalityRouter(
        config=RouterConfig(
            min_html_text_length=10, min_image_width=20, min_image_height=20, min_image_bytes=10
        )
    )

    img_bytes = _create_image_bytes(100, 100)
    raw_img = RawImage(
        image_id="img1",
        data=img_bytes,
        content_type="image/jpeg",
        disposition=ImageDisposition.INLINE,
    )

    po = ParserOutput(
        email_id="msg_mm",
        text="This email has both long meaningful text body and an attached image.",
        images=(raw_img,),
    )

    res = router.route(po)
    assert res.record.modality is Modality.MULTIMODAL
    assert res.record.has_text is True
    assert res.record.has_meaningful_image is True
    assert res.selected_image_tensor is not None


def test_router_empty():
    router = ModalityRouter(config=RouterConfig(min_html_text_length=10))
    po = ParserOutput(
        email_id="msg_empty",
        text="Hi",  # Below 10
        images=(),
    )

    res = router.route(po)
    assert res.record.modality is Modality.EMPTY
    assert res.record.has_text is False
    assert res.record.has_meaningful_image is False
    assert res.selected_image_tensor is None
