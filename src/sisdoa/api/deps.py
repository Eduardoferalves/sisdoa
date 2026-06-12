from __future__ import annotations

from collections.abc import Generator

from sqlalchemy.orm import Session

from sisdoa.repository.database import Database


def get_db() -> Generator[Session, None, None]:
    db = Database()
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()
