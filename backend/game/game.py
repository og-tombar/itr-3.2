"""Game management service."""

import asyncio
import random
import uuid
from typing import Generator

from events.data import GameUpdateData, MessageData
from events.events import EventQueue, ServerEvent
from game.models import GamePhase, Phase
from gemini.gemini import Gemini
from player.player import BotLevel, Player, PlayerType, PowerUp, bot_names
from questions.models import Category, Question
from questions.provider import QuestionProvider


class Game:
    """A game of trivia."""

    NUM_QUESTIONS = 10

    def __init__(self, game_id: str, players: dict[str, Player]):
        self._id = game_id
        self._players = players
        self._bot_level: BotLevel | None = None
        self._category = Category.RANDOM
        self._phase: Phase | None = None
        self._question_provider = QuestionProvider()
        self._current_question: Question | None = None

    #################################################
    # Public methods
    #################################################

    async def start(self) -> None:
        """Starts the game."""
        for p in self._phases():
            self._phase = p
            await self._run_phase()

    def set_bot_level(self, level: BotLevel) -> None:
        """Sets the bot level for the game.

        Args:
            level (BotLevel): The level of the bot.
        """
        self._bot_level = level

    def submit_answer(self, player: Player, answer: int) -> None:
        """Submits an answer for a player.

        Args:
            player (Player): The player who submitted the answer.
            answer (int): The answer submitted by the player.
        """
        player.answer = answer
        points = self._phase.time_remaining
        if player.double_points:
            points *= 2
        if answer == self._current_question.correct_index:
            player.score += points

    async def use_powerup(self, player: Player, powerup: PowerUp) -> None:
        """Uses a powerup for the player.

        Args:
            player (Player): The player who uses the powerup.
            powerup (PowerUp): The powerup to use.
        """
        if powerup in player.used_powerups:
            return
        player.used_powerups.append(powerup)
        match powerup:
            case PowerUp.FIFTY_FIFTY: self._fifty_fifty(player)
            case PowerUp.CALL_FRIEND: await self._call_friend(player)
            case PowerUp.DOUBLE_POINTS: player.double_points = True

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
            bot = Player(
                sid=str(uuid.uuid4()),
                type=PlayerType.BOT,
                name=name)
            if self._bot_level is not None:
                bot.level = self._bot_level
            self._players[bot.sid] = bot

    def _phases(self) -> Generator[Phase, None, None]:
        """Yields the phases of the game.

        Yields:
            Generator[Phase, None, None]: The phases of the game.
        """
        yield self._make_phase(GamePhase.GAME_STARTED)
        if len(self._players) == 1:
            yield self._make_phase(GamePhase.BOT_LEVEL_SELECTION)
        yield self._make_phase(GamePhase.CATEGORY_SELECTION)
        yield self._make_phase(GamePhase.CATEGORY_RESULTS)
        for _ in range(Game.NUM_QUESTIONS):
            yield self._make_phase(GamePhase.AWAITING_ANSWERS)
            yield self._make_phase(GamePhase.ROUND_ENDED)
            self._next_question()
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
            case GamePhase.BOT_LEVEL_SELECTION:
                p.should_stop = self._is_bot_level_set
                p.teardown = self._add_bots
            case GamePhase.CATEGORY_SELECTION:
                p.should_stop = self._all_selected_category
                p.teardown = self._load_questions
            case GamePhase.AWAITING_ANSWERS:
                p.setup = self._round_reset
                p.should_stop = self._all_answered
                p.teardown = self._update_bot_scores
            case GamePhase.ROUND_ENDED:
                p.setup = self._adjust_difficulty
        return p

    async def _run_phase(self) -> None:
        """Runs the current phase."""
        self._phase.setup()
        await self._update()
        while self._phase.time_remaining > 0 and not self._phase.should_stop():
            await self._tick()
            await self._update()
        self._phase.teardown()

    def _next_question(self) -> None:
        """Gets the next question."""
        self._current_question = next(
            self._question_provider.questions(), None)

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
        """Resets the players for a new game."""
        for p in self._players.values():
            p.total_reset()

    def _round_reset(self) -> None:
        """Resets the answers for each player."""
        for p in self._players.values():
            p.round_reset()

    def _is_bot_level_set(self) -> bool:
        """Checks if the bot level has been set.

        Returns:
            bool: True if the bot level has been set, False otherwise.
        """
        return self._bot_level is not None

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
        self._question_provider.load_questions(self._category)
        self._next_question()

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

    def _adjust_difficulty(self) -> None:
        """Adjusts the difficulty of the questions."""
        humans = self._get_players_by_type(PlayerType.HUMAN)
        answers = [h.answer for h in humans]
        correct = [a == self._current_question.correct_index for a in answers]
        if all(correct):
            self._question_provider.increase_difficulty()
        if not any(correct):
            self._question_provider.decrease_difficulty()

    def _fifty_fifty(self, player: Player) -> None:
        """Hides two incorrect options for the player.

        Args:
            player (Player): The player who uses the powerup.
        """
        correct = self._current_question.correct_index
        indices = [i for i in range(4) if i != correct]
        random.shuffle(indices)
        player.visible_options[indices[0]] = False
        player.visible_options[indices[1]] = False

    async def _call_friend(self, player: Player) -> None:
        """Sends a message to the player's friend.

        Args:
            player (Player): The player who uses the powerup.
        """
        await self._friend_message(player.sid, "Thinking...")
        q = self._current_question
        prompt = Gemini.call_friend_prompt(q.text, q.options)
        response = await Gemini.query_async(prompt)
        await self._friend_message(player.sid, response)

    async def _friend_message(self, destination_id: str, message: str) -> None:
        """Sends a message to the player's friend.

        Args:
            destination_id (str): The ID of the player to send the message to.
            message (str): The message to send to the player.
        """
        message = MessageData(
            id=str(uuid.uuid4()),
            sender_id=str(uuid.uuid4()),
            username="Friend",
            message=message,
            destination_id=destination_id
        )
        await EventQueue.put(ServerEvent.MESSAGE, message)
