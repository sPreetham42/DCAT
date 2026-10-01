import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm
from typing import Dict, Any

from dcat.evaluation.metrics import DcatMetrics

class DcatTrainer:
    """Training and evaluation loop for DCAT."""
    
    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        optimizer: torch.optim.Optimizer,
        device: torch.device,
        amp: bool = True,
        pos_weight: torch.Tensor = None
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.optimizer = optimizer
        self.device = device
        self.amp = amp
        
        self.criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
        self.scaler = torch.cuda.amp.GradScaler() if amp and device.type == 'cuda' else None
        
    def _move_to_device(self, batch: Dict[str, Any]) -> Dict[str, Any]:
        """Moves tensor values in batch to the correct device."""
        for k, v in batch.items():
            if isinstance(v, torch.Tensor):
                batch[k] = v.to(self.device)
        return batch

    def train_epoch(self) -> float:
        self.model.train()
        total_loss = 0.0
        
        for batch in tqdm(self.train_loader, desc="Training"):
            batch = self._move_to_device(batch)
            labels = batch["labels"]
            
            self.optimizer.zero_grad()
            
            if self.amp and self.device.type == 'cuda':
                with torch.autocast(device_type='cuda', dtype=torch.float16):
                    logits = self.model(batch)
                    loss = self.criterion(logits, labels)
                
                self.scaler.scale(loss).backward()
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                logits = self.model(batch)
                loss = self.criterion(logits, labels)
                loss.backward()
                self.optimizer.step()
                
            total_loss += loss.item()
            
        return total_loss / len(self.train_loader)
        
    def evaluate(self, threshold: float = 0.5, return_preds: bool = False) -> Dict[str, Any]:
        self.model.eval()
        total_loss = 0.0
        
        all_labels = []
        all_probs = []
        all_modalities = []
        
        with torch.no_grad():
            for batch in tqdm(self.val_loader, desc="Evaluating"):
                batch = self._move_to_device(batch)
                labels = batch["labels"]
                
                if self.amp and self.device.type == 'cuda':
                    with torch.autocast(device_type='cuda', dtype=torch.float16):
                        logits = self.model(batch)
                        loss = self.criterion(logits, labels)
                else:
                    logits = self.model(batch)
                    loss = self.criterion(logits, labels)
                    
                total_loss += loss.item()
                
                probs = torch.sigmoid(logits).cpu().numpy()
                all_probs.extend(probs.flatten())
                all_labels.extend(labels.cpu().numpy().flatten())
                all_modalities.extend(batch["modality"])
                
        metrics = DcatMetrics.calculate(all_labels, all_probs, modalities=all_modalities, threshold=threshold)
        metrics["val_loss"] = total_loss / len(self.val_loader)
        
        if return_preds:
            metrics["_raw_probs"] = all_probs
            metrics["_raw_labels"] = all_labels
            
        return metrics
