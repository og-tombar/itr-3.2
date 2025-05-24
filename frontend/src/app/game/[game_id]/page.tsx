"use client";

import { useParams } from "next/navigation";
import { useGame } from "../../game/hooks/useGame";

export default function Game() {
  const { game_id } = useParams() as { game_id: string };
  useGame();

  return (
    <div style={{ fontFamily: "sans-serif", padding: 20 }}>
      <h1>Game Started!</h1>
      <p>
        Your game ID is <strong>{game_id}</strong>
      </p>
    </div>
  );
}
