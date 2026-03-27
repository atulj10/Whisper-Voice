from services.audio_service import AudioService
from services.transcription_service import TranscriptionService
from services.clipboard_service import ClipboardService
from services.listener_service import ListenerService
from repositories.transcript_repository import TranscriptRepository


class ServiceContainer:
    def __init__(self):
        self._audio_service = None
        self._transcription_service = None
        self._clipboard_service = None
        self._listener_service = None
        self._transcript_repository = None

    @property
    def audio_service(self) -> AudioService:
        if self._audio_service is None:
            self._audio_service = AudioService()
        return self._audio_service

    @property
    def transcription_service(self) -> TranscriptionService:
        if self._transcription_service is None:
            self._transcription_service = TranscriptionService()
        return self._transcription_service

    @property
    def clipboard_service(self) -> ClipboardService:
        if self._clipboard_service is None:
            self._clipboard_service = ClipboardService()
        return self._clipboard_service

    @property
    def listener_service(self) -> ListenerService:
        if self._listener_service is None:
            self._listener_service = ListenerService(
                audio_service=self.audio_service,
                transcription_service=self.transcription_service,
                clipboard_service=self.clipboard_service,
            )
        return self._listener_service

    def create_transcript_repository(self) -> TranscriptRepository:
        return TranscriptRepository()


_container = ServiceContainer()


def get_container() -> ServiceContainer:
    return _container
