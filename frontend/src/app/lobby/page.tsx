"use client";

import React from "react";
import { useLobby } from "./hooks/useLobby";
import Countdown from "@/components/countdown/Countdown";

export default function Lobby() {
  const { timeRemaining, handleJoin } = useLobby();

  return (
    <div className="container-fullscreen">
      <h1 className="title-main animate-bounce">Takooh</h1>

      <Countdown timeRemaining={timeRemaining} />

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
