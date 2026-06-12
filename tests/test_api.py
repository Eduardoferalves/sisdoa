from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from sisdoa.api.deps import get_db
from sisdoa.api.main import app
from sisdoa.infrastructure.api_gateway import ProductFetchError, ProductNotFoundError
from sisdoa.repository.database import Database



class TestCreateDonation:
    """Test suite for POST /donations/ endpoint."""

    def test_create_donation_with_name_success(self, client: TestClient) -> None:
        """Create donation item using explicit name in body."""
        payload = {
            "name": "Arroz 5kg",
            "quantity": 10,
            "expiration_date": (date.today() + timedelta(days=30)).isoformat(),
        }
        response = client.post("/donations/", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["id"] is not None
        assert data["name"] == "Arroz 5kg"
        assert data["quantity"] == 10
        assert data["expiration_date"] == payload["expiration_date"]

    def test_create_donation_without_name_and_ean_raises_400(self, client: TestClient) -> None:
        """Creating donation without name and without ean query parameter should raise 400."""
        payload = {
            "quantity": 5,
            "expiration_date": (date.today() + timedelta(days=10)).isoformat(),
        }
        response = client.post("/donations/", json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.json()["detail"]

    @patch("sisdoa.infrastructure.api_gateway.OpenFoodFactsGateway.fetch_product_name")
    def test_create_donation_with_ean_success(
        self, mock_fetch_name: patch, client: TestClient
    ) -> None:
        """Create donation item using EAN to fetch product name."""
        mock_fetch_name.return_value = "Feijão Preto 1kg"
        payload = {
            "quantity": 20,
            "expiration_date": (date.today() + timedelta(days=60)).isoformat(),
        }
        response = client.post("/donations/?ean=7891010101010", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Feijão Preto 1kg"
        mock_fetch_name.assert_called_once_with("7891010101010")

    @patch("sisdoa.infrastructure.api_gateway.OpenFoodFactsGateway.fetch_product_name")
    def test_create_donation_with_ean_not_found(
        self, mock_fetch_name: patch, client: TestClient
    ) -> None:
        """Create donation item with EAN that is not found (404)."""
        mock_fetch_name.side_effect = ProductNotFoundError("1111111111111")
        payload = {
            "quantity": 5,
            "expiration_date": (date.today() + timedelta(days=10)).isoformat(),
        }
        response = client.post("/donations/?ean=1111111111111", json=payload)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "não foi encontrado" in response.json()["detail"]

    @patch("sisdoa.infrastructure.api_gateway.OpenFoodFactsGateway.fetch_product_name")
    def test_create_donation_with_ean_fetch_error(
        self, mock_fetch_name: patch, client: TestClient
    ) -> None:
        """Create donation item with EAN that causes a network/timeout error (503)."""
        mock_fetch_name.side_effect = ProductFetchError("Erro de conexão")
        payload = {
            "quantity": 5,
            "expiration_date": (date.today() + timedelta(days=10)).isoformat(),
        }
        response = client.post("/donations/?ean=1111111111111", json=payload)
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert "Erro de conexão" in response.json()["detail"]


class TestListDonations:
    """Test suite for GET /donations/ endpoints."""

    def test_list_donations_empty(self, client: TestClient) -> None:
        """Get all donations when DB is empty."""
        response = client.get("/donations/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_donations_with_items(self, client: TestClient, sample_item) -> None:
        """Get all donations and verify the sample item is returned."""
        response = client.get("/donations/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == sample_item.id
        assert data[0]["name"] == sample_item.name

    def test_list_expired_donations(self, client: TestClient, expired_item, sample_item) -> None:
        """Get only expired donations."""
        response = client.get("/donations/expired")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == expired_item.id
        assert data[0]["name"] == expired_item.name
        # Verify that non-expired sample_item is filtered out
        assert not any(item["id"] == sample_item.id for item in data)
