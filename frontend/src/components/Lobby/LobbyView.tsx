"use client";

import React from "react";
import { useLobby } from "./Lobby";
import "./Lobby.css";

export default function Lobby() {
  const { players, handleJoin } = useLobby();

  return (
    <div className="lobbyContainer">
      <button className="joinButton" onClick={handleJoin}>
        Join Lobby
      </button>
      <p className="playerCount">Players in lobby: {players.length}</p>
    </div>
  );
}
