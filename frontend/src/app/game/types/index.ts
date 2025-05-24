export interface GameUpdate {
  id: string;
  current_state: string;
  scores: Record<string, number>;
  question_text: string;
  question_options: string[];
  answers: Record<string, number>;
  time_remaining: number;
}
