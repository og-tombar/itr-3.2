## Milestone 1: Basic Project & "Hello World" Steel-Thread

### Phase 1.1 — Monorepo & Scaffolding

**Goal:** Establish the basic monorepo structure with a minimal Next.js frontend and a Python backend, ensuring both can be initialized.

**Tasks** (≈ 70 LOC)

- Create `backend/` folder with an empty `app.py` (for Flask) and `requirements.txt`.
- Initialize a new Next.js project in `frontend/` using `npx create-next-app@latest --ts`. This will set up the basic file structure including `pages/`, `public/`, `src/` (if chosen or manually created for organization), `next.config.js`, and `package.json`.
- Create a basic `pages/index.tsx` in the Next.js app to serve as the initial entry point.
- Add a `README.md` at the root with clear, step-by-step instructions on how to install dependencies and run both the backend and frontend development servers.

**Validation:**

- `pip install -r backend/requirements.txt` installs backend dependencies successfully.
- `cd frontend && npm install` (or `yarn install`) installs frontend dependencies successfully.
- The Python backend server (e.g., Flask development server) starts without errors.
- The Next.js frontend development server (`npm run dev` or `yarn dev`) starts, and the basic `pages/index.tsx` page is viewable in a browser.

### Phase 1.2 — Socket.IO Connection Test

**Goal:** Implement a basic "ping-pong" exchange between the Next.js frontend and the Flask-SocketIO backend to verify the real-time communication channel.

**Tasks** (≈ 100 LOC)

- Install `flask-socketio` in `backend/requirements.txt` and `socket.io-client` in `frontend/package.json`.
- In `backend/app.py`, initialize `SocketIO` with the Flask app. Implement a simple event handler for a custom `ping_event` that, upon receiving the event, emits a `pong_event` back to the client that sent it.
- In the Next.js frontend, create `src/socket.ts` to initialize and export a singleton `socket.io-client` instance.
- In `frontend/src/pages/_app.tsx` or a specific page component (e.g., `pages/index.tsx`), import the socket client. On component mount (e.g., using `useEffect` hook), establish a connection to the backend Socket.IO server and emit the `ping_event`.
- Set up an event listener for `pong_event` on the frontend. When received, log a confirmation message to the browser console.

**Validation:**

- The browser console on the Next.js page shows the "pong" message received from the backend.
- The backend server logs indicate that it received the "ping" event and sent the "pong" event.
- Connection status (connect/disconnect events) can be optionally logged on both ends for clarity.

## Milestone 2: Lobby & Matchmaking

### Phase 2.1 — `join_lobby` Event & Queue

**Goal:** Allow users to actively join a server-side matchmaking queue and see feedback on the current lobby status.

**Tasks** (≈ 120 LOC)

- Backend: Create `matchmaking.py`. This module will manage an in-memory list or dictionary to store `request.sid` (Socket.IO session ID) of players waiting in the lobby.
- Backend: In `app.py`, expose a `join_lobby` Socket.IO event handler. When a client emits `join_lobby`, this handler will delegate to `matchmaking.py` to add the player's `sid` to the queue.
- Backend: After adding a player, `matchmaking.py` should emit a `lobby_update` event back to all clients in the lobby (or at least the joining client), containing data like the current number of players in the queue and perhaps a list of player identifiers/names if available.
- Frontend: In a Next.js page (e.g., `pages/index.tsx` or a dedicated `Lobby.tsx` component imported into it), add a "Join Lobby" button.
- Frontend: On clicking the button, emit the `join_lobby` event to the server.
- Frontend: Listen for the `lobby_update` event. Upon receiving it, update the UI to display the current lobby size or other relevant information.

**Validation:**

- Clicking the "Join Lobby" button on the Next.js page results in the UI updating to show the new lobby size (e.g., "Players in lobby: 1").
- Backend logs confirm reception of `join_lobby` and addition to the queue.
- If multiple clients join, each should see the updated lobby size.

### Phase 2.2 — Timeout-Driven Game Creation

**Goal:** Automatically initiate a game session when enough players have joined the lobby or after a set timeout period.

**Tasks** (≈ 180 LOC)

