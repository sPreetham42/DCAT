import os
import sys
import json
import torch
import hydra
from hydra.core.global_hydra import GlobalHydra
from omegaconf import OmegaConf
import numpy as np

# Add src to path
sys.path.insert(0, os.path.abspath('src'))
from dcat.training.experiment import ExperimentRunner
from dcat.training.engine import DcatTrainer

class AblationExperimentRunner(ExperimentRunner):
    """Custom runner that overrides the trainer to include pos_weight."""
    def run(self):
        train_loader, val_loader, test_loader = self.setup_data()
        model = self.setup_model()
        
        # Calculate pos_weight from train_loader only
        num_spam = 0
        num_ham = 0
        for batch in train_loader:
            labels = batch["labels"]
            num_spam += (labels == 1).sum().item()
            num_ham += (labels == 0).sum().item()
            
        pos_weight_val = num_ham / num_spam if num_spam > 0 else 1.0
        pos_weight = torch.tensor([pos_weight_val], device=self.device)
        print(f"Computed pos_weight from train split: {pos_weight_val:.4f} (Spam: {num_spam}, Ham: {num_ham})")
        
        optimizer = torch.optim.AdamW(
            model.parameters(), 
            lr=1e-4, # self.cfg.training.learning_rate.new_layers
            weight_decay=0.01
        )
        
        trainer = DcatTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            optimizer=optimizer,
            device=self.device,
            amp=True,
            pos_weight=pos_weight
        )
        
        print("Training Weighted DCAT (1 Epoch)")
        trainer.train_epoch()
        
        print("Evaluating on Validation to find threshold...")
        val_metrics_final = trainer.evaluate(return_preds=True)
        raw_probs = val_metrics_final["_raw_probs"]
        raw_labels = val_metrics_final["_raw_labels"]
        
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
            val_loader=test_loader,
            optimizer=optimizer,
            device=self.device,
            amp=True,
            pos_weight=pos_weight
        )
        test_metrics = test_trainer.evaluate(threshold=best_threshold)
        test_metrics["calibrated_threshold"] = best_threshold
        print(f"Test Loss: {test_metrics['val_loss']:.4f} | Test Macro-F1: {test_metrics['macro_f1']:.4f} | Test Spam F1: {test_metrics['spam_f1']:.4f} | Test Ham F1: {test_metrics['ham_f1']:.4f}")
        
        if "macro_f1_multimodal" in test_metrics:
             print(f"Test Multimodal Macro-F1: {test_metrics['macro_f1_multimodal']:.4f}")
             
        return {"val_metrics": val_metrics_final, "test_metrics": test_metrics}

def main():
    print(f"\n{'='*50}\nStarting Imbalance Ablation (Weighted DCAT)\n{'='*50}")
    GlobalHydra.instance().clear()
    
    with hydra.initialize_config_dir(config_dir="C:/Users/Preetham S/Documents/antigravity projects/dcat/configs", job_name="test"):
        cfg = hydra.compose(config_name="config", overrides=[
            "+model_type=dcat", 
            "model.dcat.cross_attention.layers=1",
            "seed=42"
        ])
        
        cfg.training.max_epochs = 1
        cfg.training.batch_size = 64
        cfg.experiment_name = "dcat_weighted"
        
        runner = AblationExperimentRunner(cfg)
        metrics = runner.run()
        
    os.makedirs("artifacts/imbalance_ablation", exist_ok=True)
    
    # Save results
    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer): return int(obj)
            if isinstance(obj, np.floating): return float(obj)
            if isinstance(obj, np.ndarray): return obj.tolist()
            return super(NpEncoder, self).default(obj)
            
    with open("artifacts/imbalance_ablation/results.json", "w") as f:
        json.dump(metrics, f, indent=2, cls=NpEncoder)
        
    print("\nImbalance Ablation Complete.")

if __name__ == "__main__":
    main()
