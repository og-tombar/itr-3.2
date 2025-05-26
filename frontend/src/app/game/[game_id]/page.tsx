"use client";

import { GamePhase } from "../types";
import GameStartedScreen from "@/components/game-phases/game-started/GameStarted";
import AwaitingAnswersScreen from "@/components/game-phases/awaiting-answers/AwaitingAnswers";
import GameEndedScreen from "@/components/game-phases/game-ended/GameEnded";
import RoundEndedScreen from "@/components/game-phases/round-ended/RoundEnded";
import { useGame } from "../hooks/useGame";

export default function GameScreen() {
  const { gameState } = useGame();

  switch (gameState?.phase) {
    case undefined:
    case GamePhase.GAME_STARTED:
      return <GameStartedScreen />;

    case GamePhase.AWAITING_ANSWERS:
      return <AwaitingAnswersScreen gameState={gameState} />;

    case GamePhase.ROUND_ENDED:
      return <RoundEndedScreen gameState={gameState} />;

    case GamePhase.GAME_ENDED:
      return <GameEndedScreen gameState={gameState} />;
  }
}
