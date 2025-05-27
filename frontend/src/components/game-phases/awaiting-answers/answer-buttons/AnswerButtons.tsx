import useAnswerButtons from "./useAnswerButtons";
import styles from "./AnswerButtons.module.css";
import { AnswerButtonsProps } from "./types";

export default function AnswerButtons({
  options,
  currentPlayer,
}: AnswerButtonsProps) {
  const { buttonColors, answer, handleAnswerClick, didAnswer } =
    useAnswerButtons();

  return (
    <div className={styles.answersContainer}>
      <div className={styles.buttonGrid}>
        {options.slice(0, 4).map((option, index) => {
          const isSelected = answer === index;
          const isUnselected = didAnswer() && !isSelected;
          const isVisible = currentPlayer
            ? currentPlayer.visible_options[index]
            : true;

          // Don't render the button if it's not visible (fifty-fifty powerup)
          if (!isVisible) {
            return (
              <div key={index} className={styles.hiddenButton}>
                {/* Empty space to maintain grid layout */}
              </div>
            );
          }

          return (
            <button
              key={index}
              onClick={() => handleAnswerClick(index)}
              className={styles.answerButton}
              disabled={didAnswer()}
              style={{
                backgroundColor: buttonColors[index],
                color: index === 2 ? "var(--dark-gray)" : "var(--white)",
                opacity: isUnselected ? 0.4 : 1,
                cursor: didAnswer() ? "not-allowed" : "pointer",
                transform: isUnselected ? "none" : undefined,
              }}
            >
              <span className={styles.buttonText}>{option}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
