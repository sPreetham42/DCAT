import torch
from dcat.models.dcat.model import DcatModel
from dcat.data.modalities import Modality

def test_backward_pass():
    model = DcatModel(
        text_model_name="distilbert-base-uncased",
        vision_model_name="mobilevit_s",
        freeze_encoders=True,
        shared_dim=256,
        cross_attention_layers=1,
        cross_attention_heads=2
    )
    
    batch = {
        "input_ids": torch.randint(0, 1000, (3, 10)),
        "attention_mask": torch.ones(3, 10),
        "pixel_values": torch.randn(3, 3, 224, 224),
        "modality": [Modality.TEXT.value, Modality.IMAGE.value, Modality.MULTIMODAL.value],
    }
    
    logits = model(batch)
    assert logits.shape == (3, 1)
    
    loss = logits.mean()
    loss.backward()
    
    # Check that grads exist for cross-attention and projector
    assert model.projector.text_proj.weight.grad is not None
    assert model.projector.image_proj.weight.grad is not None
    assert model.classifier.net[0].weight.grad is not None
