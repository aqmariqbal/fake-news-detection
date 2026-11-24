import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.config import RAW_DATA_PATH, LABEL2ID, ID2LABEL, MAX_SEQ_LENGTH

class MultilingualFakeNewsDataset:
    """
    Multilingual Fake News Dataset Handler supporting cross-lingual partitioning,
    zero-shot language splits, and transformer preprocessing.
    """
    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = Path(data_path) if data_path else RAW_DATA_PATH
        self.records: List[Dict] = []
        self.df: pd.DataFrame = pd.DataFrame()
        self.load_data()

    def load_data(self) -> pd.DataFrame:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")
        
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.records = json.load(f)
            
        self.df = pd.DataFrame(self.records)
        self.df["label_id"] = self.df["label"].map(LABEL2ID)
        return self.df

    def get_language_distribution(self) -> Dict[str, Dict[str, int]]:
        """Returns distribution of Real vs Fake per language."""
        dist = {}
        for lang, group in self.df.groupby("language"):
            dist[lang] = {
                "total": len(group),
                "REAL": int((group["label"] == "REAL").sum()),
                "FAKE": int((group["label"] == "FAKE").sum())
            }
        return dist

    def split_data(
        self,
        test_size: float = 0.2,
        val_size: float = 0.1,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Stratified train/val/test split across languages and labels.
        """
        train_df, test_df = train_test_split(
            self.df,
            test_size=test_size,
            random_state=random_state,
            stratify=self.df["label_id"]
        )
        
        adjusted_val_size = val_size / (1.0 - test_size)
        train_df, val_df = train_test_split(
            train_df,
            test_size=adjusted_val_size,
            random_state=random_state,
            stratify=train_df["label_id"]
        )
        
        return (
            train_df.reset_index(drop=True),
            val_df.reset_index(drop=True),
            test_df.reset_index(drop=True)
        )

    def zero_shot_split(
        self,
        train_languages: List[str] = ["en"],
        eval_languages: Optional[List[str]] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Partitions dataset for zero-shot cross-lingual transfer learning.
        Train on source languages (e.g., English), evaluate on target languages (e.g., Hindi, Bengali).
        """
        train_df = self.df[self.df["language"].isin(train_languages)].copy()
        if eval_languages:
            eval_df = self.df[self.df["language"].isin(eval_languages)].copy()
        else:
            eval_df = self.df[~self.df["language"].isin(train_languages)].copy()
            
        return train_df.reset_index(drop=True), eval_df.reset_index(drop=True)


def tokenize_batch(texts: List[str], tokenizer, max_length: int = MAX_SEQ_LENGTH):
    """
    Standardized tokenizer wrapper for cross-lingual transformers (mBERT, XLM-RoBERTa).
    """
    return tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt"
    )
