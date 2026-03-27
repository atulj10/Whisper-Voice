from flask import Blueprint, jsonify
from services.container import get_container
from services.listener_service import (
    ListenerAlreadyActiveError,
    ListenerNotActiveError,
)
from utils.exceptions import ListenerError, ClipboardError, TranscriptionError, AudioServiceError
from schemas import HealthResponse

api_bp = Blueprint("api", __name__)
container = get_container()


def _error_response(error: Exception):
    error_code = getattr(error, 'code', 'INTERNAL_ERROR')
    return {"status": "error", "code": error_code, "message": str(error)}, 400


@api_bp.route("/initialize-listener", methods=["POST"])
def initialize_listener():
    try:
        result = container.listener_service.start_listener()
        return jsonify(result), 200
    except (ListenerAlreadyActiveError, ListenerError) as e:
        return _error_response(e)
    except Exception as e:
        return _error_response(e)


@api_bp.route("/stop-listener", methods=["POST"])
def stop_listener():
    try:
        result = container.listener_service.stop_listener()
        return jsonify(result), 200
    except (ListenerNotActiveError, ListenerError) as e:
        return _error_response(e)
    except Exception as e:
        return _error_response(e)


@api_bp.route("/transcripts", methods=["GET"])
def get_transcripts():
    try:
        repo = container.create_transcript_repository()
        transcripts = repo.get_all()
        result = [t.to_dict() for t in transcripts]
        repo.close()
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return _error_response(e)


@api_bp.route("/health", methods=["GET"])
def health_check():
    response = HealthResponse(status="ok")
    return jsonify(response.model_dump()), 200


@api_bp.route("/listener-status", methods=["GET"])
def listener_status():
    is_active = container.listener_service.is_active
    is_recording = (
        container.listener_service.audio_service.is_recording 
        if is_active else False
    )
    return jsonify({
        "status": "success",
        "is_active": is_active,
        "is_recording": is_recording
    }), 200
