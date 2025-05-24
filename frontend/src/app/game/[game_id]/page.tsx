"use client";

import { GamePhase } from "../types";
import GameStartedScreen from "@/components/game-phases/game-started/GameStarted";
import AwaitingAnswersScreen from "@/components/game-phases/awaiting-answers/AwaitingAnswers";
import GameEndedScreen from "@/components/game-phases/game-ended/GameEnded";
import GameExitScreen from "@/components/game-phases/game-exit/GameExit";
import RoundEndedScreen from "@/components/game-phases/round-ended/RoundEnded";
import { useGame } from "../hooks/useGame";

export default function GameScreen() {
  const { gameState } = useGame();
  if (!gameState) {
    return <GameStartedScreen />;
  }

  switch (gameState.phase) {
    case GamePhase.GAME_STARTED:
      return <GameStartedScreen />;

    case GamePhase.AWAITING_ANSWERS:
      return <AwaitingAnswersScreen gameState={gameState} />;

    case GamePhase.ROUND_ENDED:
      return <RoundEndedScreen gameState={gameState} />;

    case GamePhase.GAME_ENDED:
      return <GameEndedScreen gameState={gameState} />;

    case GamePhase.GAME_EXIT:
      return <GameExitScreen gameState={gameState} />;
  }
}
