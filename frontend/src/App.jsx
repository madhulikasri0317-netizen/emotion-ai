import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import FaceEmotion from "./pages/FaceEmotion";
import TextEmotion from "./pages/TextEmotion";
import VoiceEmotion from "./pages/VoiceEmotion";
import History from "./pages/History";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />

            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />

            <Route
              path="/face"
              element={
                <ProtectedRoute>
                  <FaceEmotion />
                </ProtectedRoute>
              }
            />

            <Route
              path="/text"
              element={
                <ProtectedRoute>
                  <TextEmotion />
                </ProtectedRoute>
              }
            />

            <Route
              path="/voice"
              element={
                <ProtectedRoute>
                  <VoiceEmotion />
                </ProtectedRoute>
              }
            />

            <Route
              path="/history"
              element={
                <ProtectedRoute>
                  <History />
                </ProtectedRoute>
              }
            />
          </Routes>
        </Layout>
      </BrowserRouter>
    </AuthProvider>
  );
}
