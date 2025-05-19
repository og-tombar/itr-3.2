"use client";

import React from "react";
import { useLobby } from "./Lobby";
import "./Lobby.css";

export default function Lobby() {
  const { players, handleJoinLobby } = useLobby();

  return (
    <div className="lobbyContainer">
      <button className="joinButton" onClick={handleJoinLobby}>
        Join Lobby
      </button>
      <p className="playerCount">Players in lobby: {players.length}</p>
    </div>
  );
}
