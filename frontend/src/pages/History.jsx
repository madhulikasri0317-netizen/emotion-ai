// frontend/src/pages/History.jsx
import React from "react";

export default function History() {
  // placeholder static history for now
  const logs = [
    { time: "Nov 17, 2025 09:30", label: "happy", note: "Woke up good" },
    { time: "Nov 16, 2025 21:15", label: "sad", note: "Tough day" },
    { time: "Nov 15, 2025 18:02", label: "neutral", note: "Normal" },
  ];

  return (
    <div style={{ padding: 20, maxWidth: 900, margin: "0 auto", fontFamily: "Inter, Arial" }}>
      <h2>Mood History</h2>
      <p style={{ color: "#9aa4b2" }}>Your recent detected moods (placeholder data).</p>

      <div style={{ marginTop: 16, display: "grid", gap: 10 }}>
        {logs.map((l, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: 12, borderRadius: 10, background: "rgba(255,255,255,0.02)" }}>
            <div>
              <div style={{ fontWeight: 700, textTransform: "capitalize" }}>{l.label}</div>
              <div style={{ color: "#9aa4b2", fontSize: 13 }}>{l.note}</div>
            </div>
            <div style={{ color: "#9aa4b2", fontSize: 13 }}>{l.time}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
