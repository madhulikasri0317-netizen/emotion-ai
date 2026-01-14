# Emotion AI

Emotion AI is a full-stack system for detecting and responding to human emotions using facial expressions, voice signals, and textual input. The application combines multimodal emotion recognition with an adaptive conversational layer to generate context-aware responses based on the user’s emotional state.

The project is built with a research-oriented mindset and is intended for exploratory, supportive, and analytical use cases rather than clinical diagnosis.

---

## Core Capabilities

- Facial emotion recognition using computer vision  
- Voice-based emotion detection from speech features  
- Text emotion classification using NLP models  
- Emotion-aware conversational responses  
- User authentication and emotion history tracking  
- Modular training pipelines for experimentation and improvement  

---

## Technology Stack

**Frontend**
- React
- JavaScript
- HTML / CSS

**Backend**
- Python
- Flask (REST APIs)
- JWT-based authentication

**Machine Learning & AI**
- TensorFlow / PyTorch
- Hugging Face Transformers (text emotion models)
- OpenCV (facial emotion analysis)
- Speech processing libraries for voice emotion detection

**Data & Storage**
- CSV-based datasets for training
- Model artifacts generated locally (not committed)
- Optional database integration for user data and emotion logs

---

## Repository Structure

backend/
├── main.py
├── auth.py
├── predict_text.py
├── face_model_loader.py
└── utils/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── context/
│   └── styles/
└── public/

training/
├── data/
├── generate_dataset.py
├── finetune_emotion.py
├── train_face.py
└── train_voice.py
