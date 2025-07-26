# config.py
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    Manages application settings using environment variables.
    Pydantic automatically reads from a .env file or system environment variables.
    """
    # --- General App Settings ---
    APP_NAME: str = "Multimedia Generation API"
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    
    # --- Server Settings ---
    # In production, use 0.0.0.0 to listen on all available network interfaces.
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --- Default Paths & IDs ---
    # These can be overridden by API requests but serve as fallbacks.
    DEFAULT_VOICE_ID: str = "21m00Tcm4TlvDq8ikWAM"
    DEFAULT_OUTPUT_DIR: str = "/tmp/api_outputs" # Use a temporary/shared volume in production

    # --- API Keys ---
    # It's critical to load secrets from the environment.
    # Replace with your actual environment variable names.
    ELEVEN_API_KEY: str
    RUNWAY_API_KEY: str
    
    class Config:
        # This tells Pydantic to look for a .env file.
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Create a single settings instance to be imported by other modules
settings = Settings()

# Ensure the output directory exists
os.makedirs(settings.DEFAULT_OUTPUT_DIR, exist_ok=True)