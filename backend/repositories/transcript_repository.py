from typing import List
from models import Transcript, SessionLocal
from utils.logger import get_logger

logger = get_logger(__name__)


class TranscriptRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, text: str, status: str) -> Transcript:
        try:
            transcript = Transcript(text=text, status=status)
            self.db.add(transcript)
            self.db.commit()
            self.db.refresh(transcript)
            logger.info(f"Transcript created with id: {transcript.id}")
            return transcript
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create transcript: {e}")
            raise

    def get_all(self) -> List[Transcript]:
        try:
            transcripts = self.db.query(Transcript).order_by(Transcript.created_at.desc()).all()
            return transcripts
        except Exception as e:
            logger.error(f"Failed to fetch transcripts: {e}")
            raise

    def get_by_id(self, transcript_id: int) -> Transcript | None:
        try:
            return self.db.query(Transcript).filter(Transcript.id == transcript_id).first()
        except Exception as e:
            logger.error(f"Failed to fetch transcript {transcript_id}: {e}")
            raise

    def delete(self, transcript_id: int) -> bool:
        try:
            transcript = self.get_by_id(transcript_id)
            if transcript:
                self.db.delete(transcript)
                self.db.commit()
                logger.info(f"Transcript {transcript_id} deleted")
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to delete transcript {transcript_id}: {e}")
            raise

    def close(self):
        self.db.close()
