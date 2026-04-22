import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DB_USER     = os.getenv('POSTGRES_USER',     'postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
DB_HOST     = os.getenv('POSTGRES_HOST',     'localhost')
DB_PORT     = os.getenv('POSTGRES_PORT',     '5432')
DB_NAME     = os.getenv('POSTGRES_DB',       'tcc_health')

DATABASE_URL       = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()


class FHIRObservation(Base):
    __tablename__ = 'fhir_observations'

    id                 = Column(Integer, primary_key=True, autoincrement=True)
    resource_id        = Column(String, unique=True, index=True)
    patient_id         = Column(String, index=True)
    code               = Column(String, index=True)
    effective_datetime = Column(DateTime, nullable=False, index=True, primary_key=True)
    resource_json      = Column(JSONB, nullable=False)


# --- Sync engine (used by the FHIR worker) ---

_sync_engine = None

def get_engine():
    global _sync_engine
    if _sync_engine is None:
        _sync_engine = create_engine(
            DATABASE_URL,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_timeout=30,
        )
    return _sync_engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def init_db():
    engine = get_engine()
    try:
        Base.metadata.create_all(engine)
        print("Database tables created.")
        with engine.connect() as conn:
            try:
                conn.execute(text(
                    "SELECT create_hypertable('fhir_observations', 'effective_datetime', "
                    "if_not_exists => TRUE);"
                ))
                conn.commit()
                print("Converted fhir_observations to hypertable.")
            except Exception as e:
                print(f"Hypertable creation skipped: {e}")
    except Exception as e:
        print(f"Database initialization failed: {e}")


# --- Async engine (used by the FastAPI API) ---

# 8 workers × 20 connections = 160 total, safely under max_connections=300
_async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_timeout=30,
)

AsyncSessionLocal = async_sessionmaker(
    _async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
