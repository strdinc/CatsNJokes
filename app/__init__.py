from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'e5d5d808923a8e038b69eb783456c8fa'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, '..', 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .main import main as main_bp
    from .auth import auth as auth_bp
    from .api import api as api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    return app