"""Player class."""

from dataclasses import dataclass

from questions.models import Category


@dataclass
class Player:
    """A player in the game."""
    sid: str
    name: str
    room: str = ""
    score: int = 0
    selected_category: Category | None = None
    answer: int = -1
