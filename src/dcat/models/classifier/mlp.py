import torch
import torch.nn as nn

class SharedClassifier(nn.Module):
    """Classification head for DCAT representations."""
    
    def __init__(self, input_dim: int = 256, hidden_dim: int = 128, dropout: float = 0.3):
        super().__init__()
        
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1) # Outputs logits for BCEWithLogitsLoss
        )
        
    def forward(self, features: torch.Tensor) -> torch.Tensor:
        """
        Args:
            features: [B, input_dim]
        Returns:
            logits: [B, 1]
        """
        return self.net(features)
