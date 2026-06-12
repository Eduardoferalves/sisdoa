"""Database repository for SisDoa - CRUD operations."""

from __future__ import annotations

from datetime import date

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from sisdoa.config import DATABASE_URL
from sisdoa.domain.models import Base, DonationItem


class Database:
    """Database connection and session manager.

    This class handles the SQLite connection and provides
    a session factory for database operations.
    """

    def __init__(self, db_url: str = DATABASE_URL) -> None:
        """Initialize database connection.

        Args:
            db_url: SQLAlchemy database URL. Defaults to SQLite file.
        """
        engine_kwargs = {}
        if db_url.startswith("sqlite"):
            engine_kwargs["connect_args"] = {"check_same_thread": False}
        elif db_url.startswith("postgresql"):
            engine_kwargs["poolclass"] = NullPool
            engine_kwargs["pool_pre_ping"] = True

        self.engine = create_engine(db_url, echo=False, **engine_kwargs)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._create_tables()

    def _create_tables(self) -> None:
        """Create all tables if they don't exist."""
        if self.engine.dialect.name == "sqlite":
            Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """Get a new database session.

        Returns:
            SQLAlchemy Session object.
        """
        return self.SessionLocal()


class DonationItemRepository:
    """Repository for DonationItem CRUD operations.

    This class encapsulates all database operations related
    to donation items, keeping the CLI layer free of DB logic.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session.

        Args:
            session: SQLAlchemy session instance.
        """
        self.session = session

    def create(self, name: str, quantity: int, expiration_date: date) -> DonationItem:
        """Create a new donation item.

        Args:
            name: Item name.
            quantity: Number of units.
            expiration_date: Item expiration date.

        Returns:
            The newly created DonationItem.
        """
        item = DonationItem(
            name=name,
            quantity=quantity,
            expiration_date=expiration_date,
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def get_by_id(self, item_id: int) -> DonationItem | None:
        """Get a donation item by ID.

        Args:
            item_id: The item's primary key.

        Returns:
            DonationItem if found, None otherwise.
        """
        stmt = select(DonationItem).where(DonationItem.id == item_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_all(self) -> list[DonationItem]:
        """Get all donation items.

        Returns:
            List of all DonationItem records.
        """
        stmt = select(DonationItem).order_by(DonationItem.expiration_date)
        return list(self.session.execute(stmt).scalars().all())

    def get_near_expiration(self, threshold_days: int = 7) -> list[DonationItem]:
        """Get items near their expiration date.

        Args:
            threshold_days: Days to consider as "near expiration".

        Returns:
            List of DonationItem records expiring within threshold.
        """
        stmt = select(DonationItem).order_by(DonationItem.expiration_date)
        items = self.session.execute(stmt).scalars().all()
        return [item for item in items if item.days_until_expiration() <= threshold_days]

    def update_quantity(self, item_id: int, quantity_delta: int) -> DonationItem | None:
        """Update item quantity (add or remove).

        Args:
            item_id: The item's primary key.
            quantity_delta: Amount to add (positive) or remove (negative).

        Returns:
            Updated DonationItem if successful, None if item not found.

        Raises:
            ValueError: If resulting quantity would be negative.
        """
        stmt = select(DonationItem).where(DonationItem.id == item_id)
        item = self.session.execute(stmt).scalar_one_or_none()
        if item is None:
            return None

        new_quantity = item.quantity + quantity_delta
        if new_quantity < 0:
            raise ValueError(
                f"Insufficient stock: cannot remove {abs(quantity_delta)} units "
                f"from item with {item.quantity} units"
            )

        item.quantity = new_quantity
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, item_id: int) -> bool:
        """Delete a donation item.

        Args:
            item_id: The item's primary key.

        Returns:
            True if item was deleted, False if not found.
        """
        item = self.get_by_id(item_id)
        if item is None:
            return False

        self.session.delete(item)
        self.session.commit()
        return True

    def get_expired(self) -> list[DonationItem]:
        """Get all expired items.

        Returns:
            List of DonationItem records that have already expired.
        """
        stmt = select(DonationItem).order_by(DonationItem.expiration_date)
        items = self.session.execute(stmt).scalars().all()
        return [item for item in items if item.days_until_expiration() < 0]
