# Architecture Document

## System Components

### 1. Frontend (React)
- **Purpose**: User interface for initializing listener and viewing transcripts
- **Components**:
  - `InitializeListener.jsx`: Controls listener state, shows recording status
  - `TranscriptList.jsx`: Displays historical transcripts
  - `App.jsx`: Main application component

### 2. API Layer (Flask)
- **Purpose**: HTTP interface between frontend and backend services
- **File**: `api/routes.py`
- **Responsibilities**:
  - Route incoming HTTP requests
  - Return JSON responses
  - Handle error responses

### 3. Service Layer
- **Purpose**: Encapsulates all business logic
- **Services**:
  - `ListenerService`: Manages global hotkey listener lifecycle
  - `AudioService`: Handles audio recording with sounddevice
  - `TranscriptionService`: Local AI transcription using faster-whisper
  - `ClipboardService`: Copies text and auto-pastes

### 4. Repository Layer
- **Purpose**: Handles all database operations
- **File**: `repositories/transcript_repository.py`
- **Responsibilities**: CRUD operations for transcripts

### 5. Model Layer
- **Purpose**: Defines database schema
- **File**: `models/transcript.py`
- **Components**: SQLAlchemy model for transcripts table

### 6. Utility Layer
- **Purpose**: Shared utilities
- **File**: `utils/logger.py`
- **Components**: Centralized logging configuration

## Data Flow

```
User clicks "Initialize Listener"
    │
    ▼
React Component calls API
    │
    ▼
Flask Route receives request
    │
    ▼
ListenerService.start_listener()
    │
    ▼
Background thread starts pynput Listener
    │
    ▼
User presses Ctrl+Space
    │
    ▼
AudioService.start_recording() captures audio
    │
    ▼
User releases Ctrl+Space
    │
    ▼
AudioService.stop_recording() saves to WAV file
    │
    ▼
TranscriptionService.transcribe() - faster-whisper AI
    │
    ▼
ClipboardService.copy_and_paste()
    │
    ├── pyperclip.copy() - copies to clipboard
    └── pyautogui.hotkey("ctrl", "v") - auto-pastes
```

## Layer Responsibilities

### API Layer
- HTTP request handling
- Response formatting
- **DO NOT**: Contains business logic

### Service Layer
- Business logic implementation
- External service integration (whisper, pyautogui)
- Audio processing
- Clipboard + paste operations
- **DO NOT**: Direct database access

### Repository Layer
- Database CRUD operations
- Session management
- **DO NOT**: Business logic

### Model Layer
- Database schema definition
- ORM mappings
- **DO NOT**: Business logic or API

## Why This Architecture?

### 1. Separation of Concerns
Each layer has a single, well-defined responsibility. Changes to one layer don't cascade to others.

### 2. Testability
Services can be unit tested by mocking dependencies. Routes can be integration tested.

### 3. Maintainability
New features can be added by extending existing layers without modifying others.

### 4. Predictability
Clear data flow makes debugging and understanding the system straightforward.

### 5. Reusability
Services like ClipboardService can be reused without modification.

## Threading Model

```
Main Thread (Flask)
    │
    |---- API requests handled here
    |
    +---- Listener Thread (daemon)
             |
             +---- pynput Listener (hotkey detection)
             +---- sounddevice (audio recording)
             +---- faster-whisper (transcription)
             +---- pyperclip + pyautogui (paste)
```

Listener thread is `daemon=True` - terminates when main program exits.

## Key Libraries

| Library | Purpose |
|---------|---------|
| pynput | Global hotkey detection |
| sounddevice | Audio recording |
| faster-whisper | Local AI transcription |
| pyperclip | Clipboard operations |
| pyautogui | Auto-paste (Ctrl+V) |
| Flask | Web API |
| React | User interface |

## Error Handling Strategy

1. **Services**: Catch exceptions, log errors, return meaningful messages
2. **Routes**: Return appropriate HTTP status codes
3. **Repository**: Rollback transactions on failure
4. **Logging**: All errors logged with timestamps

## Validation Requirements

1. **Audio**: Must be at least 0.5 seconds duration
2. **Transcription**: Must return non-empty text
3. **Clipboard**: Must handle empty text gracefully

## Design Decisions

### Why faster-whisper over cloud APIs?

1. **Privacy**: Audio never leaves the machine
2. **No API Keys**: Free, no account needed
3. **Offline Capable**: Works without internet
4. **Optimized**: C++ implementation is fast

### Why pyautogui for paste?

- Simple cross-platform solution
- Works with any focused application
- No complex IPC needed

### Why daemon thread?

- Flask must remain responsive for API calls
- Listener should not block the main thread
- Automatic cleanup on program exit
