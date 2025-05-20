"use client";

import React from "react";
import { useLobby } from "./Lobby";
import "./Lobby.css";

export default function Lobby() {
  const { timeRemaining, handleJoin } = useLobby();

  return (
    <div className="lobbyContainer">
      <h1 className="mainTitle">Triv-YA!</h1>
      <div className="timer">
        <span>{timeRemaining}</span>
      </div>
      <div className="mainContent">
        <button className="joinButton" onClick={handleJoin}>
          Join Game
        </button>
      </div>
      <div className="decorativeElements">
        <div className="bubble bubble1"></div>
        <div className="bubble bubble2"></div>
        <div className="bubble bubble3"></div>
      </div>
    </div>
  );
}
