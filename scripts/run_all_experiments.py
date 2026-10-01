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
from dcat.evaluation.metrics import DcatMetrics
from dcat.data.modalities import Modality

class ReproducibleRunner(ExperimentRunner):
    def run(self):
        train_loader, val_loader, test_loader = self.setup_data()
        model = self.setup_model()
        
        # Calculate pos_weight from train_loader
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
            lr=1e-4, 
            weight_decay=0.01,
            betas=[0.9, 0.999],
            eps=1.0e-8
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
        
        print(f"Training {self.cfg.experiment_name} (1 Epoch)")
        trainer.train_epoch()
        
        os.makedirs("checkpoints", exist_ok=True)
        torch.save(model.state_dict(), f"checkpoints/{self.cfg.experiment_name}.pt")
        
        print("Evaluating on Validation to find threshold...")
        val_metrics_final = trainer.evaluate(return_preds=True)
        raw_probs = val_metrics_final["_raw_probs"]
        raw_labels = val_metrics_final["_raw_labels"]
        
        from sklearn.metrics import f1_score
        best_threshold = 0.5
        best_macro_f1 = -1
        
        for th in np.linspace(0.01, 0.99, 99):
            preds = (np.array(raw_probs) >= th).astype(int)
            macro_f1 = f1_score(raw_labels, preds, average='macro', zero_division=0)
            if macro_f1 > best_macro_f1:
                best_macro_f1 = macro_f1
                best_threshold = th
                
        test_trainer = DcatTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=test_loader,
            optimizer=optimizer,
            device=self.device,
            amp=True,
            pos_weight=pos_weight
        )
        
        test_trainer.model.eval()
        all_labels = []
        all_probs = []
        all_modalities = []
        with torch.no_grad():
            for batch in test_loader:
                batch = test_trainer._move_to_device(batch)
                labels = batch["labels"]
                
                if test_trainer.amp and test_trainer.device.type == 'cuda':
                    with torch.autocast(device_type='cuda', dtype=torch.float16):
                        logits = test_trainer.model(batch)
                else:
                    logits = test_trainer.model(batch)
                    
                probs = torch.sigmoid(logits).cpu().numpy()
                all_probs.extend(probs.flatten())
                all_labels.extend(labels.cpu().numpy().flatten())
                all_modalities.extend(batch["modality"])
                
        test_metrics = DcatMetrics.calculate(all_labels, all_probs, modalities=all_modalities, threshold=best_threshold)
        test_metrics["calibrated_threshold"] = best_threshold
        
        test_metrics["_raw_probs"] = all_probs
        test_metrics["_raw_labels"] = all_labels
        test_metrics["_raw_modalities"] = all_modalities
             
        return {"val_metrics": val_metrics_final, "test_metrics": test_metrics}

def run_experiment(overrides, exp_name):
    print(f"\n{'='*50}\nStarting {exp_name}\n{'='*50}")
    GlobalHydra.instance().clear()
    with hydra.initialize_config_dir(config_dir="C:/Users/Preetham S/Documents/antigravity projects/dcat/configs", job_name="test"):
        cfg = hydra.compose(config_name="config", overrides=overrides)
        cfg.training.max_epochs = 1
        cfg.training.batch_size = 64
        cfg.experiment_name = exp_name
        runner = ReproducibleRunner(cfg)
        metrics = runner.run()
        
    os.makedirs(f"results_final_70k/{exp_name}", exist_ok=True)
    
    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer): return int(obj)
            if isinstance(obj, np.floating): return float(obj)
            if isinstance(obj, np.ndarray): return obj.tolist()
            return super(NpEncoder, self).default(obj)
            
    with open(f"results_final_70k/{exp_name}/results.json", "w") as f:
        if "_raw_probs" in metrics["val_metrics"]: del metrics["val_metrics"]["_raw_probs"]
        if "_raw_labels" in metrics["val_metrics"]: del metrics["val_metrics"]["_raw_labels"]
        json.dump(metrics, f, indent=2, cls=NpEncoder)
        
    return metrics

def main():
    os.makedirs("results_final_70k", exist_ok=True)
    
    configs = [
        ("Full DCAT", ["+model_type=dcat", "model.dcat.cross_attention.layers=2", "seed=42"], "dcat_full"),
        ("Late Fusion", ["+model_type=baseline", "seed=42"], "late_fusion"),
        ("Text-Only", ["+model_type=baseline", "seed=42", "force_modality=text"], "text_only"),
        ("Image-Only", ["+model_type=baseline", "seed=42", "force_modality=image"], "image_only"),
        ("No Routing Ablation", ["+model_type=dcat", "routing=static", "seed=42"], "ablation_no_routing"),
        ("No Cross-Attention Ablation", ["+model_type=dcat", "model.dcat.cross_attention.layers=0", "seed=42"], "ablation_no_ca")
    ]
    
    all_results = {}
    for name, overrides, exp_name in configs:
        res = run_experiment(overrides, exp_name)
        
        # Strip raw data before storing in master JSON to keep it small
        if "_raw_probs" in res["test_metrics"]: del res["test_metrics"]["_raw_probs"]
        if "_raw_labels" in res["test_metrics"]: del res["test_metrics"]["_raw_labels"]
        if "_raw_modalities" in res["test_metrics"]: del res["test_metrics"]["_raw_modalities"]
        
        all_results[exp_name] = res
        
    with open("results_final_70k/FINAL_RESULTS_70K.json", "w") as f:
        json.dump(all_results, f, indent=2)

if __name__ == "__main__":
    main()
