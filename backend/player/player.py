"""Player class."""

import random
from dataclasses import dataclass, field
from enum import Enum

from questions.models import Category


class PlayerType(str, Enum):
    """The type of player."""
    HUMAN = "human"
    BOT = "bot"


class BotLevel(str, Enum):
    """The level of the bot."""
    NOVICE = "novice"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"

    def get_success_rate(self) -> float:
        """Gets the success rate for the bot level."""
        match self:
            case BotLevel.NOVICE: return 0.2
            case BotLevel.INTERMEDIATE: return 0.4
            case BotLevel.EXPERT: return 0.6

    def mock_round_points(self) -> int:
        """Mocks the points for a round.

        Returns:
            int: The points for a round.
        """
        success = random.random() < self.get_success_rate()
        if not success:
            return 0
        match self:
            case BotLevel.NOVICE:
                return random.randint(1, 20)
            case BotLevel.INTERMEDIATE:
                return random.randint(6, 25)
            case BotLevel.EXPERT:
                return random.randint(11, 30)


class PowerUp(str, Enum):
    """The power ups for the player."""
    FIFTY_FIFTY = "fifty_fifty"
    CALL_FRIEND = "call_friend"
    DOUBLE_POINTS = "double_points"


@dataclass
class Player:
    """A player in the game."""
    sid: str
    type: PlayerType = PlayerType.HUMAN
    level: BotLevel = BotLevel.NOVICE
    name: str = "Player"
    room: str = ""
    score: int = 0
    selected_category: Category | None = None
    answer: int = -1
    visible_options: list[bool] = field(
        default_factory=lambda: [True, True, True, True])
    used_powerups: list[PowerUp] = field(default_factory=list)
    double_points: bool = False

    def total_reset(self) -> None:
        """Resets the player for a new game."""
        self.score = 0
        self.selected_category = None
        self.used_powerups.clear()
        self.round_reset()

    def round_reset(self) -> None:
        """Resets the player for a new round."""
        self.answer = -1
        self.visible_options = [True, True, True, True]
        self.double_points = False


bot_names = [
    "Quiztopher",
    "Botrick",
    "Factzilla",
    "Triviatron",
    "WrongAgain",
    "LOLbert",
    "Guessica",
    "NotAlexa",
    "QuizzlyBear",
    "SmartyFartz",
    "Mehgellan",
    "A.I. Dunno",
    "Botney Spears",
    "Quackademic",
    "IQuit",
    "ThinkyWinky",
    "SirGuessalot",
    "WhoDatBot",
    "TriviaSaurus",
    "Boogle",
    "UhhSure",
    "BotatoHead",
    "JeoparDunce",
    "QuesoBot",
    "Prof. Meh",
    "KnowNada",
    "GuessAndGo",
    "MissTakes",
    "Guesstavo",
    "NoClueNancy",
    "Trivibot3000",
    "Bot McWrongface",
    "Albot Einstein",
    "FactCheckYoSelf",
    "IGuessSo",
    "Botchee",
    "Quizneezer",
    "TrueOrNah",
    "Quizmarkable",
    "QuippyBot",
    "DuhVinci",
    "BotchedIt",
    "Mehgan Fox",
    "WrongTheConqueror",
    "GuessiePie",
    "KnowItYall",
    "NotSoBot",
    "Quizzelda",
    "SnarkMatter",
    "WinOrDinner"
]
