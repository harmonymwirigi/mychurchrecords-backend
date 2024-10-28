from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from flask.cli import AppGroup

# Initialize SQLAlchemy and Flask-Mail instances
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize Flask extensions
    db.init_app(app)
    mail.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Initialize CLI commands
    init_cli_commands(app)
    
    # Import and register blueprints
    from .routes import main
    from .dashboard_routes import dashboard
    app.register_blueprint(main)
    app.register_blueprint(dashboard)

    # Create tables and ensure admin user is created on app startup
    # with app.app_context():
    #     initialize_database()

    return app

def initialize_database():
    """Create tables if they don't exist and create admin user if needed."""
    db.create_all()  # Create tables if they don't exist
    create_admin_user_once()  # Ensure the admin user is created once

def create_admin_user_once():
    """Create an admin user if one does not already exist."""
    from .models import AdminUser
    from werkzeug.security import generate_password_hash

    # Check if an admin already exists
    if not AdminUser.query.first():
        # Create the admin user if none exists
        admin = AdminUser(
            name="Admin",
            email="admin@churchrecord.us",
            password_hash=generate_password_hash("adminpassword"),
            phone="1234567890"
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")

# Define CLI commands
def init_cli_commands(app):
    admin_cli = AppGroup('admin')

    @admin_cli.command('create')
    def create_admin():
        # Function to create the admin user
        create_admin_user(name="Admin", email="admin@churchrecord.us", password="adminpassword", phone="1234567890")

    app.cli.add_command(admin_cli)

def create_admin_user(name, email, password, phone):
    # Implementation of the admin user creation logic
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
