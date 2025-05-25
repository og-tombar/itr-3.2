import { useCallback, useEffect, useState } from "react";
import socket from "@/shared/socket";
import { ClientEvent, ServerEvent } from "@/shared/events";
import { PlayerInfo } from "../types";

export default function usePlayerInfo() {
  const [player, setPlayer] = useState<PlayerInfo | null>(null);
  const [isRegistered, setIsRegistered] = useState<boolean | null>(null);

  // on mount
  useEffect(() => {
    console.log("[frontend] getting player");
    socket.emit(ClientEvent.GET_PLAYER, {});
  }, []);

  const handlePlayerInfo = useCallback((player: PlayerInfo) => {
    console.log("[frontend] got player", player);
    setPlayer(player);
    setIsRegistered(player.name !== "");
  }, []);

  const handlePlayerRegistered = useCallback(() => {
    console.log("[frontend] player registered");
    setIsRegistered(true);
  }, []);

  useEffect(() => {
    socket.on(ServerEvent.PLAYER_INFO, handlePlayerInfo);
    socket.on(ServerEvent.PLAYER_REGISTERED, handlePlayerRegistered);
    return () => {
      socket.off(ServerEvent.PLAYER_INFO, handlePlayerInfo);
      socket.off(ServerEvent.PLAYER_REGISTERED, handlePlayerRegistered);
    };
  }, [handlePlayerInfo, handlePlayerRegistered]);

  return { player, isRegistered };
}