- Backend: In `matchmaking.py`, when the first player joins the lobby (and the queue was previously empty), start a configurable countdown timer (e.g., 30 seconds, from `config.py`).
- Backend: If the timer expires or if a predefined number of players (e.g., ≥ 2) join the queue before the timer expires, `matchmaking.py` should trigger game creation. This involves selecting the players from the queue and calling a (yet-to-be-created) `game_manager.start_game(selected_players)` function.
- Backend: Generate a unique game ID (e.g., using UUID). Create a new Socket.IO room named after this game ID and move the sockets of the selected players into this room. This isolates game-specific communication.
- Backend: Emit a `game_started` event to all players who were moved into the game room. This event should include the `gameId` and potentially initial game state or player list.
- Frontend: Listen for the `game_started` event. Upon receiving it, the UI should change to indicate that the game has begun. This might involve navigating to a new game page using Next.js router (e.g., `router.push('/game/' + gameId)` if using dynamic routes like `pages/game/[gameId].tsx`) or conditionally rendering a game interface.

**Validation:**

- If one client joins, after 30 seconds (or configured timeout), they receive the `game_started` event and their UI transitions to a game view.
- If two or more clients join, they should receive the `game_started` event sooner than the timeout, and their UIs should transition.
- Backend logs should show the matchmaking timer starting, players being added to a room, and the `game_started` event being emitted.

## Milestone 3: Question Delivery & Basic UI

### Phase 3.1 — Static Question Provider

**Goal:** Deliver a single, hard-coded trivia question from the backend to all players in an active game room, and display it on the frontend.

**Tasks** (≈ 100 LOC)

- Backend: Create `question_provider.py`. Implement a function `get_next_question()` that initially returns a hard-coded question object (e.g., with `text`, `options` array, `correctIndex`).
- Backend: Create `game_manager.py`. Implement a basic `start_game(players_list, game_id)` function. Upon being called by `matchmaking.py`, this function will use `question_provider.get_next_question()` to fetch the static question.
- Backend: `game_manager` then emits a `new_question` event to the specific game room (using the `game_id`), sending the question object as payload.
- Frontend: In the Next.js game page (e.g., `pages/game/[gameId].tsx`), listen for the `new_question` event.
- Frontend: Create a React component (e.g., `src/components/Game/Question.tsx`) to render the question. This component will take the question object as a prop and display the `text` and `options`. The options could be simple buttons or list items for now.

**Validation:**

- After a game starts (from Milestone 2.2), all clients in that game room automatically display the same static question text and its options.
- Backend logs show `game_manager` fetching the question and emitting `new_question` to the correct room.

### Phase 3.2 — Answer Submission & Ack

**Goal:** Enable players to select an answer to the displayed question and receive an acknowledgment from the server that their answer was submitted.

**Tasks** (≈ 150 LOC)

- Frontend: In the `Question.tsx` component (or wherever options are rendered), make each option clickable (e.g., a button).
- Frontend: When a player clicks an option, emit a `submit_answer` event to the server. The payload should include necessary information, like `{ choiceIndex: number }` and potentially the `gameId` (though the server knows the room from `request.sid`).
- Backend: In `game_manager.py`, implement a handler for the `submit_answer` event. This handler should log the `request.sid` (player ID) and their `choiceIndex`.
- Backend: As a simple acknowledgment, the handler should emit an `answer_received` event back to the submitting client, perhaps with their chosen `choiceIndex`.
- Frontend: Listen for the `answer_received` event. Upon receiving it, update the UI to give feedback, for example, by highlighting the player's chosen option or disabling other options.

**Validation:**

- Clicking an answer option on the Next.js page highlights that option (or provides other visual feedback).
- The backend logs show the `submit_answer` event from the correct player SID with the correct choice index.
- The submitting client receives the `answer_received` acknowledgment.

## Milestone 4: Scoring & Timer

### Phase 4.1 — Simple Scoring Logic

**Goal:** Implement basic scoring for submitted answers based on correctness (initially) and broadcast score updates.

**Tasks** (≈ 180 LOC)

