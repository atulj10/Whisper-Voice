import pyperclip
from utils.logger import get_logger

logger = get_logger(__name__)


class ClipboardService:
    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        try:
            if not text or not text.strip():
                logger.error("Clipboard copy failed: empty text")
                raise ValueError("Text cannot be empty")
            
            pyperclip.copy(text)
            logger.info("Text copied to clipboard successfully")
            return True
        except ValueError as e:
            logger.error(f"Clipboard validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to copy to clipboard: {e}")
            raise
