import Countdown from "@/components/countdown/Countdown";
import QuestionDisplay from "./question-display/QuestionDisplay";
import AnswerButtons from "./answer-buttons/AnswerButtons";
import PowerupButtons from "./powerup-buttons/PowerupButtons";
import { AwaitingAnswersScreenProps } from "./types";
import styles from "./AwaitingAnswers.module.css";
import socket from "@/shared/socket";

export default function AwaitingAnswersScreen({
  gameState,
}: AwaitingAnswersScreenProps) {
  // Get current player
  const currentPlayer = socket.id ? gameState.players[socket.id] : null;

  return (
    <div className={`container-fullscreen ${styles.container}`}>
      {/* Countdown Timer */}
      <div className={styles.countdownTimer}>
        <Countdown timeRemaining={gameState.time_remaining} />
      </div>

      {/* Powerup Buttons */}
      <PowerupButtons currentPlayer={currentPlayer} />

      {/* Main Content */}
      <div className={styles.mainContent}>
        {/* Question Display */}
        <QuestionDisplay questionText={gameState.question_text} />

        {/* Answer Buttons */}
        <AnswerButtons
          options={gameState.question_options}
          currentPlayer={currentPlayer}
        />
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
