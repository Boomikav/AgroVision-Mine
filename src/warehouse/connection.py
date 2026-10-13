"""
Database Connection and Engine Factory for AgroVision-Mine.
Provides unified SQLAlchemy abstraction supporting SQLite for local development
and PostgreSQL for enterprise/cloud deployments.
"""
import os
from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine, text, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Enforces SQLite foreign key constraints on every new connection.
    In SQLite, foreign key constraints are disabled by default.
    """
    if type(dbapi_connection).__module__.startswith("sqlite3"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


from src.utils.config import get_config
from src.utils.logger import setup_logger

logger = setup_logger("warehouse_connection")

_ENGINE: Optional[Engine] = None
_SESSION_FACTORY: Optional[sessionmaker] = None


def get_warehouse_db_url() -> str:
    """
    Constructs database URL based on environment or config.yaml.
    Defaults to SQLite in the database/ directory.
    """
    cfg = get_config()
    db_type = os.getenv("DB_TYPE", cfg.get("warehouse", {}).get("default_dialect", "sqlite")).lower()

    if db_type == "postgresql":
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "agrovision_dw")
        user = os.getenv("DB_USER", "postgres")
        pw = os.getenv("DB_PASSWORD", "postgres")
        url = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db_name}"
        logger.info(f"Using PostgreSQL connection: {user}@{host}:{port}/{db_name}")
        return url
    else:
        # SQLite
        sqlite_path = os.getenv(
            "DB_SQLITE_PATH",
            cfg.get("warehouse", {}).get("sqlite_path", "database/agrovision_warehouse.db")
        )
        path_obj = Path(sqlite_path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        abs_path = str(path_obj.resolve()).replace("\\", "/")
        url = f"sqlite:///{abs_path}"
        logger.info(f"Using SQLite warehouse at: {abs_path}")
        return url


def get_db_engine(echo: Optional[bool] = None) -> Engine:
    """
    Returns a singleton SQLAlchemy engine instance.
    """
    global _ENGINE
    if _ENGINE is None:
        cfg = get_config()
        should_echo = echo if echo is not None else cfg.get("warehouse", {}).get("echo_sql", False)
        db_url = get_warehouse_db_url()
        _ENGINE = create_engine(db_url, echo=should_echo, future=True)
    return _ENGINE


def get_db_session() -> Session:
    """
    Provides a new database session from the session factory.
    """
    global _SESSION_FACTORY
    if _SESSION_FACTORY is None:
        engine = get_db_engine()
        _SESSION_FACTORY = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return _SESSION_FACTORY()


def reset_db_connection() -> None:
    """Disposes active engine to release file locks / pool connections."""
    global _ENGINE, _SESSION_FACTORY
    if _ENGINE is not None:
        _ENGINE.dispose()
        _ENGINE = None
        _SESSION_FACTORY = None
