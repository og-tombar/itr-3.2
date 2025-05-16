"""Matchmaking module."""


class Lobby:
    """A simple in-memory lobby."""

    ROOM = 'lobby'

    def __init__(self):
        self.players = []

    def add_player(self, sid: str) -> None:
        """Adds a player to the lobby.

        Args:
            sid (str): The sid of the player to add.
        """
        if sid not in self.players:
            self.players.append(sid)

    def get_update(self) -> list[str]:
        """Gets the list of players in the lobby.

        Returns:
            list[str]: The list of player sids.
        """
        return self.players
