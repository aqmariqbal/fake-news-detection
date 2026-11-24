import sys
import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
import numpy as np

# Bootstrap project root
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.config import MODELS_DIR, ID2LABEL, LABEL2ID, SUPPORTED_LANGUAGES
from src.models.transformer_classifier import MultilingualTransformerClassifier
from src.explainability.attention_explainer import AttentionExplainer
from src.explainability.shap_explainer import TokenShapleyExplainer

logger = logging.getLogger(__name__)

class MultilingualPredictor:
    """
    Unified Inference and Explainability Engine.
    Takes arbitrary multilingual news posts, classifies authenticity,
    and produces visual attention heatmaps and SHAP token attributions.
    """
    def __init__(self, model_checkpoint: Optional[Union[str, Path]] = None):
        self.model_checkpoint = Path(model_checkpoint) if model_checkpoint else (MODELS_DIR / "transformer_checkpoint")
        self.model = MultilingualTransformerClassifier()
        if self.model_checkpoint.exists():
            try:
                self.model.load_model(self.model_checkpoint)
                logger.info(f"Loaded trained model checkpoint from {self.model_checkpoint}")
            except Exception as e:
                logger.warning(f"Could not load checkpoint ({e}). Using initialized cross-lingual weights.")
        self.attention_explainer = AttentionExplainer()

    def predict_and_explain(self, text: str, lang: Optional[str] = None) -> Dict:
        """
        Runs complete inference + dual explainability pipeline (Attention Rollout + SHAP).
        """
        # Step 1: Transformer Inference & Attention Matrix Extraction
        res = self.model.predict_text(text)
        tokens = res["tokens"]
        attentions = res["attentions"]
        
        # Step 2: Attention Rollout Saliency
        if attentions:
            token_saliency = self.attention_explainer.extract_token_saliency(tokens, attentions)
        else:
            # Fallback saliency based on token position & length
            token_saliency = [
                {"token": t, "raw_attention": 0.1, "saliency_weight": 0.2, "is_special": False}
                for t in tokens
            ]
            
        attention_html = self.attention_explainer.render_html_heatmap(token_saliency)

        # Step 3: SHAP Token Attribution (marginal leave-one-out)
        def predict_proba_fn(texts: List[str]) -> np.ndarray:
            probas = []
            for t in texts:
                out = self.model.predict_text(t)
                probas.append([out["probabilities"]["REAL"], out["probabilities"]["FAKE"]])
            return np.array(probas)

        shap_explainer = TokenShapleyExplainer(predict_proba_fn=predict_proba_fn)
        shap_attributions = shap_explainer.explain_instance(text, target_class_idx=1)
        shap_html = shap_explainer.render_shap_badges(shap_attributions)

        # Step 4: Top deceptive / credible tokens ranking
        ranked_deceptive_tokens = sorted(
            [item for item in token_saliency if not item.get("is_special", False)],
            key=lambda x: x["saliency_weight"],
            reverse=True
        )[:5]

        return {
            "text": text,
            "language": lang or "auto-detected",
            "prediction": res["label"],
            "label": res["label"],
            "confidence": res["confidence"],
            "probabilities": res["probabilities"],
            "tokens": tokens,
            "token_saliency": token_saliency,
            "ranked_deceptive_tokens": [t["token"] for t in ranked_deceptive_tokens],
            "attention_html": attention_html,
            "shap_attributions": shap_attributions,
            "shap_html": shap_html
        }


def cli_predict(text: str, lang: Optional[str] = None):
    predictor = MultilingualPredictor()
    result = predictor.predict_and_explain(text, lang)
    
    print("\n" + "="*60)
    print("  MULTILINGUAL FAKE NEWS DETECTION & EXPLAINABILITY (XAI)")
    print("="*60)
    print(f"Input Text:       {result['text']}")
    print(f"Predicted Class:  {result['prediction']} ({result['confidence']*100:.2f}% Confidence)")
    print(f"Probabilities:    REAL: {result['probabilities']['REAL']:.4f} | FAKE: {result['probabilities']['FAKE']:.4f}")
    print(f"Top Flagged Tokens: {', '.join(result['ranked_deceptive_tokens'])}")
    print("="*60 + "\n")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=True, help="News text to verify")
    parser.add_argument("--lang", type=str, default="en", help="Language code (en, hi, bn, es, fr)")
    args = parser.parse_args()
    cli_predict(args.text, args.lang)
