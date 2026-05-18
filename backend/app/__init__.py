import os

from flask import Flask, jsonify
from flask_cors import CORS

from .config import Config
from .extensions import db
from .routes import register_blueprints
from .services.seed import seed_database


def _parse_origins(raw_origins):
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


def create_app(config_object=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    CORS(
        app,
        resources={r"/api/*": {"origins": _parse_origins(app.config["CORS_ORIGINS"])}},
    )

    register_blueprints(app)

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(_error):
        return jsonify({"error": "Internal server error"}), 500

    with app.app_context():
        db.create_all()
        seed_database()

    return app
