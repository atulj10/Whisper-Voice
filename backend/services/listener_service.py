import threading
from pynput import keyboard
from utils.logger import get_logger
from utils.exceptions import (
    ListenerAlreadyActiveError,
    ListenerNotActiveError,
    ListenerError,
)

logger = get_logger(__name__)


class ListenerService:
    def __init__(
        self,
        audio_service=None,
        transcription_service=None,
        clipboard_service=None,
    ):
        from services.audio_service import AudioService
        from services.transcription_service import TranscriptionService
        from services.clipboard_service import ClipboardService
        
        self.is_active = False
        self.listener_thread = None
        self.audio_service = audio_service or AudioService()
        self.transcription_service = transcription_service or TranscriptionService()
        self.clipboard_service = clipboard_service or ClipboardService()
        self._ctrl_pressed = False
        self._space_pressed = False
        self._recording_started = False
        self._controller = None

    def start_listener(self) -> dict:
        if self.is_active:
            logger.warning("Listener is already active")
            raise ListenerAlreadyActiveError()
        
        self.is_active = True
        self._ctrl_pressed = False
        self._space_pressed = False
        self._recording_started = False
        self.listener_thread = threading.Thread(target=self._run_listener, daemon=True)
        self.listener_thread.start()
        logger.info("Listener started")
        return {"status": "success", "message": "Listener started successfully"}

    def stop_listener(self) -> dict:
        if not self.is_active:
            logger.warning("Listener is not active")
            raise ListenerNotActiveError()
        
        self.is_active = False
        if self._controller:
            self._controller.stop()
            self._controller = None
        
        logger.info("Listener stopped")
        return {"status": "success", "message": "Listener stopped successfully"}

    def _stop_recording(self):
        self._recording_started = False
        try:
            audio_path = self.audio_service.stop_recording()
            text = self.transcription_service.transcribe(audio_path)
            self.clipboard_service.copy_and_paste(text)
            logger.info("Recording processed, copied and pasted")
        except Exception as e:
            logger.error(f"Error processing recording: {e}")

    def _run_listener(self):
        def on_press(key):
            if not self.is_active:
                return
            try:
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    self._ctrl_pressed = True
                    logger.info("Ctrl key pressed")
                
                if key == keyboard.Key.space:
                    if not self._space_pressed and self._ctrl_pressed and not self._recording_started:
                        self._space_pressed = True
                        self._recording_started = True
                        self.audio_service.start_recording()
                        logger.info("Hotkey pressed - recording started")
                    elif not self._ctrl_pressed:
                        self._space_pressed = True
            except Exception as e:
                logger.error(f"Error in on_press: {e}")

        def on_release(key):
            if not self.is_active:
                return
            try:
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    self._ctrl_pressed = False
                    logger.info("Ctrl key released")
                    if self._recording_started:
                        self._stop_recording()
                
                if key == keyboard.Key.space:
                    self._space_pressed = False
                    logger.info("Space key released")
                    if self._recording_started:
                        self._stop_recording()
            except Exception as e:
                logger.error(f"Error in on_release: {e}")

        self._controller = keyboard.Listener(on_press=on_press, on_release=on_release)
        self._controller.start()
        self._controller.join()
