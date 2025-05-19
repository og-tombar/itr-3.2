## Milestone 1: Basic Project & "Hello World" Steel-Thread

### Phase 1.1 — Monorepo & Scaffolding

**Goal:** Establish the basic monorepo structure with a minimal Next.js frontend (using App Router) and a Python backend, ensuring both can be initialized.

**Tasks** (≈ 70 LOC)

- Create `backend/` folder with initial Python files:
  - `main.py`: Entry point for the Flask-SocketIO server
  - `server.py`: Core server setup with Flask and SocketIO
  - `app_manager.py`: Main application manager
  - `lobby.py`: Lobby management
  - `game_manager.py`: Game state management
  - `events.py`: Event definitions and queue
  - `questions.py`: Question management
- Initialize a new Next.js project in `frontend/` using `npx create-next-app@latest --ts`
- Organize the Next.js project to use a `src` directory structure
- Add a `README.md` at the root with clear setup instructions

**Validation:**

- Backend dependencies install successfully
- Frontend dependencies install successfully
- Both servers start without errors
- Basic Next.js page is viewable in browser

### Phase 1.2 — Socket.IO Connection Test

**Goal:** Implement a basic "ping-pong" exchange between the Next.js frontend and the Flask-SocketIO backend.

**Tasks** (≈ 100 LOC)

- Backend: In `server.py`, initialize `SocketIO` with the Flask app
- Backend: In `events.py`, define `ClientEvent` and `ServerEvent` enums for event names
- Backend: In `app_manager.py`, implement basic event handling
- Frontend: Create `src/socket.ts` to initialize and export a singleton `socket.io-client` instance
- Frontend: In `src/app/page.tsx`, implement basic socket connection and event handling

**Validation:**

- Socket connection is established successfully
- Events are properly emitted and received
- Connection status is logged appropriately

## Milestone 2: Lobby & Matchmaking

### Phase 2.1 — Lobby Management

**Goal:** Implement the lobby system for players to join and wait for a game.

**Tasks** (≈ 120 LOC)

- Backend: In `lobby.py`, implement the `Lobby` class with:
  - `add_player(sid: str)`: Add player to lobby
  - `remove_player(sid: str)`: Remove player from lobby
  - `get_players()`: Get current lobby players
  - `clear()`: Clear the lobby
- Backend: In `events.py`, add `JOIN_LOBBY` and `LOBBY_UPDATE` events
- Backend: In `server.py`, implement `handle_join_lobby` event handler
- Backend: In `app_manager.py`, implement lobby management methods
- Frontend: Create lobby UI component with join button
- Frontend: Implement lobby state management and updates

**Validation:**

- Players can join the lobby
- Lobby updates are broadcast to all players
- Player count is displayed correctly

### Phase 2.2 — Game Creation & Room Management

**Goal:** Implement automatic game creation when lobby conditions are met.

**Tasks** (≈ 180 LOC)

- Backend: In `lobby.py`, implement:
  - `TIMEOUT_SECONDS` and `MIN_PLAYERS` constants
  - Timer management with `_start_timer` and `_stop_timer`
  - `_on_timeout` and `_on_start_game` handlers
- Backend: In `events.py`, add `NEW_GAME` event
- Backend: In `game_manager.py`, implement `new_game` method
- Backend: In `app_manager.py`, implement:
  - `_new_game` method for game creation
  - `join_game` for room management
- Frontend: Implement game room joining logic
- Frontend: Add game state management

**Validation:**

- Games are created when timeout occurs or minimum players reached
- Players are moved to game rooms correctly
- Game state is properly initialized

## Milestone 3: Question Delivery & Basic UI

### Phase 3.1 — Question Management

**Goal:** Implement question delivery system.

**Tasks** (≈ 100 LOC)

- Backend: In `questions.py`, implement:
  - Question data structure
  - Question provider interface
  - Static question implementation
- Backend: In `events.py`, add `NEW_QUESTION` event
- Backend: In `game_manager.py`, implement question delivery
- Frontend: Create question display component
- Frontend: Implement question state management

**Validation:**

- Questions are delivered to game rooms
- Question display updates correctly
- Question state is managed properly

### Phase 3.2 — Answer Submission

**Goal:** Implement answer submission and validation.

**Tasks** (≈ 150 LOC)

- Backend: In `events.py`, add answer-related events
- Backend: In `game_manager.py`, implement:
  - Answer validation
  - Score tracking
  - Answer acknowledgment
- Frontend: Implement answer selection UI
- Frontend: Add answer submission handling
- Frontend: Implement answer feedback

**Validation:**

- Answers can be submitted
- Correct/incorrect feedback is provided
- Score updates are reflected

## Milestone 4: Scoring & Timer

### Phase 4.1 — Scoring System

**Goal:** Implement comprehensive scoring system.

**Tasks** (≈ 180 LOC)

- Backend: In `game_manager.py`, implement:
  - Score calculation
  - Score tracking per player
  - Score update events
- Frontend: Create scoreboard component
- Frontend: Implement score display and updates
- Frontend: Add score animations

