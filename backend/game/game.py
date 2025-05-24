"""Game management service."""

import asyncio
from typing import Generator

from events.data import GameUpdateData
from events.events import EventQueue, ServerEvent
from game.models import GamePhase, Phase, Player, Question
from questions.questions import QuestionDB


class Game:
    """A game of trivia."""

    def __init__(self, game_id: str, players: list[str]):
        self._id = game_id
        self._players = {p: Player(p) for p in players}
        self._questions = iter(QuestionDB.get_questions())
        self._next_question: Question | None = None
        self._phase: Phase | None = None

    #################################################
    # Public methods
    #################################################

    async def start(self) -> None:
        """Starts the game."""
        for p in self._phases():
            self._phase = p
            await self._run_phase()

    def submit_answer(self, player: str, answer: int) -> None:
        """Submits an answer to the game.

        Args:
            player (str): The player submitting the answer.
            answer (int): The answer to the question.
        """
        self._players[player].answer = answer

    #################################################
    # Private methods
    #################################################

    def _phases(self) -> Generator[Phase, None, None]:
        """Yields the phases of the game.

        Yields:
            Generator[Phase, None, None]: The phases of the game.
        """
        yield self._make_phase(GamePhase.GAME_STARTED)
        self._next_question = next(self._questions, None)
        while self._next_question is not None:
            yield self._make_phase(GamePhase.AWAITING_ANSWERS)
            self._next_question = next(self._questions, None)
            if self._next_question is not None:
                yield self._make_phase(GamePhase.ROUND_ENDED)
        yield self._make_phase(GamePhase.GAME_ENDED)
        yield self._make_phase(GamePhase.GAME_EXIT)

    def _make_phase(self, title: GamePhase) -> Phase:
        """Makes a Phase object for a phase.

        Args:
            title (GamePhase): The title of the phase.

        Returns:
            Phase: The Phase object for the phase.
        """
        p = Phase(title=title, time_remaining=title.get_duration())
        if title == GamePhase.AWAITING_ANSWERS:
            p.setup = self._reset_answers
            p.teardown = self._update_scores
            p.should_stop = self._all_answered
        return p

    async def _run_phase(self) -> None:
        """Runs the current phase."""
        self._phase.setup()
        await self._update()
        while self._phase.time_remaining > 0 and not self._phase.should_stop():
            await self._tick()
            await self._update()
        self._phase.teardown()

    async def _update(self) -> None:
        """Updates the game state and yields the current state."""
        update = GameUpdateData(
            id=self._id,
            title=self._phase.title,
            scores=self._get_scores(),
            time_remaining=self._phase.time_remaining,
            answers=self._get_answers(),
        )
        if self._phase.title == GamePhase.AWAITING_ANSWERS:
            update.question_text = self._next_question.text
            update.question_options = self._next_question.options
        await EventQueue.put(ServerEvent.GAME_UPDATE, update)

    async def _tick(self) -> None:
        """Ticks the game timer."""
        await asyncio.sleep(1)
        self._phase.time_remaining -= 1

    def _get_scores(self) -> dict[str, int]:
        """Gets the scores for each player.

        Returns:
            dict[str, int]: The scores for each player.
        """
        return {p.id: p.score for p in self._players.values()}

    def _update_scores(self) -> None:
        """Updates the scores for each player."""
        for p in self._players.values():
            p.score += p.answer == self._next_question.correct_index

    def _get_answers(self) -> dict[str, int]:
        """Gets the answers for each player.

        Returns:
            dict[str, int]: The answers for each player.
        """
        return {p.id: p.answer for p in self._players.values()}

    def _all_answered(self) -> bool:
        """Checks if all players have answered the current question.

        Returns:
            bool: True if all players have answered the current question, False otherwise.
        """
        return sum(p.answer != -1 for p in self._players.values()) == len(self._players)

    def _reset_answers(self) -> None:
        """Resets the answers for each player."""
        for p in self._players.values():
            p.answer = -1
