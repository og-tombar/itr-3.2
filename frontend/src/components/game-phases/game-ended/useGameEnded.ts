import { GameUpdate } from "@/app/game/types";
import socket from "@/shared/socket";
import { useRouter } from "next/navigation";

export default function useGameEnded(gameState: GameUpdate) {
  const router = useRouter();
  const sortedScores = Object.entries(gameState.players).sort(
    ([, a], [, b]) => b.score - a.score
  );

  const getPlayer = () => {
    return socket.id ? gameState.players[socket.id] : null;
  };

  const getName = () => {
    return getPlayer()?.name;
  };

  const getScore = () => {
    return getPlayer()?.score;
  };

  const getRank = () => {
    return 1 + sortedScores.findIndex(([playerId]) => playerId === socket.id);
  };

  const isOnPodium = () => {
    return getRank() <= 3;
  };

  const handleBackToLobby = () => {
    router.push("/lobby");
  };

  return {
    sortedScores,
    handleBackToLobby,
    getName,
    getScore,
    getRank,
    isOnPodium,
  };
}
