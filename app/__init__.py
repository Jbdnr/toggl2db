"""Flask application factory."""
from flask import Flask
from .database import init_db
from .routes import bp

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(bp)
    init_db()

    return app
