import pytest
import torch
from dcat.data.dataset import DcatCollator
from dcat.data.modalities import Modality

def test_collator_rejects_empty():
    collator = DcatCollator()
    batch = [
        {"email_id": "1", "modality": Modality.TEXT.value, "label": 0, "input_ids": torch.zeros(10), "attention_mask": torch.zeros(10), "pixel_values": torch.zeros(3, 224, 224)},
        {"email_id": "2", "modality": Modality.EMPTY.value, "label": -1, "input_ids": torch.zeros(10), "attention_mask": torch.zeros(10), "pixel_values": torch.zeros(3, 224, 224)}
    ]
    with pytest.raises(ValueError, match="EMPTY modality in collator"):
        collator(batch)

def test_collator_shapes():
    collator = DcatCollator()
    batch = [
        {"email_id": "1", "modality": Modality.TEXT.value, "label": 1, "input_ids": torch.zeros(10), "attention_mask": torch.zeros(10), "pixel_values": torch.zeros(3, 224, 224)},
        {"email_id": "2", "modality": Modality.MULTIMODAL.value, "label": 0, "input_ids": torch.zeros(10), "attention_mask": torch.zeros(10), "pixel_values": torch.zeros(3, 224, 224)}
    ]
    
    out = collator(batch)
    assert out["labels"].shape == (2, 1)
    assert out["input_ids"].shape == (2, 10)
    assert out["pixel_values"].shape == (2, 3, 224, 224)
