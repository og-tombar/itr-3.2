export enum GamePhase {
  GAME_STARTED = "game_started",
  AWAITING_ANSWERS = "awaiting_answers",
  ROUND_ENDED = "round_ended",
  GAME_ENDED = "game_ended",
  GAME_EXIT = "game_exit",
}

export interface GameUpdate {
  id: string;
  phase: string;
  scores: Record<string, number>;
  question_text: string;
  question_options: string[];
  answers: Record<string, number>;
  time_remaining: number;
}
