import hydra
from omegaconf import DictConfig
from dcat.training.experiment import ExperimentRunner

@hydra.main(version_base=None, config_path="../configs", config_name="config")
def main(cfg: DictConfig):
    runner = ExperimentRunner(cfg)
    runner.run()

if __name__ == "__main__":
    main()
