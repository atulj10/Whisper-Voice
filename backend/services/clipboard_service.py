import pyperclip
import pyautogui
import time
from utils.logger import get_logger
from utils.exceptions import EmptyTextError, ClipboardError

logger = get_logger(__name__)


class ClipboardService:
    def copy_and_paste(self, text: str) -> bool:
        if not text or not text.strip():
            logger.error("Clipboard copy failed: empty text")
            raise EmptyTextError()
        
        try:
            pyperclip.copy(text)
            logger.info("Text copied to clipboard successfully")
            
            time.sleep(0.1)
            pyautogui.hotkey("ctrl", "v")
            logger.info("Text pasted successfully")
            
            return True
        except EmptyTextError:
            raise
        except Exception as e:
            logger.error(f"Failed to copy/paste: {e}")
            raise ClipboardError(f"Failed to copy/paste: {e}")
