import React from "react";
import { Link } from "react-router-dom";

const sectionStyle = (image) => ({
  minHeight: "100vh",
  width: "100%",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  textAlign: "center",
  padding: "0 10vw",
  backgroundImage: `
    linear-gradient(
      rgba(0,0,0,0.65),
      rgba(0,0,0,0.65)
    ),
    url(${image})
  `,
  backgroundSize: "cover",
  backgroundPosition: "center",
  backgroundRepeat: "no-repeat",
});

const headingStyle = {
  fontSize: "clamp(3rem, 6vw, 5rem)",
  fontWeight: 700,
  color: "#ffffff",
  marginBottom: "1.5rem",
  lineHeight: 1.1,
};

const textStyle = {
  fontSize: "clamp(1.25rem, 2.2vw, 1.6rem)",
  color: "#e5e7eb",
  maxWidth: "900px",
  margin: "0 auto",
  lineHeight: 1.7,
};

export default function Home() {
  return (
    <>
      {/* SECTION 1 */}
      <section
        style={sectionStyle(
          "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"
        )}
      >
        <div>
          <h1 style={headingStyle}>
            On certain days,<br />even thought bleeds mute.
          </h1>
          <p style={textStyle}>
            When words feel heavy.<br />
            When silence speaks louder.<br />
            We stay with you.
          </p>
        </div>
      </section>

      {/* SECTION 2 */}
      <section
        style={sectionStyle(
          "https://images.unsplash.com/photo-1506126613408-eca07ce68773"
        )}
      >
        <div>
          <h2 style={headingStyle}>
            We understand — even when you cannot talk
          </h2>
          <p style={textStyle}>
            Emotion.AI gently reflects emotional signals through text, voice,
            and expression — only when you choose to share.
          </p>
        </div>
      </section>

      {/* SECTION 3 */}
      <section
        style={sectionStyle(
          "https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d"
        )}
      >
        <div>
          <h2 style={headingStyle}>
            Awareness, not diagnosis
          </h2>
          <p style={textStyle}>
            This is not medical judgment.<br />
            It is emotional awareness — private, calm, and respectful.
          </p>
        </div>
      </section>

      {/* SECTION 4 */}
      <section
        style={sectionStyle(
          "https://images.unsplash.com/photo-1511632765486-a01980e01a18"
        )}
      >
        <div>
          <h2 style={headingStyle}>
            Express in the way that feels safest
          </h2>
          <p style={textStyle}>
            Write. Speak. Or simply be seen.<br />
            Emotion.AI adapts to how you choose to express yourself.
          </p>
        </div>
      </section>

      {/* SECTION 5 */}
      <section
        style={sectionStyle(
          "https://images.unsplash.com/photo-1494790108377-be9c29b29330"
        )}
      >
        <div>
          <h2 style={headingStyle}>
            You are not alone
          </h2>
          <p style={textStyle}>
            Connect with people who experience similar emotional rhythms —
            ADHD, anxiety, burnout, OCD, and more.
          </p>
        </div>
      </section>

      {/* SECTION 6 */}
      <section
        style={sectionStyle(
          "https://images.unsplash.com/photo-1506784983877-45594efa4cbe"
        )}
      >
        <div>
          <h2 style={headingStyle}>
            Begin when you are ready
          </h2>
          <p style={textStyle}>
            Private. Gentle. On your terms.
          </p>

          <div style={{ marginTop: "3rem" }}>
            <Link to="/text">
              <button
                style={{
                  padding: "14px 32px",
                  fontSize: "1.1rem",
                  borderRadius: "10px",
                  border: "none",
                  background: "#22c55e",
                  color: "#022c22",
                  cursor: "pointer",
                  fontWeight: 600,
                }}
              >
                Login / Sign Up
              </button>
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
