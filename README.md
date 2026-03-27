# Voice Clipboard Assistant

A local desktop voice-to-text application that transcribes speech and automatically pastes it anywhere.

## Features

- **Global Hotkey**: Works across all applications via pynput
- **Local Transcription**: No API keys needed - uses faster-whisper (Whisper AI)
- **Auto-Paste**: Automatically pastes transcribed text after recording
- **Background Threading**: Flask server stays responsive
- **Real-time Status**: UI shows recording state

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd voice-clipboard-assistant
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 4. Run the Backend

```bash
cd backend
python app.py
```

> **Note**: First run will download the Whisper AI model (~500MB).

Backend runs on: `http://localhost:5000`

### 5. Run the Frontend

```bash
cd frontend
npm run dev
```

Frontend runs on: `http://localhost:3000`

---

## How to Use

1. Open `http://localhost:3000` in your browser
2. Click **Initialize Listener**
3. Click on any application (browser, Notepad, etc.)
4. Press and hold **Ctrl+Space** to start recording
5. Speak your text
6. Release **Ctrl+Space** to stop
7. Text is transcribed and automatically pasted!

---

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
    ├── Transcription (faster-whisper)
    └── Clipboard + Auto-Paste (pyperclip + pyautogui)
```

### Directory Structure

```
voice-clipboard-assistant/
├── backend/
│   ├── api/routes.py              # HTTP endpoints
│   ├── services/
│   │   ├── container.py           # Dependency injection
│   │   ├── listener_service.py    # Hotkey management
│   │   ├── audio_service.py      # Audio recording
│   │   ├── transcription_service.py # AI transcription
│   │   └── clipboard_service.py   # Copy + paste
│   ├── repositories/             # Database access
│   ├── models/                   # Database models
│   ├── schemas/                  # Data validation
│   ├── utils/
│   │   ├── logger.py             # Logging
│   │   └── exceptions.py         # Custom exceptions
│   ├── ai/agents.md              # AI governance
│   ├── app.py                    # Flask entry point
│   ├── config.py                 # Configuration
│   └── requirements.txt          # Dependencies
├── frontend/                      # React UI
└── README.md
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/initialize-listener` | POST | Start global hotkey listener |
| `/stop-listener` | POST | Stop listener |
| `/listener-status` | GET | Check if listener is active |
| `/transcripts` | GET | Get transcript history |
| `/health` | GET | Health check |

---

## Technical Decisions

### Why faster-whisper instead of cloud APIs?

| Factor | faster-whisper | Cloud APIs |
|--------|---------------|------------|
| Privacy | Audio stays local | Sent to servers |
| Cost | Free | API costs |
| Internet | Works offline | Required |
| Speed | Fast (CPU optimized) | Network dependent |

### Why layered architecture?

- **Separation of Concerns**: Each layer has one job
- **Testability**: Easy to mock dependencies
- **Maintainability**: Changes isolated to specific layers
- **Predictability**: Clear data flow

---

## Known Limitations

1. **Model Download**: First run downloads ~500MB Whisper model
2. **Platform**: Windows-focused (pynput/pyautogui)
3. **Microphone**: Uses default system microphone
4. **Languages**: Currently English only

---

## Future Extensions

- Multi-language support
- Custom hotkey configuration
- Microphone selection UI
- Transcript editing and deletion
- Dark mode UI
- Audio device settings

---

## License

MIT
