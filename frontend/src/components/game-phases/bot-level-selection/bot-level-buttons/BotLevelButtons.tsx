import useBotLevelButtons from "./useBotLevelButtons";
import styles from "./BotLevelButtons.module.css";
import { BotLevelButtonsProps } from "./types";
import Image from "next/image";

interface BotLevel {
  level: string;
  label: string;
  color: string;
  imagePath: string;
}

export default function BotLevelButtons({}: BotLevelButtonsProps) {
  const { selectedLevel, handleLevelClick } = useBotLevelButtons();

  const botLevels: BotLevel[] = [
    {
      level: "novice",
      label: "Novice",
      color: "var(--accent-teal)",
      imagePath: "/images/bot-levels/novice.png",
    },
    {
      level: "intermediate",
      label: "Intermediate",
      color: "var(--accent-yellow)",
      imagePath: "/images/bot-levels/intermediate.png",
    },
    {
      level: "expert",
      label: "Expert",
      color: "var(--accent-red)",
      imagePath: "/images/bot-levels/expert.png",
    },
  ];

  const renderBotLevelOption = (botLevel: BotLevel) => {
    const isSelected = selectedLevel === botLevel.level;

    return (
      <div
        key={botLevel.level}
        className={`${styles.botLevelOption} ${
          isSelected ? styles.selected : ""
        }`}
        onClick={() =>
          selectedLevel === null && handleLevelClick(botLevel.level)
        }
      >
        <div className={styles.imageContainer}>
          <Image
            src={botLevel.imagePath}
            alt={botLevel.label}
            className={styles.botImage}
            width={300}
            height={300}
          />
          {isSelected && <div className={styles.selectedOverlay} />}
        </div>
        <div
          className={styles.labelContainer}
          style={{ backgroundColor: botLevel.color }}
        >
          <span className={styles.levelLabel}>{botLevel.label}</span>
        </div>
      </div>
    );
  };

  return (
    <div className={styles.botLevelsContainer}>
      <div className={styles.optionsRow}>
        {botLevels.map((botLevel) => renderBotLevelOption(botLevel))}
      </div>
    </div>
  );
}
