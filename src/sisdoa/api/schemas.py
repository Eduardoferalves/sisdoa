from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class DonationItemCreate(BaseModel):
    name: str | None = Field(
        default=None, description="Item name (optional if EAN is provided via query parameter)"
    )
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")
    expiration_date: date = Field(..., description="Expiration date of the item")


class DonationItemResponse(BaseModel):
    id: int
    name: str
    quantity: int
    expiration_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
