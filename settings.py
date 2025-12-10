"""Application configuration from environment variables."""
import os


class Config:
    """Flask application configuration."""

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN')
