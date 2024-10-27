from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from flask.cli import AppGroup

# Define a command to create the admin user
admin_cli = AppGroup('admin')

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
    init_cli_commands(app)

    # Import and register blueprints
    from .routes import main
    from .dashboard_routes import dashboard
    
    app.register_blueprint(main)
    app.register_blueprint(dashboard)

    

    return app


# Define CLI commands
def init_cli_commands(app):
    admin_cli = AppGroup('admin')

    @admin_cli.command('create')
    def create_admin():
        # Function to create the admin user
        create_admin_user(name="Admin", email="admin@churchrecord.us", password="adminpassword", phone="1234567890")

    app.cli.add_command(admin_cli)

def create_admin_user(name, email, password, phone):
    # Implementation of the admin user creation logic (similar to what was shared earlier)
    from .models import AdminUser
    from werkzeug.security import generate_password_hash
    from . import db

    # Check if an admin already exists
    if AdminUser.query.first():
        print("An admin user already exists. Only one admin user is allowed.")
        return

    # Create the admin user
    admin = AdminUser(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        phone=phone
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully.")