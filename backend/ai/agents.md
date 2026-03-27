# AI Governance Document

## Rules

1. **Never place business logic in routes**
   - Routes should only handle HTTP requests/responses
   - All business logic belongs in services

2. **Always validate inputs**
   - Check all inputs before processing
   - Raise exceptions for invalid data
   - Never assume valid input

3. **Always log failures**
   - Use the centralized logger
   - Include context in log messages
   - Log at appropriate levels (ERROR, WARNING, INFO)

4. **Always write tests for new logic**
   - Unit tests for services
   - Mock external dependencies
   - Test edge cases

5. **Keep functions under 40 lines**
   - Extract helper functions
   - Single responsibility per function
   - Improves readability and testability

## Constraints

1. **No global mutable state**
   - Use dependency injection
   - Pass dependencies explicitly
   - Makes testing easier

2. **No hidden side effects**
   - All side effects should be explicit
   - Log all state changes
   - Document when functions modify state

3. **Prefer explicit dependencies**
   - Don't use global imports for services
   - Initialize dependencies in __init__
   - Pass dependencies to constructors

## Implementation Guidelines

### Service Layer
```python
class AudioService:
    def __init__(self, config: AudioConfig):
        self.config = config
        self.logger = get_logger(__name__)
    
    def validate_audio(self, audio_path: Path) -> bool:
        if not audio_path.exists():
            self.logger.error(f"File not found: {audio_path}")
            return False
        return True
```

### Repository Layer
```python
class TranscriptRepository:
    def create(self, text: str, status: str) -> Transcript:
        transcript = Transcript(text=text, status=status)
        self.db.add(transcript)
        self.db.commit()
        return transcript
```

### Routes Layer
```python
@api_bp.route("/transcripts", methods=["GET"])
def get_transcripts():
    try:
        repo = TranscriptRepository()
        transcripts = repo.get_all()
        return jsonify([t.to_dict() for t in transcripts]), 200
    except Exception as e:
        logger.error(f"Failed to fetch transcripts: {e}")
        return jsonify({"error": str(e)}), 500
```

## Error Handling Pattern

```python
try:
    result = service.process()
except ValueError as e:
    logger.warning(f"Validation error: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

## Logging Pattern

```python
logger.info("Operation started", extra={"context": "value"})
logger.warning("Potential issue", extra={"warning": "detail"})
logger.error("Operation failed", extra={"error": "detail"})
```

## Testing Pattern

```python
def test_service_with_mock():
    mock_repo = Mock(spec=TranscriptRepository)
    service = ListenerService(repository=mock_repo)
    result = service.start()
    assert result["status"] == "success"
```
