import styles from "./AnswerButtons.module.css";

interface AnswerButtonsProps {
  options: string[];
  onAnswerClick: (optionIndex: number) => void;
}

export default function AnswerButtons({
  options,
  onAnswerClick,
}: AnswerButtonsProps) {
  const buttonColors = [
    "var(--accent-red)",
    "var(--accent-teal)",
    "var(--accent-yellow)",
    "var(--accent-green)",
  ];

  return (
    <div className={styles.answersContainer}>
      <div className={styles.buttonGrid}>
        {options.slice(0, 4).map((option, index) => (
          <button
            key={index}
            onClick={() => onAnswerClick(index)}
            className={styles.answerButton}
            style={{
              backgroundColor: buttonColors[index],
              color: index === 2 ? "var(--dark-gray)" : "var(--white)", // Yellow needs dark text
            }}
          >
            <span className={styles.buttonText}>
              {String.fromCharCode(65 + index)}. {option}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
