from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager

db = SQLAlchemy()  # Initialize SQLAlchemy instance here, but not tied to the app yet
mail = Mail()  # Initialize Flask-Mail instance here, but not tied to the app yet


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    jwt = JWTManager(app)
    CORS(app)
    # Initialize SQLAlchemy and Flask-Mail with the app
    db.init_app(app)
    mail.init_app(app)

    # Import and register blueprints
    from .routes import main
    from .dashboard_routes import dashboard
    
    app.register_blueprint(main)
    app.register_blueprint(dashboard)

    # Create database tables (optional)
    @app.before_request
    def create_tables():
        db.create_all()

    return app
