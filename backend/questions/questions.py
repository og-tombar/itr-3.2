"""Question management service."""

import sqlite3
from pathlib import Path

from questions.models import Question


class QuestionDB:
    """Database for managing questions."""

    DB_PATH = Path(__file__).parent / "questions.db"

    @staticmethod
    def get_questions() -> list[Question]:
        """Gets 10 questions from the sqlite database.

        Returns:
            list[Question]: The questions from the database.
        """
        with sqlite3.connect(QuestionDB.DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 10")
            rows = cur.fetchall()
            questions = [Question.from_row(r) for r in rows]
            cur.close()
        return questions
