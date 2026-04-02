"""
GitHub repository code scraper service
Fetches and processes files from GitHub repositories
"""
import os
import re
import requests
from typing import List, Dict

try:
    from ..config import settings
except ImportError:
    # Allow running this file directly: python scraper.py
    import sys
    from pathlib import Path

    backend_dir = Path(__file__).resolve().parents[2]
    if str(backend_dir) not in sys.path:
        sys.path.append(str(backend_dir))
    from app.config import settings


def chunk_text(text: str, max_chars: int = None) -> List[str]:
    """
    Split text into smaller chunks for API requests
    
    Args:
        text: Text to chunk
        max_chars: Maximum characters per chunk
        
    Returns:
        List of text chunks
    """
    if max_chars is None:
        max_chars = settings.MAX_CHUNK_SIZE
    
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks


def compress_python_code(code: str) -> str:
    """
    Extract only meaningful sections of Python code to reduce LLM token usage.
    Removes unnecessary whitespace and comments.
    
    Args:
        code: Python code to compress
        
    Returns:
        Compressed code with key sections only
    """
    imports = re.findall(r"^(?:from\s+\S+\s+import\s+\S+|import\s+\S+)", code, re.MULTILINE)
    classes = re.findall(r"class\s+\w+(?:\([^)]*\))?:", code)
    functions = re.findall(r"def\s+\w+\s*\([^)]*\):", code)
    docstrings = re.findall(r'"""(.*?)"""', code, re.DOTALL)

    compressed = [
        "### IMPORTS:\n" + "\n".join(imports),
        "### CLASSES:\n" + "\n".join(classes),
        "### FUNCTIONS:\n" + "\n".join(functions),
        "### DOCSTRINGS:\n" + "\n".join(docstrings[:3])
    ]

    return "\n\n".join([block for block in compressed if block.strip() != ""])


def compress_generic_text(text: str, max_chars: int) -> str:
    """Compress non-Python text to keep only high-signal content under a strict budget."""
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    return text[:max_chars]


def should_include_file(path: str, name: str, ext: str) -> bool:
    """Decide if a file should be sent to the LLM pipeline."""
    lower_path = f"/{path.lower()}"
    lower_name = name.lower()

    if any(fragment in lower_path for fragment in settings.SKIP_PATH_CONTAINS):
        return False
    if any(pattern in lower_name for pattern in settings.SKIP_FILE_PATTERNS):
        return False

    if lower_name in settings.INCLUDE_FILENAMES:
        return True
    if ext in settings.INCLUDE_EXTENSIONS:
        return True
    return False


def fetch_repo_code(repo_url: str) -> List[Dict[str, str]]:
    """
    Fetch all relevant files from a GitHub repository.
    
    Args:
        repo_url: GitHub repository URL (e.g., https://github.com/owner/repo)
        
    Returns:
        List of dictionaries with 'path' and 'content' keys
        
    Raises:
        ValueError: If repo_url is invalid or token is not set
    """
    token = settings.GITHUB_TOKEN
    if not token:
        raise ValueError("GITHUB_TOKEN not set in environment")
    
    headers = {"Authorization": f"token {token}"}
    
    try:
        owner, repo = repo_url.rstrip("/").split("/")[-2:]
    except (ValueError, IndexError):
        raise ValueError(f"Invalid GitHub URL: {repo_url}")

    def get_files(path: str = "") -> List[Dict[str, str]]:
        """Recursively fetch files from GitHub API"""
        url = f"{settings.GITHUB_API_BASE_URL}/repos/{owner}/{repo}/contents/{path}"
        
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 404:
                raise ValueError(f"Repository not found: {repo_url}")
            if r.status_code != 200:
                raise ValueError(f"GitHub API error: {r.status_code}")
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch from GitHub: {str(e)}")

        files = []
        for item in r.json():
            name = item["name"]
            ext = os.path.splitext(name)[1]
            item_path = item.get("path", "")

            # Skip useless dirs/files
            if item["type"] == "dir" and name in settings.SKIP_DIRECTORIES:
                continue
            if item["type"] == "file" and ext in settings.SKIP_EXTENSIONS:
                continue
            if item["type"] == "file" and item.get("size", 0) > settings.MAX_FILE_SIZE:
                continue
            if item["type"] == "file" and not should_include_file(item_path, name, ext):
                continue

            if item["type"] == "file":
                if len(files) >= settings.MAX_FILES_TO_SUMMARIZE:
                    break
                try:
                    text = requests.get(item["download_url"], headers=headers, timeout=10).text

                    # Keep only high-signal sections to reduce token usage.
                    if ext == ".py":
                        text = compress_python_code(text)
                    else:
                        text = compress_generic_text(text, settings.MAX_FILE_CONTENT_CHARS)

                    if len(text) > settings.MAX_FILE_CONTENT_CHARS:
                        text = text[:settings.MAX_FILE_CONTENT_CHARS]

                    files.append({"path": item["path"], "content": text})

                except Exception as e:
                    print(f"⚠️ Error reading {item['path']}: {e}")

            elif item["type"] == "dir":
                files.extend(get_files(item["path"]))

        return files

    return get_files()
if __name__ == "__main__":
    sample_repo = "https://github.com/rivindu-ashinsa/AI-Powered-Web-site-Audit-Tool"
    result = fetch_repo_code(sample_repo)
    print(f"Fetched {len(result)} files from {sample_repo}")