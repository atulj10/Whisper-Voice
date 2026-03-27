import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "voice_clipboard.db"

SAMPLE_RATE = 16000
CHANNELS = 1
AUDIO_FORMAT = "int16"
TEMP_AUDIO_PATH = BASE_DIR / "data" / "temp_recording.wav"
HOTKEY_KEY = "ctrl_r"

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

MIN_AUDIO_DURATION = 0.5

os.makedirs(BASE_DIR / "data", exist_ok=True)
