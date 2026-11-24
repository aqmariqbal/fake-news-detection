from typing import Dict, List, Optional, Union
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

def compute_classification_metrics(
    y_true: Union[List[int], np.ndarray],
    y_pred: Union[List[int], np.ndarray],
    y_prob: Optional[Union[List[float], np.ndarray]] = None
) -> Dict[str, Union[float, Dict]]:
    """
    Computes comprehensive binary classification metrics for fake news detection.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist()
    }
    
    if y_prob is not None:
        try:
            metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob))
        except Exception:
            metrics["roc_auc"] = None
            
    return metrics


def evaluate_multilingual_breakdown(
    df_eval: pd.DataFrame,
    y_true_col: str = "label_id",
    y_pred_col: str = "pred_id",
    lang_col: str = "language"
) -> Dict[str, Dict[str, float]]:
    """
    Evaluates classification performance across individual languages to measure
    cross-lingual consistency and detect low-resource performance disparities.
    """
    results_by_lang = {}
    for lang, group in df_eval.groupby(lang_col):
        y_t = group[y_true_col].values
        y_p = group[y_pred_col].values
        
        results_by_lang[lang] = {
            "samples": len(group),
            "accuracy": float(accuracy_score(y_t, y_p)),
            "f1": float(f1_score(y_t, y_p, average="macro", zero_division=0)),
            "precision": float(precision_score(y_t, y_p, zero_division=0)),
            "recall": float(recall_score(y_t, y_p, zero_division=0))
        }
        
    return results_by_lang


def compute_cross_lingual_transfer_gap(
    source_f1: float,
    target_f1: float
) -> float:
    """
    Calculates cross-lingual transfer degradation percentage:
    Gap = (Source F1 - Target F1) / Source F1 * 100%
    """
    if source_f1 <= 0:
        return 0.0
    return round(((source_f1 - target_f1) / source_f1) * 100.0, 2)
