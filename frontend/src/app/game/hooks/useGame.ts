"use client";

import { useCallback, useEffect } from "react";
import socket from "../../../shared/socket";
import { ServerEvent } from "../../../shared/events";
import { GameUpdate } from "../types";

export function useGame() {
  const handleGameUpdate = useCallback((update: GameUpdate) => {
    console.log("[frontend] game_update", update);
  }, []);

  useEffect(() => {
    socket.on(ServerEvent.GAME_UPDATE, handleGameUpdate);
    return () => {
      socket.off(ServerEvent.GAME_UPDATE, handleGameUpdate);
    };
  }, [handleGameUpdate]);

  return { handleGameUpdate };
}
