import { GameUpdate, GamePhase } from "../types";
import GameStartedPhase from "./phases/GameStartedPhase";
import AwaitingAnswersPhase from "./phases/AwaitingAnswersPhase";
import RoundEndedPhase from "./phases/RoundEndedPhase";
import GameEndedPhase from "./phases/GameEndedPhase";
import GameExitPhase from "./phases/GameExitPhase";

interface GamePhaseRendererProps {
  gameState: GameUpdate;
  onAnswerClick?: (optionIndex: number) => void;
}

export default function GamePhaseRenderer({
  gameState,
  onAnswerClick,
}: GamePhaseRendererProps) {
  switch (gameState.phase) {
    case GamePhase.GAME_STARTED:
      return <GameStartedPhase gameState={gameState} />;

    case GamePhase.AWAITING_ANSWERS:
      return (
        <AwaitingAnswersPhase
          gameState={gameState}
          onAnswerClick={onAnswerClick}
        />
      );

    case GamePhase.ROUND_ENDED:
      return <RoundEndedPhase gameState={gameState} />;

    case GamePhase.GAME_ENDED:
      return <GameEndedPhase gameState={gameState} />;

    case GamePhase.GAME_EXIT:
      return <GameExitPhase gameState={gameState} />;

    default:
      // Fallback for unknown phases
      return (
        <div className="container-fullscreen">
          <div
            className="card card-large text-center"
            style={{ position: "relative", zIndex: 10 }}
          >
            <h1 className="title-large" style={{ color: "var(--accent-red)" }}>
              ❓ Unknown Game Phase
            </h1>
            <div
              className="badge badge-warning"
              style={{
                fontSize: "1.2rem",
                padding: "var(--space-sm) var(--space-lg)",
                marginBottom: "var(--space-lg)",
              }}
            >
              {gameState.phase}
            </div>
            <div className="info-panel">
              <p className="text-body">
                Current phase: <strong>{gameState.phase}</strong>
              </p>
              <p className="text-body">
                Game ID: <strong>{gameState.id}</strong>
              </p>
            </div>
          </div>
          <div className="decorative-elements">
            <div className="bubble bubble-1"></div>
            <div className="bubble bubble-2"></div>
            <div className="bubble bubble-3"></div>
          </div>
        </div>
      );
  }
}
