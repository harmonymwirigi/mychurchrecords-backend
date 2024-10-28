import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
# Load environment variables from the .env file
load_dotenv()

#^[pwgBt}a)$r
# johngilb_harmony
# database - johngilb_harmonytest

class Config:
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')  # Default key if none in .env

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', f'sqlite:///{os.path.join(basedir, "churchrecords.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    # Email configuration (for Flask-Mail)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Default to port 587 (TLS)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'  # Converts to boolean
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'  # Optional SSL (default False)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Email for sending
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Email password

    # PayPal configuration
    PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
    PAYPAL_SECRET = os.getenv('PAYPAL_SECRET')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    