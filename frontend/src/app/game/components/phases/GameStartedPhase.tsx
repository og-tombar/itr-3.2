import { GameUpdate } from "../../types";

interface GameStartedPhaseProps {
  gameState: GameUpdate;
}

export default function GameStartedPhase({ gameState }: GameStartedPhaseProps) {
  return (
    <div className="container-fullscreen">
      <div
        className="card card-large text-center"
        style={{ position: "relative", zIndex: 10 }}
      >
        <h1
          className="title-main animate-bounce"
          style={{
            color: "var(--accent-red)",
            textShadow:
              "3px 3px 0 var(--accent-teal), 6px 6px 0 var(--accent-yellow)",
            marginBottom: "var(--space-xl)",
          }}
        >
          Get Ready!
        </h1>

        <div
          className="badge badge-primary"
          style={{
            fontSize: "1.2rem",
            padding: "var(--space-sm) var(--space-lg)",
            marginBottom: "var(--space-xl)",
          }}
        >
          {gameState.phase}
        </div>

        <div className="text-body" style={{ marginBottom: "var(--space-lg)" }}>
          <p style={{ fontSize: "1.3rem", marginBottom: "var(--space-md)" }}>
            The game is about to begin...
          </p>
          <p className="text-small">
            Game ID:{" "}
            <strong style={{ color: "var(--primary-purple)" }}>
              {gameState.id}
            </strong>
          </p>
        </div>

        {gameState.time_remaining > 0 && (
          <div className="info-panel-highlight animate-pulse text-center">
            <span
              style={{
                fontSize: "2rem",
                fontWeight: "bold",
                color: "var(--accent-green)",
              }}
            >
              Starting in: {gameState.time_remaining}s
            </span>
          </div>
        )}
      </div>

      <div className="decorative-elements">
        <div className="bubble bubble-1"></div>
        <div className="bubble bubble-2"></div>
        <div className="bubble bubble-3"></div>
      </div>
    </div>
  );
}
