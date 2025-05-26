"""Game management service."""

import asyncio
from typing import Generator

from events.data import GameUpdateData
from events.events import EventQueue, ServerEvent
from game.models import GamePhase, Phase
from player.player import Player
from questions.questions import QuestionDB


class Game:
    """A game of trivia."""

    def __init__(self, game_id: str, players: dict[str, Player]):
        self._id = game_id
        self._players = players
        self._questions = iter(QuestionDB.get_questions())
        self._current_question = next(self._questions, None)
        self._phase: Phase | None = None

    #################################################
    # Public methods
    #################################################

    async def start(self) -> None:
        """Starts the game."""
        for p in self._phases():
            self._phase = p
            await self._run_phase()

    def remove_player(self, player: Player) -> None:
        """Removes a player from the game.

        Args:
            player (Player): The player to remove.
        """
        self._players.pop(player.sid)

    def is_empty(self) -> bool:
        """Checks if the game is empty.

        Returns:
            bool: True if the game is empty, False otherwise.
        """
        return len(self._players) == 0

    #################################################
    # Private methods
    #################################################

    def _phases(self) -> Generator[Phase, None, None]:
        """Yields the phases of the game.

        Yields:
            Generator[Phase, None, None]: The phases of the game.
        """
        yield self._make_phase(GamePhase.GAME_STARTED)
        while self._current_question is not None:
            yield self._make_phase(GamePhase.AWAITING_ANSWERS)
            next_question = next(self._questions, None)
            if next_question is not None:
                yield self._make_phase(GamePhase.ROUND_ENDED)
            self._current_question = next_question
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
        match title:
            case GamePhase.GAME_STARTED:
                p.setup = self._reset_scores
            case GamePhase.AWAITING_ANSWERS:
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
        question_text = ""
        question_options = []
        if self._current_question is not None:
            question_text = self._current_question.text
            question_options = self._current_question.options

        correct_answer = -1
        if self._phase.title == GamePhase.ROUND_ENDED:
            correct_answer = self._current_question.correct_index

        update = GameUpdateData(
            id=self._id,
            phase=self._phase.title,
            players=self._players,
            question_text=question_text,
            question_options=question_options,
            correct_answer=correct_answer,
            time_remaining=self._phase.time_remaining,
        )
        await EventQueue.put(ServerEvent.GAME_UPDATE, update)

    async def _tick(self) -> None:
        """Ticks the game timer."""
        await asyncio.sleep(1)
        self._phase.time_remaining -= 1

    def _reset_scores(self) -> None:
        for p in self._players.values():
            p.score = 0

    def _get_scores(self) -> dict[str, int]:
        """Gets the scores for each player.

        Returns:
            dict[str, int]: The scores for each player.
        """
        return {p.sid: p.score for p in self._players.values()}

    def _update_scores(self) -> None:
        """Updates the scores for each player."""
        for p in self._players.values():
            p.score += p.answer == self._current_question.correct_index

    def _get_answers(self) -> dict[str, int]:
        """Gets the answers for each player.

        Returns:
            dict[str, int]: The answers for each player.
        """
        return {p.sid: p.answer for p in self._players.values()}

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
