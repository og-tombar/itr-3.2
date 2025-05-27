export enum GamePhase {
  GAME_STARTED = "game_started",
  BOT_LEVEL_SELECTION = "bot_level_selection",
  CATEGORY_SELECTION = "category_selection",
  CATEGORY_RESULTS = "category_results",
  AWAITING_ANSWERS = "awaiting_answers",
  ROUND_ENDED = "round_ended",
  GAME_ENDED = "game_ended",
}

export enum PowerUp {
  FIFTY_FIFTY = "fifty_fifty",
  CALL_FRIEND = "call_friend",
  DOUBLE_POINTS = "double_points",
}

export interface Player {
  sid: string;
  name: string;
  score: number;
  answer: number;
  visible_options: boolean[];
  used_powerups: string[];
  double_points: boolean;
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
