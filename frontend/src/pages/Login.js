import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { API_BASE } from "../config";
import styles from "./Login.module.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [mode, setMode] = useState("login");

  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch(`${API_BASE}/auth`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, mode }),
      });

      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Failed");
        return;
      }

      login(data.token);
      navigate("/dashboard");
    } catch {
      setError("Backend not reachable");
    }
  };

  return (
    <div className={styles.wrapper}>
      <form className={styles.card} onSubmit={handleSubmit}>
        <div className={styles.brand}>emotion.ai</div>

        <h1 className={styles.title}>
          {mode === "login" ? "Welcome back" : "Create your account"}
        </h1>

        <p className={styles.subtitle}>
          {mode === "login"
            ? "Sign in to continue to your dashboard."
            : "Start understanding emotions intelligently."}
        </p>

        <div className={styles.field}>
          <input
            className={styles.input}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email address"
          />
        </div>

        <div className={styles.field}>
          <input
            className={styles.input}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
          />
        </div>

        <button className={styles.button} type="submit">
          {mode === "login" ? "Sign in" : "Create account"}
        </button>

        {error && <div className={styles.error}>{error}</div>}

        <div className={styles.footer}>
          {mode === "login"
            ? "Don't have an account?"
            : "Already have an account?"}
          <br />
          <button
            type="button"
            className={styles.toggleBtn}
            onClick={() =>
              setMode(mode === "login" ? "signup" : "login")
            }
          >
            {mode === "login" ? "Create account" : "Sign in"}
          </button>
        </div>
      </form>
    </div>
  );
}
