// Client event types
export interface NewPlayer {
  name: string;
}

// Server event types
export interface PlayerInfo {
  id: string;
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
