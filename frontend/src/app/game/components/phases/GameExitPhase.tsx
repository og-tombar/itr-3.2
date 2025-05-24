import { GameUpdate } from "../../types";

interface GameExitPhaseProps {
  gameState: GameUpdate;
}

export default function GameExitPhase({ gameState }: GameExitPhaseProps) {
  return (
    <div className="container-fullscreen">
      <div
        className="card card-large text-center"
        style={{ position: "relative", zIndex: 10, maxWidth: "700px" }}
      >
        <h1
          className="title-large"
          style={{
            color: "var(--medium-gray)",
            textShadow: "2px 2px 0 var(--light-gray)",
          }}
        >
          👋 Game Session Ended
        </h1>

        <div
          className="badge badge-warning"
          style={{
            fontSize: "1.2rem",
            padding: "var(--space-sm) var(--space-lg)",
            marginBottom: "var(--space-xl)",
          }}
        >
          {gameState.phase}
        </div>

        <div
          className="info-panel"
          style={{
            backgroundColor: "#f8d7da",
            border: "2px solid var(--accent-red)",
            marginBottom: "var(--space-lg)",
          }}
        >
          <p
            className="text-body"
            style={{
              margin: 0,
              color: "#721c24",
              fontWeight: "600",
            }}
          >
            ⚠️ The game has been terminated or you have left the session.
          </p>
        </div>

        <div
          className="flex-column"
          style={{ textAlign: "left", marginBottom: "var(--space-lg)" }}
        >
          <div className="info-panel">
            <strong>Game ID:</strong>
            <span className="badge badge-primary">{gameState.id}</span>
          </div>

          {Object.keys(gameState.scores).length > 0 && (
            <div className="info-panel">
              <strong className="title-small">🏆 Final Scores:</strong>
              <div style={{ marginTop: "var(--space-sm)" }}>
                {Object.entries(gameState.scores)
                  .sort(([, a], [, b]) => b - a)
                  .map(([player, score]) => (
                    <div
                      key={player}
                      className="flex-between"
                      style={{ padding: "var(--space-xs) 0" }}
                    >
                      <span className="text-body">{player}:</span>
                      <span className="badge badge-primary">{score}</span>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>

        <div
          className="info-panel"
          style={{
            background: "linear-gradient(135deg, var(--accent-teal), #d1ecf1)",
            border: "2px solid var(--accent-teal)",
          }}
        >
          <p
            className="text-body"
            style={{
              margin: 0,
              color: "var(--dark-gray)",
              fontWeight: "600",
            }}
          >
            💜 Thanks for participating! You can close this window or navigate
            back to the main page.
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
