"""End-to-end Phase 1 integration test.

Covers:
raw .eml bytes
  -> MimeParser
  -> HtmlProcessor & ImageProcessor
  -> ModalityRouter
  -> EmailRecord
  -> ParquetDatasetWriter / ParquetDatasetReader
"""

from __future__ import annotations

import io
import tempfile
from pathlib import Path

from PIL import Image

from dcat.data import Modality
from dcat.data.parquet import ParquetDatasetReader, ParquetDatasetWriter
from dcat.preprocessing import MimeParser, ModalityRouter


def _build_sample_eml() -> bytes:
    buf = io.BytesIO()
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    img.save(buf, format="JPEG")
    img_bytes = buf.getvalue()

    import base64

    b64_img = base64.b64encode(img_bytes).decode("ascii")

    eml = (
        f"From: sender@example.com\n"
        f"To: victim@example.com\n"
        f"Subject: Multimodal Special Offer\n"
        f"MIME-Version: 1.0\n"
        f"Content-Type: multipart/mixed; boundary=boundary123\n\n"
        f"--boundary123\n"
        f"Content-Type: text/html; charset=utf-8\n\n"
        f"<html><body><h2>Special Multimodal Offer</h2><p>Check out our image below!</p></body></html>\n"
        f"--boundary123\n"
        f"Content-Type: image/jpeg\n"
        f"Content-Transfer-Encoding: base64\n"
        f"Content-Disposition: attachment; filename=offer.jpg\n\n"
        f"{b64_img}\n"
        f"--boundary123--\n"
    ).encode("utf-8")

    return eml


def test_end_to_end_phase1_pipeline():
    eml_bytes = _build_sample_eml()

    # 1. Parse raw MIME
    parser = MimeParser()
    po = parser.parse_bytes(eml_bytes, email_id="integration_001")

    assert po.subject == "Multimodal Special Offer"
    assert po.text is not None
    assert "Special Multimodal Offer" in po.text
    assert len(po.images) == 1

    # 2. Route & process images/text
    from dcat.preprocessing.router import RouterConfig

    router = ModalityRouter(config=RouterConfig(min_image_bytes=10))
    routed = router.route(
        po,
        label=1,
        sender_hash="hash_sender_example",
        campaign_id="cmp_001",
        split="train",
    )

    rec = routed.record
    assert rec.email_id == "integration_001"
    assert rec.label == 1
    assert rec.has_text is True
    assert rec.has_meaningful_image is True
    assert rec.modality is Modality.MULTIMODAL
    assert routed.selected_image_tensor is not None
    assert routed.selected_image_tensor.shape == (3, 224, 224)

    # 3. Serialize to Parquet and reload
    with tempfile.TemporaryDirectory() as tmpdir:
        pq_file = Path(tmpdir) / "test_out.parquet"
        ParquetDatasetWriter.save_records([rec], pq_file)

        loaded_records = ParquetDatasetReader.load_records(pq_file)
        assert len(loaded_records) == 1
        loaded_rec = loaded_records[0]

        assert loaded_rec.email_id == rec.email_id
        assert loaded_rec.modality is Modality.MULTIMODAL
        assert loaded_rec.has_text is True
        assert loaded_rec.has_meaningful_image is True
