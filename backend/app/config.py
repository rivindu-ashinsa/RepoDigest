"""
Configuration and settings for the Agentic AI Application backend
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend directory (regardless of where script is run from)
backend_dir = Path(__file__).resolve().parent.parent
env_file = backend_dir / ".env"
load_dotenv(env_file)


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
    MAX_FILE_CONTENT_CHARS: int = int(os.getenv("MAX_FILE_CONTENT_CHARS", "3500"))
    MAX_FILES_TO_SUMMARIZE: int = int(os.getenv("MAX_FILES_TO_SUMMARIZE", "45"))

    # Token/cost controls
    SUMMARIZER_MAX_OUTPUT_TOKENS: int = int(os.getenv("SUMMARIZER_MAX_OUTPUT_TOKENS", "420"))
    README_MAX_OUTPUT_TOKENS: int = int(os.getenv("README_MAX_OUTPUT_TOKENS", "1400"))
    README_MAX_SUMMARY_CHARS: int = int(os.getenv("README_MAX_SUMMARY_CHARS", "22000"))
    
    # Site info for OpenRouter (optional)
    SITE_URL: str = os.getenv("SITE_URL", "")
    SITE_NAME: str = os.getenv("SITE_NAME", "Agentic AI Application")
    
    # Skip patterns
    SKIP_EXTENSIONS: set = {
        ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico", ".mp4", ".zip", ".exe", ".dll",
        ".csv", ".tsv", ".parquet", ".feather", ".h5", ".hdf5", ".npy", ".npz", ".pkl", ".pickle",
        ".pt", ".pth", ".ckpt", ".onnx", ".bin", ".safetensors"
    }
    SKIP_DIRECTORIES: set = {
        "node_modules", ".git", "dist", "build", "__pycache__", "venv", ".idea",
        "data", "dataset", "datasets", "artifacts", "checkpoints", "weights"
    }
    INCLUDE_EXTENSIONS: set = {
        ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rs", ".rb", ".php", ".cs",
        ".cpp", ".c", ".h", ".hpp", ".kt", ".swift", ".scala", ".json", ".yaml", ".yml",
        ".toml", ".ini", ".env", ".sh", ".sql", ".md"
    }
    INCLUDE_FILENAMES: set = {
        "dockerfile", "makefile", "requirements.txt", "pyproject.toml", "package.json",
        "package-lock.json", "pnpm-lock.yaml", "go.mod", "cargo.toml", "pom.xml", "build.gradle"
    }
    SKIP_PATH_CONTAINS: tuple = (
        "/tests/", "/test/", "/docs/", "/examples/", "/example/", "/samples/", "/fixtures/",
        "/migrations/", "/generated/", "/coverage/", "/vendor/", "/third_party/",
        "/data/", "/dataset/", "/datasets/", "/artifacts/", "/checkpoints/", "/weights/"
    )
    SKIP_FILE_PATTERNS: tuple = (
        ".min.", ".bundle.", "generated", "snapshot", ".lock"
    )
    
    # FastAPI
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()
