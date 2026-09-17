# Kanbanana 🍌

A simple Kanban board: add cards and move them from **To Do** → **In Progress** → **Done**.

Built for Homework 2 of the [AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp) by DataTalks.Club.

## Docs

- Product spec: [`_docs/specs.md`](_docs/specs.md)
- Instructions for AI coding agents: [`AGENTS.md`](AGENTS.md)

## Tech stack

- **Frontend:** React + Vite
- **Backend:** Python + FastAPI, managed with uv
- **Database:** SQLite via SQLAlchemy
- **Tests:** pytest

## How to run

Run the backend and frontend at the same time, each in its own terminal.

### Backend

```powershell
cd backend
uv run uvicorn app.main:app --reload
```

The API is served at http://localhost:8000, with all endpoints under `/api` (e.g. http://localhost:8000/api/cards). It currently uses an in-memory mock store, so data resets whenever the server restarts. The API contract is documented in [`_docs/openapi.yaml`](_docs/openapi.yaml).

### Backend tests

```powershell
cd backend
uv run pytest
```

### Frontend

```powershell
cd frontend
npm run dev
```

The app is served at http://localhost:5173 and talks to the backend at http://localhost:8000/api by default. To point it at a different backend URL, set the `VITE_API_URL` environment variable before starting the dev server.

Start the backend first (or make sure it's already running), then start the frontend and open http://localhost:5173 in your browser.
