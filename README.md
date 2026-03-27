# Voice Clipboard Assistant

A local desktop-assisted web application for voice-to-clipboard transcription.

## Project Overview

This application allows users to:
1. Initialize a global listener that works even when the browser is not focused
2. Press **Ctrl+Space** to start recording audio
3. Release **Ctrl+Space** to stop recording
4. Have the transcribed text automatically copied to the clipboard

## Architecture

```
React UI (Frontend)
    |
    v
Flask API (Backend)
    |
    v
Listener Service (Background Thread)
    |
    v
Hotkey Listener (pynput) -> Audio Recorder (sounddevice) -> Transcription (OpenAI) -> Clipboard (pyperclip)
    |
    v
SQLite Database
```

## Directory Structure

```
voice-clipboard-assistant/
├── backend/
│   ├── api/               # API routes layer
│   ├── services/          # Business logic services
│   ├── repositories/     # Database access layer
│   ├── models/           # Database models
│   ├── schemas/          # Data validation schemas
│   ├── utils/           # Utilities (logging)
│   ├── ai/              # AI governance documents
│   ├── app.py           # Flask application entry point
│   ├── config.py        # Configuration
│   └── requirements.txt # Flask-only requirements
├── frontend/            # React frontend
├── requirements.txt     # Full Python dependencies
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd voice-clipboard-assistant/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd voice-clipboard-assistant/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## How to Run

### Start Backend

```bash
cd voice-clipboard-assistant/backend
python app.py
```

The backend will start on `http://localhost:5000`.

### Start Frontend

```bash
cd voice-clipboard-assistant/frontend
npm run dev
```

The frontend will start on `http://localhost:3000`.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/initialize-listener` | POST | Start the global hotkey listener |
| `/stop-listener` | POST | Stop the global hotkey listener |
| `/transcripts` | GET | Get all transcripts from the database |
| `/listener-status` | GET | Check if listener is active |
| `/health` | GET | Health check endpoint |

## Design Decisions

### Layered Architecture

The application follows a strict layered architecture:
- **API Layer**: Handles HTTP requests/responses
- **Service Layer**: Contains business logic
- **Repository Layer**: Handles database operations
- **Model Layer**: Defines database schema
- **Schema Layer**: Validates input/output data
- **Utility Layer**: Provides logging and helpers

### Why This Architecture?

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Testability**: Easy to mock dependencies for unit testing
3. **Maintainability**: Changes in one layer don't affect others
4. **Predictability**: Clear data flow makes the system easy to understand

### Threading Model

The listener runs in a background thread to avoid blocking the Flask server. This allows the web application to remain responsive while the hotkey listener operates continuously.

## Known Limitations

1. **AI Transcription**: Currently returns placeholder text (TODO)
2. **Database Storage**: Not yet saving transcripts to database (TODO)
3. **Platform Support**: Requires Windows for pynput hotkey detection
4. **Audio Quality**: Uses default system microphone settings

## Future Extensions

1. **OpenAI Whisper Integration**: Complete AI transcription
2. **Multiple Hotkeys**: Support custom hotkey configurations
3. **Audio Settings**: Allow users to select microphone and adjust settings
4. **Transcript Management**: Edit, delete, and search transcripts
5. **Dark Mode**: Add theme support to the frontend
6. **Keyboard Shortcuts**: Add keyboard shortcuts for common actions

## Testing

To run tests (when implemented):
```bash
cd voice-clipboard-assistant/backend
pytest tests/
```

## License

MIT
