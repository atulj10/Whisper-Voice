from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DATABASE_PATH

Base = declarative_base()

engine = create_engine(f"sqlite:///{DATABASE_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
        }


def init_db():
    Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
