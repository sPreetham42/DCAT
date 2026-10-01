from __future__ import annotations

import torch
from torch.utils.data import Dataset
from transformers import PreTrainedTokenizerFast, AutoTokenizer
from pathlib import Path
from PIL import Image

from dcat.data.parquet import ParquetDatasetReader
from dcat.data.records import EmailRecord
from dcat.data.modalities import Modality
from dcat.preprocessing.image_processor import ImageProcessor, ImageProcessorConfig

class DcatDataset(Dataset):
    """PyTorch Dataset for DCAT multimodal email records."""
    
    def __init__(
        self, 
        records_path: str | Path, 
        tokenizer_name: str = "distilbert-base-uncased",
        max_length: int = 256,
        image_size: tuple[int, int] = (224, 224),
        force_modality: str | None = None
    ):
        raw_records = ParquetDatasetReader.load_records(records_path)
        self.records: list[EmailRecord] = [r for r in raw_records if r.modality != Modality.EMPTY]
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.max_length = max_length
        self.force_modality = force_modality
        self.image_processor = ImageProcessor(
            config=ImageProcessorConfig(target_size=image_size)
        )
        
    def __len__(self) -> int:
        return len(self.records)
        
    def __getitem__(self, idx: int) -> dict:
        record = self.records[idx]
        modality_value = record.modality.value
        
        # Override modality if requested
        if self.force_modality == 'text':
            modality_value = Modality.TEXT.value
        elif self.force_modality == 'image':
            modality_value = Modality.IMAGE.value
            
        item = {
            "email_id": record.email_id,
            "modality": modality_value,
            "label": record.label if record.label is not None else -1,
        }
        
        modality_enum = Modality(modality_value)
        if modality_enum == Modality.EMPTY:
            raise ValueError(f"Record {record.email_id} has EMPTY modality. Dataset should not process empty emails.")
        
        if modality_enum.uses_text_encoder and record.text:
            # Tokenize text
            encoded = self.tokenizer(
                record.text,
                padding="max_length",
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt"
            )
            item["input_ids"] = encoded["input_ids"].squeeze(0)
            item["attention_mask"] = encoded["attention_mask"].squeeze(0)
        else:
            # Empty tensor for text if not used
            item["input_ids"] = torch.zeros(self.max_length, dtype=torch.long)
            item["attention_mask"] = torch.zeros(self.max_length, dtype=torch.long)
            
        if modality_enum.uses_image_encoder:
            # Find the selected image
            selected_img = None
            for img in record.images:
                if img.selected and img.source_path:
                    selected_img = img
                    break
            
            if selected_img and selected_img.source_path:
                try:
                    with Image.open(selected_img.source_path) as pil_img:
                        item["pixel_values"] = self.image_processor._to_normalized_tensor(pil_img)
                except Exception:
                    # Fallback to zeros if image cannot be loaded
                    item["pixel_values"] = torch.zeros(3, *self.image_processor.config.target_size)
            else:
                item["pixel_values"] = torch.zeros(3, *self.image_processor.config.target_size)
        else:
            item["pixel_values"] = torch.zeros(3, *self.image_processor.config.target_size)
            
        return item

class DcatCollator:
    """Collates a batch of DCAT items."""
    
    def __call__(self, batch: list[dict]) -> dict:
        for item in batch:
            if item["modality"] == Modality.EMPTY.value:
                raise ValueError(f"Encountered EMPTY modality in collator for email_id {item['email_id']}")
                
        collated = {
            "email_id": [item["email_id"] for item in batch],
            "modality": [item["modality"] for item in batch],
        }
        
        labels = [item["label"] for item in batch]
        if any(l != -1 for l in labels):
            collated["labels"] = torch.tensor(labels, dtype=torch.float32).unsqueeze(1)
            
        collated["input_ids"] = torch.stack([item["input_ids"] for item in batch])
        collated["attention_mask"] = torch.stack([item["attention_mask"] for item in batch])
        collated["pixel_values"] = torch.stack([item["pixel_values"] for item in batch])
        
        return collated
