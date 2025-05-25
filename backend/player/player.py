"""Player class."""

from dataclasses import dataclass


@dataclass
class Player:
    """A player in the game."""
    sid: str
    name: str
    room: str = ""
    score: int = 0
    answer: int = -1
