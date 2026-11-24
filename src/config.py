import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "multilingual_fakenews.json"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
AUGMENTED_DATA_PATH = DATA_DIR / "augmented" / "augmented_multilingual.json"
MODELS_DIR = BASE_DIR / "models_saved"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
(DATA_DIR / "raw").mkdir(parents=True, exist_ok=True)
(DATA_DIR / "processed").mkdir(parents=True, exist_ok=True)
(DATA_DIR / "augmented").mkdir(parents=True, exist_ok=True)

# Model Architecture Configs
SUPPORTED_MODELS = {
    "xlm-roberta": "xlm-roberta-base",
    "mbert": "bert-base-multilingual-cased",
    "distilbert-multilingual": "distilbert-base-multilingual-cased"
}

DEFAULT_MODEL_KEY = "mbert"

# Training & Inference Hyperparameters
MAX_SEQ_LENGTH = 128
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
NUM_EPOCHS = 3
WEIGHT_DECAY = 0.01
SEED = 42

# Label Mappings
LABEL2ID = {"REAL": 0, "FAKE": 1}
ID2LABEL = {0: "REAL", 1: "FAKE"}

# Supported Languages for Cross-Lingual Evaluation
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi (हिंदी)",
    "bn": "Bengali (বাংলা)",
    "es": "Spanish (Español)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
    "ta": "Tamil (தமிழ்)"
}
