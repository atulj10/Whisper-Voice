# Walkthrough Script (10-15 minutes)

## Introduction (1 minute)

Welcome to the Voice Clipboard Assistant project walkthrough.

This is a local desktop-assisted web application that allows users to:
- Initialize a global listener
- Record audio by pressing Ctrl+Space
- Have transcribed text automatically copied to clipboard

The system works even when the browser is not in focus.

---

## Project Overview (1 minute)

The project is organized into two main parts:

```
voice-clipboard-assistant/
├── backend/           # Python Flask API
└── frontend/         # React web application
```

Key features implemented:
1. Global hotkey detection using pynput
2. Audio recording using sounddevice
3. Text copying to clipboard using pyperclip
4. RESTful API with Flask
5. Clean React UI

---

## Architecture Deep Dive (3 minutes)

### Layered Architecture

We follow a strict layered architecture to ensure maintainability and testability:

```
┌─────────────────────────────────────┐
│         API Layer (Routes)          │  HTTP handling only
├─────────────────────────────────────┤
│        Service Layer                │  Business logic
├─────────────────────────────────────┤
│       Repository Layer              │  Database access
├─────────────────────────────────────┤
│         Model Layer                 │  Database schema
└─────────────────────────────────────┘
```

### Why Layered Architecture?

1. **Separation of Concerns**: Each layer has one job
2. **Testability**: Easy to mock dependencies
3. **Maintainability**: Changes isolated to specific layers
4. **Predictability**: Clear data flow

### Component Responsibilities

| Layer | File | Responsibility |
|-------|------|----------------|
| API | `api/routes.py` | HTTP requests/responses |
| Service | `services/listener_service.py` | Listener lifecycle management |
| Service | `services/audio_service.py` | Audio recording |
| Service | `services/clipboard_service.py` | Clipboard operations |
| Repository | `repositories/transcript_repository.py` | Database CRUD |
| Model | `models/transcript.py` | Database schema |

---

## Code Structure Walkthrough (4 minutes)

### Backend Entry Point

`backend/app.py`:
```python
def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    init_db()
    return app
```

- Creates Flask application
- Registers API blueprints
- Initializes database

### Listener Service

`backend/services/listener_service.py`:
```python
class ListenerService:
    def start_listener(self) -> dict:
        self.listener_thread = threading.Thread(target=self._run_listener, daemon=True)
        self.listener_thread.start()
```

Key points:
- Runs in background thread (daemon)
- Uses pynput for global hotkey detection
- Orchestrates audio, transcription, and clipboard services

### Audio Service

`backend/services/audio_service.py`:
```python
def start_recording(self) -> None:
    self.stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        callback=callback,
    )
    self.stream.start()
```

Key points:
- Uses sounddevice for audio capture
- Stores audio data in memory during recording
- Validates minimum duration (0.5s)

### Clipboard Service

`backend/services/clipboard_service.py`:
```python
def copy_to_clipboard(text: str) -> bool:
    pyperclip.copy(text)
    logger.info("Text copied to clipboard successfully")
```

Key points:
- Simple wrapper around pyperclip
- Validates non-empty text
- Comprehensive logging

---

## Technical Decisions (2 minutes)

### 1. Threading for Background Listener

**Decision**: Use Python threading with daemon threads

**Rationale**:
- Listener must run continuously
- Must not block Flask server
- Daemon threads terminate with main program

**Alternative considered**: Async/await with asyncio
- More complex for this use case
- pynput is synchronous by design

### 2. Audio Storage

**Decision**: Save to temporary WAV file

**Rationale**:
- Simple to implement
- Easy to validate
- Works with future AI integration

**Alternative considered**: In-memory processing
- Would require buffer management
- More complex validation

### 3. Hotkey Choice

**Decision**: Ctrl+Space

**Rationale**:
- Easy to press and release
- Unlikely to conflict with other applications
- Clear press/release states

---

## Current TODOs (2 minutes)

### 1. AI Transcription

Status: **NOT YET IMPLEMENTED**

Location: `backend/services/transcription_service.py`

Current implementation:
```python
def transcribe(self, audio_path: Path) -> str:
    # TODO: Call OpenAI Whisper API
    return "[Transcription placeholder - AI integration pending]"
```

Required:
- OpenAI API key
- Whisper API integration
- Error handling for API failures

### 2. Database Storage

Status: **NOT YET IMPLEMENTED**

Location: `backend/services/listener_service.py`

Required:
- Connect to repository
- Save transcript after transcription
- Handle database failures gracefully

---

## Risks and Mitigations (1 minute)

### Risk 1: Platform Compatibility
**Issue**: pynput hotkeys may not work on all platforms
**Mitigation**: Currently Windows-focused; can extend to Linux/Mac

### Risk 2: Audio Device Access
**Issue**: May fail if no microphone available
**Mitigation**: Add validation and user feedback

### Risk 3: Thread Safety
**Issue**: Multiple recordings could conflict
**Mitigation**: Single-threaded listener prevents concurrent recordings

---

## Extension Approach (1 minute)

To extend this system:

1. **Add AI Transcription**
   - Integrate OpenAI Whisper API
   - Add API key management
   - Implement retry logic

2. **Add Database Storage**
   - Connect repository to listener
   - Add status tracking
   - Implement cleanup

3. **Add Settings UI**
   - Microphone selection
   - Hotkey customization
   - Theme options

4. **Add Real-time Updates**
   - WebSocket for status
   - Live transcript display
   - Recording indicator

---

## Summary (30 seconds)

We built a small, production-quality system with:
- Clean layered architecture
- Comprehensive logging
- Error handling at all levels
- Threading for background operation
- Placeholder for AI integration

The system is ready for extension with AI transcription and database storage.
