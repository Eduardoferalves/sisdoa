"""Pytest fixtures for SisDoa tests.

This module provides fixtures for isolated testing with in-memory SQLite.
Tests using these fixtures will NOT touch the disk or affect production data.
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Generator
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from sisdoa.api.main import app, get_repository
from sisdoa.domain.models import DonationItem
from sisdoa.repository.database import Database, DonationItemRepository


@pytest.fixture
def in_memory_db_url() -> Generator[str, None, None]:
    """Provide temporary SQLite URL for tests.

    Yields:
        SQLite temp file connection string.
    """
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield f"sqlite:///{path}"
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass


@pytest.fixture
def test_db(in_memory_db_url: str) -> Database:
    """Create Database instance for tests.

    Returns a Database object configured with in-memory SQLite.
    """
    db = Database(in_memory_db_url)
    return db


@pytest.fixture
def test_repo(test_db: Database) -> DonationItemRepository:
    """Create DonationItemRepository for tests.

    Returns a repository connected to in-memory database.
    """
    return DonationItemRepository(test_db.get_session())


@pytest.fixture
def sample_item_data() -> dict:
    """Provide sample item data for tests.

    Returns:
        Dictionary with valid item data.
    """
    return {
        "name": "Arroz 5kg",
        "quantity": 10,
        "expiration_date": date.today() + timedelta(days=30),
    }


@pytest.fixture
def sample_item(test_repo: DonationItemRepository) -> DonationItem:
    """Create a sample item in the database.

    Returns a persisted DonationItem for use in tests.
    """
    return test_repo.create(
        name="Arroz 5kg",
        quantity=10,
        expiration_date=date.today() + timedelta(days=30),
    )


@pytest.fixture
def near_expiry_item(test_repo: DonationItemRepository) -> DonationItem:
    """Create an item near its expiration date.

    Returns a DonationItem expiring in 3 days.
    """
    return test_repo.create(
        name="Leite UHT",
        quantity=5,
        expiration_date=date.today() + timedelta(days=3),
    )


@pytest.fixture
def expired_item(test_repo: DonationItemRepository) -> DonationItem:
    """Create an expired item.

    Returns a DonationItem that expired 5 days ago.
    """
    return test_repo.create(
        name="Biscoito Vencido",
        quantity=3,
        expiration_date=date.today() - timedelta(days=5),
    )


@pytest.fixture
def multiple_items(test_repo: DonationItemRepository) -> list[DonationItem]:
    """Create multiple items with varying expiration dates.

    Returns a list of DonationItems for testing list/filter operations.
    """
    items = [
        test_repo.create(
            name="Arroz 5kg",
            quantity=10,
            expiration_date=date.today() + timedelta(days=60),
        ),
        test_repo.create(
            name="Feijão 1kg",
            quantity=20,
            expiration_date=date.today() + timedelta(days=5),
        ),
        test_repo.create(
            name="Macarrão 500g",
            quantity=15,
            expiration_date=date.today() + timedelta(days=365),
        ),
        test_repo.create(
            name="Leite em Pó",
            quantity=8,
            expiration_date=date.today() - timedelta(days=2),
        ),
    ]
    return items


@pytest.fixture
def client(test_db: Database) -> Generator[TestClient, None, None]:
    """Substitui o repositório real por um injetado com SQLite em memória."""

    def _override_get_repository():
        from sisdoa.repository.database import DonationItemRepository

        session = test_db.get_session()
        return DonationItemRepository(session)

    app.dependency_overrides[get_repository] = _override_get_repository

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
