"use client";

import React from "react";
import { useLobby } from "./hooks/useLobby";

export default function Lobby() {
  const { timeRemaining, handleJoin } = useLobby();

  return (
    <div className="container-fullscreen">
      <h1 className="title-main animate-bounce">Takooh</h1>

      <div
        style={{
          position: "absolute",
          top: "20px",
          right: "20px",
          width: "150px",
          height: "150px",
          background: "rgba(255, 255, 255, 0.9)",
          borderRadius: "50%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          boxShadow: "var(--shadow-medium)",
        }}
      >
        <span
          style={{
            fontFamily: "var(--font-body)",
            fontSize: "4rem",
            fontWeight: "bold",
            color: "var(--primary-purple)",
          }}
        >
          {timeRemaining}
        </span>
      </div>

      <div className="flex-column text-center">
        <button className="btn btn-primary btn-large" onClick={handleJoin}>
          Join Game
        </button>
      </div>

      <div className="decorative-elements">
        <div className="bubble bubble-1"></div>
        <div className="bubble bubble-2"></div>
        <div className="bubble bubble-3"></div>
      </div>
    </div>
  );
}
