import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB

# Configuration
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'tcc_health')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()

class FHIRObservation(Base):
    __tablename__ = 'fhir_observations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(String, unique=True, index=True)
    patient_id = Column(String, index=True)
    code = Column(String, index=True) # Loinc code
    effective_datetime = Column(DateTime, nullable=False, index=True, primary_key=True)
    resource_json = Column(JSONB, nullable=False) # Full FHIR resource

    # Create a hypertable index on effective_datetime for TimescaleDB
    # Note: Requires manual hypertable conversion if not handled by init scripts

def get_engine():
    return create_engine(DATABASE_URL)

def init_db():
    """Initializes the database tables."""
    engine = get_engine()
    try:
        Base.metadata.create_all(engine)
        print("Database tables created.")
        
        # Convert to hypertable (TimescaleDB specific)
        with engine.connect() as conn:
            try:
                from sqlalchemy import text
                # Check if already a hypertable to prevent values
                conn.execute(text("SELECT create_hypertable('fhir_observations', 'effective_datetime', if_not_exists => TRUE);"))
                conn.commit()
                print("Converted fhir_observations to hypertable.")
            except Exception as e:
                print(f"Hypertable creation failed (might already exist or not TimescaleDB): {e}")

    except Exception as e:
        print(f"Database initialization failed: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
