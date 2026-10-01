import torch
import torch.nn as nn

class ModalityProjector(nn.Module):
    """Projects text and image features into a shared latent space."""
    
    def __init__(self, text_dim: int = 768, image_dim: int = 640, shared_dim: int = 256):
        super().__init__()
        # Using a simple linear projection for both modalities.
        self.text_proj = nn.Linear(text_dim, shared_dim)
        self.image_proj = nn.Linear(image_dim, shared_dim)
        
        # We can add LayerNorm after projection for stability
        self.text_norm = nn.LayerNorm(shared_dim)
        self.image_norm = nn.LayerNorm(shared_dim)
        
    def project_text(self, text_features: torch.Tensor) -> torch.Tensor:
        """
        Args:
            text_features: [B, T, D_text]
        Returns:
            [B, T, shared_dim]
        """
        return self.text_norm(self.text_proj(text_features))
        
    def project_image(self, image_features: torch.Tensor) -> torch.Tensor:
        """
        Args:
            image_features: [B, N, D_img]
        Returns:
            [B, N, shared_dim]
        """
        return self.image_norm(self.image_proj(image_features))
