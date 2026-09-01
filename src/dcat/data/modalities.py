"""Modality types for DCAT.

An email is routed to one of three computational paths based on the actual
content that survives extraction and image filtering. This module defines the
single source of truth for those routes.
"""

from __future__ import annotations

from enum import Enum


class Modality(str, Enum):
    """The computational route an email is sent down.

    The route is deterministic: it depends only on whether meaningful text and
    meaningful images were extracted, never on a learned classifier.

    - ``TEXT``: meaningful text present, no meaningful image.
    - ``IMAGE``: meaningful image present, no meaningful text.
    - ``MULTIMODAL``: both meaningful text and a meaningful image present.
    - ``EMPTY``: neither; the email carries no meaningful content for DCAT.
    """

    TEXT = "text"
    IMAGE = "image"
    MULTIMODAL = "multimodal"
    EMPTY = "empty"

    @property
    def is_multimodal(self) -> bool:
        """True when both encoders are required."""
        return self is Modality.MULTIMODAL

    @property
    def uses_text_encoder(self) -> bool:
        return self in (Modality.TEXT, Modality.MULTIMODAL)

    @property
    def uses_image_encoder(self) -> bool:
        return self in (Modality.IMAGE, Modality.MULTIMODAL)


def modality_from_flags(has_text: bool, has_meaningful_image: bool) -> Modality:
    """Determine the modality deterministically from content flags.

    Args:
        has_text: whether meaningful text was extracted.
        has_meaningful_image: whether at least one meaningful (post-filter) image exists.

    Returns:
        The corresponding :class:`Modality`. No modality is ever discarded
        silently: an email with neither content maps to ``EMPTY``.
    """
    if has_text and has_meaningful_image:
        return Modality.MULTIMODAL
    if has_text:
        return Modality.TEXT
    if has_meaningful_image:
        return Modality.IMAGE
    return Modality.EMPTY
