# Software Design Document

Real-Time Multiplayer Trivia Competition

## Table of Contents

1.  [Introduction](#1-introduction)
2.  [System Overview](#2-system-overview)
3.  [Architecture](#3-architecture)
    - [Backend](#31-backend)
    - [Frontend](#32-frontend)
4.  [Data Models](#4-data-models)
5.  [Core Flows](#5-core-flows)
    - [Matchmaking & Game Start](#matchmaking--game-start)
    - [Question Loop & Scoring](#question-loop--scoring)
    - [Helps & LLM Integration](#helps--llm-integration)
    - [Chat & Emoji](#chat--emoji)
6.  [Configuration](#6-configuration)
7.  [Deployment & Scaling](#7-deployment--scaling)
8.  [Testing Strategy](#8-testing-strategy)
9.  [Next Steps & Extensions](#9-next-steps--extensions)

## 1. Introduction

This document outlines the design for a real-time, socket-driven trivia game. Human players are matched in 30-second pools, play 10 adaptive-difficulty questions, can use special "helps," and chat live. Single players are paired with 1–3 simulated bots. Technologies:

- **Backend**: Python + Flask-SocketIO
- **Frontend**: React + Socket.IO client

A software engineer can follow this doc to implement a maintainable, testable, and extensible system.

## 2. System Overview

- **Matchmaking**: Players join a "lobby." After 30 s (or once enough players join), a game is created.
- **Game Play**: 10 questions per game. Each question is timed; faster correct answers score more. Difficulty adapts per-player performance.
- **Helps**:
  - **50/50**: Remove two wrong options.
  - **Call a Friend**: Query an LLM for advice.
  - **Double Score**: Doubles points earned on that question.
- **Bots**: If < 2 humans, spawn 1–3 bots with imperfect accuracy and random delays.
- **Chat**: In-game chat + emoji support.
- **Leaderboard**: Displayed at game end with winner.

## 3. Architecture

### 3.1 Backend

```text
backend/
├── app.py
├── config.py
├── requirements.txt
├── matchmaking.py
├── game_manager.py
├── question_provider.py
├── bot_player.py
├── chat.py
├── helpers/
│   ├── llm_client.py
│   └── timers.py
└── models/
    ├── player.py
    ├── game.py
    └── question.py
```

- **`app.py`**
  - Initialize Flask + Flask-SocketIO server.
  - Load `config.py`.
  - Register socket event handlers delegating to other modules.
- **`config.py`**
  - Static settings (e.g. `MATCHMAKING_TIMEOUT=30`, API keys, default question durations).
- **`matchmaking.py`**
  - Manages a queue of waiting players.
  - Starts a countdown on the first join; on timeout or threshold, calls `game_manager.start_game(players_list)`.
- **`game_manager.py`**
  - Creates a `Game` instance (in `models/game.py`).
  - Coordinates question delivery, collects answers, computes adaptive difficulty, and tallies scores.
  - Emits socket events: `question`, `score_update`, `game_over`.
- **`question_provider.py`**
  - Loads question bank from JSON or database.
  - Exposes `get_next_question(prevCorrect: bool)` to pick question based on previous performance.
- **`bot_player.py`**
  - Defines `Bot` class with methods to simulate `submit_answer` events.
  - Randomized delay and accuracy < 100%.
  - Hooked into `game_manager` when needed.
- **`chat.py`**
  - Listens for `chat_message` and `emoji` events; broadcasts to game room.
- **`helpers/llm_client.py`**
  - Wraps calls to an LLM API (e.g., OpenAI).
  - Method `get_call_friend_advice(question, options)` returns a short hint string.
- **`helpers/timers.py`**
  - Utilities for scheduling timeouts (matchmaking countdown, question timer).
- **`models/`**
  - **`player.py`**: fields `id`, `name`, `score`, `helpsRemaining`…
  - **`question.py`**: fields `id`, `text`, `options`, `correctIndex`, `difficulty`.
  - **`game.py`**: fields `id`, `players`, `currentQuestion`, `questionHistory`, `startTime`.

### 3.2 Frontend

```text
frontend/
├── package.json
└── src/
    ├── index.tsx
    ├── socket.ts
    ├── App.tsx
    ├── contexts/
    │   ├── LobbyContext.tsx
    │   └── GameContext.tsx
    ├── services/
    │   └── api.ts
    ├── hooks/
    │   └── useSocketEvent.ts
    ├── components/
    │   ├── Lobby/
    │   ├── Game/
    │   ├── Chat/
    │   └── Shared/
    └── styles/
```

- **`socket.ts`**
  - Exports a singleton `socket = io(…)` for reuse.
- **`contexts/LobbyContext.tsx`**
  - Tracks lobby state: joined players list, countdown timer.
- **`contexts/GameContext.tsx`**
  - Holds game state: current question, options, timers, score, helps, chat messages.
- **`hooks/useSocketEvent.ts`**
  - Custom hook: `useSocketEvent(event, handler)` handles subscribe/unsubscribe.
- **`services/api.ts`**
  - (Optional) REST calls for preloading question bank or user profiles.
- **`components/Lobby/`**
  - **`Lobby.tsx`**: UI to join and show waiting players + countdown.
  - **`Lobby.css`**: Styles.
- **`components/Game/`**
  - **`Question.tsx`**: Renders question text, options, help buttons. Triggers `socket.emit('submit_answer', …)` and `socket.emit('use_help', …)`.
  - **`Scoreboard.tsx`**: Live updating scores.
  - **`Leaderboard.tsx`**: Final results after 10 questions.
- **`components/Chat/`**
  - **`ChatBox.tsx`**: Message list + input.
  - **`EmojiPicker.tsx`**: Small emoji selection grid.
- **`components/Shared/`**
  - **`Timer.tsx`**: Countdown timer component.
  - **`Button.tsx`**: Styled button with loading/disabled states.

## 4. Data Models

### Player

```typescript
interface Player {
  id: string;
  name: string;
  score: number;
  helps: {
    fiftyFifty: boolean;
    callFriend: boolean;
    doubleScore: boolean;
  };
}
```

### Question

```typescript
interface Question {
  id: string;
  text: string;
  options: string[];
  correctIndex: number;
  difficulty: "easy" | "medium" | "hard";
}
```

### Game

```typescript
interface Game {
  id: string;
  players: Player[];
  currentQuestionIndex: number;
  startTime: number; // timestamp
  questionHistory: Array<{
    question: Question;
    responses: {
      [playerId: string]: {
        time: number;
        correct: boolean;
        usedDouble: boolean;
      };
    };
  }>;
}
```

## 5. Core Flows

### Matchmaking & Game Start

1.  Client emits `join_lobby` on connect.
2.  `matchmaking.py` adds player to queue. If first player, start 30 s timer.
3.  On timer expiry or min-players reached, call `game_manager.start_game(players)`.
4.  `app.py` moves sockets into a Socket.IO "room" named after game ID.

### Question Loop & Scoring

For each of 10 questions:

1.  `game_manager` calls `question_provider.get_next_question(prevCorrect)` per player.
2.  Broadcast `new_question` with text, options, duration.
3.  Start server‐side timer; collect `submit_answer` events with timestamps.
4.  Compute points:
    ```text
    base = 1000
    timeFactor = max(0, duration - (responseTime - sendTime))
    points = floor(base * (timeFactor / duration))
    if usedDouble: points *= 2
    ```
5.  Update each player's score.
6.  After last question, broadcast `game_over` with sorted leaderboard.

### Helps & LLM Integration

- **50/50**: on client click, emit `use_help: { type: '5050' }`. Server responds with two removed indexes.
- **Call a Friend**: emit `use_help: { type: 'callFriend' }`. Server calls `llm_client.get_call_friend_advice(question, options)` and returns hint.
- **Double Score**: emit `use_help: { type: 'doubleScore' }`. Server flags player's next answer to double points.

### Chat & Emoji

- Clients emit `chat_message: { text }` or `emoji: { code }`.
- `chat.py` rebroadcasts to room with sender metadata.

## 6. Configuration

`config.py` holds:

```python
MATCHMAKING_TIMEOUT = 30 # seconds
QUESTION_DURATION = 15 # seconds per question
BOT_MIN_DELAY = 1.0 # seconds
BOT_MAX_DELAY = 5.0 # seconds
BOT_ACCURACY_RANGE = (0.6, 0.9)
LLM_API_KEY = 'your_llm_api_key_here' # Example: 'sk-...'
```

Environment variables override production credentials.

## 7. Deployment & Scaling

### Backend:

- Containerize with Docker.
- Use multiple worker processes behind a load-balancer with sticky sessions (or Redis adapter for Socket.IO).

### Frontend:

- Build static bundle served by CDN.

### Persistence (future):

- Store game logs in database for analytics.

## 8. Testing Strategy

- **Unit Tests**:
  - `question_provider`, `game_manager` logic, `bot_player` behavior—no socket.
- **Integration Tests**:
  - Spawn a test Socket.IO server; simulate clients joining, answering, and using helps.
- **Frontend Tests**:
  - Jest + React Testing Library; mock `socket.ts` to emit and receive events.

## 9. Next Steps & Extensions

- Authentication & Profiles (persist player stats).
- Persistent Question Store (database with categories).
- Spectator Mode (watch ongoing games).
- Mobile-Friendly UI and Accessibility improvements.
- Leaderboards & Achievements across sessions.

This design balances simplicity with clear separation of concerns, allowing parallel development of backend modules and frontend components. Each module can be independently tested and extended.
