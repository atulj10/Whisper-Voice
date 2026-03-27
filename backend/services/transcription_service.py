from pathlib import Path
from faster_whisper import WhisperModel
from utils.logger import get_logger
from utils.exceptions import (
    TranscriptionError,
    EmptyTranscriptionError,
    AudioFileNotFoundError,
)

logger = get_logger(__name__)


class TranscriptionService:
    def __init__(self):
        logger.info("Loading Whisper model...")
        self.model = WhisperModel("base", device="cpu", compute_type="int8")
        logger.info("Whisper model loaded successfully")

    def transcribe(self, audio_path: Path) -> str:
        logger.info("Transcription started")
        
        if not audio_path.exists():
            logger.error(f"Audio file not found: {audio_path}")
            raise AudioFileNotFoundError(f"Audio file not found: {audio_path}")
        
        try:
            segments, _ = self.model.transcribe(str(audio_path), language="en")
            
            text = " ".join([segment.text for segment in segments]).strip()
            
            if not text:
                logger.warning("Transcription returned empty text")
                raise EmptyTranscriptionError()
            
            logger.info(f"Transcription succeeded: {text}")
            return text
            
        except EmptyTranscriptionError:
            raise
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise TranscriptionError(f"Transcription failed: {e}")
