import { GameUpdate } from "../../types";

interface AwaitingAnswersPhaseProps {
  gameState: GameUpdate;
  onAnswerClick?: (optionIndex: number) => void;
}

export default function AwaitingAnswersPhase({
  gameState,
  onAnswerClick,
}: AwaitingAnswersPhaseProps) {
  const handleAnswerClick = (optionIndex: number) => {
    if (onAnswerClick) {
      onAnswerClick(optionIndex);
    } else {
      console.log(`Answer ${optionIndex} clicked`);
    }
  };

  return (
    <div className="container-split">
      {/* Answer Options Section */}
      <div
        className="flex-column"
        style={{ flex: 1, position: "relative", zIndex: 10 }}
      >
        <h2
          className="title-medium"
          style={{
            color: "var(--white)",
            textShadow: "2px 2px 0 var(--accent-red)",
          }}
        >
          🎯 Answer Options
        </h2>
        <div className="grid-2x2">
          {gameState.question_options.slice(0, 4).map((option, index) => (
            <button
              key={index}
              onClick={() => handleAnswerClick(index)}
              className="btn btn-large"
              style={{
                backgroundColor: [
                  "var(--accent-red)",
                  "var(--accent-teal)",
                  "var(--accent-yellow)",
                  "var(--accent-green)",
                ][index],
                color: index === 2 ? "var(--dark-gray)" : "var(--white)", // Yellow needs dark text
                minHeight: "100px",
                fontSize: "1.2rem",
                padding: "var(--space-lg)",
                border: "3px solid var(--white)",
                borderRadius: "var(--radius-lg)",
              }}
            >
              <span style={{ fontWeight: "bold" }}>
                {String.fromCharCode(65 + index)}. {option}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Game Information Section */}
      <div
        className="container-content"
        style={{ flex: 1, position: "relative", zIndex: 10 }}
      >
        <h2 className="title-medium">📊 Game Information</h2>

        <div className="flex-column">
          <div className="info-panel">
            <strong>Game ID:</strong>
            <span className="badge badge-primary">{gameState.id}</span>
          </div>

          <div className="info-panel">
            <strong>Phase:</strong>
            <span className="badge badge-success">{gameState.phase}</span>
          </div>

          <div className="info-panel">
            <strong>⏰ Time Remaining:</strong>
            <span
              className={`badge ${
                gameState.time_remaining < 10 ? "badge-danger" : "badge-success"
              }`}
              style={{ fontSize: "1.2rem", marginLeft: "var(--space-sm)" }}
            >
              {gameState.time_remaining}s
            </span>
          </div>

          <div className="info-panel-highlight">
            <strong className="title-small">❓ Question:</strong>
            <div
              className="text-body"
              style={{
                fontStyle: "italic",
                marginTop: "var(--space-sm)",
                color: "var(--primary-purple)",
                fontWeight: "600",
              }}
            >
              {gameState.question_text}
            </div>
          </div>

          <div className="info-panel">
            <strong className="title-small">🏆 Scores:</strong>
            <div style={{ marginTop: "var(--space-sm)" }}>
              {Object.keys(gameState.scores).length > 0 ? (
                Object.entries(gameState.scores).map(([player, score]) => (
                  <div
                    key={player}
                    className="flex-between"
                    style={{ padding: "var(--space-xs) 0" }}
                  >
                    <span className="text-body">{player}:</span>
                    <span className="badge badge-primary">{score}</span>
                  </div>
                ))
              ) : (
                <em className="text-small">No scores yet</em>
              )}
            </div>
          </div>

          <div className="info-panel">
            <strong className="title-small">✅ Current Answers:</strong>
            <div style={{ marginTop: "var(--space-sm)" }}>
              {Object.keys(gameState.answers).length > 0 ? (
                Object.entries(gameState.answers).map(
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
                          20
                        )}
                        {gameState.question_options[answerIndex]?.length > 20
                          ? "..."
                          : ""}
                      </span>
                    </div>
                  )
                )
              ) : (
                <em className="text-small">No answers submitted yet</em>
              )}
            </div>
          </div>
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
