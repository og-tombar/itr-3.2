"""Player class."""

import random
from dataclasses import dataclass
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
                return random.randint(1, 10)
            case BotLevel.INTERMEDIATE:
                return random.randint(6, 15)
            case BotLevel.EXPERT:
                return random.randint(11, 20)


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
