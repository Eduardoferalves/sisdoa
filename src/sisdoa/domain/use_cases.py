from __future__ import annotations

from datetime import date

from sisdoa.domain.interfaces import DonationItemRepositoryInterface, ProductGatewayInterface
from sisdoa.domain.models import DonationItem


class RegisterDonationUseCase:
    """Use case to register a new donation, fetching the name from the gateway if EAN is provided."""

    def __init__(
        self, repo: DonationItemRepositoryInterface, gateway: ProductGatewayInterface
    ) -> None:
        self.repo = repo
        self.gateway = gateway

    def execute(
        self, ean: str | None, name: str | None, quantity: int, expiration_date: date
    ) -> DonationItem:
        """Register the donation record."""
        if ean:
            product_name = self.gateway.fetch_product_name(ean)
        else:
            if not name:
                raise ValueError("O campo 'name' é obrigatório quando 'ean' não é fornecido.")
            product_name = name

        return self.repo.create(
            name=product_name,
            quantity=quantity,
            expiration_date=expiration_date,
        )


class ListDonationsUseCase:
    """Use case to list donation items, with optional expiry alerts filtering."""

    def __init__(self, repo: DonationItemRepositoryInterface) -> None:
        self.repo = repo

    def execute(
        self, alerts_only: bool = False, expiry_threshold_days: int = 7
    ) -> list[DonationItem]:
        """Fetch all donation items, optionally filtering for those near/past expiry."""
        items = self.repo.get_all()
        if alerts_only:
            items = [i for i in items if i.days_until_expiration() <= expiry_threshold_days]
        return items


class ListExpiredDonationsUseCase:
    """Use case to list all expired donation items."""

    def __init__(self, repo: DonationItemRepositoryInterface) -> None:
        self.repo = repo

    def execute(self) -> list[DonationItem]:
        """Fetch all expired donation items."""
        return self.repo.get_expired()
