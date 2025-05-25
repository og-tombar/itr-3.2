import styles from "./QuestionDisplay.module.css";

interface QuestionDisplayProps {
  questionText: string;
}

export default function QuestionDisplay({
  questionText,
}: QuestionDisplayProps) {
  return (
    <div className={styles.questionContainer}>
      <h1 className={styles.questionText}>{questionText}</h1>
    </div>
  );
}
