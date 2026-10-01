import numpy as np
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score, 
    roc_auc_score,
    average_precision_score,
    confusion_matrix
)
from typing import Dict, Any

from dcat.data.modalities import Modality

class DcatMetrics:
    """Calculates evaluation metrics for DCAT predictions."""
    
    @staticmethod
    def calculate(
        y_true: list[int] | np.ndarray, 
        y_pred_prob: list[float] | np.ndarray,
        modalities: list[str] | np.ndarray = None,
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Args:
            y_true: Ground truth binary labels (0 or 1).
            y_pred_prob: Predicted probabilities for the positive class (spam).
            modalities: Optional list of modality strings for sliced metrics.
            threshold: Decision threshold.
        Returns:
            Dictionary of metrics.
        """
        y_true = np.array(y_true)
        y_pred_prob = np.array(y_pred_prob)
        y_pred = (y_pred_prob >= threshold).astype(int)
        
        metrics = DcatMetrics._calc_base_metrics(y_true, y_pred, y_pred_prob)
        
        if modalities is not None:
            modalities = np.array(modalities)
            for mod in [Modality.TEXT.value, Modality.IMAGE.value, Modality.MULTIMODAL.value]:
                mask = (modalities == mod)
                if np.sum(mask) >= 5: # Need a minimum number of samples to be meaningful
                    mod_metrics = DcatMetrics._calc_base_metrics(y_true[mask], y_pred[mask], y_pred_prob[mask])
                    for k, v in mod_metrics.items():
                        if not isinstance(v, list): # Don't nest confusion matrices
                            metrics[f"{k}_{mod}"] = v
                            
        return metrics

    @staticmethod
    def _calc_base_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_pred_prob: np.ndarray) -> Dict[str, Any]:
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0), # Default pos_label=1 (Spam F1)
            "spam_f1": f1_score(y_true, y_pred, zero_division=0, pos_label=1),
            "ham_f1": f1_score(y_true, y_pred, zero_division=0, pos_label=0),
            "macro_f1": f1_score(y_true, y_pred, zero_division=0, average='macro'),
        }
        
        # Confusion matrix: [[TN, FP], [FN, TP]]
        cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
        metrics["confusion_matrix"] = cm.tolist()
        
        # ROC-AUC and PR-AUC require both classes to be present in y_true, otherwise it raises an error
        if len(np.unique(y_true)) > 1:
            metrics["roc_auc"] = roc_auc_score(y_true, y_pred_prob)
            metrics["pr_auc"] = average_precision_score(y_true, y_pred_prob)
        else:
            metrics["roc_auc"] = 0.0
            metrics["pr_auc"] = 0.0
            
        return metrics
