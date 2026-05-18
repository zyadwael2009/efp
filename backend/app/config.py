import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"


def _build_database_uri() -> str:
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        if database_url.startswith("postgres://"):
            return database_url.replace("postgres://", "postgresql://", 1)
        return database_url

    return f"sqlite:///{INSTANCE_DIR / 'store.db'}"


def _default_cors_origins(frontend_url: str) -> str:
    """Allow Vite dev server on either localhost or 127.0.0.1 (same machine, different browser origin)."""
    if "://localhost:" in frontend_url:
        return f"{frontend_url},{frontend_url.replace('://localhost:', '://127.0.0.1:', 1)}"
    if "://127.0.0.1:" in frontend_url:
        return f"{frontend_url},{frontend_url.replace('://127.0.0.1:', '://localhost:', 1)}"
    return frontend_url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "replace-this-in-production")
    SQLALCHEMY_DATABASE_URI = _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", _default_cors_origins(FRONTEND_URL))
    ADMIN_BOOTSTRAP_KEY = os.getenv("ADMIN_BOOTSTRAP_KEY", "")
    ADMIN_TOKEN_MAX_AGE_SECONDS = int(os.getenv("ADMIN_TOKEN_MAX_AGE_SECONDS", "86400"))
    ENABLE_ADMIN_BOOTSTRAP = os.getenv("ENABLE_ADMIN_BOOTSTRAP", "false").lower() in ("1", "true", "yes")
