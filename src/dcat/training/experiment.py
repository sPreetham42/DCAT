import os
import torch
from pathlib import Path
from torch.utils.data import DataLoader
from omegaconf import DictConfig

from dcat.data.dataset import DcatDataset, DcatCollator
from dcat.models.dcat.model import DcatModel
from dcat.models.dcat.baseline import LateFusionBaseline, PublishedBaseline
from dcat.training.engine import DcatTrainer

class ExperimentRunner:
    """Runs a complete DCAT training experiment based on Hydra configuration."""
    
    def __init__(self, cfg: DictConfig):
        self.cfg = cfg
        self.device = torch.device(cfg.device if cfg.device != "auto" else ('cuda' if torch.cuda.is_available() else 'cpu'))
        print(f"Initializing Experiment: {cfg.experiment_name} on {self.device}")
        
    def setup_data(self) -> tuple[DataLoader, DataLoader, DataLoader]:
        dataset = DcatDataset(
            records_path=self.cfg.data.processed_dir + "/records.parquet",
            tokenizer_name=self.cfg.model.distilbert.model_name,
            max_length=self.cfg.model.distilbert.max_length,
            image_size=self.cfg.model.mobilevit.image_size,
            force_modality=self.cfg.get("force_modality", None)
        )
        
        # Use pre-computed splits from the records to ensure leakage-safe boundaries
        train_indices = [i for i, r in enumerate(dataset.records) if r.split == "train"]
        val_indices = [i for i, r in enumerate(dataset.records) if r.split == "val"]
        test_indices = [i for i, r in enumerate(dataset.records) if r.split == "test"]
        
        train_ds = torch.utils.data.Subset(dataset, train_indices)
        val_ds = torch.utils.data.Subset(dataset, val_indices)
        test_ds = torch.utils.data.Subset(dataset, test_indices)
        
        collator = DcatCollator()
        
        # In multi-gpu we'd use DistributedSampler, but this is a base implementation
        train_loader = DataLoader(
            train_ds, 
            batch_size=self.cfg.training.batch_size, 
            shuffle=True, 
            collate_fn=collator,
            num_workers=self.cfg.training.num_workers,
            pin_memory=self.cfg.training.pin_memory
        )
        val_loader = DataLoader(
            val_ds, 
            batch_size=self.cfg.training.batch_size, 
            shuffle=False, 
            collate_fn=collator,
            num_workers=self.cfg.training.num_workers,
            pin_memory=self.cfg.training.pin_memory
        )
        test_loader = DataLoader(
            test_ds, 
            batch_size=self.cfg.training.batch_size, 
            shuffle=False, 
            collate_fn=collator,
            num_workers=self.cfg.training.num_workers,
            pin_memory=self.cfg.training.pin_memory
        )
        return train_loader, val_loader, test_loader
        
    def setup_model(self) -> torch.nn.Module:
        model_type = self.cfg.get("model_type", "dcat")
        
        if model_type == "baseline":
            model = LateFusionBaseline(
                text_model_name=self.cfg.model.distilbert.model_name,
                vision_model_name=self.cfg.model.mobilevit.model_name,
                freeze_encoders=self.cfg.model.distilbert.freeze,
                shared_dim=self.cfg.model.dcat.shared_dim,
                classifier_hidden=self.cfg.model.dcat.classifier.hidden_dim
            )
        elif model_type == "published_baseline":
            model = PublishedBaseline(
                text_model_name=self.cfg.model.distilbert.model_name,
                vision_model_name="resnet18",
                freeze_encoders=self.cfg.model.distilbert.freeze,
                shared_dim=self.cfg.model.dcat.shared_dim,
                classifier_hidden=self.cfg.model.dcat.classifier.hidden_dim
            )
        else:
            model = DcatModel(
                text_model_name=self.cfg.model.distilbert.model_name,
                vision_model_name=self.cfg.model.mobilevit.model_name,
                freeze_encoders=self.cfg.model.distilbert.freeze,
                shared_dim=self.cfg.model.dcat.shared_dim,
                cross_attention_layers=self.cfg.model.dcat.cross_attention.layers,
                cross_attention_heads=self.cfg.model.dcat.cross_attention.heads,
                classifier_hidden=self.cfg.model.dcat.classifier.hidden_dim,
                pooling=self.cfg.model.dcat.pooling
            )
            model.use_early_exit = self.cfg.get("use_early_exit", False)
        return model

    def run(self):
        train_loader, val_loader, test_loader = self.setup_data()
        model = self.setup_model()
        
        optimizer = torch.optim.AdamW(
            model.parameters(), 
            lr=self.cfg.training.learning_rate.new_layers,
            weight_decay=self.cfg.training.optimizer.weight_decay,
            betas=self.cfg.training.optimizer.betas,
            eps=self.cfg.training.optimizer.eps
        )
        
        trainer = DcatTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            optimizer=optimizer,
            device=self.device,
            amp=self.cfg.training.amp
        )
        
        best_val_f1 = -1
        checkpoint_dir = Path(self.cfg.training.checkpoint.dir)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        for epoch in range(self.cfg.training.max_epochs):
            print(f"Epoch {epoch+1}/{self.cfg.training.max_epochs}")
            train_loss = trainer.train_epoch()
            val_metrics = trainer.evaluate()
            
            print(f"Train Loss: {train_loss:.4f}")
            print(f"Val Loss: {val_metrics['val_loss']:.4f} | Val F1: {val_metrics['f1']:.4f} | Val ROC-AUC: {val_metrics['roc_auc']:.4f}")
            
            if val_metrics['f1'] > best_val_f1:
                best_val_f1 = val_metrics['f1']
                print(f"New best model! F1: {best_val_f1:.4f}")
                if self.cfg.training.checkpoint.save_best:
                    torch.save(model.state_dict(), checkpoint_dir / f"{self.cfg.experiment_name}_best.pt")
                    
        print("Training complete. Performing validation threshold calibration...")
        
        # Load best weights if saved
        if self.cfg.training.checkpoint.save_best:
            best_model_path = checkpoint_dir / f"{self.cfg.experiment_name}_best.pt"
            if best_model_path.exists():
                print("Loading best model weights for evaluation...")
                model.load_state_dict(torch.load(best_model_path, map_location=self.device, weights_only=True))
                
        # Run one final evaluation on validation to calibrate
        val_trainer = DcatTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            optimizer=optimizer,
            device=self.device,
            amp=self.cfg.training.amp
        )
        val_metrics_final = val_trainer.evaluate(return_preds=True)
        raw_probs = val_metrics_final["_raw_probs"]
        raw_labels = val_metrics_final["_raw_labels"]
        
        import numpy as np
        from sklearn.metrics import f1_score
        
        best_threshold = 0.5
        best_macro_f1 = -1
        
        # Grid search over thresholds
        for th in np.linspace(0.01, 0.99, 99):
            preds = (np.array(raw_probs) >= th).astype(int)
            macro_f1 = f1_score(raw_labels, preds, average='macro', zero_division=0)
            if macro_f1 > best_macro_f1:
                best_macro_f1 = macro_f1
                best_threshold = th
                
        print(f"Optimal validation threshold found: {best_threshold:.2f} (Macro-F1: {best_macro_f1:.4f})")
        
        test_trainer = DcatTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=test_loader,  # pass test_loader as val_loader for evaluation
            optimizer=optimizer,
            device=self.device,
            amp=self.cfg.training.amp
        )
        test_metrics = test_trainer.evaluate(threshold=best_threshold)
        test_metrics["calibrated_threshold"] = best_threshold
        print(f"Test Loss: {test_metrics['val_loss']:.4f} | Test Macro-F1: {test_metrics['macro_f1']:.4f} | Test Spam F1: {test_metrics['spam_f1']:.4f} | Test Ham F1: {test_metrics['ham_f1']:.4f}")
        
        # Multimodal specific test metrics (already calculated by DcatMetrics if multimodal subset present)
        if "macro_f1_multimodal" in test_metrics:
             print(f"Test Multimodal Macro-F1: {test_metrics['macro_f1_multimodal']:.4f} | Multimodal ROC-AUC: {test_metrics.get('roc_auc_multimodal', 0):.4f}")
             
        return {"val_metrics": val_metrics_final, "test_metrics": test_metrics}
