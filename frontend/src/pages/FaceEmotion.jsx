import React, { useRef, useState } from "react";
import { API_BASE } from "../config";
import { useAuth } from "../context/AuthContext";

export default function FaceEmotion() {
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const { token } = useAuth();

  const [cameraOn, setCameraOn] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  
  const startCamera = async () => {
    try {
      setError("");

      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      streamRef.current = stream;

      const video = videoRef.current;
      video.srcObject = stream;
      video.muted = true;
      video.playsInline = true;

      await video.play();
      setCameraOn(true);
    } catch {
      setCameraOn(false);
      setError("Camera permission denied or unavailable.");
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop());
      streamRef.current = null;
    }
    videoRef.current.srcObject = null;
    setCameraOn(false);
    setError("");
    setResult(null);
  };

  const captureEmotion = async () => {
    if (!cameraOn) return;

    const canvas = document.createElement("canvas");
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(videoRef.current, 0, 0);

    const image = canvas.toDataURL("image/jpeg");

    const res = await fetch(`${API_BASE}/predict_face`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: token,
      },
      body: JSON.stringify({ image }),
    });

    const data = await res.json();
    setResult(data);
  };


  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <h1 style={styles.title}>Face Emotion Analysis</h1>
        <p style={styles.subtitle}>
          Your camera is private. You decide when it’s active.
        </p>
      </header>

      <section style={styles.panel}>
        <div style={styles.videoShell}>
          <video
            ref={videoRef}
            style={{
              ...styles.video,
              opacity: cameraOn ? 1 : 0,
            }}
          />
          {!cameraOn && (
            <div style={styles.videoPlaceholder}>
              <span>Camera is off</span>
            </div>
          )}

          <span
            style={{
              ...styles.status,
              background: cameraOn ? "#16a34a" : "#334155",
            }}
          >
            {cameraOn ? "Camera Active" : "Camera Disabled"}
          </span>
        </div>

        <div style={styles.actions}>
          <button style={styles.primary} onClick={startCamera}>
            Enable Camera
          </button>

          <button
            style={styles.secondary}
            onClick={captureEmotion}
            disabled={!cameraOn}
          >
            Capture Emotion
          </button>

          <button
            style={styles.secondary}
            onClick={() => setResult(null)}
            disabled={!result}
          >
            Clear Result
          </button>

          <button style={styles.danger} onClick={stopCamera}>
            Stop Camera
          </button>
        </div>

        {error && <div style={styles.error}>{error}</div>}

        {result && (
          <div style={styles.resultBox}>
            <h3 style={styles.resultTitle}>Detected Emotion</h3>
            <pre style={styles.result}>
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </section>
    </div>
  );
}


const styles = {
  page: {
    minHeight: "100vh",
    padding: "48px 24px",
    background:
      "radial-gradient(circle at top, #0f172a 0%, #020617 70%)",
    color: "#e5e7eb",
  },

  header: {
    maxWidth: 1100,
    margin: "0 auto 32px",
  },

  title: {
    fontSize: 36,
    fontWeight: 700,
    marginBottom: 8,
  },

  subtitle: {
    color: "#94a3b8",
    fontSize: 16,
  },

  panel: {
    maxWidth: 1100,
    margin: "0 auto",
    background: "rgba(255,255,255,0.04)",
    borderRadius: 24,
    padding: 32,
    boxShadow: "0 40px 120px rgba(0,0,0,0.5)",
  },

  videoShell: {
    position: "relative",
    height: 420,
    borderRadius: 20,
    overflow: "hidden",
    border: "1px solid rgba(255,255,255,0.15)",
    marginBottom: 24,
  },

  video: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    transition: "opacity 0.3s ease",
  },

  videoPlaceholder: {
    position: "absolute",
    inset: 0,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "#64748b",
    fontSize: 16,
  },

  status: {
    position: "absolute",
    top: 16,
    left: 16,
    padding: "6px 12px",
    borderRadius: 999,
    fontSize: 12,
    fontWeight: 600,
    color: "#fff",
  },

  actions: {
    display: "flex",
    gap: 12,
    flexWrap: "wrap",
    marginBottom: 16,
  },

  primary: {
    background: "#38bdf8",
    color: "#020617",
    border: "none",
    padding: "12px 20px",
    borderRadius: 12,
    fontWeight: 600,
    cursor: "pointer",
  },

  secondary: {
    background: "transparent",
    color: "#e5e7eb",
    border: "1px solid rgba(255,255,255,0.25)",
    padding: "12px 20px",
    borderRadius: 12,
    cursor: "pointer",
  },

  danger: {
    background: "#ef4444",
    color: "#fff",
    border: "none",
    padding: "12px 20px",
    borderRadius: 12,
    fontWeight: 600,
    cursor: "pointer",
  },

  error: {
    marginTop: 12,
    color: "#f87171",
    fontSize: 14,
  },

  resultBox: {
    marginTop: 24,
    background: "#020617",
    padding: 20,
    borderRadius: 16,
  },

  resultTitle: {
    marginBottom: 8,
    fontSize: 16,
    fontWeight: 600,
  },

  result: {
    fontSize: 14,
    color: "#cbd5f5",
  },
};
