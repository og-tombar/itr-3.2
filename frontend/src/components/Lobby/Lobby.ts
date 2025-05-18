import { useEffect, useState } from "react";
import socket from "../../socket";
import { useRouter } from "next/navigation";

interface GameState {
  id: string;
  players: string[];
}

export function useLobby() {
  const router = useRouter();
  const [players, setPlayers] = useState<string[]>([]);

  const handleJoin = () => {
    socket.emit("join_lobby", {});
  };

  useEffect(() => {
    socket.on("lobby_update", (players: string[]) => {
      console.log("[frontend] lobby_update", players);
      setPlayers(players);
    });

    socket.on("game_start", (game: GameState) => {
      console.log("[frontend] game_start", game);
      router.push(`/game/${game.id}`);
    });

    return () => {
      socket.off("lobby_update");
      socket.off("game_start");
    };
  }, [router]);

  return { players, handleJoin };
}
