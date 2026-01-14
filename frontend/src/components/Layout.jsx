import React from "react";
import { Link, useLocation } from "react-router-dom";

export default function Layout({ children }) {
  const location = useLocation();

  // Hide navbar on auth pages
  const hideNavbar =
    location.pathname === "/login";

  return (
    <div>
      {!hideNavbar && (
        <nav
          style={{
            height: 64,
            display: "flex",
            alignItems: "center",
            padding: "0 32px",
            background: "#020617",
            borderBottom: "1px solid #0f172a",
          }}
        >
          <div
            style={{
              fontWeight: 600,
              color: "#38bdf8",
              marginRight: 32,
              fontSize: 18,
            }}
          >
            emotion.ai
          </div>

          <div style={{ display: "flex", gap: 20 }}>
            <Link
              to="/dashboard"
              style={{ color: "#e5e7eb", textDecoration: "none" }}
            >
              Dashboard
            </Link>

            <Link
              to="/history"
              style={{ color: "#e5e7eb", textDecoration: "none" }}
            >
              History
            </Link>

            <Link
              to="/logout"
              style={{ color: "#e5e7eb", textDecoration: "none" }}
            >
              Logout
            </Link>
          </div>
        </nav>
      )}

      {children}
    </div>
  );
}
