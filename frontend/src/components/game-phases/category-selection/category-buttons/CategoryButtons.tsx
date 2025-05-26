import useCategoryButtons from "./useCategoryButtons";
import styles from "./CategoryButtons.module.css";
import { CategoryButtonsProps } from "./types";

export default function CategoryButtons({}: CategoryButtonsProps) {
  const { selectedCategory, handleCategoryClick } = useCategoryButtons();

  // Define all categories as they appear in the backend
  const categories = {
    // First row: Special categories + General Knowledge
    firstRow: ["All", "Random", "General Knowledge"],

    // Remaining 20 categories distributed across 4 rows of 5 each
    secondRow: ["Art", "Board Games", "Books"],
    thirdRow: ["Film", "Music", "Musicals & Theatres", "Television"],
    fourthRow: ["Video Games", "Geography", "History", "Mythology", "Politics"],
    fifthRow: ["Science & Nature", "Computers", "Mathematics", "Sports"],
  };

  const renderCategoryButton = (category: string, index: number) => {
    const isSelected = selectedCategory === category;

    return (
      <button
        key={index}
        onClick={() => handleCategoryClick(category)}
        className={`${styles.categoryButton} ${
          isSelected ? styles.selected : ""
        }`}
        disabled={selectedCategory !== null}
      >
        <span className={styles.buttonText}>{category}</span>
      </button>
    );
  };

  return (
    <div className={styles.categoriesContainer}>
      {/* First row - 3 buttons */}
      <div className={`${styles.buttonRow} ${styles.firstRow}`}>
        {categories.firstRow.map((category, index) =>
          renderCategoryButton(category, index)
        )}
      </div>

      {/* Second row - 5 buttons */}
      <div className={styles.buttonRow}>
        {categories.secondRow.map((category, index) =>
          renderCategoryButton(category, index + 3)
        )}
      </div>

      {/* Third row - 5 buttons */}
      <div className={styles.buttonRow}>
        {categories.thirdRow.map((category, index) =>
          renderCategoryButton(category, index + 8)
        )}
      </div>

      {/* Fourth row - 5 buttons */}
      <div className={styles.buttonRow}>
        {categories.fourthRow.map((category, index) =>
          renderCategoryButton(category, index + 13)
        )}
      </div>

      {/* Fifth row - 5 buttons */}
      <div className={styles.buttonRow}>
        {categories.fifthRow.map((category, index) =>
          renderCategoryButton(category, index + 18)
        )}
      </div>
    </div>
  );
}