- Backend: In `game_manager.py`, when handling `submit_answer`, compare the `choiceIndex` with the `correctIndex` of the current question (requires `game_manager` to store the current question details).
- Backend: For now, assign a fixed number of points for a correct answer (e.g., 1000 points) and 0 for incorrect.
- Backend: Maintain a simple score object/dictionary within the `game_manager` for the current game, mapping `playerId` (or `sid`) to their score.
- Backend: After processing an answer, emit a `score_update` event to all players in the game room. The payload should be an object like `{ scores: { playerId1: newScore1, playerId2: newScore2, ... } }` or individual updates `{ playerId, newScore }`.
- Frontend: In the Next.js game page, create a `Scoreboard.tsx` component (e.g., `src/components/Game/Scoreboard.tsx`).
- Frontend: Listen for the `score_update` event. Update the `Scoreboard.tsx` component to display the latest scores for all players in the game.

**Validation:**

- After a player submits a correct answer, their score on the `Scoreboard` increases by the defined amount. Incorrect answers result in no score change.
- All players in the game room see the updated scores simultaneously.
- Backend logs confirm correct/incorrect answer processing and score calculation.

### Phase 4.2 — Question Timer & Auto-advance

**Goal:** Implement a server-side timer for each question. If time runs out, unanswered players score zero, and the game automatically proceeds to the next question (or ends if it's the last one).

**Tasks** (≈ 160 LOC)

- Backend: Create `helpers/timers.py` if not already present, or use `threading.Timer` / `asyncio.sleep` directly in `game_manager.py`.
- Backend: When `game_manager.py` emits `new_question`, it should also start a server-side timer for the question's duration (e.g., 15 seconds, from `config.py`).
- Backend: If the timer expires before all players have answered, the `game_manager` should:
  - Consider any player who hasn't answered yet as having scored 0 points for that question.
  - Trigger the delivery of the next question (for now, it can be the same static question, or a simple list of questions in `question_provider.py`). If it's the last question, trigger a `game_over` flow (to be detailed later).
- Frontend: In the Next.js game page, display a visual countdown timer (e.g., using a `Timer.tsx` component in `src/components/Shared/Timer.tsx`) synchronized with the question duration. This timer is primarily for user feedback; the server is the source of truth.
- Frontend: When a `new_question` event is received (because the previous one timed out or was answered), the UI should reset to display the new question, and the countdown timer should restart.

**Validation:**

- The frontend displays a countdown timer for each question.
- If players don't answer within the allotted time, the question automatically changes (or the game ends).
- Players who didn't answer receive 0 points for that question (verifiable via `score_update` or backend logs).
- Backend logs show timers starting and expiring correctly, and question advancement.

## Milestone 5: Bots & Adaptive Difficulty

### Phase 5.1 — Bot Simulation

**Goal:** Introduce simulated bot players into games when there are fewer than a minimum number of human players, to ensure a game can always start.

**Tasks** (≈ 180 LOC)

- Backend: Create `bot_player.py`. Define a `Bot` class or set of functions.
- Backend: `Bot` logic should include:
  - A way to "join" a game (the `game_manager` will instantiate them).
  - A method to simulate `submit_answer` after a random delay (within `BOT_MIN_DELAY` and `BOT_MAX_DELAY` from `config.py`).
  - Simulated accuracy: The bot should have a configurable chance (e.g., 60-90% from `BOT_ACCURACY_RANGE` in `config.py`) of choosing the correct answer.
- Backend: In `game_manager.py`, when a game is about to start, if the number of human players is less than a threshold (e.g., < 2), instantiate 1 to 3 `Bot` players.
- Backend: These bots will need to be integrated into the game's player list, score tracking, and will emit `submit_answer` events as if they were clients (perhaps internally calling the same answer processing logic).
- Frontend: Bot players should appear in the `Scoreboard.tsx` and their scores should update like human players. No specific frontend changes are needed if bots correctly mimic player data and events.

**Validation:**

- If a single human player starts a game, 1-3 bot players are added and appear on the scoreboard.
- Bots automatically submit answers after some delay.
- Bots' scores reflect their configured accuracy (i.e., they get some answers right, some wrong).
- Backend logs show bot creation and their simulated actions.

### Phase 5.2 — Adaptive Question Difficulty

**Goal:** Modify the question provider to select questions of varying difficulty based on a player's previous performance.

**Tasks** (≈ 140 LOC)

- Backend: In `question_provider.py`, expand the question data structure to include a `difficulty` field ("easy", "medium", "hard"). Create separate lists or a database structure for questions of different difficulties.
- Backend: Modify `question_provider.get_next_question(player_id, prev_correct: bool)` to accept the player's ID and whether their previous answer was correct.
- Backend: Implement logic in `get_next_question` to select an easier question if `prev_correct` was `false`, and a harder one if `true` (or stay at the same level). This needs to track each player's current difficulty level or adapt dynamically.
- Backend: In `game_manager.py`, when it's time to send the next question to a player (or the whole room if difficulty is room-wide initially, simplifying by sending the same difficulty question to all players based on an average or a specific player's performance for now), call the updated `get_next_question` with the relevant performance data.
- Frontend: Optionally, display the current question's difficulty level in the `Question.tsx` component if this information is sent with the question object.

