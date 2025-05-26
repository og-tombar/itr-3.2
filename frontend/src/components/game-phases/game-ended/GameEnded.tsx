import { GameUpdate } from "@/app/game/types";
import { useRouter } from "next/navigation";
import styles from "./GameEnded.module.css";

interface GameEndedScreenProps {
  gameState: GameUpdate;
}

export default function GameEndedScreen({ gameState }: GameEndedScreenProps) {
  const router = useRouter();
  const sortedScores = Object.entries(gameState.players).sort(
    ([, a], [, b]) => b.score - a.score
  );

  const handleBackToLobby = () => {
    router.push("/lobby");
  };

  return (
    <div className={`container-fullscreen ${styles.container}`}>
      <div className={styles.mainContent}>
        {/* Game Over Title */}
        <h1 className={styles.title}>Game Over</h1>

        {/* Leaderboard Table */}
        <div className={styles.leaderboardSection}>
          <div className={styles.leaderboardTable}>
            <div className={styles.tableHeader}>
              <div className={styles.headerRank}>Place</div>
              <div className={styles.headerName}>Player</div>
              <div className={styles.headerScore}>Score</div>
            </div>
            {sortedScores.length > 0 ? (
              sortedScores.slice(0, 3).map(([player, playerData], index) => (
                <div
                  key={player}
                  className={`${styles.tableRow} ${styles[`rank${index + 1}`]}`}
                >
                  <div className={styles.rankCell}>
                    <span className={styles.rankIcon}>
                      {index === 0 ? "🥇" : index === 1 ? "🥈" : "🥉"}
                    </span>
                  </div>
                  <div className={styles.nameCell}>{playerData.name}</div>
                  <div className={styles.scoreCell}>
                    <span className={styles.scoreValue}>
                      {playerData.score}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <div className={styles.noScores}>No scores available</div>
            )}
          </div>
        </div>

        {/* Back to Lobby Button */}
        <button className={styles.backButton} onClick={handleBackToLobby}>
          Back to Lobby
        </button>
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
