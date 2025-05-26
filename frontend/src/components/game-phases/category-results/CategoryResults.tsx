import { GameUpdate } from "@/app/game/types";
import styles from "./CategoryResults.module.css";

interface CategoryResultsScreenProps {
  gameState: GameUpdate;
}

export default function CategoryResultsScreen({
  gameState,
}: CategoryResultsScreenProps) {
  return (
    <div className="container-fullscreen">
      <h1 className={`title-large text-center ${styles.categorySelectedTitle}`}>
        Category Selected!
      </h1>
      <h2 className={`animate-bounce text-center ${styles.categoryName}`}>
        {gameState.category}
      </h2>
      <div className="decorative-elements">
        <div className="bubble bubble-1"></div>
        <div className="bubble bubble-2"></div>
        <div className="bubble bubble-3"></div>
      </div>
    </div>
  );
}