**Validation:**

- Backend logs show the `question_provider` selecting questions from different difficulty pools based on the `prev_correct` flag.
- If a player consistently answers correctly, they start receiving questions marked as "harder" (if this data is exposed or logged).
- If a player struggles, they receive "easier" questions.

## Milestone 6: "Helps" & LLM Stub

### Phase 6.1 — 50/50 Help

**Goal:** Implement the "50/50" help feature, allowing players to remove two incorrect options from the current question.

**Tasks** (≈ 120 LOC)

- Backend: In `game_manager.py`, handle a new `use_help` event with a payload like `{ type: '5050' }`.
- Backend: Verify the player has this help available (requires adding `helpsRemaining` to the player model in `game_manager` or `models/player.py` if it exists).
- Backend: If available, randomly select two incorrect answer options for the current question. Emit an event like `help_used_5050` back to the requesting client, with the indexes of the two options to be removed: `{ removed_options: [index1, index2] }`. Decrement the player's available "50/50" helps.
- Frontend: In the Next.js `Question.tsx` component, add a "50/50" button.
- Frontend: On click, emit `use_help: { type: '5050' }`. Disable the button after use or if unavailable.
- Frontend: Listen for `help_used_5050`. When received, update the UI to disable or visually hide the specified incorrect answer options.

**Validation:**

- Clicking the "50/50" button on the frontend disables/hides two incorrect answer options. The correct answer and one other incorrect option remain.
- The button becomes unavailable after one use (or as per game rules).
- Backend logs show the help being used and the correct options being identified for removal.

### Phase 6.2 — "Call a Friend" Stub

**Goal:** Wire up the "Call a Friend" help feature, initially returning a stubbed hint from the backend without making a real LLM API call.

**Tasks** (≈ 100 LOC)

- Backend: Create `helpers/llm_client.py`. Implement a stub function `get_call_friend_advice(question_text, options)` that returns a hard-coded hint string (e.g., "I'm not sure, but option C looks suspicious!").
- Backend: In `game_manager.py`, handle `use_help: { type: 'callFriend' }`. Verify availability.
- Backend: Call the stubbed `llm_client.get_call_friend_advice()` with the current question's details.
- Backend: Emit an event like `help_used_call_friend` back to the client with the hint: `{ hint: "some advice" }`. Decrement availability.
- Frontend: In `Question.tsx`, add a "Call a Friend" button.
- Frontend: On click, emit `use_help: { type: 'callFriend' }`. Disable appropriately.
- Frontend: Listen for `help_used_call_friend`. Display the received `hint` in a small, temporary overlay or a dedicated area in the UI.

**Validation:**

- Clicking the "Call a Friend" button displays the predefined stubbed hint on the UI.
- The button becomes unavailable after use.
- Backend logs show the stub function being called and the hint being sent.

## Milestone 7: Chat, Emoji & Double-Score

### Phase 7.1 — In-Game Chat & Emoji

**Goal:** Implement a real-time chat system allowing players within the same game room to send and receive text messages and basic emojis.

**Tasks** (≈ 140 LOC)

