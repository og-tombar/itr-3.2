export enum GamePhase {
  GAME_STARTED = "game_started",
  CATEGORY_SELECTION = "category_selection",
  CATEGORY_RESULTS = "category_results",
  AWAITING_ANSWERS = "awaiting_answers",
  ROUND_ENDED = "round_ended",
  GAME_ENDED = "game_ended",
}

export interface Player {
  sid: string;
  name: string;
  score: number;
  answer: number;
}

export interface GameUpdate {
  id: string;
  category: string;
  phase: string;
  players: Record<string, Player>;
  question_text: string;
  question_options: string[];
  correct_answer: number;
  time_remaining: number;
}
