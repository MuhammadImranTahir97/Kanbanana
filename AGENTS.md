# AGENTS.md

Instructions for AI coding agents working on **Kanbanana**.

## Start here

- Read `_docs/specs.md` before changing anything. It is the source of truth.
- Build only what the spec describes. Skip everything under "Not in this version".

## Project layout

| Folder      | What's inside                  |
|-------------|--------------------------------|
| `frontend/` | React + Vite app (JavaScript)  |
| `backend/`  | FastAPI app, managed with `uv` |
| `_docs/`    | Spec and other project docs    |

## Commands

| Task           | Run in      | Command                                | URL                   |
|----------------|-------------|----------------------------------------|-----------------------|
| Start frontend | `frontend/` | `npm run dev`                          | http://localhost:5173 |
| Start backend  | `backend/`  | `uv run uvicorn app.main:app --reload` | http://localhost:8000 |
| Run tests      | `backend/`  | `uv run pytest`                        |                       |

Keep these commands working. If one has to change, update this file and `README.md`.

## Frontend rules

- Put every backend call in one file: `frontend/src/api.js`.
- The backend base URL is `http://localhost:8000/api`. Read it from the `VITE_API_URL` environment variable, with that URL as the default.

## Backend rules

- Use `uv` for all Python work (`uv add`, `uv run`). Don't call `pip` directly.
- Write the tests for an endpoint first, then implement it.
- When a real database is added, go through SQLAlchemy so the database can be swapped later.
- Allow CORS requests from `http://localhost:5173`.

## Working with the developer

- The developer is new to web development and uses Windows. Terminal commands must work in PowerShell.
- Work in small steps and keep the app runnable after each one.
- After backend changes, run the tests and make sure they pass.
- When you finish a task, explain in 2–3 short, plain sentences what changed and how to try it.
