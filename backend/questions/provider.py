"""A provider for questions."""

from typing import Generator

from questions.db import QuestionDB
from questions.models import Category, Question


class QuestionProvider:
    """A provider for questions."""

    def __init__(self):
        self._questions: list[list[Question]] = [[] for _ in range(10)]
        self._difficulty = 0

    def load_questions(self, category: Category = Category.RANDOM) -> None:
        """Loads questions from the database.

        Args:
            category (Category, optional): The category of questions to load. Defaults to RANDOM.
        """
        questions = QuestionDB.get_questions(category)
        for q in questions:
            self._questions[q.difficulty - 1].append(q)
        self._questions = [l for l in self._questions if l]
        self._difficulty = len(self._questions) // 2

    def questions(self) -> Generator[Question, None, None]:
        """Generator for the questions.

        Yields:
            Generator[Question, None, None]: A generator of questions.
        """
        while self._questions:
            if not self._questions[self._difficulty]:
                self._questions.pop(self._difficulty)
                self._difficulty = min(
                    self._difficulty, len(self._questions) - 1)
            else:
                yield self._questions[self._difficulty].pop()

    def increase_difficulty(self) -> None:
        """Increases the difficulty of the questions."""
        self._difficulty = min(1 + self._difficulty, len(self._questions) - 1)

    def decrease_difficulty(self) -> None:
        """Decreases the difficulty of the questions."""
        self._difficulty = max(0, self._difficulty - 1)
