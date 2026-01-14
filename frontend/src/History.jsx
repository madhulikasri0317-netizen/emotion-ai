import React from "react";

export default function History() {
  const logs = [
    { time: "Nov 17, 2025 09:30", label: "happy", note: "Detected from text input" },
    { time: "Nov 16, 2025 21:15", label: "sad", note: "Detected from text input" },
    { time: "Nov 15, 2025 18:02", label: "neutral", note: "Detected from text input" },
  ];

  return (
    <div className="app-page">
      <div className="page-container">
        <h2>Emotion History</h2>
        <p>
          Recent emotion detections based on your interactions.
          These are interpretations, not diagnoses.
        </p>

        <div style={{ marginTop: 20, display: "grid", gap: 12 }}>
          {logs.map((l, i) => (
            <div key={i} className="card">
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <div>
                  <div style={{ fontWeight: 700, textTransform: "capitalize" }}>
                    {l.label}
                  </div>
                  <div className="muted">{l.note}</div>
                </div>
                <div className="muted">{l.time}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
