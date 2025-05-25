import { ClientEvent, ServerEvent } from "@/shared/events";
import socket from "@/shared/socket";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { LobbyUpdate, NewGame } from "../types";

export default function useJoinLobby() {
  const router = useRouter();
  const [isJoined, setIsJoined] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState<number | null>(null);

  const onJoinLobby = () => {
    socket.emit(ClientEvent.JOIN_LOBBY, {});
  };

  const handleLobbyUpdate = useCallback((data: LobbyUpdate) => {
    console.log("[frontend] lobby_update", data);
    setIsJoined(true);
    setTimeRemaining(data.time_remaining);
  }, []);

  const handleNewGame = useCallback(
    (game: NewGame) => {
      socket.emit(ClientEvent.JOIN_GAME, { game_id: game.id });
      router.push(`/game/${game.id}`);
    },
    [router]
  );

  useEffect(() => {
    socket.on(ServerEvent.LOBBY_UPDATE, handleLobbyUpdate);
    socket.on(ServerEvent.NEW_GAME, handleNewGame);
    return () => {
      socket.off(ServerEvent.LOBBY_UPDATE, handleLobbyUpdate);
      socket.off(ServerEvent.NEW_GAME, handleNewGame);
    };
  }, [handleLobbyUpdate, handleNewGame]);

  return { onJoinLobby, isJoined, timeRemaining };
}
