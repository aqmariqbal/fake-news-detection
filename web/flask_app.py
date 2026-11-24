import sys
import os
import time
import pickle
import base64
from pathlib import Path
from flask import Flask, render_template, request, jsonify

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.multilingual_engine import evaluate_multilingual_content, detect_language
from src.media_extractor import extract_text_from_file, extract_text_from_image

MODEL_PATH = BASE_DIR / "models_saved" / "baseline_model.pkl"

TEMPLATE_DIR = BASE_DIR / "web" / "templates"
STATIC_DIR = BASE_DIR / "web" / "static"
app = Flask(__name__, template_folder=str(TEMPLATE_DIR), static_folder=str(STATIC_DIR))

# Load Baseline Model (TF-IDF + Classifier)
model = None
if MODEL_PATH.exists():
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print(f"[OK] Successfully loaded baseline model from {MODEL_PATH}")
    except Exception as e:
        print(f"[WARN] Error loading model: {e}")
else:
    print("[INFO] Model file not found. Fallback linguistic heuristic will be utilized.")


@app.route("/")
def index():
    """Serves the clean minimal single-column interface."""
    return render_template("index.html")


@app.route("/upload_media", methods=["POST"])
def upload_media():
    """
    Accepts uploaded documents (DOCX, PPTX, PDF, TXT) or Images (PNG, JPG, WEBP)
    as well as clipboard-pasted base64 images, extracting text via OCR or native parsers.
    """
    try:
        # 1. Check for file upload
        if "file" in request.files:
            uploaded_file = request.files["file"]
            filename = uploaded_file.filename
            if not filename:
                return jsonify({"error": "No filename provided"}), 400
            file_bytes = uploaded_file.read()
            extracted_text, file_type = extract_text_from_file(file_bytes, filename)
            return jsonify({
                "success": True,
                "text": extracted_text,
                "filename": filename,
                "file_type": file_type
            })

        # 2. Check for base64 pasted image from clipboard
        data = request.get_json(silent=True) or {}
        image_b64 = data.get("image_base64", "")
        if image_b64:
            if "," in image_b64:
                image_b64 = image_b64.split(",", 1)[1]
            image_bytes = base64.b64decode(image_b64)
            extracted_text = extract_text_from_image(image_bytes)
            return jsonify({
                "success": True,
                "text": extracted_text,
                "filename": "Pasted_Screenshot.png",
                "file_type": "Pasted Image OCR"
            })

        return jsonify({"error": "No file or image data provided"}), 400

    except Exception as e:
        return jsonify({"error": f"Failed to extract text: {str(e)}"}), 500


@app.route("/predict", methods=["POST"])
def predict():
    """API endpoint for multilingual news & fact-checking evaluation."""
    data = request.get_json(silent=True) or request.form.to_dict()
    headline = data.get("headline", "").strip()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Content text cannot be empty"}), 400

    res = evaluate_multilingual_content(headline, text, model=model)

    return jsonify({
        "prediction": res["prediction"],
        "confidence": res["confidence"],
        "language_name": res["language_name"],
        "language_code": res["language_code"],
        "word_count": res["word_count"],
        "vocab_density": res["vocab_density"],
        "latency_ms": res["latency_ms"],
        "credibility_style": res["style"],
        "fact_check_flag": res.get("fact_check_flag", False),
        "fact_check_note": res.get("fact_check_note", "")
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
