export enum ClientEvent {
  NEW_PLAYER = "new_player",
  JOIN_GAME = "join_game",
  SUBMIT_ANSWER = "submit_answer",
  MESSAGE = "client_message",
  DISCONNECT = "disconnect",
}

export enum ServerEvent {
  LOBBY_UPDATE = "lobby_update",
  NEW_GAME = "new_game",
  GAME_UPDATE = "game_update",
  MESSAGE = "server_message",
}
