"""SQLite database and SQLAlchemy setup for ScamGraph AI Phase 1."""

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Investigation(Base):
    """Investigation result persistence model for local SQLite storage."""

    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String(50), nullable=False)
    scam_probability = Column(String(50), nullable=False)
    scam_type = Column(String(100), nullable=False)
    indicators = Column(Text, nullable=False)
    entities = Column(Text, nullable=False)
    evidence = Column(Text, nullable=False)
    recommendations = Column(Text, nullable=False)
    created_at = Column(String(50), nullable=False)


DATABASE_URL = "sqlite:///./scamgraph.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create tables for the local SQLite database."""
    Base.metadata.create_all(bind=engine)
