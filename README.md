# Voice Clipboard Assistant

A local desktop voice-to-text application that transcribes speech and automatically pastes it.

## Project Overview

This application allows users to:
1. Initialize a global listener (works even when browser is not focused)
2. Press **Ctrl+Space** to start recording audio
3. Release **Ctrl+Space** to stop recording
4. Have speech transcribed locally using AI (Whisper)
5. Text is automatically copied to clipboard AND pasted

## Architecture

```
React UI (Frontend)
    │
    ▼
Flask API (Backend)
    │
    ▼
Listener Service (Background Thread)
    │
    ├── Hotkey Listener (pynput)
    ├── Audio Recorder (sounddevice)
    ├── Transcription (faster-whisper - local AI)
    └── Clipboard + Auto-Paste (pyperclip + pyautogui)
```

## Features

- **Global Hotkey**: Works across all applications via pynput
- **Local Transcription**: No API keys needed - uses faster-whisper (Whisper AI)
- **Auto-Paste**: Automatically pastes transcribed text after recording
- **Background Threading**: Flask server stays responsive
- **Real-time Status**: UI shows recording state

## Directory Structure

```
voice-clipboard-assistant/
├── backend/
│   ├── api/routes.py          # API endpoints
│   ├── services/
│   │   ├── listener_service.py     # Hotkey management
│   │   ├── audio_service.py        # Audio recording
│   │   ├── transcription_service.py # Whisper AI
│   │   └── clipboard_service.py     # Copy + paste
│   ├── repositories/          # Database access
│   ├── models/                # Database models
│   ├── schemas/               # Data validation
│   ├── utils/logger.py        # Logging
│   ├── ai/agents.md           # AI governance
│   ├── app.py                 # Flask entry point
│   ├── config.py              # Configuration
│   └── requirements.txt       # Dependencies
├── frontend/                  # React UI
├── .gitignore
├── README.md
├── architecture.md
└── walkthrough_script.md
```

## Setup Instructions

### Backend

```bash
cd voice-clipboard-assistant/backend
pip install -r requirements.txt
python app.py
```

**Note**: First run will download the Whisper AI model (~500MB).

### Frontend

```bash
cd voice-clipboard-assistant/frontend
npm install
npm run dev
```

## How to Use

1. Start the backend server: `python app.py`
2. Start the frontend: `npm run dev`
3. Open `http://localhost:3000`
4. Click **Initialize Listener**
5. Press **Ctrl+Space** anywhere on your computer
6. Speak your text
7. Release **Ctrl+Space**
8. Text is automatically transcribed and pasted!

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/initialize-listener` | POST | Start global hotkey listener |
| `/stop-listener` | POST | Stop listener |
| `/listener-status` | GET | Check if listener is active |
| `/transcripts` | GET | Get transcript history |
| `/health` | GET | Health check |

## Technical Decisions

### Why faster-whisper instead of cloud APIs?

1. **Privacy**: Audio never leaves your machine
2. **No API Keys**: Free to use, no account needed
3. **Offline Capable**: Works without internet
4. **Fast**: Optimized C++ implementation

### Why layered architecture?

- **Separation of Concerns**: Each layer has one job
- **Testability**: Easy to mock dependencies
- **Maintainability**: Changes isolated to specific layers
- **Predictability**: Clear data flow

### Why threading?

The hotkey listener runs in a background daemon thread so Flask can still handle API requests without blocking.

## Known Limitations

1. **Model Download**: First run downloads ~500MB Whisper model
2. **Platform**: Windows-focused (pynput/pyautogui)
3. **Microphone**: Uses default system microphone
4. **Languages**: Currently English only

## Future Extensions

1. Multi-language support
2. Custom hotkey configuration
3. Microphone selection UI
4. Transcript editing and deletion
5. Dark mode UI
6. Audio device settings

## License

MIT
