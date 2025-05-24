"use client";

import { useParams } from "next/navigation";
import { useGame } from "../../game/hooks/useGame";
import GamePhaseRenderer from "../components/GamePhaseRenderer";

export default function Game() {
  const { game_id } = useParams() as { game_id: string };
  const { gameState } = useGame();

  const handleAnswerClick = (optionIndex: number) => {
    // TODO: Implement answer handling logic later
    console.log(`Answer ${optionIndex} clicked`);
  };

  if (!gameState) {
    return (
      <div style={{ fontFamily: "sans-serif", padding: 20 }}>
        <h1>Game Started!</h1>
        <p>
          Your game ID is <strong>{game_id}</strong>
        </p>
        <p>Waiting for game updates...</p>
      </div>
    );
  }

  return (
    <GamePhaseRenderer
      gameState={gameState}
      onAnswerClick={handleAnswerClick}
    />
  );
}
