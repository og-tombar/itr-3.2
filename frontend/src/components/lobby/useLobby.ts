import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import socket from "../../shared/socket";
import { ClientEvent, ServerEvent } from "../../shared/events";
import { LobbyUpdate, NewGame, NewPlayer } from "./types";

export function useLobby() {
  const router = useRouter();
  const [players, setPlayers] = useState<string[]>([]);
  const [timeRemaining, setTimeRemaining] = useState<number | undefined>();

  const handleNewPlayer = useCallback(() => {
    console.log("[frontend] new_player");
    const data: NewPlayer = { name: "John Doe" };
    socket.emit(ClientEvent.NEW_PLAYER, data);
  }, []);

  const handleLobbyUpdate = useCallback((update: LobbyUpdate) => {
    console.log("[frontend] lobby_update", update);
    setPlayers(update.players);
    setTimeRemaining(update.time_remaining);
  }, []);

  const handleNewGame = useCallback(
    (data: NewGame) => {
      console.log("[frontend] new_game", data);
      router.push(`/game/${data.id}`);
      socket.emit(ClientEvent.JOIN_GAME, { game_id: data.id });
    },
    [router]
  );

  useEffect(() => {
    socket.on(ServerEvent.LOBBY_UPDATE, handleLobbyUpdate);
    socket.on(ServerEvent.NEW_GAME, handleNewGame);

    return () => {
      socket.off(ServerEvent.LOBBY_UPDATE);
      socket.off(ServerEvent.NEW_GAME);
    };
  }, [handleLobbyUpdate, handleNewGame]);

  return { players, timeRemaining, handleNewPlayer };
}
