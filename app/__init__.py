from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask.cli import AppGroup
from flask_migrate import Migrate  # Optional: for database migrations

# Initialize extensions (but don't bind them to the app yet)
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()  # Optional: only if you're using Flask-Migrate

def create_app():
    # Create the Flask app
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object(Config)
    
    # Initialize extensions with the app
    db.init_app(app)
    mail.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Initialize Flask-Migrate (if using)
    migrate.init_app(app, db)  # Optional

    # Initialize custom CLI commands
    init_cli_commands(app)
    
    # Import and register blueprints
    from .routes import main
    from .dashboard_routes import dashboard
    
    app.register_blueprint(main)
    app.register_blueprint(dashboard)
    
    return app

# Define CLI commands
def init_cli_commands(app):
    # Admin CLI group
    admin_cli = AppGroup('admin')

    @admin_cli.command('create')
    def create_admin():
        # Function to create the admin user
        create_admin_user(name="Admin", email="admin@churchrecord.us", password="adminpassword", phone="1234567890")

    # Register the CLI command group to the app
    app.cli.add_command(admin_cli)
    
    # Database initialization CLI command
    @app.cli.command("init-db")
    def init_db():
        """Initialize the database and create tables."""
        with app.app_context():
            db.create_all()
            print("Database initialized successfully.")

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
