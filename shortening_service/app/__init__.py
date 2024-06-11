from flask import Flask
from .views import shortening_service_blueprint
from database import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(shortening_service_blueprint)
    return app