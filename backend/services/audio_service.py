import wave
import numpy as np
import sounddevice as sd
from pathlib import Path
from config import SAMPLE_RATE, CHANNELS, TEMP_AUDIO_PATH, MIN_AUDIO_DURATION
from utils.logger import get_logger

logger = get_logger(__name__)


class AudioService:
    def __init__(self):
        self.is_recording = False
        self.audio_data = []

    def start_recording(self) -> None:
        self.audio_data = []
        self.is_recording = True
        logger.info("Recording started")

        def callback(indata, frames, time, status):
            if status:
                logger.warning(f"Audio callback status: {status}")
            if self.is_recording:
                self.audio_data.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            callback=callback,
        )
        self.stream.start()

    def stop_recording(self) -> Path:
        self.is_recording = False

        if hasattr(self, "stream"):
            self.stream.stop()
            self.stream.close()

        if not self.audio_data:
            logger.error("No audio data recorded")
            raise ValueError("No audio data recorded")

        audio_combined = np.concatenate(self.audio_data, axis=0)
        duration = len(audio_combined) / SAMPLE_RATE

        logger.info(f"Recording stopped. Duration: {duration:.2f}s")

        if duration < MIN_AUDIO_DURATION:
            logger.error(
                f"Audio too short: {duration:.2f}s "
                f"(minimum: {MIN_AUDIO_DURATION}s)"
            )
            raise ValueError(
                f"Audio duration {duration:.2f}s is below minimum "
                f"{MIN_AUDIO_DURATION}s"
            )

        with wave.open(str(TEMP_AUDIO_PATH), "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_combined.tobytes())

        logger.info(f"Audio saved to {TEMP_AUDIO_PATH}")
        return TEMP_AUDIO_PATH

    def validate_audio_file(self, file_path: Path) -> bool:
        if not file_path.exists():
            logger.error(f"Audio file does not exist: {file_path}")
            return False
        if file_path.stat().st_size == 0:
            logger.error("Audio file is empty")
            return False
        return True
