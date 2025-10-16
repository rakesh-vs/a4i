"""Configuration management for ADK agents."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    # Google Cloud
    GOOGLE_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    
    # Agent Configuration
    AGENT_MODEL = os.getenv("AGENT_MODEL", "gemini-2.5-flash")
    AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration."""
        if not cls.GOOGLE_PROJECT_ID:
            print("⚠️  Warning: GOOGLE_CLOUD_PROJECT not set")
        return True

