import os
import sys
import json
import torch
import numpy as np
import hydra
from hydra.core.global_hydra import GlobalHydra

sys.path.insert(0, os.path.abspath('src'))
from dcat.training.experiment import ExperimentRunner
from dcat.training.engine import DcatTrainer
from dcat.evaluation.metrics import DcatMetrics

class VerifyRunner(ExperimentRunner):
    def run(self):
        train_loader, val_loader, test_loader = self.setup_data()
        model = self.setup_model()
        
        # Load checkpoint
        ckpt_path = f"checkpoints/{self.cfg.experiment_name}_seed42_best.pt"
        if not os.path.exists(ckpt_path):
            ckpt_path = f"checkpoints/{self.cfg.experiment_name}_best.pt"
        print(f"Loading {ckpt_path}...")
        model.load_state_dict(torch.load(ckpt_path, map_location=self.device, weights_only=True))
        
        # We only evaluate on test_loader
        trainer = DcatTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=test_loader,
            optimizer=torch.optim.AdamW(model.parameters()),
            device=self.device,
            amp=False
        )
        
        trainer.model.eval()
        all_labels = []
        all_probs = []
        all_modalities = []
        
        with torch.no_grad():
            for batch in test_loader:
                batch = trainer._move_to_device(batch)
                logits = trainer.model(batch)
                probs = torch.sigmoid(logits).cpu().numpy()
                all_probs.extend(probs.flatten())
                all_labels.extend(batch["labels"].cpu().numpy().flatten())
                all_modalities.extend(batch["modality"])
                
        metrics = DcatMetrics.calculate(all_labels, all_probs, modalities=all_modalities, threshold=0.5)
        print(f"Verified Macro-F1: {metrics['macro_f1']:.4f}")
        return metrics

def main():
    GlobalHydra.instance().clear()
    with hydra.initialize_config_dir(config_dir="C:/Users/Preetham S/Documents/antigravity projects/dcat/configs", job_name="verify"):
        cfg = hydra.compose(config_name="config", overrides=["+model_type=dcat", "model.dcat.cross_attention.layers=2"])
        cfg.training.batch_size = 128
        cfg.experiment_name = "full-dcat"
        runner = VerifyRunner(cfg)
        metrics = runner.run()
        
        print("\nExisting metrics from final_results.json:")
        with open("experiments/final_results.json", "r") as f:
            d = json.load(f)
            print("Macro-F1:", d["Full-DCAT"]["seeds"]["42"]["test_metrics"].get("macro_f1"))

if __name__ == "__main__":
    main()
