"""Provides a fixed sequence of questions, looping."""

import json
from pathlib import Path

from data_models import Question


class QuestionProvider:
    """Returns a fixed sequence of questions, looping."""

    _db_path = Path(__file__).parent / "db" / "questions.json"
    _questions: list[Question] = []

    @staticmethod
    def load_db() -> None:
        """Load the questions from the database."""
        with open(QuestionProvider._db_path, "r", encoding="utf-8") as f:
            db = json.load(f)
        QuestionProvider._questions = [Question(**q) for q in db]

    @staticmethod
    def get_questions() -> list[Question]:
        """Get the questions from the database."""
        QuestionProvider.load_db()
        return QuestionProvider._questions
