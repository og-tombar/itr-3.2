import { RoundEndedScreenProps } from "./types";
import socket from "@/shared/socket";
import styles from "./RoundEnded.module.css";

export default function RoundEndedScreen({ gameState }: RoundEndedScreenProps) {
  // Get current player's answer to check if they were correct
  const currentPlayerId = socket.id;
  const currentPlayer = currentPlayerId
    ? gameState.players[currentPlayerId]
    : null;
  const isCorrect =
    currentPlayer && currentPlayer.answer === gameState.correct_answer;

  // Get current player's standing
  const sortedPlayers = Object.entries(gameState.players).sort(
    ([, a], [, b]) => b.score - a.score
  );

  const currentPlayerStanding = currentPlayer
    ? sortedPlayers.findIndex(([playerId]) => playerId === currentPlayerId) + 1
    : null;

  // Answer button colors (same as AwaitingAnswers)
  const buttonColors = [
    "var(--accent-red)",
    "var(--accent-teal)",
    "var(--accent-yellow)",
    "var(--accent-green)",
  ];

  return (
    <div className={`container-fullscreen ${styles.container}`}>
      {/* Main Content */}
      <div className={styles.mainContent}>
        {/* Title */}
        <h1 className={styles.title}>Round Complete!</h1>

        {/* Current Player Standing */}
        {currentPlayerStanding && currentPlayer && (
          <div className={styles.standingContainer}>
            <div className={styles.standingDisplay}>
              <div className={styles.standingIcon}>
                {currentPlayerStanding === 1
                  ? "🥇"
                  : currentPlayerStanding === 2
                  ? "🥈"
                  : currentPlayerStanding === 3
                  ? "🥉"
                  : "🏅"}
              </div>
              <div className={styles.standingText}>
                <div className={styles.standingPosition}>
                  {currentPlayerStanding === 1
                    ? "1st Place!"
                    : currentPlayerStanding === 2
                    ? "2nd Place!"
                    : currentPlayerStanding === 3
                    ? "3rd Place!"
                    : `${currentPlayerStanding}th Place`}
                </div>
                <div className={styles.standingScore}>
                  {currentPlayer.score} points
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Answer Feedback */}
        <div className={styles.answerSection}>
          <div
            className={styles.feedbackContainer}
            style={{
              background: isCorrect
                ? "linear-gradient(135deg, var(--accent-green), #d4edda)"
                : "linear-gradient(135deg, var(--accent-red), #f8d7da)",
            }}
          >
            <div className={styles.feedbackText}>
              {isCorrect ? "Correct!" : "Incorrect"}
            </div>
          </div>

          {!isCorrect && (
            <div className={styles.correctAnswerLabel}>Correct Answer:</div>
          )}
          <div
            className={styles.correctAnswerButton}
            style={{
              backgroundColor: buttonColors[gameState.correct_answer],
              color:
                gameState.correct_answer === 2
                  ? "var(--dark-gray)"
                  : "var(--white)",
            }}
          >
            <span className={styles.answerText}>
              {gameState.question_options[gameState.correct_answer]}
            </span>
          </div>
        </div>
      </div>

      {/* Decorative Elements */}
      <div className="decorative-elements">
        <div className="bubble bubble-1"></div>
        <div className="bubble bubble-2"></div>
        <div className="bubble bubble-3"></div>
      </div>
    </div>
  );
}
