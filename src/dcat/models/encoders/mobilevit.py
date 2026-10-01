import torch
import torch.nn as nn
import timm

class VisionEncoder(nn.Module):
    """MobileViT wrapper returning pre-pooling spatial features."""
    
    def __init__(self, model_name: str = "mobilevit_s", freeze: bool = True):
        super().__init__()
        # Use forward_features to get spatial features before pooling
        self.model = timm.create_model(model_name, pretrained=True, num_classes=0)
        
        if freeze:
            for param in self.model.parameters():
                param.requires_grad = False
                
    def forward(self, pixel_values: torch.Tensor) -> torch.Tensor:
        """
        Args:
            pixel_values: [B, 3, H, W] (e.g. 224x224)
        Returns:
            features: [B, N, D_img] where N = H' * W'
            For mobilevit_s (224x224), output is [B, 640, 7, 7] -> [B, 49, 640]
        """
        # forward_features returns [B, C, H', W'] for convolutional/hybrid models
        features = self.model.forward_features(pixel_values)
        
        # Flatten spatial dimensions: [B, C, H', W'] -> [B, C, H'*W'] -> [B, H'*W', C]
        if features.dim() == 4:
            b, c, h, w = features.shape
            features = features.view(b, c, h * w).transpose(1, 2)
            
        return features
