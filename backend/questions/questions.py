"""Question management service."""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Question:
    """The data for a question. Includes the correct answer (do not send to clients)."""
    id: str
    text: str
    options: list[str]
    correct_index: int


class QuestionDB:
    """Database for managing questions."""

    DB_PATH = Path(__file__).parent / "questions.json"
    _questions: list[Question] = []

    @staticmethod
    def load_questions() -> None:
        """Load the questions from the database."""
        with open(QuestionDB.DB_PATH, "r", encoding="utf-8") as f:
            db = json.load(f)
        QuestionDB._questions = [Question(**q) for q in db]

    @staticmethod
    def get_questions() -> list[Question]:
        """Gets the questions from the database.

        Returns:
            list[Question]: The questions from the database.
        """
        QuestionDB.load_questions()
        return QuestionDB._questions
