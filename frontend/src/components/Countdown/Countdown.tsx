import styles from "./Countdown.module.css";

export default function Countdown({
  timeRemaining,
}: {
  timeRemaining: number | undefined;
}) {
  return (
    <div className={styles.countdownContainer}>
      <span className={styles.countdownText}>{timeRemaining}</span>
    </div>
  );
}
