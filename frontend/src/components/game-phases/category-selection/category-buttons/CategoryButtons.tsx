import useCategoryButtons from "./useCategoryButtons";
import styles from "./CategoryButtons.module.css";
import { CategoryButtonsProps } from "./types";

export default function CategoryButtons({}: CategoryButtonsProps) {
  const { selectedCategory, handleCategoryClick } = useCategoryButtons();

  const categories = {
    row1: ["All", "Random", "General Knowledge"],
    row2: ["Art", "Board Games", "Books", "Film"],
    row3: ["Music", "Musicals & Theatres", "Television", "Video Games"],
    row4: ["Geography", "History", "Mythology", "Politics"],
    row5: ["Science & Nature", "Computers", "Mathematics", "Sports"],
  };

  const buttonColors = [
    "var(--accent-red)",
    "var(--accent-teal)",
    "var(--accent-yellow)",
    "var(--accent-green)",
    "var(--accent-orange)",
    "var(--primary-purple)",
    "var(--primary-pink)",
  ];

  const renderCategoryButton = (category: string, index: number) => {
    const isSelected = selectedCategory === category;
    const colorIndex = index % buttonColors.length;
    const buttonColor = buttonColors[colorIndex];

    return (
      <button
        key={index}
        onClick={() => handleCategoryClick(category)}
        className={`${styles.categoryButton} ${
          isSelected ? styles.selected : ""
        }`}
        disabled={selectedCategory !== null}
        style={{
          backgroundColor: isSelected ? "var(--accent-green)" : buttonColor,
          borderColor: isSelected ? "var(--accent-green)" : "var(--white)",
        }}
      >
        <span className={styles.buttonText}>{category}</span>
      </button>
    );
  };

  return (
    <div className={styles.categoriesContainer}>
      {/* First row - 3 buttons */}
      <div className={`${styles.buttonRow} ${styles.firstRow}`}>
        {categories.row1.map((category, index) =>
          renderCategoryButton(category, index)
        )}
      </div>

      {/* Second row - 4 buttons */}
      <div className={styles.buttonRow}>
        {categories.row2.map((category, index) =>
          renderCategoryButton(category, index + 3)
        )}
      </div>

      {/* Third row - 4 buttons */}
      <div className={styles.buttonRow}>
        {categories.row3.map((category, index) =>
          renderCategoryButton(category, index + 7)
        )}
      </div>

      {/* Fourth row - 4 buttons */}
      <div className={styles.buttonRow}>
        {categories.row4.map((category, index) =>
          renderCategoryButton(category, index + 11)
        )}
      </div>

      {/* Fifth row - 4 buttons */}
      <div className={styles.buttonRow}>
        {categories.row5.map((category, index) =>
          renderCategoryButton(category, index + 15)
        )}
      </div>
    </div>
  );
}
