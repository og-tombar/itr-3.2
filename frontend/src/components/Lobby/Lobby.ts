import { useEffect, useState } from "react";
import socket from "../../socket";
import { useRouter } from "next/navigation";

enum ClientEvents {
  JOIN_LOBBY = "join_lobby",
  JOIN_GAME = "join_game",
  TEST = "test",
}

enum ServerEvents {
  LOBBY_UPDATE = "lobby_update",
  NEW_GAME = "new_game",
  TEST = "test",
}

export function useLobby() {
  const router = useRouter();
  const [players, setPlayers] = useState<string[]>([]);

  const handleJoinLobby = () => {
    socket.emit(ClientEvents.JOIN_LOBBY, {});
  };

  useEffect(() => {
    socket.on(ServerEvents.LOBBY_UPDATE, (players: string[]) => {
      console.log("[frontend] lobby_update", players);
      setPlayers(players);
    });

    socket.on(ServerEvents.NEW_GAME, (gameId: string) => {
      console.log("[frontend] new_game", gameId);
      socket.emit(ClientEvents.JOIN_GAME, { game_id: gameId });
      router.push(`/game/${gameId}`);
    });

    socket.on(ServerEvents.TEST, (message: string) => {
      console.log("[frontend] test", message);
    });

    return () => {
      socket.off(ServerEvents.LOBBY_UPDATE);
      socket.off(ServerEvents.NEW_GAME);
      socket.off(ServerEvents.TEST);
    };
  }, [router]);

  return { players, handleJoinLobby };
}
