import torch
import torch.nn as nn
from transformers import AutoModel

class TextEncoder(nn.Module):
    """DistilBERT wrapper that returns token-level hidden states."""
    
    def __init__(self, model_name: str = "distilbert-base-uncased", freeze: bool = True):
        super().__init__()
        self.model = AutoModel.from_pretrained(model_name)
        
        if freeze:
            for param in self.model.parameters():
                param.requires_grad = False
                
    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        """
        Args:
            input_ids: [B, T]
            attention_mask: [B, T]
        Returns:
            hidden_states: [B, T, D_text] (D_text=768 for distilbert-base)
        """
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
        # DistilBERT returns BaseModelOutput. last_hidden_state is the first element.
        return outputs.last_hidden_state
