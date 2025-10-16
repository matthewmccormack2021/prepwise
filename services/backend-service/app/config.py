"""
Configuration management for PrepWise backend service.
"""

import os
from typing import Optional


class Config:
    """Application configuration settings."""
    
    # Ollama configuration
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    # Session management
    SESSION_STORAGE_DIR: str = os.getenv("SESSION_STORAGE_DIR", "./data/sessions")
    
    # Conversation management
    MAX_CONVERSATION_MESSAGES: int = int(os.getenv("MAX_CONVERSATION_MESSAGES", "50"))
    SUMMARIZATION_THRESHOLD: int = int(os.getenv("SUMMARIZATION_THRESHOLD", "30"))
    
    # API configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8002"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_ROTATION: str = os.getenv("LOG_ROTATION", "1 day")
    LOG_RETENTION: str = os.getenv("LOG_RETENTION", "7 days")
    
    # CORS settings
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    
    @classmethod
    def get_ollama_host(cls) -> str:
        """Get Ollama host URL."""
        return cls.OLLAMA_HOST
    
    @classmethod
    def get_ollama_model(cls) -> str:
        """Get Ollama model ID."""
        return cls.OLLAMA_MODEL
    
    @classmethod
    def get_session_storage_dir(cls) -> str:
        """Get session storage directory."""
        return cls.SESSION_STORAGE_DIR
    
    @classmethod
    def ensure_session_storage_dir(cls) -> str:
        """Ensure session storage directory exists and return path."""
        os.makedirs(cls.SESSION_STORAGE_DIR, exist_ok=True)
        return cls.SESSION_STORAGE_DIR


# Global config instance
config = Config()
