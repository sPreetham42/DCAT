import torch
from dcat.models.crossattention.attention import BidirectionalCrossAttention

def test_bidirectional_attention_shape():
    attn = BidirectionalCrossAttention(layers=1, d_model=256, heads=4)
    
    text = torch.randn(2, 256, 256) # [B, T, D]
    image = torch.randn(2, 49, 256) # [B, N, D]
    
    # Simulate text padding mask (True means padding)
    mask = torch.zeros(2, 256, dtype=torch.bool)
    mask[0, 100:] = True 
    
    out_text, out_image = attn(text, image, mask)
    
    # Output shapes should strictly match input sequence lengths
    assert out_text.shape == (2, 256, 256)
    assert out_image.shape == (2, 49, 256)
