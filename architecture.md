# Architecture Document

## System Overview

Voice Clipboard Assistant is a local desktop application that:
1. Listens for global hotkey (Ctrl+Space)
2. Records audio when hotkey is pressed
3. Transcribes speech using local AI (faster-whisper)
4. Copies and pastes text automatically

---

## System Components

### 1. Frontend (React)
- **Purpose**: User interface for initializing listener and viewing transcripts
- **Components**:
  - `InitializeListener.jsx`: Controls listener state, shows recording status
  - `TranscriptList.jsx`: Displays historical transcripts
  - `App.jsx`: Main application component

### 2. API Layer (Flask)
- **File**: `api/routes.py`
- **Responsibilities**:
  - Route incoming HTTP requests
  - Return JSON responses
  - Handle error responses with consistent format
- **DO NOT**: Contains business logic

### 3. Service Layer
- **Files**:
  - `services/container.py`: Dependency injection container
  - `services/listener_service.py`: Hotkey and recording orchestration
  - `services/audio_service.py`: Audio capture and file management
  - `services/transcription_service.py`: AI transcription
  - `services/clipboard_service.py`: Copy and paste operations
- **DO NOT**: Direct database access

### 4. Repository Layer
- **File**: `repositories/transcript_repository.py`
- **Responsibilities**: CRUD operations for transcripts

### 5. Model Layer
- **File**: `models/transcript.py`
- **Responsibilities**: SQLAlchemy model, database schema

### 6. Utility Layer
- **Files**:
  - `utils/logger.py`: Centralized logging
  - `utils/exceptions.py`: Custom exception classes

---

## Directory Structure

```
backend/
├── api/
│   └── routes.py              # HTTP endpoints
├── services/
│   ├── container.py          # Dependency injection
│   ├── listener_service.py    # Hotkey management
│   ├── audio_service.py      # Audio recording
│   ├── transcription_service.py # AI transcription
│   ├── clipboard_service.py   # Copy + paste
│   └── __init__.py
├── repositories/
│   └── transcript_repository.py
├── models/
│   └── transcript.py
├── schemas/
│   └── transcript_schema.py
├── utils/
│   ├── logger.py
│   ├── exceptions.py          # Custom exceptions
│   └── __init__.py
├── ai/
│   └── agents.md             # AI governance
├── app.py                     # Entry point
├── config.py                  # Configuration
└── requirements.txt
```

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        USER ACTION                           │
│                   Press Ctrl+Space                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     pynput Listener                          │
│              Detects hotkey combination                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   AudioService                               │
│              sounddevice records audio                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  User releases key                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  WAV file saved                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               TranscriptionService                           │
│                  faster-whisper AI                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                ClipboardService                              │
│              pyperclip + pyautogui                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Dependency Injection

### Service Container

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

**Benefits:**
- Lazy initialization (services created on demand)
- Easy mocking for unit tests
- Single source of truth for service instances

---

## Custom Exceptions

All exceptions follow a consistent hierarchy:

```python
# Base exceptions
class AudioServiceError(Exception):
    code = "AUDIO_ERROR"

class TranscriptionError(Exception):
    code = "TRANSCRIPTION_ERROR"

class ClipboardError(Exception):
    code = "CLIPBOARD_ERROR"

class ListenerError(Exception):
    code = "LISTENER_ERROR"

# Specific exceptions
class NoAudioDataError(AudioServiceError):
    code = "NO_AUDIO_DATA"

class AudioTooShortError(AudioServiceError):
    code = "AUDIO_TOO_SHORT"

class EmptyTranscriptionError(TranscriptionError):
    code = "EMPTY_TRANSCRIPTION"

class EmptyTextError(ClipboardError):
    code = "EMPTY_TEXT"
```

**API Response Format:**
```json
{
  "status": "error",
  "code": "LISTENER_ALREADY_ACTIVE",
  "message": "Listener is already active"
}
```

---

## Error Handling Strategy

### Services
- Validate inputs before processing
- Raise specific exceptions with context
- Log errors with timestamps

### Routes
```python
def _error_response(error: Exception):
    error_code = getattr(error, 'code', 'INTERNAL_ERROR')
    return {"status": "error", "code": error_code, "message": str(error)}, 400
```

### Repository
- Rollback transactions on failure
- Close sessions in finally block

---

## Threading Model

```
┌────────────────────────────────────────┐
│         Main Thread (Flask)              │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │    API Request Handler           │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
                    │
                    │ spawns
                    ▼
┌────────────────────────────────────────┐
│    Listener Thread (daemon=True)        │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │    pynput Listener               │  │
│  │    - on_press callback           │  │
│  │    - on_release callback         │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

- Daemon thread terminates when main process exits
- Non-blocking - Flask remains responsive

---

## Key Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web API framework |
| pynput | 1.7.6 | Global hotkey detection |
| sounddevice | 0.4.6 | Audio recording |
| faster-whisper | 1.0.0+ | Local AI transcription |
| pyperclip | 1.8.2 | Clipboard operations |
| pyautogui | 0.9.54+ | Auto-paste simulation |
| React | 18.2.0 | Frontend UI |
| Tailwind CSS | 3.4.17 | Styling |

---

## Validation Requirements

| Component | Validation | Error |
|-----------|------------|-------|
| Audio | Duration >= 0.5s | `AudioTooShortError` |
| Audio | Data recorded | `NoAudioDataError` |
| Transcription | Non-empty result | `EmptyTranscriptionError` |
| Clipboard | Non-empty text | `EmptyTextError` |

---

## Design Decisions

### Why faster-whisper?

| Factor | faster-whisper | Cloud APIs |
|--------|---------------|------------|
| Privacy | Audio stays local | Sent to servers |
| Cost | Free | API costs |
| Offline | Works | Requires internet |
| Speed | CPU optimized | Network dependent |

### Why dependency injection?

- Services can be mocked for testing
- Dependencies are explicit
- Easy to swap implementations

### Why custom exceptions?

- Consistent error format across all services
- Machine-readable error codes
- Hierarchical (specific → general)

---

## Layer Responsibilities Summary

| Layer | Responsibility | Access |
|-------|---------------|--------|
| API | HTTP handling | Calls services |
| Service | Business logic | Orchestrates components |
| Repository | Data access | CRUD operations |
| Model | Schema definition | Used by repository |

**Rules:**
- API never contains business logic
- Services never access database directly
- All external integrations are in services
