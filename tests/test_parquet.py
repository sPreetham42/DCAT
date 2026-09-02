"""Unit tests for Parquet serialization and deserialization."""

from __future__ import annotations

import tempfile
from pathlib import Path

from dcat.data import EmailRecord, ImageRecord, Modality
from dcat.data.parquet import ParquetDatasetReader, ParquetDatasetWriter


def test_parquet_serialization_roundtrip():
    img1 = ImageRecord(
        image_id="img_101",
        mime_type="image/jpeg",
        width=300,
        height=200,
        byte_size=15000,
        exact_hash="abc123hash",
        filtered=False,
    )

    rec1 = EmailRecord(
        email_id="email_001",
        label=1,
        subject="Spam Offer",
        text="Click here to win $1000000 right now!",
        html="<p>Click here to win $1000000 right now!</p>",
        images=(img1,),
        has_text=True,
        has_meaningful_image=True,
        modality=Modality.MULTIMODAL,
        sender_hash="sender_hash_xyz",
        campaign_id="campaign_99",
        split="train",
    )

    rec2 = EmailRecord(
        email_id="email_002",
        label=0,
        subject="Meeting Schedule",
        text="Hi team, please find attached the meeting notes for today.",
        html=None,
        images=(),
        has_text=True,
        has_meaningful_image=False,
        modality=Modality.TEXT,
        sender_hash="sender_boss",
        split="val",
    )

    original_records = [rec1, rec2]

    with tempfile.TemporaryDirectory() as tmpdir:
        pq_path = Path(tmpdir) / "records.parquet"
        ParquetDatasetWriter.save_records(original_records, pq_path)
        assert pq_path.is_file()

        loaded_records = ParquetDatasetReader.load_records(pq_path)
        assert len(loaded_records) == 2

        assert loaded_records[0].email_id == rec1.email_id
        assert loaded_records[0].label == rec1.label
        assert loaded_records[0].modality == rec1.modality
        assert len(loaded_records[0].images) == 1
        assert loaded_records[0].images[0].image_id == img1.image_id
        assert loaded_records[0].images[0].exact_hash == img1.exact_hash

        assert loaded_records[1].email_id == rec2.email_id
        assert loaded_records[1].label == rec2.label
        assert loaded_records[1].modality == rec2.modality
