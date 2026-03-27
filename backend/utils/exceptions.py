class AudioServiceError(Exception):
    code = "AUDIO_ERROR"
    message = "Audio service error"


class NoAudioDataError(AudioServiceError):
    code = "NO_AUDIO_DATA"
    message = "No audio data recorded"


class AudioTooShortError(AudioServiceError):
    code = "AUDIO_TOO_SHORT"
    message = "Audio duration is below minimum"


class AudioFileNotFoundError(AudioServiceError):
    code = "AUDIO_FILE_NOT_FOUND"
    message = "Audio file not found"


class TranscriptionError(Exception):
    code = "TRANSCRIPTION_ERROR"
    message = "Transcription failed"


class EmptyTranscriptionError(TranscriptionError):
    code = "EMPTY_TRANSCRIPTION"
    message = "Transcription returned empty text"


class ClipboardError(Exception):
    code = "CLIPBOARD_ERROR"
    message = "Clipboard operation failed"


class EmptyTextError(ClipboardError):
    code = "EMPTY_TEXT"
    message = "Text cannot be empty"


class ListenerError(Exception):
    code = "LISTENER_ERROR"
    message = "Listener error"


class ListenerAlreadyActiveError(ListenerError):
    code = "LISTENER_ALREADY_ACTIVE"
    message = "Listener is already active"


class ListenerNotActiveError(ListenerError):
    code = "LISTENER_NOT_ACTIVE"
    message = "Listener is not active"
