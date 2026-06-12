from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from sisdoa.api.deps import get_db
from sisdoa.api.schemas import DonationItemCreate, DonationItemResponse
from sisdoa.infrastructure.api_gateway import (
    OpenFoodFactsGateway,
    ProductFetchError,
    ProductNotFoundError,
)
from sisdoa.repository.database import DonationItemRepository

app = FastAPI(title="SisDoa API")

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/donations/", response_model=DonationItemResponse, status_code=status.HTTP_201_CREATED)
def create_donation(
    payload: DonationItemCreate,
    db: Annotated[Session, Depends(get_db)],
    ean: Annotated[str | None, Query(description="Código de barras opcional para buscar o nome do produto")] = None,
) -> DonationItemResponse:
    """Create a new donation item.

    If query parameter 'ean' is provided, fetches the product name from OpenFoodFacts.
    """
    if ean:
        gateway = OpenFoodFactsGateway()
        try:
            product_name = gateway.fetch_product_name(ean)
        except ProductNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
        except ProductFetchError as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)) from e
    else:
        if not payload.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O campo 'name' é obrigatório quando 'ean' não é fornecido.",
            )
        product_name = payload.name

    repo = DonationItemRepository(db)
    item = repo.create(
        name=product_name,
        quantity=payload.quantity,
        expiration_date=payload.expiration_date,
    )
    return item

@app.get("/donations/", response_model=list[DonationItemResponse])
def list_donations(db: Annotated[Session, Depends(get_db)]) -> list[DonationItemResponse]:
    """Retrieve all donation items."""
    repo = DonationItemRepository(db)
    return repo.get_all()

@app.get("/donations/expired", response_model=list[DonationItemResponse])
def list_expired_donations(db: Annotated[Session, Depends(get_db)]) -> list[DonationItemResponse]:
    """Retrieve all expired donation items."""
    repo = DonationItemRepository(db)
    return repo.get_expired()
