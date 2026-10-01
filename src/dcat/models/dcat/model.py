import torch
import torch.nn as nn
from typing import Dict, Any

from dcat.models.encoders.distilbert import TextEncoder
from dcat.models.encoders.mobilevit import VisionEncoder
from dcat.models.projection.projector import ModalityProjector
from dcat.models.crossattention.attention import BidirectionalCrossAttention
from dcat.models.classifier.mlp import SharedClassifier
from dcat.data.modalities import Modality

class DcatModel(nn.Module):
    """The full DCAT architecture with conditional modality routing."""
    
    def __init__(
        self,
        text_model_name: str = "distilbert-base-uncased",
        vision_model_name: str = "mobilevit_s",
        freeze_encoders: bool = True,
        shared_dim: int = 256,
        cross_attention_layers: int = 2,
        cross_attention_heads: int = 4,
        classifier_hidden: int = 128,
        pooling: str = "mean"
    ):
        super().__init__()
        
        # Encoders
        self.text_encoder = TextEncoder(model_name=text_model_name, freeze=freeze_encoders)
        self.vision_encoder = VisionEncoder(model_name=vision_model_name, freeze=freeze_encoders)
        
        # Determine feature dimensions based on models.
        # Mobilevit_s output dim is 640 for forward_features
        # DistilBERT is 768
        self.projector = ModalityProjector(text_dim=768, image_dim=640, shared_dim=shared_dim)
        
        # Cross Attention (Multimodal Fusion)
        self.cross_attention = BidirectionalCrossAttention(
            layers=cross_attention_layers,
            d_model=shared_dim,
            heads=cross_attention_heads
        )
        
        # Classifier
        self.classifier = SharedClassifier(input_dim=shared_dim, hidden_dim=classifier_hidden)
        self.pooling = pooling
        
        # Auxiliary text-only classifier for early exit
        self.use_early_exit = False
        self.text_early_exit_classifier = SharedClassifier(input_dim=shared_dim, hidden_dim=classifier_hidden)
        self.early_exit_threshold_high = 0.95
        self.early_exit_threshold_low = 0.05
        
    def _mean_pool(self, features: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        """
        Mean pools over the sequence dimension.
        Args:
            features: [B, SeqLen, D]
            mask: [B, SeqLen] True means valid, False means padding. 
                  (Wait, transformers uses 1 for valid, 0 for padding)
        Returns:
            [B, D]
        """
        if mask is not None:
            # mask is [B, SeqLen] (1 for valid, 0 for pad)
            mask = mask.unsqueeze(-1).float()
            return torch.sum(features * mask, dim=1) / torch.clamp(torch.sum(mask, dim=1), min=1e-9)
        else:
            return features.mean(dim=1)

    def forward(self, batch: Dict[str, Any]) -> torch.Tensor:
        """
        Args:
            batch: dict containing:
                input_ids: [B, T]
                attention_mask: [B, T] (1 for valid, 0 for pad)
                pixel_values: [B, 3, H, W]
                modality: list of str representing Modality enum values
        Returns:
            logits: [B, 1]
        """
        device = batch["input_ids"].device
        bsz = len(batch["modality"])
        
        final_reps = torch.zeros(bsz, self.projector.text_proj.out_features, device=device, dtype=self.projector.text_proj.weight.dtype)
        
        # Modality routing masks
        is_text = torch.tensor([m == Modality.TEXT.value for m in batch["modality"]], device=device)
        is_image = torch.tensor([m == Modality.IMAGE.value for m in batch["modality"]], device=device)
        is_multi = torch.tensor([m == Modality.MULTIMODAL.value for m in batch["modality"]], device=device)
        
        # 1. Compute Text representations for TEXT and MULTI
        has_text_mask = is_text | is_multi
        text_reps_all = None
        if has_text_mask.any():
            text_inputs = batch["input_ids"][has_text_mask]
            text_attn = batch["attention_mask"][has_text_mask]
            text_feats = self.text_encoder(text_inputs, text_attn)
            text_reps_all = self.projector.project_text(text_feats)
            
        # 2. Process TEXT ONLY
        if is_text.any():
            text_only_idx_in_subset = is_text[has_text_mask]
            text_only_reps = text_reps_all[text_only_idx_in_subset]
            text_only_attn = batch["attention_mask"][is_text]
            pooled_text = self._mean_pool(text_only_reps, text_only_attn)
            final_reps[is_text] = pooled_text.to(final_reps.dtype)
            
        # 3. Process MULTIMODAL (with Early Exit)
        early_exited_mask = torch.zeros(bsz, dtype=torch.bool, device=device)
        logits = torch.zeros(bsz, 1, device=device, dtype=final_reps.dtype)
        
        if is_multi.any():
            multi_text_idx = is_multi[has_text_mask]
            multi_text_reps = text_reps_all[multi_text_idx]
            multi_text_attn = batch["attention_mask"][is_multi]
            
            # Evaluate text-only early exit
            pooled_multi_text = self._mean_pool(multi_text_reps, multi_text_attn)
            
            if self.use_early_exit:
                text_only_logits = self.text_early_exit_classifier(pooled_multi_text)
                text_only_probs = torch.sigmoid(text_only_logits).squeeze(-1)
                
                # Confident if prob > 0.95 or prob < 0.05
                confident_mask = (text_only_probs > self.early_exit_threshold_high) | (text_only_probs < self.early_exit_threshold_low)
            else:
                confident_mask = torch.zeros(len(multi_text_reps), dtype=torch.bool, device=device)
            
            # Get absolute indices in the batch that are multi AND confident
            multi_indices = torch.where(is_multi)[0]
            exited_multi_indices = multi_indices[confident_mask]
            not_exited_multi_indices = multi_indices[~confident_mask]
            
            early_exited_mask[exited_multi_indices] = True
            
            # Assign early exit logits
            if self.use_early_exit and confident_mask.any():
                logits[exited_multi_indices] = text_only_logits[confident_mask].to(logits.dtype)
            
        # 4. Compute Image representations ONLY for IMAGE-ONLY and NON-EXITED MULTIMODAL
        needs_image_processing = is_image | (is_multi & ~early_exited_mask)
        image_reps_all = None
        if needs_image_processing.any():
            img_inputs = batch["pixel_values"][needs_image_processing]
            img_feats = self.vision_encoder(img_inputs)
            image_reps_all = self.projector.project_image(img_feats)
            
        # 5. Process IMAGE ONLY
        if is_image.any():
            img_only_idx_in_subset = is_image[needs_image_processing]
            img_only_reps = image_reps_all[img_only_idx_in_subset]
            pooled_img = self._mean_pool(img_only_reps)
            final_reps[is_image] = pooled_img.to(final_reps.dtype)
            
        # 6. Process remaining MULTIMODAL (Cross-Attention)
        remaining_multi = is_multi & ~early_exited_mask
        if remaining_multi.any():
            # Get text reps for remaining
            rem_multi_text_idx = remaining_multi[has_text_mask]
            rem_multi_text_reps = text_reps_all[rem_multi_text_idx]
            rem_multi_text_attn = batch["attention_mask"][remaining_multi]
            
            # Get image reps for remaining
            rem_multi_img_idx = remaining_multi[needs_image_processing]
            rem_multi_img_reps = image_reps_all[rem_multi_img_idx]
            
            ca_mask = (rem_multi_text_attn == 0)
            fused_text, fused_img = self.cross_attention(rem_multi_text_reps, rem_multi_img_reps, ca_mask)
            
            pooled_fused_text = self._mean_pool(fused_text, rem_multi_text_attn)
            pooled_fused_img = self._mean_pool(fused_img)
            
            fused_rep = (pooled_fused_text + pooled_fused_img) / 2.0
            final_reps[remaining_multi] = fused_rep.to(final_reps.dtype)
            
        # Pass non-exited reps through main classifier
        needs_main_classifier = ~early_exited_mask
        if needs_main_classifier.any():
            logits[needs_main_classifier] = self.classifier(final_reps[needs_main_classifier]).to(logits.dtype)
            
        return logits
