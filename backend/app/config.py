"""
Configuration and settings for the Agentic AI Application backend
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # API Keys
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    
    # LLM Models
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "x-ai/grok-code-fast-1")
    HF_MODEL: str = os.getenv("HF_MODEL", "deepseek-ai/DeepSeek-V3.2-Exp:novita")
    
    # API Configuration
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    HF_BASE_URL: str = "https://router.huggingface.co/v1"
    GITHUB_API_BASE_URL: str = "https://api.github.com"
    
    # Application settings
    MAX_CHUNK_SIZE: int = 2000  # Characters per chunk for API requests
    MAX_FILE_SIZE: int = 200_000  # Max file size in bytes
    
    # Site info for OpenRouter (optional)
    SITE_URL: str = os.getenv("SITE_URL", "")
    SITE_NAME: str = os.getenv("SITE_NAME", "Agentic AI Application")
    
    # Skip patterns
    SKIP_EXTENSIONS: set = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico", ".mp4", ".zip", ".exe", ".dll"}
    SKIP_DIRECTORIES: set = {"node_modules", ".git", "dist", "build", "__pycache__", "venv", ".idea"}
    
    # FastAPI
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()
