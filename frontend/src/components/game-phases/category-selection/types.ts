import { GameUpdate } from "@/app/game/types";

export interface CategorySelectionScreenProps {
  gameState: GameUpdate;
}

export interface CategoryButtonsProps {
  onCategorySelect: (category: string) => void;
  selectedCategory: string | null;
}
