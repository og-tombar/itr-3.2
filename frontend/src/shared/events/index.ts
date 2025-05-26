export enum ClientEvent {
  GET_PLAYER = "get_player",
  NEW_PLAYER = "new_player",
  JOIN_LOBBY = "join_lobby",
  JOIN_GAME = "join_game",
  SET_BOT_LEVEL = "set_bot_level",
  SELECT_CATEGORY = "select_category",
  SUBMIT_ANSWER = "submit_answer",
  MESSAGE = "client_message",
  DISCONNECT = "disconnect",
}

export enum ServerEvent {
  PLAYER_INFO = "player_info",
  PLAYER_REGISTERED = "player_registered",
  LOBBY_UPDATE = "lobby_update",
  NEW_GAME = "new_game",
  GAME_UPDATE = "game_update",
  MESSAGE = "server_message",
}
