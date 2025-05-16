import { useEffect, useState } from "react";
import socket from "../../socket";

export function useLobby() {
  const [players, setPlayers] = useState<string[]>([]);

  const handleJoin = () => {
    socket.emit("join_lobby", {});
  };

  useEffect(() => {
    const handler = (newPlayers: string[]) => {
      console.log("[frontend] lobby_update", newPlayers);
      setPlayers(newPlayers);
    };

    socket.on("lobby_update", handler);
    return () => {
      socket.off("lobby_update", handler);
    };
  }, []);

  return { players, handleJoin };
}
