# backend/predict_text.py
"""
Model loading and small wrapper for text -> emotion prediction.

Usage:
- import classify_text from this module:
    from predict_text import classify_text
    classify_text("I am happy")
- The function returns a dict: {"label": str, "score": float}

Behavior:
- Tries to load a HF model + tokenizer from (in order):
    1) training/emotion_model
    2) training/results-distilbert
- If neither exists or loading fails, falls back to a simple keyword classifier (safe fallback).
"""

import os
import math


SIMPLE_KEYWORDS = {
    "happy": "joy",
    "joy": "joy",
    "glad": "joy",
    "love": "joy",
    "excited": "joy",
    "sad": "sadness",
    "unhappy": "sadness",
    "depressed": "sadness",
    "angry": "anger",
    "mad": "anger",
    "furious": "anger",
    "scared": "fear",
    "afraid": "fear",
    "nervous": "fear",
    "surprised": "surprise",
    "wow": "surprise",
    "neutral": "neutral",
    "okay": "neutral",
    "fine": "neutral",
}


def simple_classify(text: str):
    t = (text or "").lower()
    for kw, label in SIMPLE_KEYWORDS.items():
        if kw in t:
            return {"label": label, "score": 0.9}
    if "!" in text:
        return {"label": "joy", "score": 0.6}
    if "?" in text:
        return {"label": "neutral", "score": 0.55}
    return {"label": "neutral", "score": 0.5}



MODEL_PATH_CANDIDATES = [
    os.path.join(os.path.dirname(__file__), "..", "training", "emotion_model"),
    os.path.join(os.path.dirname(__file__), "..", "training", "results-distilbert"),
]


MODEL_PATH_CANDIDATES = [os.path.normpath(p) for p in MODEL_PATH_CANDIDATES]

_use_model = False
_tokenizer = None
_model = None
_id2label = None


MODEL_NAME = "distilbert-base-uncased"

_use_model = False
_tokenizer = None
_model = None
_id2label = None

try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch

    for p in MODEL_PATH_CANDIDATES:
        if os.path.isdir(p):
            try:
                # --- tokenizer: try local first (avoid hub); if missing, fall back to base tokenizer name
                try:
                    # local_files_only avoids hub network requests for local folders
                    _tokenizer = AutoTokenizer.from_pretrained(p, local_files_only=True)
                    print(f"[predict_text] Loaded tokenizer from local folder: {p}")
                except Exception as tok_err:
                    # fallback to the base tokenizer from the hub (or local cache)
                    print(f"[predict_text] Local tokenizer not found in {p}, falling back to '{MODEL_NAME}': {tok_err}")
                    _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

                # --- model: load from the local folder (safetensors or pytorch files)
                # Use local_files_only=True so it reads the files from disk and doesn't try to resolve a hub id
                _model = AutoModelForSequenceClassification.from_pretrained(p, local_files_only=True)

                # get id2label mapping from model config (best-effort)
                cfg = getattr(_model, "config", None)
                if cfg and hasattr(cfg, "id2label"):
                    _id2label = {int(k): v for k, v in getattr(cfg, "id2label", {}).items()}
                else:
                    num = getattr(cfg, "num_labels", None)
                    if num:
                        _id2label = {i: str(i) for i in range(num)}

                _use_model = True
                print(f"[predict_text] Loaded model from: {p}")
                break
            except Exception as e:
                # print and try next candidate
                print(f"[predict_text] Failed to load model from {p}: {e}")
                _tokenizer = None
                _model = None
                _id2label = None

    if _use_model and _model is None:
        _use_model = False
except Exception as e:
    # transformers / torch might not be installed or failed to import
    print(f"[predict_text] Transformers/torch not available: {e}")
    _use_model = False


def classify_text(text: str):
    """
    Returns {"label": str, "score": float}
    """
    if not text or not isinstance(text, str) or text.strip() == "":
        return {"label": "neutral", "score": 0.0}

    if _use_model and _tokenizer is not None and _model is not None:
        try:
            # prepare inputs
            inputs = _tokenizer(text, truncation=True, padding=True, return_tensors="pt")
            _model.eval()
            with torch.no_grad():
                outputs = _model(**inputs)
                logits = outputs.logits
                # softmax
                probs = torch.softmax(logits, dim=-1).squeeze().cpu().numpy()
                # pick best
                best_idx = int(probs.argmax())
                best_score = float(probs[best_idx])
                label = _id2label.get(best_idx, str(best_idx)) if _id2label else str(best_idx)
                # ensure label is a string
                label = str(label)
                # clamp score
                if isinstance(best_score, (float, int)) and (not math.isnan(best_score)):
                    score = float(best_score)
                else:
                    score = 0.0
                return {"label": label, "score": score}
        except Exception as e:
            # fallback to simple classifier on any model error
            print(f"[predict_text] Model inference failed, falling back to rule-based. Error: {e}")
            return simple_classify(text)

    # fallback
    return simple_classify(text)


# convenience: allow import of function as default
if __name__ == "__main__":
    # quick interactive demo when run directly
    while True:
        try:
            s = input("Enter text (or 'quit'): ").strip()
            if s.lower() in ("quit", "q", "exit"):
                break
            print(classify_text(s))
        except KeyboardInterrupt:
            break
