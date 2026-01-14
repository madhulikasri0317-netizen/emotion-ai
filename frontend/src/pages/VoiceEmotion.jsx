import React, { useEffect, useRef, useState } from "react";
export default function VoiceEmotion() {
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);

  const [recording, setRecording] = useState(false);
  const [error, setError] = useState("");
  const [time, setTime] = useState(0);

  // Timer
  useEffect(() => {
    if (!recording) return;
    const i = setInterval(() => setTime((t) => t + 1), 1000);
    return () => clearInterval(i);
  }, [recording]);

  const startRecording = async () => {
    setError("");
    setTime(0);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;

      recorder.start();
      setRecording(true);
    } catch (e) {
      setError("Microphone access denied.");
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    streamRef.current?.getTracks().forEach((t) => t.stop());
    setRecording(false);
  };

  return (
    <div style={styles.page}>
      <h1 style={styles.title}>Voice Emotion</h1>
      <p style={styles.subtitle}>
        Record freely. No data leaves your device yet.
      </p>

      <div style={styles.panel}>
        <div style={styles.timer}>
          {Math.floor(time / 60)}:{String(time % 60).padStart(2, "0")}
        </div>

        <div style={styles.actions}>
          {!recording ? (
            <button style={styles.primary} onClick={startRecording}>
              Start Recording
            </button>
          ) : (
            <button style={styles.danger} onClick={stopRecording}>
              Stop Recording
            </button>
          )}
        </div>

        {error && <div style={styles.error}>{error}</div>}
      </div>
    </div>
  );
}


const styles = {
  page: {
    minHeight: "100vh",
    padding: "48px",
    background:
      "radial-gradient(circle at top, #0f172a 0%, #020617 70%)",
    color: "#e5e7eb",
  },
  title: {
    fontSize: 36,
    fontWeight: 700,
  },
  subtitle: {
    color: "#94a3b8",
    marginBottom: 24,
  },
  panel: {
    background: "rgba(255,255,255,0.05)",
    padding: 32,
    borderRadius: 24,
    maxWidth: 600,
  },
  timer: {
    fontSize: 48,
    fontWeight: 700,
    marginBottom: 24,
  },
  actions: {
    display: "flex",
    gap: 16,
  },
  primary: {
    background: "#38bdf8",
    color: "#020617",
    border: "none",
    padding: "14px 24px",
    borderRadius: 14,
    fontWeight: 600,
    cursor: "pointer",
  },
  danger: {
    background: "#ef4444",
    color: "#fff",
    border: "none",
    padding: "14px 24px",
    borderRadius: 14,
    fontWeight: 600,
    cursor: "pointer",
  },
  error: {
    color: "#f87171",
    marginTop: 12,
  },
};
