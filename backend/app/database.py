"""Database setup.

The rest of the app never talks to SQLAlchemy directly — everything goes
through `app.storage.CardStore`. This module just wires up the engine, so
swapping SQLite for another database later means changing `DATABASE_URL`
(and the connect args below), not the storage layer's callers.
"""

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

BACKEND_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATABASE_URL = f"sqlite:///{BACKEND_DIR / 'kanbanana.db'}"
DATABASE_URL = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    from app import db_models  # noqa: F401  (registers the table on Base)

    Base.metadata.create_all(bind=engine)
