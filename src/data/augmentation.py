import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import random

logger = logging.getLogger(__name__)

class MultilingualAugmentor:
    """
    Data Augmentation Engine for Multilingual NLP.
    Implements Back-Translation and Lexical Substitution to alleviate
    class imbalance in low-resource regional languages.
    """
    def __init__(self, pivot_lang: str = "en"):
        self.pivot_lang = pivot_lang
        self._translator = None

    def _get_translator(self):
        if self._translator is None:
            try:
                from deep_translator import GoogleTranslator
                self._translator = GoogleTranslator
            except ImportError:
                logger.warning("deep-translator not installed. Falling back to heuristic perturbation.")
                self._translator = None
        return self._translator

    def back_translate(self, text: str, source_lang: str) -> str:
        """
        Back-translates text from source_lang -> pivot_lang -> source_lang.
        If source is already pivot (en), uses an intermediate bridge like French ('fr') or German ('de').
        """
        if not text or len(text.strip()) == 0:
            return text

        translator_cls = self._get_translator()
        if translator_cls is None:
            return self.lexical_perturbation(text, source_lang)

        try:
            intermediate_lang = "es" if source_lang == "en" else "en"
            
            # Step 1: Forward Translation (source -> intermediate)
            forward_translator = translator_cls(source=source_lang, target=intermediate_lang)
            intermediate_text = forward_translator.translate(text)
            
            # Step 2: Backward Translation (intermediate -> source)
            backward_translator = translator_cls(source=intermediate_lang, target=source_lang)
            back_translated = backward_translator.translate(intermediate_text)
            
            return back_translated if back_translated else text
        except Exception as e:
            logger.debug(f"Back-translation API call failed: {e}. Using lexical perturbation.")
            return self.lexical_perturbation(text, source_lang)

    def lexical_perturbation(self, text: str, lang: str = "en") -> str:
        """
        Heuristic syntactic & lexical augmentation fallback:
        Inserts contextual markers or subtle rephrasing to enrich training representation.
        """
        words = text.split()
        if len(words) < 4:
            return text
            
        # Subtle variations while keeping label semantics intact
        replacements = {
            "en": {
                "announces": "reports",
                "reveals": "discloses",
                "confirmed": "verified",
                "warning": "alert",
                "urgent": "critical",
                "study": "research report"
            },
            "hi": {
                "घोषणा": "ऐलान",
                "सफल": "कामयाब",
                "चेतावनी": "सावधानी संदेश",
                "बड़ी": "प्रमुख"
            }
        }
        
        target_dict = replacements.get(lang, replacements["en"])
        new_words = []
        replaced = False
        for w in words:
            clean_w = w.strip(".,!?:;\"'").lower()
            if not replaced and clean_w in target_dict:
                new_words.append(target_dict[clean_w])
                replaced = True
            else:
                new_words.append(w)
                
        if not replaced and len(words) > 5:
            # Word re-ordering / jitter for robust generalization
            idx = random.randint(1, len(words) - 2)
            # Swap adjacent non-boundary words
            new_words[idx], new_words[idx + 1] = new_words[idx + 1], new_words[idx]

        return " ".join(new_words)

    def augment_dataset(
        self,
        input_records: List[Dict],
        target_languages: Optional[List[str]] = None,
        augmentation_factor: int = 1
    ) -> List[Dict]:
        """
        Augments dataset records for specified target languages or underrepresented classes.
        """
        augmented_records = list(input_records)
        target_langs = target_languages or ["hi", "bn", "es", "fr"]

        for item in input_records:
            if item.get("language") in target_langs:
                for i in range(augmentation_factor):
                    augmented_text = self.back_translate(item["text"], item["language"])
                    if augmented_text and augmented_text != item["text"]:
                        aug_item = dict(item)
                        aug_item["id"] = f"{item['id']}_AUG_{i+1}"
                        aug_item["text"] = augmented_text
                        aug_item["is_augmented"] = True
                        augmented_records.append(aug_item)
                        
        return augmented_records


def generate_augmented_corpus(raw_path: Path, output_path: Path):
    """Generates and saves the augmented multilingual corpus."""
    with open(raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    augmentor = MultilingualAugmentor()
    augmented = augmentor.augment_dataset(data, target_languages=["hi", "bn", "es", "fr"])
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(augmented, f, ensure_ascii=False, indent=2)
        
    print(f"Augmented corpus created with {len(augmented)} records (Original: {len(data)}) at {output_path}")
    return augmented
