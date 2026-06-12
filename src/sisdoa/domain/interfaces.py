from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from sisdoa.domain.models import DonationItem


class DonationItemRepositoryInterface(ABC):
    """Abstract interface defining operations for the DonationItem repository."""

    @abstractmethod
    def create(self, name: str, quantity: int, expiration_date: date) -> DonationItem:
        """Create a new donation item."""
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> DonationItem | None:
        """Get a donation item by ID."""
        pass

    @abstractmethod
    def get_all(self) -> list[DonationItem]:
        """Get all donation items."""
        pass

    @abstractmethod
    def get_near_expiration(self, threshold_days: int = 7) -> list[DonationItem]:
        """Get items near their expiration date."""
        pass

    @abstractmethod
    def update_quantity(self, item_id: int, quantity_delta: int) -> DonationItem | None:
        """Update item quantity (add or remove)."""
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        """Delete a donation item."""
        pass

    @abstractmethod
    def get_expired(self) -> list[DonationItem]:
        """Get all expired items."""
        pass


class ProductGatewayInterface(ABC):
    """Abstract interface defining external product gateway client operations."""

    @abstractmethod
    def fetch_product_name(self, ean: str) -> str:
        """Fetch product name by barcode (EAN)."""
        pass

    @abstractmethod
    def fetch_product(self, ean: str) -> dict:
        """Fetch full product details by barcode (EAN)."""
        pass
