from flask import Blueprint, jsonify
from services import ListenerService
from repositories import TranscriptRepository
from schemas import HealthResponse

api_bp = Blueprint("api", __name__)

listener_service = ListenerService()


@api_bp.route("/initialize-listener", methods=["POST"])
def initialize_listener():
    result = listener_service.start_listener()
    status_code = 200 if result["status"] == "success" else 400
    return jsonify(result), status_code


@api_bp.route("/stop-listener", methods=["POST"])
def stop_listener():
    result = listener_service.stop_listener()
    status_code = 200 if result["status"] == "success" else 400
    return jsonify(result), status_code


@api_bp.route("/transcripts", methods=["GET"])
def get_transcripts():
    try:
        repo = TranscriptRepository()
        transcripts = repo.get_all()
        result = [t.to_dict() for t in transcripts]
        repo.close()
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@api_bp.route("/health", methods=["GET"])
def health_check():
    response = HealthResponse(status="ok")
    return jsonify(response.model_dump()), 200


@api_bp.route("/listener-status", methods=["GET"])
def listener_status():
    is_active = listener_service.is_active
    is_recording = listener_service.audio_service.is_recording if is_active else False
    return jsonify({
        "status": "success",
        "is_active": is_active,
        "is_recording": is_recording
    }), 200
