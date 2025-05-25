import Countdown from "@/components/countdown/Countdown";
import QuestionDisplay from "./question-display/QuestionDisplay";
import AnswerButtons from "./answer-buttons/AnswerButtons";
import { AwaitingAnswersScreenProps } from "./types";
import styles from "./AwaitingAnswers.module.css";

export default function AwaitingAnswersScreen({
  gameState,
}: AwaitingAnswersScreenProps) {
  return (
    <div className={`container-fullscreen ${styles.container}`}>
      {/* Countdown Timer */}
      <div className={styles.countdownTimer}>
        <Countdown timeRemaining={gameState.time_remaining} />
      </div>

      {/* Main Content */}
      <div className={styles.mainContent}>
        {/* Question Display */}
        <QuestionDisplay questionText={gameState.question_text} />

        {/* Answer Buttons */}
        <AnswerButtons options={gameState.question_options} />
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
