import { PowerUp } from "@/app/game/types";
import { PowerupButtonsProps } from "./types";
import usePowerupButtons from "./usePowerupButtons";
import styles from "./PowerupButtons.module.css";

export default function PowerupButtons({ currentPlayer }: PowerupButtonsProps) {
  const { handlePowerupClick } = usePowerupButtons();

  if (!currentPlayer) {
    return null;
  }

  const isPowerupUsed = (powerup: PowerUp) => {
    return currentPlayer.used_powerups.includes(powerup);
  };

  return (
    <div className={styles.powerupContainer}>
      {/* Fifty-Fifty Powerup */}
      <div className={styles.powerupButtonWrapper}>
        <button
          className={`${styles.powerupButton} ${styles.fiftyFiftyButton} ${
            isPowerupUsed(PowerUp.FIFTY_FIFTY) ? styles.disabled : ""
          }`}
          onClick={() => handlePowerupClick(PowerUp.FIFTY_FIFTY)}
          disabled={isPowerupUsed(PowerUp.FIFTY_FIFTY)}
        >
          <span className={styles.powerupText}>50/50</span>
        </button>
        <div className={styles.tooltip}>Remove two wrong answers</div>
      </div>

      {/* Call a Friend Powerup */}
      <div className={styles.powerupButtonWrapper}>
        <button
          className={`${styles.powerupButton} ${styles.callFriendButton} ${
            isPowerupUsed(PowerUp.CALL_FRIEND) ? styles.disabled : ""
          }`}
          onClick={() => handlePowerupClick(PowerUp.CALL_FRIEND)}
          disabled={isPowerupUsed(PowerUp.CALL_FRIEND)}
        >
          <span className={styles.powerupEmoji}>📞</span>
        </button>
        <div className={styles.tooltip}>Get help from a friend in chat</div>
      </div>

      {/* Double Points Powerup */}
      <div className={styles.powerupButtonWrapper}>
        <button
          className={`${styles.powerupButton} ${styles.doublePointsButton} ${
            isPowerupUsed(PowerUp.DOUBLE_POINTS) ? styles.disabled : ""
          }`}
          onClick={() => handlePowerupClick(PowerUp.DOUBLE_POINTS)}
          disabled={isPowerupUsed(PowerUp.DOUBLE_POINTS)}
        >
          <span className={styles.powerupText}>x2</span>
        </button>
        <div className={styles.tooltip}>Double round points</div>
      </div>
    </div>
  );
}