**Validation:**

- Scores are calculated correctly
- Score updates are broadcast
- Scoreboard updates in real-time

### Phase 4.2 — Question Timer

**Goal:** Implement question timer system.

**Tasks** (≈ 160 LOC)

- Backend: In `game_manager.py`, implement:
  - Question timer management
  - Timeout handling
  - Auto-advance logic
- Frontend: Create timer component
- Frontend: Implement timer display
- Frontend: Add timer animations

**Validation:**

- Timers work correctly
- Timeouts are handled properly
- Questions advance automatically

## Milestone 5: Bots & Adaptive Difficulty

### Phase 5.1 — Bot Implementation

**Goal:** Add bot players for single-player games.

**Tasks** (≈ 180 LOC)

- Backend: In `game_manager.py`, implement:
  - Bot player creation
  - Bot answer simulation
  - Bot difficulty levels
- Frontend: Update UI to show bot players
- Frontend: Add bot indicators

**Validation:**

- Bots join games appropriately
- Bot answers are simulated
- Bot scores are tracked

### Phase 5.2 — Adaptive Difficulty

**Goal:** Implement dynamic question difficulty.

**Tasks** (≈ 140 LOC)

- Backend: In `questions.py`, implement:
  - Difficulty levels
  - Question categorization
  - Difficulty adjustment logic
- Backend: In `game_manager.py`, implement:
  - Player performance tracking
  - Difficulty selection
- Frontend: Show difficulty indicators
- Frontend: Add difficulty transitions

**Validation:**

- Difficulty adjusts based on performance
- Questions are appropriately challenging
- Difficulty changes are smooth

## Milestone 6: Help Features

### Phase 6.1 — 50/50 Help

**Goal:** Implement 50/50 help feature.

**Tasks** (≈ 120 LOC)

- Backend: In `game_manager.py`, implement:
  - Help availability tracking
  - 50/50 option elimination
  - Help usage events
- Frontend: Add 50/50 button
- Frontend: Implement option elimination
- Frontend: Add help cooldown

**Validation:**

- 50/50 works correctly
- Options are eliminated properly
- Help usage is tracked

### Phase 6.2 — Call a Friend

**Goal:** Implement Call a Friend help feature.

**Tasks** (≈ 100 LOC)

- Backend: In `game_manager.py`, implement:
  - Friend call simulation
  - Hint generation
  - Help usage tracking
- Frontend: Add Call a Friend button
- Frontend: Implement hint display
- Frontend: Add help cooldown

**Validation:**

- Hints are generated
- Help usage is tracked
- UI updates appropriately

## Milestone 7: Social Features

### Phase 7.1 — Chat System

**Goal:** Implement in-game chat.

**Tasks** (≈ 140 LOC)

- Backend: In `events.py`, add chat events
- Backend: In `game_manager.py`, implement:
  - Chat message handling
  - Message broadcasting
  - Chat room management
- Frontend: Create chat component
- Frontend: Implement message display
- Frontend: Add emoji support

**Validation:**

- Chat messages are sent/received
- Messages are displayed correctly
- Emojis work properly

### Phase 7.2 — Double Score

**Goal:** Implement double score power-up.

**Tasks** (≈ 100 LOC)

- Backend: In `game_manager.py`, implement:
  - Double score activation
  - Score multiplication
  - Power-up tracking
- Frontend: Add double score button
- Frontend: Implement score multiplier display
- Frontend: Add power-up animations

**Validation:**

- Double score works correctly
- Scores are multiplied properly
- UI updates appropriately

## Milestone 8: Final Polish

### Phase 8.1 — Game Over & Leaderboard

**Goal:** Implement game conclusion and leaderboard.

**Tasks** (≈ 80 LOC)

- Backend: In `game_manager.py`, implement:
  - Game end detection
  - Final score calculation
  - Leaderboard generation
- Frontend: Create leaderboard component
- Frontend: Implement game over screen
- Frontend: Add victory animations

**Validation:**

- Games end properly
- Leaderboard is accurate
- UI transitions smoothly

### Phase 8.2 — Deployment

**Goal:** Prepare for production deployment.

**Tasks** (≈ 150 LOC)

- Backend: Create `Dockerfile`
- Frontend: Create `Dockerfile`
- Add Docker Compose configuration
- Set up CI/CD pipeline
- Configure production environment

**Validation:**

- Docker builds succeed
- Containers run properly
- CI/CD pipeline works

### Phase 8.3 — Analytics (Stretch)

**Goal:** Add game analytics.

**Tasks** (≈ 200 LOC)

- Backend: Implement:
  - Game session logging
  - Player statistics
  - Performance metrics
- Frontend: Add:
  - Player statistics display
  - Performance graphs
  - Achievement system

**Validation:**

- Data is logged correctly
- Statistics are accurate
- UI displays properly

## Throughout Development:

- Maintain consistent error handling
- Follow established design patterns
- Keep code modular and testable
- Document all major components
- Ensure proper type hints
- Maintain clean code structure
