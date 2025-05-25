export interface NewPlayer {
  name: string;
}

export interface LobbyUpdate {
  players: string[];
  time_remaining: number;
  should_start_game: boolean;
}

export interface NewGame {
  id: string;
}
