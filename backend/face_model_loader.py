from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image


ROOT_DIR = Path(__file__).resolve().parent.parent / "training"
MODEL_PATH = ROOT_DIR / "results-face" / "face_model.pt"
CLASS_FILE = ROOT_DIR / "results-face" / "class_names.txt"

if not MODEL_PATH.exists():
    raise RuntimeError(f"Face model not found: {MODEL_PATH}")

if not CLASS_FILE.exists():
    raise RuntimeError(f"Class names file not found: {CLASS_FILE}")


with open(CLASS_FILE, "r", encoding="utf-8") as f:
    CLASS_NAMES = [line.strip() for line in f if line.strip()]

NUM_CLASSES = len(CLASS_NAMES)


weights = models.ResNet18_Weights.DEFAULT
_model = models.resnet18(weights=weights)

num_features = _model.fc.in_features
_model.fc = nn.Linear(num_features, NUM_CLASSES)

state = torch.load(MODEL_PATH, map_location="cpu")
_model.load_state_dict(state)
_model.eval()

_transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)


def predict_face_emotion(image: Image.Image) -> dict:
    """
    Run inference on one face crop.

    Returns:
        {
          "label": "<top_label>",
          "score": <top_prob in 0–1>,
          "all_predictions": [
              {"label": "angry", "score": 0.x},
              {"label": "disgust", "score": 0.y},
              ...
          ]
        }
    """
    img_t = _transform(image).unsqueeze(0)  # shape (1, 3, 224, 224)

    with torch.no_grad():
        logits = _model(img_t)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()  # numpy array, sums to 1

    # build per-class list (0–1 probabilities)
    predictions = []
    for label, p in zip(CLASS_NAMES, probs):
        predictions.append(
            {
                "label": label,
                "score": float(p),  # 0–1 range
            }
        )

    # sort highest to lowest
    predictions.sort(key=lambda x: x["score"], reverse=True)

    top = predictions[0]

    return {
        "label": top["label"],
        "score": float(top["score"]),   # 0–1
        "all_predictions": predictions, # list of all emotions
    }
