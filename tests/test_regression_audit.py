import pytest
from dcat.data.modalities import modality_from_flags, Modality

def test_modality_routing_regression():
    # If text has < 10 chars, it's considered non-existent for routing
    has_text = True
    has_image = True
    
    assert modality_from_flags(True, True) == Modality.MULTIMODAL
    assert modality_from_flags(True, False) == Modality.TEXT
    assert modality_from_flags(False, True) == Modality.IMAGE
    assert modality_from_flags(False, False) == Modality.EMPTY

from dcat.evaluation.metrics import DcatMetrics
import numpy as np

def test_metric_aggregation_regression():
    # Enforce Macro-F1 vs F1 differences
    y_true = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 0]) # 90% spam
    y_pred = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) # always predict spam
    
    # 0.5 threshold
    metrics = DcatMetrics.calculate(y_true, y_pred, threshold=0.5)
    
    # Accuracy is 90%
    assert metrics["accuracy"] == 0.9
    
    # Spam-F1 is high (0.947)
    assert metrics["spam_f1"] > 0.9
    
    # Ham-F1 is 0 (0 TP)
    assert metrics["ham_f1"] == 0.0
    
    # Macro-F1 should be EXACTLY mean of spam_f1 and ham_f1
    assert metrics["macro_f1"] == (metrics["spam_f1"] + metrics["ham_f1"]) / 2.0
    
    # Macro-F1 is NOT accuracy or weighted-F1
    assert metrics["macro_f1"] < 0.5 # Because it averages ~0.94 and 0.0
