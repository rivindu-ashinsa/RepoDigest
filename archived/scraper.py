import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()



def chunk_text(text, max_chars=2000):
    """Split text into smaller chunks for API requests"""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks


def compress_python_code(code: str) -> str:
    """Extract only meaningful sections of Python code to reduce LLM token usage."""
    imports = re.findall(r"^(?:from\s+\S+\s+import\s+\S+|import\s+\S+)", code, re.MULTILINE)
    classes = re.findall(r"class\s+\w+(?:\([^)]*\))?:", code)
    functions = re.findall(r"def\s+\w+\s*\([^)]*\):", code)
    docstrings = re.findall(r'"""(.*?)"""', code, re.DOTALL)

    compressed = [
        "### IMPORTS:\n" + "\n".join(imports),
        "### CLASSES:\n" + "\n".join(classes),
        "### FUNCTIONS:\n" + "\n".join(functions),
        "### DOCSTRINGS:\n" + "\n".join(docstrings[:3])  # limit to first 3 docstrings to save tokens
    ]

    return "\n\n".join([block for block in compressed if block.strip() != ""])


def fetch_repo_code(repo_url):
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"}
    owner, repo = repo_url.rstrip("/").split("/")[-2:]

    SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico", ".mp4", ".zip", ".exe", ".dll"}
    SKIP_DIRS = {"node_modules", ".git", "dist", "build", "__pycache__", "venv", ".idea"}

    def get_files(path=""):
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            return []

        files = []
        for item in r.json():
            name = item["name"]
            ext = os.path.splitext(name)[1]

            # Skip useless dirs/files
            if item["type"] == "dir" and name in SKIP_DIRS:
                continue
            if item["type"] == "file" and ext in SKIP_EXT:
                continue
            if item["type"] == "file" and item.get("size", 0) > 200_000:
                continue  # Skip huge files

            if item["type"] == "file":
                try:
                    text = requests.get(item["download_url"], headers=headers).text

                    # Compress Python files only
                    if ext == ".py":
                        text = compress_python_code(text)

                    files.append({"path": item["path"], "content": text})

                except Exception as e:
                    print(f"⚠️ Error reading {item['path']}: {e}")

            elif item["type"] == "dir":
                files.extend(get_files(item["path"]))

        return files

    return get_files()



# files = fetch_repo_code("https://github.com/rivindu-ashinsa/Doc-Drafter")

# for file in files:
#     chunks = chunk_text(file["content"])
#     for chunk in chunks:
#         print("----- Chunk Start -----")
#         print(f"Chunk length: {len(chunk)}")
#         print(chunk)
#         print("----- Chunk End -----\n\n")
