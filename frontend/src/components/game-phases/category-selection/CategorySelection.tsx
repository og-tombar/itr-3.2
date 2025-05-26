import Countdown from "@/components/countdown/Countdown";
import CategoryButtons from "./category-buttons/CategoryButtons";
import { CategorySelectionScreenProps } from "./types";
import styles from "./CategorySelection.module.css";

export default function CategorySelectionScreen({
  gameState,
}: CategorySelectionScreenProps) {
  return (
    <div className={`container-fullscreen ${styles.container}`}>
      {/* Countdown Timer */}
      <div className={styles.countdownTimer}>
        <Countdown timeRemaining={gameState.time_remaining} />
      </div>

      {/* Main Content */}
      <div className={styles.mainContent}>
        {/* Heading */}
        <div className={styles.headingContainer}>
          <h1 className={styles.heading}>Select Category</h1>
        </div>

        {/* Category Buttons */}
        <CategoryButtons onCategorySelect={() => {}} selectedCategory={null} />
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
