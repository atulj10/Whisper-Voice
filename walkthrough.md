# Voice Clipboard Assistant - Technical Walkthrough

**Duration: 10-15 minutes**

---

## Introduction (1 minute)

Welcome! Today I'll walk you through the Voice Clipboard Assistant - a local desktop application that transcribes speech to text.

**What it does:**
- Press Ctrl+Space to record audio
- Speech is transcribed using local AI (faster-whisper)
- Text is automatically pasted where your cursor is
- Works in the background, even when the browser isn't focused

**Tech Stack:**
- Backend: Python Flask
- Frontend: React with Tailwind CSS
- AI: faster-whisper (local Whisper model)
- Hotkey: pynput
- Automation: pyautogui

---

## Project Structure (1 minute)

```
voice-clipboard-assistant/
├── backend/
│   ├── api/                    # HTTP endpoints
│   │   └── routes.py
│   ├── services/              # Business logic
│   │   ├── container.py        # Dependency injection
│   │   ├── listener_service.py # Hotkey management
│   │   ├── audio_service.py    # Audio recording
│   │   ├── transcription_service.py # AI transcription
│   │   └── clipboard_service.py # Copy + paste
│   ├── repositories/           # Database access
│   ├── models/                # Database schema
│   ├── schemas/               # Validation
│   ├── utils/
│   │   ├── logger.py          # Logging
│   │   └── exceptions.py       # Custom exceptions
│   └── app.py                 # Entry point
├── frontend/                  # React UI
└── README.md
```

**Key principle:** Each layer has one job. No business logic in routes, no direct DB access in services.

---

## Architecture Deep Dive (2 minutes)

### Layered Architecture

```
┌────────────────────────────────────────┐
│         API Layer (routes.py)           │  HTTP only
├────────────────────────────────────────┤
│        Service Layer (business logic)   │  What we do
├────────────────────────────────────────┤
│       Repository Layer (data access)    │  How we store
├────────────────────────────────────────┤
│        Model Layer (database schema)    │  What we store
└────────────────────────────────────────┘
```

### Data Flow

```
User presses Ctrl+Space
         │
         ▼
   pynput detects
         │
         ▼
   sounddevice records
         │
         ▼
   WAV file saved
         │
         ▼
   faster-whisper transcribes
         │
         ▼
   pyperclip copies
         │
         ▼
   pyautogui pastes
```

---

## Code Walkthrough (5 minutes)

### 1. Entry Point - app.py

```python
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from api import api_bp
from models import init_db

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api_bp)
    init_db()
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
```

**Key points:**
- CORS enabled for frontend communication
- Environment variables loaded from .env
- Blueprint registration for modular routes
- Database initialized on startup

### 2. Service Container - container.py

```python
class ServiceContainer:
    @property
    def listener_service(self) -> ListenerService:
        if self._listener_service is None:
            self._listener_service = ListenerService(
                audio_service=self.audio_service,
                transcription_service=self.transcription_service,
                clipboard_service=self.clipboard_service,
            )
        return self._listener_service
```

**Why this matters:**
- Lazy initialization (services created on demand)
- Dependency injection (easy to mock for testing)
- Single instance (singleton pattern)

### 3. Listener Service - listener_service.py

```python
def _run_listener(self):
    def on_press(key):
        if key == keyboard.Key.space and self._ctrl_pressed:
            self.audio_service.start_recording()

    def on_release(key):
        if key == keyboard.Key.space and self._recording_started:
            self._stop_recording()

    self._controller = keyboard.Listener(on_press=on_press, on_release=on_release)
    self._controller.start()
```

