"""
Konfigurasi aplikasi backend.
"""

import os

# ── JWT Config ─────────────────────────────────────────────────────────────────
SECRET_KEY: str = os.getenv(
    "SECRET_KEY", "super-secret-key-ganti-di-production-2024"
)
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

# ── Dummy Users ────────────────────────────────────────────────────────────────
# Untuk production, ganti dengan database + hashed passwords
DUMMY_USERS: dict = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "full_name": "Administrator",
        "role": "admin",
    },
    "user": {
        "username": "user",
        "password": "user123",
        "full_name": "Regular User",
        "role": "viewer",
    },
}

# ── Data Path ──────────────────────────────────────────────────────────────────
# This file lives at backend/core/config.py → go up 3 levels to reach project root
BASE_DIR = os.path.dirname(   # project root
    os.path.dirname(          # backend/
        os.path.dirname(os.path.abspath(__file__))  # backend/core/
    )
)
DATA_CSV_PATH = os.path.join(BASE_DIR, "data", "sales_data.csv")
ML_DIR = os.path.join(BASE_DIR, "ml")
