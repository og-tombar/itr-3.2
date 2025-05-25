"use client";

import React from "react";
import Countdown from "@/components/countdown/Countdown";
import LobbyForm from "../lobby-form/LobbyForm";
import LargeButton from "../large-button/LargeButton";
import useJoinLobby from "../hooks/useJoinLobby";
import usePlayerInfo from "../hooks/usePlayerInfo";
import useNameInput from "../hooks/useNameInput";

export default function LobbyScreen() {
  const { isRegistered } = usePlayerInfo();
  const { nameInput, onChangeName, onSubmitName } = useNameInput();
  const { onJoinLobby, isJoined, timeRemaining } = useJoinLobby();

  return (
    <div className="container-fullscreen">
      <h1 className="title-main animate-bounce">Takooh</h1>

      <div className="flex-column text-center">
        {isRegistered === false && (
          <LobbyForm
            input={nameInput}
            onChange={onChangeName}
            onSubmit={onSubmitName}
          />
        )}

        {isRegistered === true && !isJoined && (
          <LargeButton label="Join Game" onClick={onJoinLobby} />
        )}

        {isJoined && timeRemaining !== null && (
          <Countdown timeRemaining={timeRemaining} />
        )}
      </div>

      <div className="decorative-elements">
        <div className="bubble bubble-1"></div>
        <div className="bubble bubble-2"></div>
        <div className="bubble bubble-3"></div>
      </div>
    </div>
  );
}
