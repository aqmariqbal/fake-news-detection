import unittest
from pathlib import Path
import numpy as np

from src.data.dataset_loader import MultilingualFakeNewsDataset
from src.data.augmentation import MultilingualAugmentor
from src.models.baseline import MultilingualBaselineClassifier
from src.models.transformer_classifier import MultilingualTransformerClassifier
from src.explainability.attention_explainer import AttentionExplainer
from src.explainability.shap_explainer import TokenShapleyExplainer
from src.evaluation.metrics import compute_classification_metrics

class TestFakeNewsPipeline(unittest.TestCase):

    def test_dataset_loader(self):
        dataset = MultilingualFakeNewsDataset()
        df = dataset.df
        self.assertGreater(len(df), 0)
        self.assertIn("text", df.columns)
        self.assertIn("label", df.columns)
        self.assertIn("language", df.columns)

    def test_augmentation(self):
        augmentor = MultilingualAugmentor()
        text = "This warning is confirmed by scientific study."
        aug_text = augmentor.lexical_perturbation(text, lang="en")
        self.assertTrue(len(aug_text) > 0)

    def test_baseline_classifier(self):
        dataset = MultilingualFakeNewsDataset()
        train_df, _, test_df = dataset.split_data()
        baseline = MultilingualBaselineClassifier()
        metrics = baseline.train(train_df["text"].tolist(), train_df["label_id"].tolist())
        self.assertIn("f1_macro", metrics)
        preds, probas = baseline.predict(["Breaking news test sample"])
        self.assertEqual(len(preds), 1)
        self.assertEqual(probas.shape[1], 2)

    def test_transformer_classifier(self):
        model = MultilingualTransformerClassifier()
        res = model.predict_text("Breaking news: Scientists discover water on Mars.")
        self.assertIn("label", res)
        self.assertIn(res["label"], ["REAL", "FAKE"])
        self.assertIn("confidence", res)
        self.assertGreaterEqual(res["confidence"], 0.0)

    def test_attention_explainer(self):
        explainer = AttentionExplainer()
        dummy_attn = [np.random.rand(1, 4, 10, 10) for _ in range(3)]
        tokens = [f"tok_{i}" for i in range(10)]
        saliency = explainer.extract_token_saliency(tokens, dummy_attn)
        self.assertEqual(len(saliency), 10)
        self.assertIn("saliency_weight", saliency[0])

    def test_shap_explainer(self):
        def dummy_predict_proba(texts):
            return np.array([[0.2, 0.8] for _ in texts])
        shap_exp = TokenShapleyExplainer(dummy_predict_proba)
        attrs = shap_exp.explain_instance("This is a test viral alert")
        self.assertGreater(len(attrs), 0)
        self.assertIn("shap_value", attrs[0])

    def test_metrics(self):
        y_true = [0, 1, 0, 1]
        y_pred = [0, 1, 0, 0]
        y_prob = [0.1, 0.9, 0.2, 0.4]
        metrics = compute_classification_metrics(y_true, y_pred, y_prob)
        self.assertEqual(metrics["accuracy"], 0.75)
        self.assertIn("f1_macro", metrics)

if __name__ == "__main__":
    unittest.main()
