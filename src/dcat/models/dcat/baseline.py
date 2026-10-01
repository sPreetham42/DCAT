import torch
import torch.nn as nn
from typing import Dict, Any

from dcat.models.encoders.distilbert import TextEncoder
from dcat.models.encoders.mobilevit import VisionEncoder
from dcat.models.projection.projector import ModalityProjector
from dcat.models.encoders.resnet import ResNetEncoder
from dcat.models.classifier.mlp import SharedClassifier
from dcat.data.modalities import Modality

class LateFusionBaseline(nn.Module):
    """A Late-Fusion multimodal baseline for comparison."""
    
    def __init__(
        self,
        text_model_name: str = "distilbert-base-uncased",
        vision_model_name: str = "mobilevit_s",
        freeze_encoders: bool = True,
        shared_dim: int = 256,
        classifier_hidden: int = 128
    ):
        super().__init__()
        
        self.text_encoder = TextEncoder(model_name=text_model_name, freeze=freeze_encoders)
        self.vision_encoder = VisionEncoder(model_name=vision_model_name, freeze=freeze_encoders)
        self.projector = ModalityProjector(text_dim=768, image_dim=640, shared_dim=shared_dim)
        
        # Classifier for late fusion
        # unimodal uses 256, multimodal uses 512
        self.unimodal_classifier = SharedClassifier(input_dim=shared_dim, hidden_dim=classifier_hidden)
        self.multimodal_classifier = SharedClassifier(input_dim=shared_dim * 2, hidden_dim=classifier_hidden)
        
    def _mean_pool(self, features: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        if mask is not None:
            mask = mask.unsqueeze(-1).float()
            return torch.sum(features * mask, dim=1) / torch.clamp(torch.sum(mask, dim=1), min=1e-9)
        else:
            return features.mean(dim=1)

    def forward(self, batch: Dict[str, Any]) -> torch.Tensor:
        device = batch["input_ids"].device
        bsz = len(batch["modality"])
        
        # Allocate logits with the same dtype as model parameters to support AMP
        logits = torch.zeros(bsz, 1, device=device, dtype=self.projector.text_proj.weight.dtype)
        
        is_text = torch.tensor([m == Modality.TEXT.value for m in batch["modality"]], device=device)
        is_image = torch.tensor([m == Modality.IMAGE.value for m in batch["modality"]], device=device)
        is_multi = torch.tensor([m == Modality.MULTIMODAL.value for m in batch["modality"]], device=device)
        
        has_text_mask = is_text | is_multi
        text_reps_all = None
        if has_text_mask.any():
            text_inputs = batch["input_ids"][has_text_mask]
            text_attn = batch["attention_mask"][has_text_mask]
            text_feats = self.text_encoder(text_inputs, text_attn)
            text_reps_all = self.projector.project_text(text_feats)
            
        has_image_mask = is_image | is_multi
        image_reps_all = None
        if has_image_mask.any():
            img_inputs = batch["pixel_values"][has_image_mask]
            img_feats = self.vision_encoder(img_inputs)
            image_reps_all = self.projector.project_image(img_feats)
            
        if is_text.any():
            text_only_idx = is_text[has_text_mask]
            pooled_text = self._mean_pool(text_reps_all[text_only_idx], batch["attention_mask"][is_text])
            logits[is_text] = self.unimodal_classifier(pooled_text).to(logits.dtype)
            
        if is_image.any():
            img_only_idx = is_image[has_image_mask]
            pooled_img = self._mean_pool(image_reps_all[img_only_idx])
            logits[is_image] = self.unimodal_classifier(pooled_img).to(logits.dtype)
            
        if is_multi.any():
            multi_text_idx = is_multi[has_text_mask]
            multi_img_idx = is_multi[has_image_mask]
            
            pooled_text = self._mean_pool(text_reps_all[multi_text_idx], batch["attention_mask"][is_multi])
            pooled_img = self._mean_pool(image_reps_all[multi_img_idx])
            
            # Late fusion concatenation
            fused_reps = torch.cat([pooled_text, pooled_img], dim=-1)
            logits[is_multi] = self.multimodal_classifier(fused_reps).to(logits.dtype)
            
        return logits

class PublishedBaseline(nn.Module):
    """Reimplementation of published multimodal baseline (e.g., MMTD archetype).
    Uses standard text (DistilBERT) and vision (ResNet) encoders with late fusion."""
    
    def __init__(
        self,
        text_model_name: str = "distilbert-base-uncased",
        vision_model_name: str = "resnet18",
        freeze_encoders: bool = True,
        shared_dim: int = 256,
        classifier_hidden: int = 128
    ):
        super().__init__()
        
        self.text_encoder = TextEncoder(model_name=text_model_name, freeze=freeze_encoders)
        self.vision_encoder = ResNetEncoder(model_name=vision_model_name, freeze=freeze_encoders)
        
        # ResNet18 outputs 512, DistilBERT outputs 768
        self.projector = ModalityProjector(text_dim=768, image_dim=512, shared_dim=shared_dim)
        
        # Classifier for late fusion
        # unimodal uses 256, multimodal uses 512
        self.unimodal_classifier = SharedClassifier(input_dim=shared_dim, hidden_dim=classifier_hidden)
        self.multimodal_classifier = SharedClassifier(input_dim=shared_dim * 2, hidden_dim=classifier_hidden)
        
    def _mean_pool(self, features: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        if mask is not None:
            mask = mask.unsqueeze(-1).float()
            return torch.sum(features * mask, dim=1) / torch.clamp(torch.sum(mask, dim=1), min=1e-9)
        else:
            return features.mean(dim=1)

    def forward(self, batch: Dict[str, Any]) -> torch.Tensor:
        device = batch["input_ids"].device
        bsz = len(batch["modality"])
        
        # Allocate logits with the same dtype as model parameters to support AMP
        logits = torch.zeros(bsz, 1, device=device, dtype=self.projector.text_proj.weight.dtype)
        
        is_text = torch.tensor([m == Modality.TEXT.value for m in batch["modality"]], device=device)
        is_image = torch.tensor([m == Modality.IMAGE.value for m in batch["modality"]], device=device)
        is_multi = torch.tensor([m == Modality.MULTIMODAL.value for m in batch["modality"]], device=device)
        
        has_text_mask = is_text | is_multi
        text_reps_all = None
        if has_text_mask.any():
            text_inputs = batch["input_ids"][has_text_mask]
            text_attn = batch["attention_mask"][has_text_mask]
            text_feats = self.text_encoder(text_inputs, text_attn)
            text_reps_all = self.projector.project_text(text_feats)
            
        has_image_mask = is_image | is_multi
        image_reps_all = None
        if has_image_mask.any():
            img_inputs = batch["pixel_values"][has_image_mask]
            img_feats = self.vision_encoder(img_inputs)
            image_reps_all = self.projector.project_image(img_feats)
            
        if is_text.any():
            text_only_idx = is_text[has_text_mask]
            pooled_text = self._mean_pool(text_reps_all[text_only_idx], batch["attention_mask"][is_text])
            logits[is_text] = self.unimodal_classifier(pooled_text).to(logits.dtype)
            
        if is_image.any():
            img_only_idx = is_image[has_image_mask]
            pooled_img = self._mean_pool(image_reps_all[img_only_idx])
            logits[is_image] = self.unimodal_classifier(pooled_img).to(logits.dtype)
            
        if is_multi.any():
            multi_text_idx = is_multi[has_text_mask]
            multi_img_idx = is_multi[has_image_mask]
            
            pooled_text = self._mean_pool(text_reps_all[multi_text_idx], batch["attention_mask"][is_multi])
            pooled_img = self._mean_pool(image_reps_all[multi_img_idx])
            
            # Late fusion concatenation
            fused_reps = torch.cat([pooled_text, pooled_img], dim=-1)
            logits[is_multi] = self.multimodal_classifier(fused_reps).to(logits.dtype)
            
        return logits
