"use client";

import socket from "../../../socket";
import { useCallback, useEffect } from "react";

enum ServerEvent {
  GAME_UPDATE = "game_update",
}

interface GameUpdate {
  id: string;
  current_state: string;
  scores: Record<string, number>;
  question_text: string;
  question_options: string[];
  answers: Record<string, number>;
  time_remaining: number;
}
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
