"""Configuration settings for SisDoa."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Database configuration
DEFAULT_DB_NAME = "sisdoa.db"
DEFAULT_EXPIRY_THRESHOLD_DAYS = 7

# Get database URL from environment
raw_database_url = os.environ.get("DATABASE_URL")

if raw_database_url:
    if raw_database_url.startswith("postgres://"):
        DATABASE_URL = raw_database_url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif raw_database_url.startswith("postgresql://"):
        DATABASE_URL = raw_database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    else:
        DATABASE_URL = raw_database_url
else:
    # Get database path from environment or use default
    DB_PATH_ENV = os.environ.get("SISDOA_DB_PATH")

    if DB_PATH_ENV:
        DATABASE_PATH = Path(DB_PATH_ENV)
    else:
        # Default to user's home directory under .sisdoa
        DATA_DIR = Path.home() / ".sisdoa"
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        DATABASE_PATH = DATA_DIR / DEFAULT_DB_NAME

    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Expiry alert threshold (days)
EXPIRY_THRESHOLD_DAYS = int(
    os.environ.get("SISDOA_EXPIRY_THRESHOLD", DEFAULT_EXPIRY_THRESHOLD_DAYS)
)
