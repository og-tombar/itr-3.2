"""Player management service."""

from player.player import Player


class PlayerManager:
    """Manages the players in the game."""

    def __init__(self):
        self._players = {}

    def add_player(self, sid: str, name: str) -> Player:
        """Adds a player to the manager.

        Args:
            sid (str): The socket id of the player.
            name (str): The name of the player.

        Returns:
            Player: The player object.
        """
        p = Player(sid, name)
        self._players[sid] = p
        return p

    def get_player(self, sid: str) -> Player:
        """Gets a player from the manager.

        Args:
            sid (str): The socket id of the player.

        Returns:
            Player: The player object.
        """
        return self._players.get(sid)

    def remove_player(self, sid: str) -> None:
        """Removes a player from the manager.

        Args:
            sid (str): The socket id of the player.
        """
        self._players.pop(sid, None)
