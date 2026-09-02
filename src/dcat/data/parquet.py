"""Parquet serialization and deserialization for normalized EmailRecord objects.

Stores EmailRecord dataset splits as columnar Parquet files using PyArrow.
Crucially:
- No raw binary image payloads are stored in Parquet.
- Image metadata (:class:`ImageRecord`) is serialized to structured JSON strings.
- Preserves schema metadata including DCAT dataset version.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

import pyarrow as pa
import pyarrow.parquet as pq

from dcat.data.modalities import Modality
from dcat.data.records import EmailRecord, ImageRecord

_SCHEMA_VERSION = "0.1.0"


def _image_record_to_dict(rec: ImageRecord) -> dict:
    return {
        "image_id": rec.image_id,
        "source_path": rec.source_path,
        "mime_type": rec.mime_type,
        "width": rec.width,
        "height": rec.height,
        "byte_size": rec.byte_size,
        "cid": rec.cid,
        "exact_hash": rec.exact_hash,
        "perceptual_hash": rec.perceptual_hash,
        "filtered": rec.filtered,
        "filter_reason": rec.filter_reason,
        "selected": rec.selected,
    }


def _dict_to_image_record(data: dict) -> ImageRecord:
    return ImageRecord(
        image_id=data["image_id"],
        source_path=data.get("source_path"),
        mime_type=data.get("mime_type"),
        width=data.get("width", 0),
        height=data.get("height", 0),
        byte_size=data.get("byte_size", 0),
        cid=data.get("cid"),
        exact_hash=data.get("exact_hash"),
        perceptual_hash=data.get("perceptual_hash"),
        filtered=data.get("filtered", False),
        filter_reason=data.get("filter_reason"),
        selected=data.get("selected", False),
    )


class ParquetDatasetWriter:
    """Serializes lists of EmailRecord objects to Parquet format."""

    @staticmethod
    def save_records(records: Sequence[EmailRecord], path: str | Path) -> None:
        """Write a sequence of EmailRecords to a Parquet file.

        Args:
            records: sequence of EmailRecord instances.
            path: destination file path.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        columns = {
            "email_id": [r.email_id for r in records],
            "label": [r.label if r.label is not None else -1 for r in records],  # -1 represents None
            "subject": [r.subject or "" for r in records],
            "text": [r.text or "" for r in records],
            "html": [r.html or "" for r in records],
            "images_json": [json.dumps([_image_record_to_dict(img) for img in r.images]) for r in records],
            "has_text": [r.has_text for r in records],
            "has_meaningful_image": [r.has_meaningful_image for r in records],
            "modality": [r.modality.value for r in records],
            "sender_hash": [r.sender_hash or "" for r in records],
            "campaign_id": [r.campaign_id or "" for r in records],
            "split": [r.split or "" for r in records],
        }

        table = pa.Table.from_pydict(columns)

        # Attach schema metadata
        meta = {
            b"dcat_schema_version": _SCHEMA_VERSION.encode("utf-8"),
            b"record_count": str(len(records)).encode("utf-8"),
        }
        table = table.replace_schema_metadata(meta)

        pq.write_table(table, path, compression="SNAPPY")


class ParquetDatasetReader:
    """Deserializes Parquet files back into EmailRecord lists."""

    @staticmethod
    def load_records(path: str | Path) -> list[EmailRecord]:
        """Read a Parquet file and construct EmailRecord instances.

        Args:
            path: input Parquet file path.

        Returns:
            List of reconstructed EmailRecord instances.
        """
        path = Path(path)
        if not path.is_file():
            raise FileNotFoundError(f"Parquet dataset file not found: {path}")

        table = pq.read_table(path)
        df = table.to_pandas()

        records: list[EmailRecord] = []
        for _, row in df.iterrows():
            lbl_val = int(row["label"])
            label = lbl_val if lbl_val in (0, 1) else None

            imgs_data = json.loads(row["images_json"])
            images = tuple(_dict_to_image_record(item) for item in imgs_data)

            subj = str(row["subject"]) if row["subject"] else None
            txt = str(row["text"]) if row["text"] else None
            htm = str(row["html"]) if row["html"] else None
            snd = str(row["sender_hash"]) if row["sender_hash"] else None
            cmp_id = str(row["campaign_id"]) if row["campaign_id"] else None
            spl = str(row["split"]) if row["split"] else None

            rec = EmailRecord(
                email_id=str(row["email_id"]),
                label=label,
                subject=subj,
                text=txt,
                html=htm,
                images=images,
                has_text=bool(row["has_text"]),
                has_meaningful_image=bool(row["has_meaningful_image"]),
                modality=Modality(row["modality"]),
                sender_hash=snd,
                campaign_id=cmp_id,
                split=spl,
            )
            records.append(rec)

        return records


__all__ = ["ParquetDatasetReader", "ParquetDatasetWriter"]
