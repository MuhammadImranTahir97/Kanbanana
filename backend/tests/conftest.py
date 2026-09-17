"""Test setup: point the app at a temporary SQLite file instead of the real
kanbanana.db, and give every test a clean set of tables.

The env var must be set before `app.database` is imported anywhere, so this
runs at module load time, before pytest imports any test module.
"""

import os
import shutil
import tempfile
from pathlib import Path

_tmp_dir = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = f"sqlite:///{Path(_tmp_dir) / 'test_kanbanana.db'}"

import pytest  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app import db_models  # noqa: E402, F401  (registers the table on Base)


@pytest.fixture(autouse=True)
def _clean_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def pytest_sessionfinish(session, exitstatus):
    # Release the SQLite file before removing its temp directory, otherwise
    # Windows refuses to delete a file that's still open.
    engine.dispose()
    shutil.rmtree(_tmp_dir, ignore_errors=True)
