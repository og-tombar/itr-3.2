import BotLevelButtons from "./bot-level-buttons/BotLevelButtons";
import styles from "./BotLevelSelection.module.css";

export default function BotLevelSelectionScreen() {
  return (
    <div className={`container-fullscreen ${styles.container}`}>
      {/* Main Content */}
      <div className={styles.mainContent}>
        {/* Heading */}
        <div className={styles.headingContainer}>
          <h1 className={styles.heading}>Select Bot Level</h1>
        </div>

        {/* Bot Level Buttons */}
        <BotLevelButtons onBotLevelSelect={() => {}} selectedLevel={null} />
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
