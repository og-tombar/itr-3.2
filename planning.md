## Milestone 1: Basic Project & “Hello World” Steel-Thread

### Phase 1.1 — Monorepo & Scaffolding

**Goal:** Get a minimal backend and frontend repo structure up and running.

**Tasks** (≈ 50 LOC)

- Create `backend/` folder with empty `app.py` and `requirements.txt`.
- Create `frontend/` with `package.json` and blank `src/index.tsx`.
- Add README with run instructions.

**Validation:**

- `pip install -r requirements.txt` succeeds.
- `npm install` succeeds.
- Both servers start without errors.

### Phase 1.2 — Socket.IO Connection Test

**Goal:** Wire up Socket.IO on both ends and emit a “ping”/“pong.”

**Tasks** (≈ 100 LOC)

- Install `flask-socketio` in backend and `socket.io-client` in frontend.
- In `app.py`, initialize `SocketIO(app)` and handle a `ping` event by replying `pong`.
- In React `index.tsx`, connect to the socket and emit `ping` on load; log `pong`.

**Validation:**

- Browser console shows `pong`, backend logs show it received `ping`.

## Milestone 2: Lobby & Matchmaking

### Phase 2.1 — `join_lobby` Event & Queue

**Goal:** Allow users to join a server-side queue.

**Tasks** (≈ 120 LOC)

- In backend: create `matchmaking.py` with an in-memory array of waiting sockets.
- Expose `join_lobby` handler to push `request.sid` into queue.
- Return a `lobby_update` event with current queue length.
- On frontend: add a “Join Lobby” button; on click emit `join_lobby` and display queue size.

**Validation:**

- Clicking “Join Lobby” updates lobby size in UI.

### Phase 2.2 — Timeout-Driven Game Creation

**Goal:** Start a game after 30 s or when ≥ 2 players.

**Tasks** (≈ 180 LOC)

- In `matchmaking.py`, when first player joins start a 30 s timer.
- If timer fires or queue length ≥ 2, call `game_manager.start_game(...)`.
- Move those sockets into a new Socket.IO room named by a UUID.
- Emit `game_started` with the room ID to each client.

**Validation:**

- Two clients see “Game started: <room-id>” after 30 s (or sooner with ≥ 2).

## Milestone 3: Question Delivery & Basic UI

### Phase 3.1 — Static Question Provider

**Goal:** Serve a hard-coded question to all room members.

**Tasks** (≈ 100 LOC)

- Create `question_provider.py` with `get_next_question()` returning a single JS object.
- In `game_manager.start_game`, immediately emit `new_question` with that object.
- On front, listen for `new_question` and render question text + options.

**Validation:**

- After game start, each client displays the same static question.

### Phase 3.2 — Answer Submission & Ack

**Goal:** Let clients pick an answer and get a confirmation.

**Tasks** (≈ 150 LOC)

- Frontend: wrap each option in a button that emits `submit_answer: { choiceIndex }`.
- Backend: in `game_manager`, handle `submit_answer`, log `{sid, choiceIndex}`, reply `answer_received`.
- UI: on `answer_received`, highlight the chosen option.

**Validation:**

- Clicking an option highlights it and backend logs the submission.

## Milestone 4: Scoring & Timer

### Phase 4.1 — Simple Scoring Logic

**Goal:** Calculate and broadcast points for each answer.

**Tasks** (≈ 180 LOC)

- In `game_manager`, record send time and receive time, compute `points = floor(1000*(duration–delta)/duration)`.
- Emit `score_update: { playerId, newScore }`.
- Front: maintain and display a per-player scoreboard.

**Validation:**

- After each answer, scoreboard updates with non-zero points.

### Phase 4.2 — Question Timer & Auto-advance

**Goal:** Enforce a question duration (e.g. 15 s) and automatically move to next question.

**Tasks** (≈ 160 LOC)

- Use `helpers/timers.py` to start a server-side timeout when emitting a question.
- On timeout, treat unanswered as zero points and emit next question.
- Front: display a countdown timer; if question switches, reset timer and UI.

**Validation:**

- Questions auto-advance after timeout; unanswered show zero.

## Milestone 5: Bots & Adaptive Difficulty

### Phase 5.1 — Bot Simulation

**Goal:** Spawn bots when < 2 humans and simulate answers.

**Tasks** (≈ 180 LOC)

- Implement `bot_player.py` with random delay between `BOT_MIN_DELAY` and `BOT_MAX_DELAY` and accuracy in `[0.6,0.9]`.
- When game starts with only one human, create 1–3 bot tasks that emit `submit_answer`.

**Validation:**

- Bots appear in the scoreboard and score roughly as expected.

### Phase 5.2 — Adaptive Question Difficulty

**Goal:** Pick next question based on previous correctness.

