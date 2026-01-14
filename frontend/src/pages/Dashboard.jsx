import React from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Dashboard.module.css";

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        <h1 className={styles.title}>How would you like to begin?</h1>
        <p className={styles.subtitle}>
          Choose a path. Move at your own pace.
        </p>

        <div className={styles.grid}>
          <div
            className={styles.card}
            onClick={() => navigate("/text")}
          >
            <div className={styles.cardTitle}>Text Emotion</div>
            <div className={styles.cardDesc}>
              Analyze emotions from written thoughts and messages.
            </div>
          </div>

          <div
            className={styles.card}
            onClick={() => navigate("/face")}
          >
            <div className={styles.cardTitle}>Face Emotion</div>
            <div className={styles.cardDesc}>
              Detect emotions through facial expressions using AI.
            </div>
          </div>

          <div
            className={styles.card}
            onClick={() => navigate("/voice")}
          >
            <div className={styles.cardTitle}>Voice Emotion</div>
            <div className={styles.cardDesc}>
              Understand emotions from tone and speech patterns.
            </div>
          </div>

          <div
            className={styles.card}
            onClick={() => navigate("/friends")}
          >
            <div className={styles.cardTitle}>Make Friends</div>
            <div className={styles.cardDesc}>
              Connect with like-minded people based on emotions.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
