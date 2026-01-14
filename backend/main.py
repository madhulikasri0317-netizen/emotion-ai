

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import logging
import base64
import io
import secrets
import random
from functools import wraps

import numpy as np
import cv2
from PIL import Image
from werkzeug.security import generate_password_hash, check_password_hash



from face_model_loader import predict_face_emotion

try:
    from predict_text import classify_text as model_classify_text
    HAVE_TEXT_MODEL = True
except Exception:
    model_classify_text = None
    HAVE_TEXT_MODEL = False


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("emotion.ai.backend")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})



USERS = {}
SESSIONS = {}


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or token not in SESSIONS:
            return jsonify({"error": "Unauthorized"}), 401
        request.user = SESSIONS[token]
        return f(*args, **kwargs)
    return wrapper


KEYWORDS = {
    "happy": "joy", "joy": "joy", "love": "joy", "excited": "joy",
    "sad": "sadness", "depressed": "sadness", "unhappy": "sadness",
    "angry": "anger", "mad": "anger", "furious": "anger",
    "scared": "fear", "afraid": "fear", "nervous": "fear",
    "surprised": "surprise", "wow": "surprise",
}

def simple_classify(text):
    t = (text or "").lower()
    for k, v in KEYWORDS.items():
        if k in t:
            return {"label": v, "score": 0.9}
    return {"label": "neutral", "score": 0.5}



EMOTION_RESPONSES = {
    "joy": [
        "I can feel your positive energy 😊 What’s been going well?",
        "That’s lovely to hear. Want to tell me more?",
        "Happiness suits you."
    ],
    "sadness": [
        "I’m really sorry you’re feeling this way. I’m here with you.",
        "It’s okay to feel low sometimes. What’s been weighing on you?",
        "You don’t have to go through this alone."
    ],
    "anger": [
        "That sounds frustrating. Want to talk about what happened?",
        "Strong emotions are valid. Let’s slow this down together.",
        "I’m listening — tell me what’s bothering you."
    ],
    "fear": [
        "That sounds scary. You’re safe here.",
        "Do you want to share what’s worrying you?",
        "Let’s take this one step at a time."
    ],
    "surprise": [
        "That sounds unexpected!",
        "Wow — what happened?",
        "Tell me more about that."
    ],
    "neutral": [
        "I’m listening.",
        "Tell me more.",
        "How are you feeling right now?"
    ],
}



@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "text_model": HAVE_TEXT_MODEL,
        "face_model": True,
        "bot": True
    })



@app.route("/auth", methods=["POST", "OPTIONS"])
def auth():
    if request.method == "OPTIONS":
        return make_response("", 200)

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    email = data.get("email")
    password = data.get("password")
    mode = data.get("mode")

    if not email or not password or mode not in ("signup", "login"):
        return jsonify({"error": "Missing fields"}), 400

    if mode == "signup":
        if email in USERS:
            return jsonify({"error": "User exists"}), 409

        USERS[email] = generate_password_hash(password)
        token = secrets.token_hex(24)
        SESSIONS[token] = email
        return jsonify({"success": True, "token": token})

    if email not in USERS or not check_password_hash(USERS[email], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = secrets.token_hex(24)
    SESSIONS[token] = email
    return jsonify({"success": True, "token": token})



@app.route("/predict_text", methods=["POST", "OPTIONS"])
@require_auth
def predict_text():
    if request.method == "OPTIONS":
        return make_response("", 200)

    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify({"error": "Text required"}), 400

    text = data["text"]

    try:
        if HAVE_TEXT_MODEL:
            res = model_classify_text(text)
            primary = res if isinstance(res, dict) else simple_classify(text)
        else:
            primary = simple_classify(text)
    except Exception:
        primary = simple_classify(text)

    return jsonify({
        "text": text,
        "predictions": [
            primary,
            {"label": "neutral", "score": round(1 - primary["score"], 2)}
        ]
    })


@app.route("/predict_face", methods=["POST", "OPTIONS"])
@require_auth
def predict_face():
    if request.method == "OPTIONS":
        return make_response("", 200)

    try:
        data = request.get_json(silent=True)
        if not data or "image" not in data:
            return jsonify({"error": "Image required"}), 400

        img_b64 = data["image"]
        if "," in img_b64:
            img_b64 = img_b64.split(",", 1)[1]

        img_bytes = base64.b64decode(img_b64)
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        img_np = np.array(pil_img)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        if len(faces) > 0:
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            face = img_bgr[y:y+h, x:x+w]
            pil_face = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
        else:
            pil_face = pil_img

        primary = predict_face_emotion(pil_face)

        return jsonify({
            "predictions": [
                primary,
                {"label": "neutral", "score": round(1 - primary.get("score", 0), 2)}
            ]
        })

    except Exception as e:
        log.exception("Face error")
        return jsonify({"error": str(e)}), 500



@app.route("/chat", methods=["POST"])
@require_auth
def chat():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    message = data.get("message", "")
    emotion = data.get("emotion", "neutral")

    responses = EMOTION_RESPONSES.get(emotion, EMOTION_RESPONSES["neutral"])
    reply = random.choice(responses)

    return jsonify({
        "reply": reply,
        "emotion": emotion
    })



@app.route("/logout", methods=["POST"])
@require_auth
def logout():
    token = request.headers.get("Authorization")
    SESSIONS.pop(token, None)
    return jsonify({"success": True})


if __name__ == "__main__":
    log.info("Backend running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
