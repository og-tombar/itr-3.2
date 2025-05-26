"""Models for the questions database."""

import random
from dataclasses import dataclass
from enum import Enum


class Category(str, Enum):
    """The categories of questions."""
    ALL = "All"
    RANDOM = "Random"
    ART = "Art"
    BOARD_GAMES = "Board Games"
    BOOKS = "Books"
    CARTOON_ANIMATIONS = "Cartoon & Animations"
    COMICS = "Comics"
    FILM = "Film"
    JAPANESE_ANIME_MANGA = "Japanese Anime & Manga"
    MUSIC = "Music"
    MUSICALS_THEATRES = "Musicals & Theatres"
    TELEVISION = "Television"
    VIDEO_GAMES = "Video Games"
    GENERAL_KNOWLEDGE = "General Knowledge"
    GEOGRAPHY = "Geography"
    HISTORY = "History"
    MYTHOLOGY = "Mythology"
    POLITICS = "Politics"
    SCIENCE_NATURE = "Science & Nature"
    COMPUTERS = "Computers"
    GADGETS = "Gadgets"
    MATHEMATICS = "Mathematics"
    SPORTS = "Sports"

    @staticmethod
    def randomize() -> "Category":
        """Get a random category.

        Returns:
            Category: A random category.
        """
        categories = [c for c in Category if c not in [
            Category.ALL, Category.RANDOM]]
        return random.choice(categories)


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
