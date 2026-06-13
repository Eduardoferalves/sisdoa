from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from sisdoa.api.deps import get_db
from sisdoa.api.schemas import DonationItemCreate, DonationItemResponse
from sisdoa.domain.interfaces import DonationItemRepositoryInterface, ProductGatewayInterface
from sisdoa.domain.use_cases import (
    ListDonationsUseCase,
    ListExpiredDonationsUseCase,
    RegisterDonationUseCase,
)
from sisdoa.infrastructure.api_gateway import (
    OpenFoodFactsGateway,
    ProductFetchError,
    ProductNotFoundError,
)
from sisdoa.repository.database import DonationItemRepository

app = FastAPI(title="SisDoa API")

# Configure CORS Middleware for Local Development
# Em produção (Vercel), frontend e backend dividem a mesma origem via proxy reverso.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_repository(db: Annotated[Session, Depends(get_db)]) -> DonationItemRepositoryInterface:
    """Get repository dependency."""
    return DonationItemRepository(db)


def get_gateway() -> ProductGatewayInterface:
    """Get gateway dependency."""
    return OpenFoodFactsGateway()


def get_list_donations_use_case(
    repo: Annotated[DonationItemRepositoryInterface, Depends(get_repository)],
) -> ListDonationsUseCase:
    """Get ListDonationsUseCase dependency."""
    return ListDonationsUseCase(repo)


def get_register_donation_use_case(
    repo: Annotated[DonationItemRepositoryInterface, Depends(get_repository)],
    gateway: Annotated[ProductGatewayInterface, Depends(get_gateway)],
) -> RegisterDonationUseCase:
    """Get RegisterDonationUseCase dependency."""
    return RegisterDonationUseCase(repo, gateway)


def get_list_expired_donations_use_case(
    repo: Annotated[DonationItemRepositoryInterface, Depends(get_repository)],
) -> ListExpiredDonationsUseCase:
    """Get ListExpiredDonationsUseCase dependency."""
    return ListExpiredDonationsUseCase(repo)


@app.post("/donations/", response_model=DonationItemResponse, status_code=status.HTTP_201_CREATED)
def create_donation(
    payload: DonationItemCreate,
    use_case: Annotated[RegisterDonationUseCase, Depends(get_register_donation_use_case)],
    ean: Annotated[
        str | None, Query(description="Código de barras opcional para buscar o nome do produto")
    ] = None,
) -> DonationItemResponse:
    """Create a new donation item.

    If query parameter 'ean' is provided, fetches the product name from OpenFoodFacts.
    """
    try:
        item = use_case.execute(
            ean=ean,
            name=payload.name,
            quantity=payload.quantity,
            expiration_date=payload.expiration_date,
        )
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ProductFetchError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    return item


@app.get("/donations/", response_model=list[DonationItemResponse])
def list_donations(
    use_case: Annotated[ListDonationsUseCase, Depends(get_list_donations_use_case)],
) -> list[DonationItemResponse]:
    """Retrieve all donation items."""
    return use_case.execute()


@app.get("/donations/expired", response_model=list[DonationItemResponse])
def list_expired_donations(
    use_case: Annotated[ListExpiredDonationsUseCase, Depends(get_list_expired_donations_use_case)],
) -> list[DonationItemResponse]:
    """Retrieve all expired donation items."""
    return use_case.execute()
