import React, { useState } from "react";
import { API_BASE } from "../config";
import { useAuth } from "../context/AuthContext";

export default function TextEmotion() {
  const { token } = useAuth();

  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [emotion, setEmotion] = useState(null);
  const [reply, setReply] = useState("");
  const [error, setError] = useState("");

  const speak = (message, mood) => {
    if (!window.speechSynthesis) return;

    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(message);

    if (mood === "sadness") {
      u.rate = 0.9;
      u.pitch = 0.8;
    } else if (mood === "joy") {
      u.rate = 1.05;
      u.pitch = 1.2;
    } else if (mood === "anger") {
      u.rate = 1.0;
      u.pitch = 0.9;
    } else {
      u.rate = 1.0;
      u.pitch = 1.0;
    }

    u.lang = "en-US";
    window.speechSynthesis.speak(u);
  };

  const analyzeAndChat = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setError("");
    setEmotion(null);
    setReply("");

    try {
      // 1️⃣ Detect emotion
      const emoRes = await fetch(`${API_BASE}/predict_text`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token,
        },
        body: JSON.stringify({ text }),
      });

      const emoData = await emoRes.json();
      const detectedEmotion = emoData.predictions[0].label;
      setEmotion(detectedEmotion);

      // 2️⃣ Ask bot to respond
      const chatRes = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token,
        },
        body: JSON.stringify({
          message: text,
          emotion: detectedEmotion,
        }),
      });

      const chatData = await chatRes.json();
      setReply(chatData.reply);

      // 3️⃣ Speak reply
      speak(chatData.reply, detectedEmotion);

    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <h1 style={styles.title}>Talk to Emotion.AI</h1>
      <p style={styles.subtitle}>
        Express yourself. I’ll respond based on how you feel.
      </p>

      <div style={styles.panel}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type how you’re feeling..."
          style={styles.textarea}
          rows={6}
        />

        <button
          style={styles.primary}
          onClick={analyzeAndChat}
          disabled={loading}
        >
          {loading ? "Thinking..." : "Send"}
        </button>

        {emotion && (
          <div style={styles.emotion}>
            Detected emotion: <strong>{emotion}</strong>
          </div>
        )}

        {reply && (
          <div style={styles.replyBox}>
            <strong>Emotion.AI:</strong>
            <p>{reply}</p>
          </div>
        )}

        {error && <div style={styles.error}>{error}</div>}
      </div>
    </div>
  );
}

/* ================= STYLES ================= */

const styles = {
  page: {
    minHeight: "100vh",
    padding: 48,
    background:
      "radial-gradient(circle at top, #0f172a 0%, #020617 70%)",
    color: "#e5e7eb",
  },
  title: {
    fontSize: 36,
    fontWeight: 700,
    marginBottom: 8,
  },
  subtitle: {
    color: "#94a3b8",
    marginBottom: 24,
  },
  panel: {
    maxWidth: 800,
    background: "rgba(255,255,255,0.05)",
    padding: 32,
    borderRadius: 24,
  },
  textarea: {
    width: "100%",
    background: "#020617",
    color: "#e5e7eb",
    border: "1px solid rgba(255,255,255,0.2)",
    borderRadius: 16,
    padding: 16,
    fontSize: 15,
    marginBottom: 16,
  },
  primary: {
    background: "#38bdf8",
    color: "#020617",
    border: "none",
    padding: "14px 28px",
    borderRadius: 14,
    fontWeight: 600,
    cursor: "pointer",
  },
  emotion: {
    marginTop: 16,
    color: "#38bdf8",
  },
  replyBox: {
    marginTop: 24,
    background: "#020617",
    padding: 20,
    borderRadius: 16,
    lineHeight: 1.6,
  },
  error: {
    color: "#f87171",
    marginTop: 12,
  },
};
