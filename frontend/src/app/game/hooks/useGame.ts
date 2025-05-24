"use client";

import { useCallback, useEffect, useState } from "react";
import socket from "../../../shared/socket";
import { ServerEvent } from "../../../shared/events";
import { GamePhase, GameUpdate } from "../types";
import { useRouter } from "next/navigation";

export function useGame() {
  const [gameState, setGameState] = useState<GameUpdate | null>(null);
  const router = useRouter();
  const handleGameUpdate = useCallback(
    (update: GameUpdate) => {
      console.log("[frontend] game_update", update);
      if (update.phase === GamePhase.GAME_EXIT) {
        router.push("/");
      }
      setGameState(update);
    },
    [router]
  );

  useEffect(() => {
    socket.on(ServerEvent.GAME_UPDATE, handleGameUpdate);
    return () => {
      socket.off(ServerEvent.GAME_UPDATE, handleGameUpdate);
    };
  }, [handleGameUpdate]);

  return { gameState, handleGameUpdate };
}
