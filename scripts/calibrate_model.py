import sys
import json
from pathlib import Path
import torch
import torch.nn as nn

# Bootstrap project root
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from src.config import AUGMENTED_DATA_PATH, RAW_DATA_PATH, MODELS_DIR
from src.models.transformer_classifier import MultilingualTransformerClassifier

def calibrate_and_train():
    data_path = AUGMENTED_DATA_PATH if AUGMENTED_DATA_PATH.exists() else RAW_DATA_PATH
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [d["text"] for d in data]
    labels = torch.tensor([1 if d["label"] == "FAKE" else 0 for d in data], dtype=torch.long)

    model = MultilingualTransformerClassifier(force_lightweight=True)
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()

    print(f"Calibrating transformer weights on {len(texts)} augmented multilingual samples...")
    for epoch in range(35):
        inputs = model.tokenizer(texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
        optimizer.zero_grad()
        outputs = model(inputs["input_ids"], attention_mask=inputs["attention_mask"])
        loss = criterion(outputs.logits, labels)
        loss.backward()
        optimizer.step()
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/35 - Loss: {loss.item():.4f}")

    model.eval()
    print(f"Final Training Loss: {loss.item():.4f}")

    test_samples = [
        ("सनसनीखेज दावा: इस चमत्कारिक पौधे की पत्तियां चबाने से 3 दिन में कैंसर पूरी तरह गायब हो जाता है!", "FAKE"),
        ("भारतीय अंतरिक्ष अनुसंधान संगठन (ISRO) ने मौसम उपग्रह का सफल प्रक्षेपण किया।", "REAL"),
        ("SHOCKING SECRET: Drinking boiled lemon juice with garlic cures all viruses in 24 hours guaranteed!", "FAKE"),
        ("World Health Organization announces updated international health guidelines following global clinical trials.", "REAL"),
        ("চাঞ্চল্যকর আবিষ্কার: লবঙ্গ ও মধুর মিশ্রণ খেলে ডায়াবেটিস ২৪ ঘণ্টায় চিরতরে ভালো হয়ে যায়!", "FAKE"),
        ("কলকাতা বিশ্ববিদ্যালয়ের গবেষকরা পরিবেশবান্ধব নতুন সৌরশক্তি সেল উদ্ভাবন করেছেন।", "REAL")
    ]

    print("\n--- Model Verification on Test Inputs ---")
    for text, truth in test_samples:
        res = model.predict_text(text)
        conf = res["confidence"] * 100
        lbl = res["label"]
        print(f"[{lbl}] (Conf: {conf:.1f}%) | Ground Truth: {truth} | Text: {text[:45]}...")

    save_dir = MODELS_DIR / "transformer_checkpoint"
    model.save_model(save_dir)
    print(f"\nCalibrated high-confidence model saved to {save_dir}")

if __name__ == "__main__":
    calibrate_and_train()
