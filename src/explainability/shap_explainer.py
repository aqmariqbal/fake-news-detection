from typing import Callable, Dict, List, Optional, Union
import numpy as np

class TokenShapleyExplainer:
    """
    Shapley Value / Perturbation Attribution Engine for Text Classifiers.
    Computes marginal token contributions to interpret deep learning predictions.
    """
    def __init__(self, predict_proba_fn: Callable[[List[str]], np.ndarray]):
        """
        Args:
            predict_proba_fn: Callable taking a list of string texts and returning
                              a 2D numpy array of probabilities [N, num_classes].
        """
        self.predict_proba_fn = predict_proba_fn

    def explain_instance(
        self,
        text: str,
        target_class_idx: int = 1,
        max_tokens: int = 50
    ) -> List[Dict[str, Union[str, float]]]:
        """
        Computes marginal attribution for each token using leave-one-out perturbation:
        phi_i = P(y=target | original_text) - P(y=target | text_without_token_i)
        """
        words = text.strip().split()
        if not words:
            return []
            
        words = words[:max_tokens]
        # Base prediction
        base_proba = self.predict_proba_fn([" ".join(words)])[0, target_class_idx]

        # Generate perturbed inputs (leave-one-out)
        perturbed_texts = []
        for i in range(len(words)):
            perturbed_words = words[:i] + words[i+1:]
            perturbed_texts.append(" ".join(perturbed_words) if perturbed_words else "")

        perturbed_probas = self.predict_proba_fn(perturbed_texts)[:, target_class_idx]
        attributions = base_proba - perturbed_probas

        # Normalize attributions for visualization
        max_abs = np.max(np.abs(attributions)) if len(attributions) > 0 and np.max(np.abs(attributions)) > 0 else 1.0

        results = []
        for word, raw_attr in zip(words, attributions):
            norm_attr = raw_attr / max_abs
            results.append({
                "word": word,
                "shap_value": float(raw_attr),
                "normalized_attribution": float(norm_attr),
                "impact": "increases_fake_score" if raw_attr > 0 else "supports_credibility"
            })

        return results

    @staticmethod
    def render_shap_badges(attributions: List[Dict[str, Union[str, float]]]) -> str:
        """
        Renders colored attribution badges:
        Red badges: Tokens driving the 'FAKE' classification.
        Green badges: Tokens driving the 'REAL' classification.
        """
        badges = []
        for item in attributions:
            word = item["word"]
            val = item["normalized_attribution"]
            
            if val > 0.05:
                # Pushes toward FAKE (Red)
                alpha = min(0.9, max(0.15, abs(val)))
                color = f"rgba(239, 68, 68, {alpha:.2f})"
                text_color = "#991b1b" if alpha < 0.5 else "#ffffff"
            elif val < -0.05:
                # Pushes toward REAL (Green)
                alpha = min(0.9, max(0.15, abs(val)))
                color = f"rgba(34, 197, 94, {alpha:.2f})"
                text_color = "#166534" if alpha < 0.5 else "#ffffff"
            else:
                color = "#f1f5f9"
                text_color = "#64748b"

            style = (
                f"background-color: {color}; color: {text_color}; "
                f"padding: 3px 8px; margin: 3px; border-radius: 6px; "
                f"display: inline-block; font-weight: 500; font-size: 13px;"
            )
            title = f"SHAP value: {item['shap_value']:+.4f} ({item['impact']})"
            badges.append(f'<span style="{style}" title="{title}">{word}</span>')

        return f'<div style="line-height: 2.3; background-color: #ffffff; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0;">{" ".join(badges)}</div>'
