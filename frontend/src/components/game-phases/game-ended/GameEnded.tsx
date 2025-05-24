import { GameUpdate } from "@/app/game/types";

interface GameEndedScreenProps {
  gameState: GameUpdate;
}

export default function GameEndedScreen({ gameState }: GameEndedScreenProps) {
  const sortedScores = Object.entries(gameState.scores).sort(
    ([, a], [, b]) => b - a
  );
  const winner = sortedScores[0];

  return (
    <div className="container-fullscreen">
      <div
        className="card card-large text-center"
        style={{ position: "relative", zIndex: 10, maxWidth: "900px" }}
      >
        <h1
          className="title-main animate-bounce"
          style={{
            color: "var(--accent-green)",
            textShadow:
              "3px 3px 0 var(--accent-yellow), 6px 6px 0 var(--accent-red)",
            fontSize: "3.5rem",
          }}
        >
          🎉 Game Over! 🎉
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

        {winner && (
          <div
            className="info-panel-highlight animate-pulse"
            style={{
              background:
                "linear-gradient(135deg, var(--accent-yellow), #fff3cd)",
              border: "3px solid var(--accent-yellow)",
              marginBottom: "var(--space-xl)",
            }}
          >
            <h2
              className="title-medium"
              style={{
                color: "var(--dark-gray)",
                marginBottom: "var(--space-sm)",
              }}
            >
              🏆 Winner: {winner[0]} 🏆
            </h2>
            <div
              className="text-body"
              style={{
                fontSize: "1.5rem",
                fontWeight: "bold",
                color: "var(--dark-gray)",
              }}
            >
              Final Score: {winner[1]} points
            </div>
          </div>
        )}

        <div style={{ marginBottom: "var(--space-lg)" }}>
          <h3 className="title-medium">🏅 Final Leaderboard</h3>
          <div className="info-panel">
            {sortedScores.length > 0 ? (
              sortedScores.map(([player, score], index) => (
                <div
                  key={player}
                  className="flex-between"
                  style={{
                    padding: "var(--space-md) 0",
                    borderBottom:
                      index < sortedScores.length - 1
                        ? "2px solid var(--light-gray)"
                        : "none",
                    fontSize: "1.2rem",
                  }}
                >
                  <span
                    style={{
                      fontWeight: "bold",
                      color:
                        index === 0
                          ? "var(--accent-yellow)"
                          : index === 1
                          ? "var(--medium-gray)"
                          : index === 2
                          ? "#cd7f32"
                          : "var(--dark-gray)",
                    }}
                  >
                    {index === 0
                      ? "🥇 "
                      : index === 1
                      ? "🥈 "
                      : index === 2
                      ? "🥉 "
                      : `${index + 1}. `}
                    {player}
                  </span>
                  <span
                    className="badge badge-primary"
                    style={{
                      fontSize: "1.3rem",
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
            🎮 Thanks for playing! Game ID:{" "}
            <strong style={{ color: "var(--primary-purple)" }}>
              {gameState.id}
            </strong>
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
