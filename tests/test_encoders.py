import torch
from dcat.models.encoders.distilbert import TextEncoder
from dcat.models.encoders.mobilevit import VisionEncoder
from dcat.models.projection.projector import ModalityProjector

def test_distilbert_shape():
    encoder = TextEncoder(freeze=True)
    input_ids = torch.randint(0, 1000, (2, 256))
    mask = torch.ones(2, 256)
    out = encoder(input_ids, mask)
    assert out.shape == (2, 256, 768)

def test_mobilevit_shape():
    encoder = VisionEncoder(freeze=True)
    pixel_values = torch.randn(2, 3, 224, 224)
    out = encoder(pixel_values)
    # 224 / 32 = 7 -> 7x7 = 49 patches. 640 feature channels.
    assert out.shape == (2, 49, 640)

def test_projection_shape():
    projector = ModalityProjector()
    text = torch.randn(2, 256, 768)
    image = torch.randn(2, 49, 640)
    
    p_text = projector.project_text(text)
    p_image = projector.project_image(image)
    
    assert p_text.shape == (2, 256, 256)
    assert p_image.shape == (2, 49, 256)
