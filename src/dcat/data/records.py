"""Strongly typed, normalized email records.

These are the internal representation DCAT operates on. Importantly:

- **No image binaries are ever stored on a record.** A :class:`RawImage`
  carries bytes only transiently during preprocessing; the persisted
  :class:`ImageRecord` stores references/paths and metadata (hashes, dims,
  filter status).
- The records carry no ML dependency; they are plain frozen dataclasses.

The contract is deliberately small and explicit so downstream components
(parser, router, image pipeline, dataset writers) agree on field meaning.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from dcat.data.modalities import Modality, modality_from_flags


class ImageDisposition(str, Enum):
    """How an image was attached in the original MIME message."""

    INLINE = "inline"  # referenced from the HTML body (content-id or src)
    ATTACHMENT = "attachment"  # standalone attachment
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class RawImage:
    """A decoded-but-not-yet-processed image extracted by the MIME parser.

    ``data`` holds the raw encoded bytes. This object is transient: it is used
    by the image-processing pipeline and is **never** written to Parquet.
    """

    image_id: str
    data: bytes
    content_type: str
    disposition: ImageDisposition = ImageDisposition.UNKNOWN
    cid: str | None = None
    filename: str | None = None

    @property
    def byte_size(self) -> int:
        """Size of the raw encoded payload in bytes."""
        return len(self.data)


@dataclass(frozen=True)
class ImageRecord:
    """Persisted metadata for a single image extracted from an email.

    Stores references and derived metadata only — never the binary content
    itself. ``source_path`` is an optional on-disk reference (e.g. the path to
    a decoded/processed artifact); it may be None when the image lives only in
    memory during a run.
    """

    image_id: str
    source_path: str | None = None
    mime_type: str | None = None
    width: int = 0
    height: int = 0
    byte_size: int = 0
    cid: str | None = None
    exact_hash: str | None = None
    perceptual_hash: str | None = None
    filtered: bool = False
    filter_reason: str | None = None
    selected: bool = False

    def __post_init__(self) -> None:
        if self.width < 0 or self.height < 0 or self.byte_size < 0:
            raise ValueError("ImageRecord dimensions and byte_size must be non-negative")
        if self.filtered and not self.filter_reason:
            raise ValueError("A filtered image must carry a filter_reason")


@dataclass(frozen=True)
class ParserOutput:
    """Result of deterministic MIME extraction (before routing/filtering).

    ``images`` are :class:`RawImage` objects (unprocessed). ``errors`` holds
    non-fatal parsing issues observed while walking the MIME tree; fatal
    problems raise instead and are not represented here.
    """

    email_id: str
    subject: str | None = None
    text: str | None = None
    html: str | None = None
    images: tuple[RawImage, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class EmailRecord:
    """The normalized, fully-processed representation of one email.

    ``label`` is 0 (ham) or 1 (spam), or None when unknown (e.g. for inference).
    ``text`` and ``html`` are the extracted textual content; ``images`` hold
    processed image metadata (never binaries). ``modality`` is the deterministic
    route derived from ``has_text`` and ``has_meaningful_image``.
    """

    email_id: str
    label: int | None = None
    subject: str | None = None
    text: str | None = None
    html: str | None = None
    images: tuple[ImageRecord, ...] = ()
    has_text: bool = False
    has_meaningful_image: bool = False
    modality: Modality = Modality.EMPTY
    sender_hash: str | None = None
    campaign_id: str | None = None
    split: str | None = None

    def __post_init__(self) -> None:
        if self.label is not None and self.label not in (0, 1):
            raise ValueError(f"label must be 0, 1, or None; got {self.label!r}")
        # modality must be consistent with the content flags.
        expected = modality_from_flags(self.has_text, self.has_meaningful_image)
        if self.modality is not expected:
            raise ValueError(
                f"modality {self.modality.value!r} inconsistent with "
                f"has_text={self.has_text} has_meaningful_image={self.has_meaningful_image}; "
                f"expected {expected.value!r}"
            )


__all__ = [
    "EmailRecord",
    "ImageDisposition",
    "ImageRecord",
    "Modality",
    "ParserOutput",
    "RawImage",
]