- Backend: Create `chat.py`. This module will handle chat-related Socket.IO events.
- Backend: In `app.py` or `game_manager.py` (if chat is room-specific), handle `send_chat_message` (payload: `{ text: string }`) and potentially `send_emoji` (payload: `{ emoji_code: string }`).
- Backend: When a message/emoji is received, `chat.py` should rebroadcast it as a `new_chat_message` event to all clients in the same game room. The payload should include the sender's ID/name and the message content.
- Frontend: Create a `ChatBox.tsx` component (e.g., `src/components/Chat/ChatBox.tsx`) for the Next.js game page. This component will have an input field for typing messages and an area to display received messages.
- Frontend: Implement sending `send_chat_message` when the user submits text.
- Frontend: Listen for `new_chat_message` and append new messages to the display area, showing sender and content.
- Frontend: (Optional) Add a simple `EmojiPicker.tsx` component that allows users to select from a predefined set of emojis, which then get sent via `send_emoji` or as text.

**Validation:**

- Clients in the same game room can send text messages, and all other clients in that room see the messages appear in their chat UI with sender identification.
- If emoji support is added, selected emojis are also broadcast and displayed.
- Chat messages do not interfere with game progression.

### Phase 7.2 — Double Score Help

**Goal:** Implement the "Double Score" help feature, allowing a player to double the points earned for their next correctly answered question.

**Tasks** (≈ 100 LOC)

- Backend: In `game_manager.py`, handle `use_help: { type: 'doubleScore' }`. Verify availability.
- Backend: Set a flag (e.g., `player.usedDoubleScoreNext = true`) for the requesting player in their server-side state. Decrement availability.
- Backend: In the scoring logic within `game_manager` (Phase 4.1), when calculating points for a correct answer, check if this flag is set for the player. If `true`, multiply their earned points for that question by 2, and then reset the flag to `false`.
- Frontend: In `Question.tsx`, add a "Double Score" button.
- Frontend: On click, emit `use_help: { type: 'doubleScore' }`. Disable appropriately.
- Frontend: Optionally, provide visual feedback that "Double Score" is active for their next answer (e.g., an icon near their score or name).

**Validation:**

- After a player uses "Double Score" and then answers the next question correctly, their score update reflects double the usual points for that question.
- The double score effect applies only to the one question immediately following the use of the help.
- The button becomes unavailable after use.

## Milestone 8: Final Polishing & Deployment

### Phase 8.1 — Leaderboard & Game-Over Screen

**Goal:** Clearly display the final game results and standings to all players when the game concludes.

**Tasks** (≈ 80 LOC)

- Backend: In `game_manager.py`, after the last question is completed (e.g., 10th question answered or timed out), determine the end of the game.
- Backend: Compile a list of all players with their final scores. Sort this list in descending order of score.
- Backend: Emit a `game_over` event to all players in the game room. The payload should include the sorted leaderboard data (e.g., `[{ name, score, rank }, ...]`).
- Frontend: In the Next.js game page, listen for the `game_over` event.
- Frontend: Create a `Leaderboard.tsx` component (e.g., `src/components/Game/Leaderboard.tsx`). When `game_over` is received, display this component, showing the final player names, scores, and rankings, possibly with special styling for the winner(s). This might replace the main game UI.

**Validation:**

- After the final question, all clients in the game receive the `game_over` event.
- A leaderboard is displayed showing all players, their final scores, sorted correctly, and potentially highlighting the winner.
- The game interface might transition to this leaderboard view.

### Phase 8.2 — Docker, Scaling & CI

**Goal:** Containerize both backend and frontend applications for consistent deployment and set up basic Continuous Integration checks.

**Tasks** (≈ 150 LOC)

- Backend: Write a `Dockerfile` for the Python/Flask-SocketIO backend. This should install dependencies from `requirements.txt` and define how to run the application (e.g., using `gunicorn` with `eventlet` or `gevent` workers for Socket.IO).
- Frontend: Write a `Dockerfile` for the Next.js frontend. This will typically involve a multi-stage build:
  - A build stage to install Node.js, copy `package.json`, install dependencies (`npm install`), copy source code, and run the build script (`npm run build`).
  - A smaller production stage that copies the build output (the `.next` directory and `node_modules` if using a standalone Next.js server, or static assets if exporting) from the build stage and defines the `CMD` to run the Next.js application (e.g., `npm run start`).
