import sys
import argparse
import json
import logging
from pathlib import Path
import numpy as np
import torch

# Bootstrap project root
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.config import (
    RAW_DATA_PATH,
    AUGMENTED_DATA_PATH,
    MODELS_DIR,
    BATCH_SIZE,
    LEARNING_RATE,
    NUM_EPOCHS,
    MAX_SEQ_LENGTH,
    LABEL2ID,
    ID2LABEL
)
from src.data.dataset_loader import MultilingualFakeNewsDataset
from src.data.augmentation import generate_augmented_corpus
from src.models.baseline import MultilingualBaselineClassifier
from src.models.transformer_classifier import MultilingualTransformerClassifier
from src.evaluation.metrics import (
    compute_classification_metrics,
    evaluate_multilingual_breakdown,
    compute_cross_lingual_transfer_gap
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def train_pipeline(
    use_augmentation: bool = True,
    model_type: str = "all",  # 'baseline', 'transformer', or 'all'
    transformer_name: str = "bert-base-multilingual-cased",
    epochs: int = NUM_EPOCHS,
    batch_size: int = BATCH_SIZE
):
    logger.info("=== Starting Multilingual Fake News Detection Training Pipeline ===")
    
    # Step 1: Augmentation Pipeline if requested
    if use_augmentation and not AUGMENTED_DATA_PATH.exists():
        logger.info("Executing Data Augmentation (Back-Translation & Perturbation)...")
        generate_augmented_corpus(RAW_DATA_PATH, AUGMENTED_DATA_PATH)
        data_source = AUGMENTED_DATA_PATH
    elif use_augmentation and AUGMENTED_DATA_PATH.exists():
        logger.info(f"Using existing augmented dataset: {AUGMENTED_DATA_PATH}")
        data_source = AUGMENTED_DATA_PATH
    else:
        logger.info(f"Using raw dataset: {RAW_DATA_PATH}")
        data_source = RAW_DATA_PATH

    dataset = MultilingualFakeNewsDataset(data_path=data_source)
    dist = dataset.get_language_distribution()
    logger.info(f"Dataset language distribution: {dist}")

    train_df, val_df, test_df = dataset.split_data(test_size=0.2, val_size=0.1)
    logger.info(f"Splits created: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")

    results = {}

    # Step 2: Baseline Model Training
    if model_type in ["baseline", "all"]:
        logger.info("\n--- Training Multilingual TF-IDF + Logistic Regression Baseline ---")
        baseline = MultilingualBaselineClassifier()
        train_metrics = baseline.train(train_df["text"].tolist(), train_df["label_id"].tolist())
        logger.info(f"Baseline Train F1-Macro: {train_metrics['f1_macro']:.4f}")

        # Evaluate on Test
        test_preds, test_probas = baseline.predict(test_df["text"].tolist())
        test_metrics = compute_classification_metrics(test_df["label_id"].tolist(), test_preds, test_probas[:, 1])
        logger.info(f"Baseline Test Accuracy: {test_metrics['accuracy']:.4f}, F1-Macro: {test_metrics['f1_macro']:.4f}")
        
        baseline_save_path = MODELS_DIR / "baseline_model.pkl"
        baseline.save(baseline_save_path)
        logger.info(f"Baseline model saved to {baseline_save_path}")
        results["baseline"] = test_metrics

    # Step 3: Transformer Model Training
    if model_type in ["transformer", "all"]:
        logger.info(f"\n--- Initializing Cross-Lingual Transformer ({transformer_name}) ---")
        transformer = MultilingualTransformerClassifier(
            model_name_or_path=transformer_name,
            num_classes=2
        )
        
        # Tokenize training data
        train_texts = train_df["text"].tolist()
        train_labels = torch.tensor(train_df["label_id"].tolist(), dtype=torch.long)
        
        val_texts = val_df["text"].tolist()
        val_labels = torch.tensor(val_df["label_id"].tolist(), dtype=torch.long)
        
        test_texts = test_df["text"].tolist()
        test_labels = test_df["label_id"].tolist()

        # Simple fine-tuning loop
        optimizer = torch.optim.AdamW(transformer.parameters(), lr=LEARNING_RATE)
        criterion = torch.nn.CrossEntropyLoss()
        
        logger.info(f"Training transformer for {epochs} epochs...")
        transformer.train()
        for epoch in range(epochs):
            total_loss = 0.0
            # Mini-batch gradient steps
            for i in range(0, len(train_texts), batch_size):
                batch_texts = train_texts[i:i+batch_size]
                batch_labels = train_labels[i:i+batch_size].to(transformer.device)
                
                inputs = transformer.tokenizer(
                    batch_texts,
                    padding=True,
                    truncation=True,
                    max_length=MAX_SEQ_LENGTH,
                    return_tensors="pt"
                )
                input_ids = inputs["input_ids"].to(transformer.device)
                mask = inputs.get("attention_mask")
                if mask is not None:
                    mask = mask.to(transformer.device)
                    
                optimizer.zero_grad()
                outputs = transformer(input_ids, attention_mask=mask)
                loss = criterion(outputs.logits, batch_labels)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                
            avg_loss = total_loss / max(1, len(train_texts) // batch_size)
            logger.info(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}")

        # Evaluation on Test Set
        logger.info("\nEvaluating Transformer on Multilingual Test Set...")
        transformer.eval()
        preds = []
        probas = []
        for text in test_texts:
            res = transformer.predict_text(text)
            pred_id = LABEL2ID[res["label"]]
            preds.append(pred_id)
            probas.append(res["probabilities"]["FAKE"])

        transformer_metrics = compute_classification_metrics(test_labels, preds, probas)
        logger.info(f"Transformer Test Accuracy: {transformer_metrics['accuracy']:.4f}, F1-Macro: {transformer_metrics['f1_macro']:.4f}")

        # Multilingual Breakdown
        test_df["pred_id"] = preds
        lang_breakdown = evaluate_multilingual_breakdown(test_df)
        logger.info(f"Performance across languages: {json.dumps(lang_breakdown, indent=2)}")

        # Save Transformer
        transformer_save_dir = MODELS_DIR / "transformer_checkpoint"
        transformer.save_model(transformer_save_dir)
        results["transformer"] = transformer_metrics
        results["multilingual_breakdown"] = lang_breakdown

    # Save summary report
    report_path = MODELS_DIR / "evaluation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    logger.info(f"Evaluation report saved to {report_path}")
    logger.info("=== Training and Evaluation Pipeline Completed Successfully ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--augment", action="store_true", default=True, help="Use back-translation data augmentation")
    parser.add_argument("--model", type=str, default="all", choices=["baseline", "transformer", "all"])
    parser.add_argument("--transformer", type=str, default="bert-base-multilingual-cased")
    parser.add_argument("--epochs", type=int, default=3)
    args = parser.parse_args()
    
    train_pipeline(
        use_augmentation=args.augment,
        model_type=args.model,
        transformer_name=args.transformer,
        epochs=args.epochs
    )
