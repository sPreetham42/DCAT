"""Deterministic modality routing engine for DCAT emails.

Maps extracted content (:class:`ParserOutput` + processed :class:`ImageRecord`s)
to one of four explicit modalities:

- ``TEXT``: meaningful text present, no meaningful image.
- ``IMAGE``: meaningful image present, no meaningful text.
- ``MULTIMODAL``: both text and image present.
- ``EMPTY``: neither; no computational path required.

Core design rule: Routing is strictly deterministic and content-based.
It never uses a learned classifier, fake probability distributions, or dummy vectors.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from dcat.data import EmailRecord, ImageRecord, ParserOutput, modality_from_flags
from dcat.preprocessing.image_processor import ImageProcessor, ImageProcessorConfig

if TYPE_CHECKING:
    import torch


@dataclass(frozen=True)
class RouterConfig:
    """Threshold configuration for deterministic modality routing."""

    min_html_text_length: int = 10
    min_image_width: int = 20
    min_image_height: int = 20
    min_image_bytes: int = 1024

    @classmethod
    def from_dict(cls, data: dict[str, int]) -> RouterConfig:
        return cls(
            min_html_text_length=data.get("min_html_text_length", 10),
            min_image_width=data.get("min_image_width", 20),
            min_image_height=data.get("min_image_height", 20),
            min_image_bytes=data.get("min_image_bytes", 1024),
        )


@dataclass(frozen=True)
class RoutedEmailResult:
    """Complete result of routing an email through preprocessing."""

    record: EmailRecord
    selected_image_tensor: torch.Tensor | None = None  # FloatTensor [3, 224, 224] if image route active


class ModalityRouter:
    """Deterministic content router and EmailRecord builder."""

    def __init__(
        self,
        config: RouterConfig | None = None,
        image_processor: ImageProcessor | None = None,
    ) -> None:
        self.config = config or RouterConfig()
        img_cfg = ImageProcessorConfig(
            min_image_width=self.config.min_image_width,
            min_image_height=self.config.min_image_height,
            min_image_bytes=self.config.min_image_bytes,
        )
        self.image_processor = image_processor or ImageProcessor(config=img_cfg)

    def route(
        self,
        parser_output: ParserOutput,
        label: int | None = None,
        sender_hash: str | None = None,
        campaign_id: str | None = None,
        split: str | None = None,
    ) -> RoutedEmailResult:
        """Route a ParserOutput into a normalized EmailRecord and optional image tensor.

        Args:
            parser_output: the raw extraction from MimeParser.
            label: 0 (ham), 1 (spam), or None.
            sender_hash: optional sender identifier/hash.
            campaign_id: optional campaign identifier.
            split: optional split name ("train", "val", "test").

        Returns:
            RoutedEmailResult containing EmailRecord and optional image tensor.
        """
        # 1. Evaluate text content
        extracted_text = parser_output.text or ""
        clean_text = extracted_text.strip()
        has_text = len(clean_text) >= self.config.min_html_text_length

        # 2. Evaluate and process images
        image_records: list[ImageRecord] = []
        meaningful_indices: list[int] = []

        for idx, raw_img in enumerate(parser_output.images):
            res = self.image_processor.process_raw_image(raw_img, select=False)
            image_records.append(res.record)
            if not res.record.filtered:
                meaningful_indices.append(idx)

        has_meaningful_image = len(meaningful_indices) > 0

        # Select top-1 largest meaningful image if image encoder is required
        selected_tensor = None
        if has_meaningful_image:
            # Sort non-filtered images by (byte_size, width*height) descending to pick top-1
            top_idx = max(
                meaningful_indices,
                key=lambda i: (
                    parser_output.images[i].byte_size,
                    image_records[i].width * image_records[i].height,
                ),
            )
            # Re-process top image with select=True to build normalized tensor
            top_res = self.image_processor.process_raw_image(parser_output.images[top_idx], select=True)
            image_records[top_idx] = top_res.record
            selected_tensor = top_res.tensor

        # 3. Determine deterministic modality
        modality = modality_from_flags(
            has_text=has_text,
            has_meaningful_image=has_meaningful_image,
        )

        record = EmailRecord(
            email_id=parser_output.email_id,
            label=label,
            subject=parser_output.subject,
            text=clean_text if has_text else None,
            html=parser_output.html,
            images=tuple(image_records),
            has_text=has_text,
            has_meaningful_image=has_meaningful_image,
            modality=modality,
            sender_hash=sender_hash,
            campaign_id=campaign_id,
            split=split,
        )

        return RoutedEmailResult(record=record, selected_image_tensor=selected_tensor)


__all__ = ["ModalityRouter", "RoutedEmailResult", "RouterConfig"]
