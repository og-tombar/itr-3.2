import { GameUpdate } from "@/app/game/types";

interface RoundEndedScreenProps {
  gameState: GameUpdate;
}

export default function RoundEndedScreen({ gameState }: RoundEndedScreenProps) {
  return (
    <div className="container-fullscreen">
      <div
        className="card card-large"
        style={{ position: "relative", zIndex: 10, maxWidth: "900px" }}
      >
        <h1
          className="title-large animate-pulse"
          style={{
            color: "var(--accent-green)",
            textShadow: "2px 2px 0 var(--accent-yellow)",
          }}
        >
          🎉 Round Complete! 🎉
        </h1>

        <div
          className="badge badge-success"
          style={{
            fontSize: "1.2rem",
            padding: "var(--space-sm) var(--space-lg)",
            marginBottom: "var(--space-xl)",
          }}
        >
          {gameState.phase}
        </div>

        {gameState.question_text && (
          <div
            className="info-panel-highlight"
            style={{ marginBottom: "var(--space-lg)" }}
          >
            <h3 className="title-small">❓ Question:</h3>
            <div
              className="text-body"
              style={{
                fontStyle: "italic",
                color: "var(--primary-purple)",
                fontWeight: "600",
              }}
            >
              {gameState.question_text}
            </div>
          </div>
        )}

        <div style={{ marginBottom: "var(--space-lg)" }}>
          <h3 className="title-medium">🏆 Current Scores:</h3>
          <div className="info-panel">
            {Object.keys(gameState.scores).length > 0 ? (
              Object.entries(gameState.scores)
                .sort(([, a], [, b]) => b - a) // Sort by score descending
                .map(([player, score], index) => (
                  <div
                    key={player}
                    className="flex-between"
                    style={{
                      padding: "var(--space-md) 0",
                      borderBottom:
                        index < Object.keys(gameState.scores).length - 1
                          ? "2px solid var(--light-gray)"
                          : "none",
                    }}
                  >
                    <span
                      style={{
                        fontSize: "1.3rem",
                        fontWeight: index === 0 ? "bold" : "normal",
                        color:
                          index === 0
                            ? "var(--accent-yellow)"
                            : "var(--dark-gray)",
                      }}
                    >
                      {index === 0 ? "🏆 " : `${index + 1}. `}
                      {player}
                    </span>
                    <span
                      className="badge badge-primary"
                      style={{
                        fontSize: "1.4rem",
                        padding: "var(--space-sm) var(--space-md)",
                      }}
                    >
                      {score} pts
                    </span>
                  </div>
                ))
            ) : (
              <em className="text-small">No scores available</em>
            )}
          </div>
        </div>

        {Object.keys(gameState.answers).length > 0 && (
          <div style={{ marginBottom: "var(--space-lg)" }}>
            <h3 className="title-small">✅ Player Answers:</h3>
            <div className="info-panel">
              {Object.entries(gameState.answers).map(
                ([player, answerIndex]) => (
                  <div
                    key={player}
                    className="flex-between"
                    style={{ padding: "var(--space-xs) 0" }}
                  >
                    <span className="text-body">{player}:</span>
                    <span className="badge badge-warning">
                      {String.fromCharCode(65 + answerIndex)}.{" "}
                      {gameState.question_options[answerIndex]?.substring(
                        0,
                        25
                      )}
                      {gameState.question_options[answerIndex]?.length > 25
                        ? "..."
                        : ""}
                    </span>
                  </div>
                )
              )}
            </div>
          </div>
        )}

        {gameState.time_remaining > 0 && (
          <div className="info-panel-highlight text-center animate-pulse">
            <span
              style={{
                fontSize: "1.5rem",
                fontWeight: "bold",
                color: "var(--accent-green)",
              }}
            >
              ⏱️ Next round starts in: {gameState.time_remaining}s
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
