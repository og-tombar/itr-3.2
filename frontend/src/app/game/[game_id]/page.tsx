"use client";

import { useParams } from "next/navigation";

export default function GamePage() {
  const { game_id } = useParams() as { game_id: string };

  return (
    <main style={{ fontFamily: "sans-serif", padding: 20 }}>
      <h1>Game Started!</h1>
      <p>
        Your game ID is <strong>{game_id}</strong>
      </p>
    </main>
  );
}