**Key points:**
- Runs in daemon thread (doesn't block Flask)
- Detects Ctrl+Space combination
- Starts/stops recording based on key events

### 4. Audio Service - audio_service.py

```python
def stop_recording(self) -> Path:
    if not self.audio_data:
        raise NoAudioDataError()

    audio_combined = np.concatenate(self.audio_data, axis=0)
    duration = len(audio_combined) / SAMPLE_RATE

    if duration < MIN_AUDIO_DURATION:
        raise AudioTooShortError()

    with wave.open(str(TEMP_AUDIO_PATH), "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_combined.tobytes())

    return TEMP_AUDIO_PATH
```

**Key points:**
- Validates audio duration (min 0.5s)
- Saves as WAV file (16kHz, mono, int16)
- Uses custom exceptions

### 5. Transcription Service - transcription_service.py

```python
def __init__(self):
    self.model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe(self, audio_path: Path) -> str:
    segments, _ = self.model.transcribe(str(audio_path), language="en")
    text = " ".join([s.text for s in segments]).strip()
    if not text:
        raise EmptyTranscriptionError()
    return text
```

**Why faster-whisper:**
- Runs entirely on CPU (no GPU needed)
- Optimized C++ implementation
- No API keys or internet required

### 6. Clipboard Service - clipboard_service.py

```python
def copy_and_paste(self, text: str) -> bool:
    if not text.strip():
        raise EmptyTextError()

    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    return True
```

**Key points:**
- Two-step: copy to clipboard, then paste
- pyautogui simulates Ctrl+V
- Works in any application

---

## Exception Handling (2 minutes)

### Custom Exceptions - exceptions.py

```python
class TranscriptionError(Exception):
    code = "TRANSCRIPTION_ERROR"
    message = "Transcription failed"

class EmptyTranscriptionError(TranscriptionError):
    code = "EMPTY_TRANSCRIPTION"
    message = "Transcription returned empty text"
```

**Benefits:**
- Consistent error structure across all services
- Each exception has a `code` for API responses
- Hierarchical (specific → general)

### Route Error Handling - routes.py

```python
def _error_response(error: Exception):
    error_code = getattr(error, 'code', 'INTERNAL_ERROR')
    return {"status": "error", "code": error_code, "message": str(error)}, 400

@api_bp.route("/initialize-listener", methods=["POST"])
def initialize_listener():
    try:
        return container.listener_service.start_listener(), 200
    except (ListenerAlreadyActiveError, ListenerError) as e:
        return _error_response(e)
```

**API Response format:**
```json
{
  "status": "error",
  "code": "LISTENER_ALREADY_ACTIVE",
  "message": "Listener is already active"
}
```

---

## Technical Decisions (2 minutes)

### 1. Why faster-whisper over cloud APIs?

| Factor | faster-whisper | OpenAI/Gemini |
|--------|---------------|---------------|
| Privacy | Audio stays local | Sent to servers |
| Cost | Free | API costs |
| Internet | Works offline | Requires connection |
| Speed | Fast (CPU optimized) | Depends on network |

### 2. Why daemon thread for listener?

- Flask must stay responsive for API calls
- Listener runs continuously in background
- Automatic cleanup on program exit

### 3. Why WAV format?

- Simple, universal format
- Works directly with faster-whisper
- Easy to validate (duration check)

---

## Frontend (1 minute)

### React Components

```jsx
function InitializeListener() {
  const [isActive, setIsActive] = useState(false);
  const [isRecording, setIsRecording] = useState(false);

  // Poll status every 500ms
  useEffect(() => {
    const interval = setInterval(checkStatus, 500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center">
      {/* Status indicator */}
      <div className={`w-3 h-3 rounded-full ${
        isRecording ? "bg-red-500 animate-pulse" : "bg-gray-400"
      }`} />
      {/* ... */}
    </div>
  );
}
```

**Features:**
- Real-time status updates (polling)
- Visual recording indicator (pulsing dot)
- Tailwind CSS styling
- Responsive design

---

## Testing Challenges (1 minute)

### What we CAN test:
- Clipboard service (mock pyperclip/pyautogui)
- Transcription service (mock file system)
- Route endpoints (mock services)
- Exception handling

### What we CAN'T test:
- Actual hotkey detection (requires system input)
- Audio recording (requires microphone)
- Real transcription (requires model)

### Example Test Structure:

```python
def test_clipboard_service_empty_text():
    service = ClipboardService()
    with pytest.raises(EmptyTextError):
        service.copy_and_paste("")
```

---

## Future Improvements (1 minute)

1. **Unit Tests**: Add pytest for services
2. **WebSocket**: Real-time updates instead of polling
3. **Configurable Hotkey**: Allow user to customize
4. **Multi-language**: Support non-English languages
5. **Microphone Selection**: Choose input device
6. **Transcript History**: Better persistence UI

---

## Summary (30 seconds)

We built a production-quality system with:

✅ **Clean architecture** - Layered, maintainable
✅ **Dependency injection** - Testable, flexible
✅ **Custom exceptions** - Consistent error handling
✅ **Local AI** - Privacy, no API keys
✅ **Auto-paste** - Works in any app

**The code is readable, predictable, and ready to evolve.**

---

## Questions?

Thank you for your time!
