import torch
import torch.nn as nn
import torch.nn.functional as F

class CrossAttentionLayer(nn.Module):
    """A single layer of bidirectional cross-attention with Pre-LN."""
    
    def __init__(self, d_model: int = 256, heads: int = 4, d_ff: int = 1024, dropout: float = 0.1, activation: str = "gelu"):
        super().__init__()
        
        # Text attending to Image
        self.norm_t1 = nn.LayerNorm(d_model)
        self.norm_i1 = nn.LayerNorm(d_model)
        self.mha_t2i = nn.MultiheadAttention(d_model, heads, dropout=dropout, batch_first=True)
        
        # Image attending to Text
        self.norm_i2 = nn.LayerNorm(d_model)
        self.norm_t2 = nn.LayerNorm(d_model)
        self.mha_i2t = nn.MultiheadAttention(d_model, heads, dropout=dropout, batch_first=True)
        
        # FFNs
        self.norm_t_ff = nn.LayerNorm(d_model)
        self.ff_t = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU() if activation == "gelu" else nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout)
        )
        
        self.norm_i_ff = nn.LayerNorm(d_model)
        self.ff_i = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU() if activation == "gelu" else nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout)
        )
        
    def forward(self, text: torch.Tensor, image: torch.Tensor, text_mask: torch.Tensor | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            text: [B, T, D]
            image: [B, N, D]
            text_mask: [B, T] boolean mask where True means padding.
        """
        # Pre-LN
        t_norm = self.norm_t1(text)
        i_norm = self.norm_i1(image)
        
        # Text attends to Image:
        # Query (Q) = Text
        # Key (K) = Image
        # Value (V) = Image
        # (no mask for image patches since we assume fixed size or no padding)
        t_out, _ = self.mha_t2i(query=t_norm, key=i_norm, value=i_norm)
        text = text + t_out
        
        # Image attends to Text:
        # Query (Q) = Image
        # Key (K) = Text
        # Value (V) = Text
        i_norm2 = self.norm_i2(image)
        t_norm2 = self.norm_t2(text)
        i_out, _ = self.mha_i2t(query=i_norm2, key=t_norm2, value=t_norm2, key_padding_mask=text_mask)
        image = image + i_out
        
        # FFN Text
        text = text + self.ff_t(self.norm_t_ff(text))
        
        # FFN Image
        image = image + self.ff_i(self.norm_i_ff(image))
        
        return text, image

class BidirectionalCrossAttention(nn.Module):
    """Stack of CrossAttentionLayers."""
    
    def __init__(self, layers: int = 2, d_model: int = 256, heads: int = 4, d_ff: int = 1024, dropout: float = 0.1, activation: str = "gelu"):
        super().__init__()
        self.layers = nn.ModuleList([
            CrossAttentionLayer(d_model, heads, d_ff, dropout, activation) for _ in range(layers)
        ])
        
    def forward(self, text: torch.Tensor, image: torch.Tensor, text_mask: torch.Tensor | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        for layer in self.layers:
            text, image = layer(text, image, text_mask)
        return text, image
