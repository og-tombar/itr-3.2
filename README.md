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
- **Frontend**: Next.js + Socket.IO client

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
├── pages/
│   ├── _app.tsx
│   ├── _document.tsx
│   └── index.tsx
│   └── game/[gameId].tsx
├── public/
│   └── ... static assets ...
├── src/
│   ├── components/
│   │   ├── Lobby/
│   │   │   ├── Lobby.tsx
│   │   │   └── Lobby.css
│   │   ├── Game/
│   │   │   ├── Question.tsx
│   │   │   ├── Scoreboard.tsx
│   │   │   └── Leaderboard.tsx
│   │   ├── Chat/
│   │   │   ├── ChatBox.tsx
│   │   │   └── EmojiPicker.tsx
│   │   └── Shared/
│   │       ├── Timer.tsx
│   │       └── Button.tsx
│   ├── contexts/
│   │   ├── LobbyContext.tsx
│   │   └── GameContext.tsx
│   ├── hooks/
│   │   └── useSocketEvent.ts
│   ├── services/
│   │   └── api.ts
│   ├── styles/
│   │   └── globals.css
│   └── socket.ts
├── next.config.js
└── package.json
```

- **`pages/_app.tsx`**: Custom App component to initialize pages, global CSS, and contexts. Ideal place to initialize the Socket.IO client if needed globally.
- **`pages/_document.tsx`**: Custom Document to augment `<html>` and `<body>` tags.
- **`pages/index.tsx`**: Main landing page, likely containing the Lobby UI.
- **`pages/game/[gameId].tsx`**: Dynamic route for the game interface, using Next.js file-system routing.
- **`public/`**: Directory for static assets like images, fonts.
- **`src/socket.ts`**
  - Exports a singleton `socket = io(…)` for reuse.
- **`src/contexts/LobbyContext.tsx`**
  - Tracks lobby state: joined players list, countdown timer.
- **`src/contexts/GameContext.tsx`**
  - Holds game state: current question, options, timers, score, helps, chat messages.
- **`src/hooks/useSocketEvent.ts`**
  - Custom hook: `useSocketEvent(event, handler)` handles subscribe/unsubscribe.
- **`src/services/api.ts`**
  - (Optional) REST calls for preloading question bank or user profiles. Can also be handled by Next.js data fetching methods (`getServerSideProps`, `getStaticProps`) if appropriate.
- **`src/components/Lobby/`**
  - **`Lobby.tsx`**: UI to join and show waiting players + countdown. Displayed via `pages/index.tsx`.
- **`src/components/Game/`**
  - **`Question.tsx`**: Renders question text, options, help buttons. Triggers `socket.emit('submit_answer', …)` and `socket.emit('use_help', …)`.
  - **`Scoreboard.tsx`**: Live updating scores.
  - **`Leaderboard.tsx`**: Final results after 10 questions.
    (Components above are rendered within `pages/game/[gameId].tsx`)
- **`src/components/Chat/`**
  - **`ChatBox.tsx`**: Message list + input.
  - **`EmojiPicker.tsx`**: Small emoji selection grid.
- **`src/components/Shared/`**
  - **`Timer.tsx`**: Countdown timer component.
  - **`Button.tsx`**: Styled button with loading/disabled states.

### Frontend:

- Build static bundle served by CDN.
- Deploy as a Next.js application (e.g., via Vercel, or as a Node.js server).

### Persistence (future):

- Store game logs in database for analytics.

## 8. Testing Strategy

- **Unit Tests**:
  - `question_provider`, `game_manager` logic, `bot_player` behavior—no socket.
- **Integration Tests**:
  - Spawn a test Socket.IO server; simulate clients joining, answering, and using helps.
- **Frontend Tests**:
  - Jest + React Testing Library; mock `src/socket.ts` to emit and receive events. Test Next.js specific features like routing and data fetching as needed.

## 9. Next Steps & Extensions

- Authentication & Profiles (persist player stats).
- Persistent Question Store (database with categories).
- Spectator Mode (watch ongoing games).
- Mobile-Friendly UI and Accessibility improvements.
- Leaderboards & Achievements across sessions.

This design balances simplicity with clear separation of concerns, allowing parallel development of backend modules and frontend components. Each module can be independently tested and extended.
