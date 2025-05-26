"""Models for the game."""

from dataclasses import dataclass
from enum import Enum
from typing import Callable


class GamePhase(str, Enum):
    """The phase of a game."""
    GAME_STARTED = "game_started"
    AWAITING_ANSWERS = "awaiting_answers"
    ROUND_ENDED = "round_ended"
    GAME_ENDED = "game_ended"

    def get_duration(self) -> int:
        """Gets the duration of a phase.

        Returns:
            int: The duration of the phase.
        """
        match self:
            case GamePhase.GAME_STARTED: return 3
            case GamePhase.AWAITING_ANSWERS: return 20
            case GamePhase.ROUND_ENDED: return 3
            case GamePhase.GAME_ENDED: return 5
            case _: return 0


@dataclass
class Phase:
    """The data for a game phase."""
    title: GamePhase
    time_remaining: int = 0
    setup: Callable[[], None] = lambda: None
    teardown: Callable[[], None] = lambda: None
    should_stop: Callable[[], bool] = lambda: False


@dataclass
class Question:
    """The data for a question. Includes the correct answer (do not send to clients)."""
    id: str
    text: str
    options: list[str]
    correct_index: int
