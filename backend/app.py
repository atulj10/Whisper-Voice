from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
from api import api_bp
from models import init_db
from utils.logger import get_logger

load_dotenv(Path(__file__).parent / ".env")
logger = get_logger(__name__)


def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(api_bp)
    
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    return app


if __name__ == "__main__":
    app = create_app()
    logger.info("Starting Voice Clipboard Assistant server")
    app.run(host="0.0.0.0", port=5000, debug=True)
