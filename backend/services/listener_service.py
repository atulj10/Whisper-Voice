import threading
from pynput import keyboard
from services.audio_service import AudioService
from services.transcription_service import TranscriptionService
from services.clipboard_service import ClipboardService
from utils.logger import get_logger

logger = get_logger(__name__)


class ListenerService:
    def __init__(self):
        self.is_active = False
        self.listener_thread = None
        self.audio_service = AudioService()
        self.transcription_service = TranscriptionService()
        self.clipboard_service = ClipboardService()
        self._ctrl_pressed = False
        self._space_pressed = False
        self._controller = None

    def start_listener(self) -> dict:
        if self.is_active:
            logger.warning("Listener is already active")
            return {"status": "error", "message": "Listener is already active"}
        
        self.is_active = True
        self._ctrl_pressed = False
        self._space_pressed = False
        self.listener_thread = threading.Thread(target=self._run_listener, daemon=True)
        self.listener_thread.start()
        logger.info("Listener started")
        return {"status": "success", "message": "Listener started successfully"}

    def stop_listener(self) -> dict:
        if not self.is_active:
            logger.warning("Listener is not active")
            return {"status": "error", "message": "Listener is not active"}
        
        self.is_active = False
        if self._controller:
            self._controller.stop()
            self._controller = None
        
        logger.info("Listener stopped")
        return {"status": "success", "message": "Listener stopped successfully"}

    def _run_listener(self):
        def on_press(key):
            try:
                is_ctrl = key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r
                is_space = key == keyboard.Key.space
                
                if is_ctrl:
                    self._ctrl_pressed = True
                    logger.info("Ctrl key pressed")
                if is_space:
                    self._space_pressed = True
                    logger.info("Space key pressed")
                
                if self._ctrl_pressed and self._space_pressed:
                    self.audio_service.start_recording()
                    logger.info("Hotkey pressed - recording started")
            except Exception as e:
                logger.error(f"Error in on_press: {e}")

        def on_release(key):
            try:
                is_ctrl = key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r
                is_space = key == keyboard.Key.space
                
                if is_ctrl:
                    self._ctrl_pressed = False
                    logger.info("Ctrl key released")
                if is_space:
                    self._space_pressed = False
                    logger.info("Space key released")
                
                if not self._space_pressed and self.audio_service.is_recording:
                    try:
                        audio_path = self.audio_service.stop_recording()
                        text = self.transcription_service.transcribe(audio_path)
                        self.clipboard_service.copy_to_clipboard(text)
                        logger.info("Recording processed and copied to clipboard")
                    except Exception as e:
                        logger.error(f"Error processing recording: {e}")
            except Exception as e:
                logger.error(f"Error in on_release: {e}")

        self._controller = keyboard.Listener(on_press=on_press, on_release=on_release)
        self._controller.start()
        self._controller.join()
