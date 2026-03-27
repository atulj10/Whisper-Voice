import pyperclip
import pyautogui
import time
from utils.logger import get_logger

logger = get_logger(__name__)


class ClipboardService:
    @staticmethod
    def copy_and_paste(text: str) -> bool:
        try:
            if not text or not text.strip():
                logger.error("Clipboard copy failed: empty text")
                raise ValueError("Text cannot be empty")
            
            pyperclip.copy(text)
            logger.info("Text copied to clipboard successfully")
            
            time.sleep(0.1)
            pyautogui.hotkey("ctrl", "v")
            logger.info("Text pasted successfully")
            
            return True
        except ValueError as e:
            logger.error(f"Clipboard validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to copy/paste: {e}")
            raise
