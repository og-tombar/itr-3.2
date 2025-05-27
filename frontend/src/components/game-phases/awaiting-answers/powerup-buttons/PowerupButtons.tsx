import { PowerupButtonsProps } from "./types";
import usePowerupButtons from "./usePowerupButtons";
import styles from "./PowerupButtons.module.css";

export default function PowerupButtons({ currentPlayer }: PowerupButtonsProps) {
  const { handlePowerupClick } = usePowerupButtons();

  if (!currentPlayer) {
    return null;
  }

  const isPowerupUsed = (powerup: string) => {
    return currentPlayer.used_powerups.includes(powerup);
  };

  return (
    <div className={styles.powerupContainer}>
      {/* Fifty-Fifty Powerup */}
      <div className={styles.powerupButtonWrapper}>
        <button
          className={`${styles.powerupButton} ${
            isPowerupUsed("fifty_fifty") ? styles.disabled : ""
          }`}
          onClick={() => handlePowerupClick("fifty_fifty")}
          disabled={isPowerupUsed("fifty_fifty")}
          title="50/50 - Remove two incorrect answers"
        >
          <span className={styles.powerupText}>50/50</span>
        </button>
      </div>

      {/* Call a Friend Powerup */}
      <div className={styles.powerupButtonWrapper}>
        <button
          className={`${styles.powerupButton} ${
            isPowerupUsed("call_friend") ? styles.disabled : ""
          }`}
          onClick={() => handlePowerupClick("call_friend")}
          disabled={isPowerupUsed("call_friend")}
          title="Call a Friend - Get AI assistance"
        >
          <span className={styles.powerupEmoji}>💬</span>
        </button>
      </div>

      {/* Double Points Powerup */}
      <div className={styles.powerupButtonWrapper}>
        <button
          className={`${styles.powerupButton} ${
            isPowerupUsed("double_points") ? styles.disabled : ""
          }`}
          onClick={() => handlePowerupClick("double_points")}
          disabled={isPowerupUsed("double_points")}
          title="Double Points - Get 2x points for this round"
        >
          <span className={styles.powerupText}>x2</span>
        </button>
      </div>
    </div>
  );
}
