"""Question database."""

import sqlite3
from pathlib import Path

from questions.models import Category, Question


class QuestionDB:
    """Database for managing questions."""

    DB_PATH = Path(__file__).parent / "questions.db"

    @staticmethod
    def get_questions(category: Category = Category.RANDOM) -> list[Question]:
        """Gets 10 questions from the sqlite database.

        Args:
            category (Category, optional): The category of questions to get. Defaults to ALL.

        Returns:
            list[Question]: The questions from the database.
        """
        if category == Category.RANDOM:
            category = Category.randomize()

        with sqlite3.connect(QuestionDB.DB_PATH) as conn:
            cur = conn.cursor()
            if category != Category.ALL:
                cur.execute(
                    "SELECT * FROM questions WHERE category = ? ORDER BY RANDOM()",
                    (category,))
            else:
                cur.execute(
                    "SELECT * FROM questions ORDER BY RANDOM()")
            rows = cur.fetchall()
            questions = [Question.from_row(r) for r in rows]
            cur.close()
        return questions