**Tasks** (≈ 140 LOC)

- Expand `question_provider.get_next_question(prevCorrect)` to choose from easy/medium/hard buckets.
- Pass each player's `prevCorrect` into that call.

**Validation:**

- Observe that if a player keeps answering correctly, question object's `difficulty` field moves upward.

## Milestone 6: "Helps" & LLM Stub

### Phase 6.1 — 50/50 Help

**Goal:** Implement server-side removal of two wrong options.

**Tasks** (≈ 120 LOC)

- Handle `use_help: { type: '5050' }`: compute two random wrong indexes and emit `help_5050: { removed: [i,j] }`.
- Front: on `help_5050`, disable/hide those two option buttons.

**Validation:**

- Clicking "50/50" hides two wrong answers.

### Phase 6.2 — "Call a Friend" Stub

**Goal:** Wire the LLM integration point without calling real API.

**Tasks** (≈ 100 LOC)

- In `helpers/llm_client.py`, stub `get_call_friend_advice()` to return a canned hint string.
- Handle `use_help: { type: 'callFriend' }` and emit `help_callFriend: { hint }`.
- UI: display the hint in a small overlay.

**Validation:**

- "Call a Friend" shows the stub hint.

## Milestone 7: Chat, Emoji & Double-Score

### Phase 7.1 — In-Game Chat & Emoji

**Goal:** Enable real-time chat alongside questions.

**Tasks** (≈ 140 LOC)

- In `chat.py`, handle `chat_message` and `emoji` events, rebroadcast with sender metadata.
- UI: `ChatBox` component appends messages and renders emojis.

**Validation:**

- Clients can send text and emoji; all players see them.

### Phase 7.2 — Double Score Help

**Goal:** Double the points on one question.

**Tasks** (≈ 100 LOC)

- Handle `use_help: { type: 'doubleScore' }` by flagging the next answer in `game_manager`.
- In scoring logic, if `usedDouble`, multiply points by 2.

**Validation:**

- Score update shows doubled points for that question.

## Milestone 8: Final Polishing & Deployment

### Phase 8.1 — Leaderboard & Game-Over Screen

**Goal:** Show final standings clearly.

**Tasks** (≈ 80 LOC)

- On `game_over`, emit sorted list of `{ name, score }`.
- Front: render a `Leaderboard` component with podium styling.

**Validation:**

- After Q10, all clients see the final podium.

### Phase 8.2 — Docker, Scaling & CI

**Goal:** Containerize and set up basic CI checks.

**Tasks** (≈ 150 LOC)

- Write `Dockerfile` for backend and `Dockerfile` or multi-stage build for frontend.
- Add GitHub Actions to lint, test, and build both services.

**Validation:**

- `docker build` passes.
- CI pipeline green on PR.

### Phase 8.3 — Persistence & Analytics (Stretch)

**Goal:** Log game sessions to a database.

**Tasks** (≈ 200 LOC)

- Add a simple SQLite/Postgres model for `GameLog`.
- After `game_over`, insert a record with question history and scores.

**Validation:**

- Logs appear in the DB; you can query past games.

## Throughout this process:

- Keep each PR focused on one phase (≲ 200 LOC delta).
- After each phase, run a quick sanity test: does the new feature work end-to-end in isolation?
- Only merge when both developer and a test client confirm the validation criteria.

## General Considerations & Potential Improvements

- **Configuration Management**: Consider adding a task for managing configuration (e.g., API keys, database URLs, game settings like lobby timeout, question duration) early on, perhaps in Milestone 1 or 2. This could involve environment variables or a config file.
- **Error Handling**: While not explicitly a "feature", robust error handling on both client and server (e.g., socket disconnections, invalid API responses, unexpected game states) is crucial. It might be good to weave this into the validation criteria for relevant phases or add a dedicated "Hardening/Error Handling" phase before deployment.
- **User Authentication/Identification**: The plan mentions `request.sid` and `playerId`. It might be beneficial to think about how players are identified more persistently, especially if you plan to have user accounts or leaderboards that persist beyond a single session. This could be a stretch goal or a consideration for a future version.
- **Testing Strategy**: The "Validation" sections are good for manual checks. Consider mentioning or adding tasks related to automated testing (unit tests, integration tests) as the project grows, especially for backend logic (matchmaking, game rules, scoring). This would fit well with Phase 8.2 (CI).
- **Scalability of In-Memory Queue**: Phase 2.1 mentions an "in-memory array of waiting sockets." This is fine for a small scale, but if scalability becomes a concern, this might need to be revisited (e.g., using a message queue like Redis). This is more of a future consideration than an immediate change.
- **Accessibility (a11y)**: For the frontend, it's good practice to keep accessibility in mind from the start. This isn't a specific task but a general principle when developing UI components.
