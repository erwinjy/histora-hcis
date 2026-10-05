from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import settings
from hcis.domain.models import Base

def create_engine_from_settings():
    return create_engine(settings.database_url, future=True)

engine = create_engine_from_settings()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def init_db() -> None:
    Base.metadata.create_all(engine)
