import pickle
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

from src.evaluation.metrics import compute_classification_metrics

class MultilingualBaselineClassifier:
    """
    Multilingual N-gram TF-IDF + Logistic Regression baseline model.
    Used for empirical benchmarking against Transformer architectures.
    """
    def __init__(self, max_features: int = 5000, ngram_range: Tuple[int, int] = (1, 2)):
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                max_features=max_features,
                ngram_range=ngram_range,
                strip_accents=None,  # Preserve multilingual diacritics
                lowercase=True
            )),
            ("clf", LogisticRegression(C=1.0, max_iter=1000, random_state=42))
        ])
        self.is_trained = False

    def train(self, texts: List[str], labels: List[int]) -> Dict[str, float]:
        """Trains the baseline model and returns training metrics."""
        self.pipeline.fit(texts, labels)
        self.is_trained = True
        
        preds = self.pipeline.predict(texts)
        probas = self.pipeline.predict_proba(texts)[:, 1]
        metrics = compute_classification_metrics(labels, preds, probas)
        return metrics

    def predict(self, texts: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """Returns predictions and class probabilities."""
        if not self.is_trained:
            raise RuntimeError("Baseline model has not been trained yet.")
        preds = self.pipeline.predict(texts)
        probas = self.pipeline.predict_proba(texts)
        return preds, probas

    def save(self, filepath: Union[str, Path]):
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(self.pipeline, f)

    def load(self, filepath: Union[str, Path]):
        filepath = Path(filepath)
        with open(filepath, "rb") as f:
            self.pipeline = pickle.load(f)
        self.is_trained = True
