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

_Coming soon. This section will be filled in as the app is built._
