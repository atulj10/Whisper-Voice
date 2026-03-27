# Architecture Document

## System Components

### 1. Frontend (React)
- **Purpose**: User interface for initializing listener and viewing transcripts
- **Components**:
  - `InitializeListener.jsx`: Controls listener state and displays status
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
  - `TranscriptionService`: Placeholder for AI transcription
  - `ClipboardService`: Copies text to system clipboard

### 4. Repository Layer
- **Purpose**: Handles all database operations
- **File**: `repositories/transcript_repository.py`
- **Responsibilities**:
  - CRUD operations for transcripts
  - Database session management

### 5. Model Layer
- **Purpose**: Defines database schema
- **File**: `models/transcript.py`
- **Components**:
  - `Transcript`: SQLAlchemy model for transcripts table
  - Database engine and session configuration

### 6. Schema Layer
- **Purpose**: Validates input/output data
- **File**: `schemas/transcript_schema.py`
- **Components**: Pydantic models for data validation

### 7. Utility Layer
- **Purpose**: Shared utilities
- **File**: `utils/logger.py`
- **Components**: Centralized logging configuration

## Data Flow

```
User clicks "Initialize Listener"
    |
    v
React Component calls API
    |
    v
Flask Route receives request
    |
    v
ListenerService.start_listener()
    |
    v
New thread starts pynput Listener
    |
    v
User presses Ctrl+Space
    |
    v
AudioService.start_recording() begins capturing audio
    |
    v
User releases Ctrl+Space
    |
    v
AudioService.stop_recording() saves to temp file
    |
    v
TranscriptionService.transcribe() processes audio
    |
    v
ClipboardService.copy_to_clipboard() copies text
    |
    v
[Future] TranscriptRepository saves to database
```

## Layer Responsibilities

### API Layer
- HTTP request handling
- Input validation (via schemas)
- Response formatting
- **DO NOT**: Contains business logic

### Service Layer
- Business logic implementation
- External service integration
- Audio processing
- Clipboard operations
- **DO NOT**: Direct database access

### Repository Layer
- Database CRUD operations
- Session management
- Query building
- **DO NOT**: Business logic

### Model Layer
- Database schema definition
- ORM mappings
- Connection management
- **DO NOT**: Business logic or API

## Why This Architecture?

### 1. Separation of Concerns
Each layer has a single, well-defined responsibility. Changes to one layer don't cascade to others.

### 2. Testability
Services can be unit tested by mocking repositories. Routes can be integration tested by mocking services.

### 3. Maintainability
New features can be added by extending existing layers without modifying others.

### 4. Predictability
Clear data flow makes debugging and understanding the system straightforward.

### 5. Reusability
Services like ClipboardService can be used in different contexts without modification.

## Threading Model

The system uses Python's `threading` module to run the hotkey listener in the background:

```
Main Thread (Flask)
    |
    |---- API requests handled here
    |
    +---- Listener Thread (daemon)
             |
             +---- pynput Listener
             +---- Audio recording
             +---- Transcription
             +---- Clipboard copy
```

The listener thread is marked as `daemon=True`, meaning it will be terminated when the main program exits.

## Error Handling Strategy

1. **Services**: Catch exceptions, log errors, return meaningful messages
2. **Routes**: Return appropriate HTTP status codes
3. **Repository**: Rollback transactions on failure
4. **Logging**: All errors are logged with timestamps and stack traces

## Validation Requirements

1. **Audio**: Must be at least 0.5 seconds duration
2. **Transcription**: Must return non-empty text
3. **Clipboard**: Must handle empty text gracefully

## Future Considerations

1. **Async Processing**: Use asyncio for better concurrency
2. **Queue System**: Add message queue for transcription requests
3. **Caching**: Cache recent transcripts for quick access
4. **WebSocket**: Real-time status updates to frontend
