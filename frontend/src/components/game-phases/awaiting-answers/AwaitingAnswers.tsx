import { GameUpdate } from "@/app/game/types";
import Countdown from "@/components/countdown/Countdown";
import QuestionDisplay from "./question-display/QuestionDisplay";
import AnswerButtons from "./answer-buttons/AnswerButtons";
import styles from "./AwaitingAnswers.module.css";

interface AwaitingAnswersScreenProps {
  gameState: GameUpdate;
  onAnswerClick?: (optionIndex: number) => void;
}

export default function AwaitingAnswersScreen({
  gameState,
  onAnswerClick,
}: AwaitingAnswersScreenProps) {
  const handleAnswerClick = (optionIndex: number) => {
    if (onAnswerClick) {
      onAnswerClick(optionIndex);
    } else {
      console.log(`Answer ${optionIndex} clicked`);
    }
  };

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
        <AnswerButtons
          options={gameState.question_options}
          onAnswerClick={handleAnswerClick}
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
