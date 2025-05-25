export enum ClientEvent {
  JOIN_LOBBY = "join_lobby",
  JOIN_GAME = "join_game",
  MESSAGE = "client_message",
}

export enum ServerEvent {
  LOBBY_UPDATE = "lobby_update",
  NEW_GAME = "new_game",
  GAME_UPDATE = "game_update",
  MESSAGE = "server_message",
}
