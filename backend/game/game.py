"""Game management service."""

import asyncio
import random
import uuid
from typing import Generator

from events.data import GameUpdateData
from events.events import EventQueue, ServerEvent
from game.models import GamePhase, Phase
from player.player import Player, PlayerType, bot_names
from questions.models import Category, Question
from questions.questions import QuestionDB


class Game:
    """A game of trivia."""

    def __init__(self, game_id: str, players: dict[str, Player]):
        self._id = game_id
        self._players = players
        self._category = Category.RANDOM
        self._phase: Phase | None = None
        self._questions: Generator[Question, None, None] = iter([])
        self._current_question: Question | None = None

    #################################################
    # Public methods
    #################################################

    async def start(self) -> None:
        """Starts the game."""
        if len(self._players) == 1:
            self._add_bots()

        for p in self._phases():
            self._phase = p
            await self._run_phase()

    def submit_answer(self, player: Player, answer: int) -> None:
        """Submits an answer for a player.

        Args:
            player (Player): The player who submitted the answer.
            answer (int): The answer submitted by the player.
        """
        player.answer = answer
        if answer == self._current_question.correct_index:
            player.score += self._phase.time_remaining

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

    def _add_bots(self) -> None:
        """Adds bots to the game."""
        random.shuffle(bot_names)
        names = bot_names[:3]
        for name in names:
            bot = Player(type=PlayerType.BOT, sid=str(uuid.uuid4()), name=name)
            self._players[bot.sid] = bot

    def _phases(self) -> Generator[Phase, None, None]:
        """Yields the phases of the game.

        Yields:
            Generator[Phase, None, None]: The phases of the game.
        """
        yield self._make_phase(GamePhase.GAME_STARTED)
        yield self._make_phase(GamePhase.CATEGORY_SELECTION)
        yield self._make_phase(GamePhase.CATEGORY_RESULTS)
        while self._current_question is not None:
            yield self._make_phase(GamePhase.AWAITING_ANSWERS)
            yield self._make_phase(GamePhase.ROUND_ENDED)
            self._current_question = next(self._questions, None)
        yield self._make_phase(GamePhase.GAME_ENDED)

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
                p.setup = self._players_reset
            case GamePhase.CATEGORY_SELECTION:
                p.should_stop = self._all_selected_category
                p.teardown = self._load_questions
            case GamePhase.AWAITING_ANSWERS:
                p.setup = self._reset_answers
                p.should_stop = self._all_answered
                p.teardown = self._update_bot_scores
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
            category=self._category,
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

    def _get_players_by_type(self, player_type: PlayerType) -> list[Player]:
        """Gets the players by type.

        Args:
            player_type (PlayerType): The type of player to get.

        Returns:
            list[Player]: The players by type.
        """
        return [p for p in self._players.values() if p.type == player_type]

    def _players_reset(self) -> None:
        for p in self._players.values():
            p.score = 0
            p.selected_category = None

    def _all_selected_category(self) -> bool:
        """Checks if all players have selected a category.

        Returns:
            bool: True if all players have selected a category, False otherwise.
        """
        humans = self._get_players_by_type(PlayerType.HUMAN)
        return all(h.selected_category is not None for h in humans)

    def _load_questions(self) -> None:
        """Loads the questions for the game from the category with the most votes."""
        votes = {c: 0 for c in Category}
        humans = self._get_players_by_type(PlayerType.HUMAN)
        for h in humans:
            if h.selected_category is not None:
                votes[h.selected_category] += 1
        if len(votes) == 0:
            self._category = Category.randomize()
        else:
            majority = max(votes.values())
            candidates = [c for c in votes if votes[c] == majority]
            self._category = random.choice(candidates)
        self._questions = iter(QuestionDB.get_questions(self._category))
        self._current_question = next(self._questions, None)

    def _update_bot_scores(self) -> None:
        """Updates the scores for each bot."""
        bots = self._get_players_by_type(PlayerType.BOT)
        for b in bots:
            b.score += b.level.mock_round_points()

    def _all_answered(self) -> bool:
        """Checks if all players have answered the current question.

        Returns:
            bool: True if all players have answered the current question, False otherwise.
        """
        humans = self._get_players_by_type(PlayerType.HUMAN)
        return all(h.answer != -1 for h in humans)

    def _reset_answers(self) -> None:
        """Resets the answers for each player."""
        for p in self._players.values():
            p.answer = -1
