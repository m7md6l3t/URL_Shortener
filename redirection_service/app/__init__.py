from flask import Flask
from .views import redirection_service_blueprint
from database import db


def create_app():
    app = Flask(__name__)  # Create a Flask application instance
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(redirection_service_blueprint)  # Register the blueprint
    return app  # Return the configured application instance