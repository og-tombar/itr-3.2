import { useCallback, useEffect, useState } from "react";
import socket from "../../socket";
import { useRouter } from "next/navigation";

enum ClientEvent {
  JOIN_LOBBY = "join_lobby",
  JOIN_GAME = "join_game",
}

enum ServerEvent {
  LOBBY_UPDATE = "lobby_update",
  NEW_GAME = "new_game",
}

interface LobbyUpdate {
  players: string[];
  time_remaining: number;
  should_start_game: boolean;
}

export function useLobby() {
  const router = useRouter();
  const [players, setPlayers] = useState<string[]>([]);
  const [timeRemaining, setTimeRemaining] = useState<number | undefined>();

  const handleJoin = useCallback(() => {
    console.log("[frontend] join_lobby");
    socket.emit(ClientEvent.JOIN_LOBBY, {});
  }, []);

  const handleLobbyUpdate = useCallback((update: LobbyUpdate) => {
    console.log("[frontend] lobby_update", update);
    setPlayers(update.players);
    setTimeRemaining(update.time_remaining);
  }, []);

  const handleNewGame = useCallback(
    (gameId: string) => {
      console.log("[frontend] new_game", gameId);
      router.push(`/game/${gameId}`);
      socket.emit(ClientEvent.JOIN_GAME, { game_id: gameId });
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

  return { players, timeRemaining, handleJoin };
}
