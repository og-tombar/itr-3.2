"""Models for the questions database."""

from dataclasses import dataclass
from enum import Enum


class Category(str, Enum):
    """The categories of questions."""
    ALL = "All"
    ART = "Art"
    ENTERTAINMENT_BOARD_GAMES = "Entertainment: Board Games"
    ENTERTAINMENT_BOOKS = "Entertainment: Books"
    ENTERTAINMENT_CARTOON_ANIMATIONS = "Entertainment: Cartoon & Animations"
    ENTERTAINMENT_COMICS = "Entertainment: Comics"
    ENTERTAINMENT_FILM = "Entertainment: Film"
    ENTERTAINMENT_JAPANESE_ANIME_MANGA = "Entertainment: Japanese Anime & Manga"
    ENTERTAINMENT_MUSIC = "Entertainment: Music"
    ENTERTAINMENT_MUSICALS_THEATRES = "Entertainment: Musicals & Theatres"
    ENTERTAINMENT_TELEVISION = "Entertainment: Television"
    ENTERTAINMENT_VIDEO_GAMES = "Entertainment: Video Games"
    GENERAL_KNOWLEDGE = "General Knowledge"
    GEOGRAPHY = "Geography"
    HISTORY = "History"
    MYTHOLOGY = "Mythology"
    POLITICS = "Politics"
    SCIENCE_NATURE = "Science & Nature"
    SCIENCE_COMPUTERS = "Science: Computers"
    SCIENCE_GADGETS = "Science: Gadgets"
    SCIENCE_MATHEMATICS = "Science: Mathematics"
    SPORTS = "Sports"


@dataclass
class Question:
    """The data for a question. Includes the correct answer (do not send to clients)."""
    text: str
    options: list[str]
    correct_index: int

    @staticmethod
    def from_row(r: tuple) -> "Question":
        """Create a new question object from a row.

        Args:
            r (tuple): The row from the database.

        Returns:
            Question: The question object.
        """
        return Question(
            text=r[2],
            options=r[4:],
            correct_index=r[3]
        )