- CI: Add a basic CI pipeline (e.g., using GitHub Actions).
  - For backend: Lint Python code (e.g., with `flake8`), run unit tests (if any written by this point).
  - For frontend: Lint TypeScript/JS code (e.g., with `eslint`), run unit tests (if any).
  - Optionally, add steps to build Docker images to verify Dockerfiles are correct.

**Validation:**

- `docker build . -f backend/Dockerfile` successfully builds the backend image.
- `docker build . -f frontend/Dockerfile` successfully builds the Next.js frontend image.
- Both containers can be run locally (e.g., with `docker run`).
- The CI pipeline (e.g., GitHub Actions workflow) runs successfully on code pushes or pull requests, performing linting and build checks.

### Phase 8.3 — Persistence & Analytics (Stretch)

**Goal:** (Stretch Goal) Log completed game sessions and player scores to a simple database for later review or analytics.

**Tasks** (≈ 200 LOC)

- Backend: Choose a simple database (e.g., SQLite for ease of setup, or PostgreSQL for more features). Add the necessary Python library (e.g., `psycopg2-binary` for Postgres, `sqlite3` is built-in) to `requirements.txt`.
- Backend: Define basic database models/schemas for `GameSession` (e.g., `game_id`, `start_time`, `end_time`) and `PlayerScoreInGame` (e.g., linking to `GameSession`, `player_id`, `final_score`, `rank`).
- Backend: In `game_manager.py`, after the `game_over` event is emitted (or as part of that process), write the game session details and each player's final score to the database.
- Backend: Set up basic database connection handling in `app.py` or a separate `db.py` module.

**Validation:**

- After a game completes, new records corresponding to that game session and the participating players' scores appear in the database.
- It's possible to query the database (e.g., using a DB browser for SQLite or `psql` for Postgres) and retrieve information about past games.
- The application continues to function correctly even if database writes fail (graceful error handling).

## Throughout this process:

- Keep each PR focused on one phase (≲ 200 LOC delta ideally, but can be flexible if a logical unit is slightly larger).
- After each phase, perform thorough manual end-to-end testing of the newly added feature in isolation, using the defined validation criteria.
- Only merge PRs when the developer and ideally a peer or test client confirm that the validation criteria are met and the feature works as expected.

## General Considerations & Potential Improvements

- **Configuration Management**: Early on (Milestone 1 or 2), establish a clear strategy for managing configurations (e.g., `config.py` for backend, environment variables for Next.js via `next.config.js` or `.env` files) for settings like API keys, database URLs, lobby timeout, question duration.
- **Error Handling**: Continuously implement robust error handling on both client (Next.js) and server (Flask) sides. This includes handling socket disconnections, invalid event payloads, unexpected game states, API failures (for LLM later), and database errors (if persistence is added). Validation criteria should implicitly cover some of this, but dedicated thought is needed.
- **User Authentication/Identification**: While `request.sid` is used initially, consider how players will be identified more persistently if features like user accounts or cross-session leaderboards are envisioned for the future. This could be a separate, later milestone.
- **Automated Testing**: While "Validation" sections guide manual checks, progressively add automated tests:
  - Backend: Unit tests for `game_manager` logic, `question_provider`, `bot_player`, `matchmaking` rules. Integration tests for Socket.IO event handling.
  - Frontend: Unit/integration tests for Next.js components and hooks using Jest and React Testing Library. Mock `socket.ts` for testing components that interact with Socket.IO.
    This fits well with making Phase 8.2 (CI) more meaningful.
- **Scalability of In-Memory Structures**: The in-memory lobby queue and game state in `game_manager` are suitable for initial development. If scaling to many concurrent users is a future goal, these might need to be backed by a distributed store like Redis. This is a consideration for future architecture, not immediate planning.
- **Accessibility (a11y) & UX**: For the Next.js frontend, continuously apply accessibility best practices (semantic HTML, ARIA attributes, keyboard navigation) and focus on good user experience (clear feedback, intuitive controls, responsive design).
- **Next.js Specifics**: Leverage Next.js features where appropriate:
  - API Routes (`pages/api/*`) could be used for auxiliary RESTful endpoints if needed, though primary communication is via Socket.IO.
  - Image optimization (`next/image`), routing enhancements, SSR/SSG (though less critical for a heavily dynamic Socket.IO app, could be used for landing pages or profiles).
