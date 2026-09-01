"""Unit tests for the modality enum and deterministic routing flags."""

from __future__ import annotations

import pytest

from dcat.data import Modality, modality_from_flags


@pytest.mark.parametrize(
    ("has_text", "has_image", "expected"),
    [
        (False, False, Modality.EMPTY),
        (True, False, Modality.TEXT),
        (False, True, Modality.IMAGE),
        (True, True, Modality.MULTIMODAL),
    ],
)
def test_modality_from_flags(has_text, has_image, expected):
    assert modality_from_flags(has_text, has_image) is expected


def test_multimodal_requires_both_encoders():
    m = Modality.MULTIMODAL
    assert m.uses_text_encoder and m.uses_image_encoder
    assert m.is_multimodal


def test_unimodal_routes_use_only_their_encoder():
    assert Modality.TEXT.uses_text_encoder and not Modality.TEXT.uses_image_encoder
    assert Modality.IMAGE.uses_image_encoder and not Modality.IMAGE.uses_text_encoder
    assert not Modality.EMPTY.uses_text_encoder
    assert not Modality.EMPTY.uses_image_encoder


def test_modality_values_are_lowercase_strings():
    assert Modality.MULTIMODAL.value == "multimodal"
    assert Modality.TEXT.value == "text"
    assert Modality.IMAGE.value == "image"
    assert Modality.EMPTY.value == "empty"
