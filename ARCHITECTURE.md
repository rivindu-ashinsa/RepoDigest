# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (To be created)                    │
│                  (React/Vue/HTML + GitHub Pages)               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/CORS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend Server                      │
│                      (Uvicorn + Pydantic)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GET /                                                          │
│  GET /api/health                                               │
│  POST /api/generate-readme ────┐                               │
│  GET /docs (Swagger)           │                               │
│  GET /redoc (ReDoc)            │                               │
│  GET /openapi.json             │                               │
│                                │                               │
│                                ▼                               │
│                    ┌──────────────────────┐                    │
│                    │  Request Validation  │                    │
│                    │  (Pydantic Models)   │                    │
│                    └──────────────────────┘                    │
│                            │                                    │
│                            ▼                                    │
│        ┌───────────────────────────────────────┐               │
│        │                                       │               │
│        ▼                       ▼               ▼               │
│    ┌─────────┐          ┌────────────┐  ┌──────────┐         │
│    │ Scraper │          │Summarizer  │  │ README   │         │
│    │ Service │          │ Service    │  │Generator │         │
│    └─────────┘          └────────────┘  │ Service  │         │
│         │                    │           └──────────┘         │
│         │                    │               │                 │
│         │ GitHub API         │ OpenRouter/   │                │
│         │ Requests           │ HuggingFace   │                │
│         ▼                    ▼               ▼                 │
│    ┌─────────┐          ┌────────────┐  ┌──────────┐         │
│    │ GitHub  │          │  LLM API   │  │  LLM API │         │
│    │ (Public)│          │OpenRouter  │  │HuggingFace         │
│    └─────────┘          └────────────┘  └──────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow

```
POST /api/generate-readme
    │
    ├─> Validate request (Pydantic model)
    │       │
    │       └─> repo_url: string
    │       └─> use_hf_model: boolean
    │
    ├─> Execute scraper.fetch_repo_code(repo_url)
    │       │
    │       ├─> GitHub API authentication
    │       ├─> Fetch file list recursively
    │       ├─> Filter by extension/size
    │       ├─> Compress Python files
    │       │
    │       └─> Return: List[{path, content}]
    │
    ├─> For each file, summarize (using LLM)
    │       │
    │       ├─> CodeSummarizer.summarize_file(path, content)
    │       │
    │       ├─> OpenRouter API (default)
    │       │   └─> grok-code-fast-1 model
    │       │
    │       └─> OR HuggingFace API (if use_hf_model=True)
    │           └─> deepseek-ai/DeepSeek-V3.2-Exp:novita
    │
    ├─> Generate README from summaries
    │       │
    │       ├─> ReadmeGenerator.generate(summaries)
    │       │
    │       ├─> OpenRouter API (default)
    │       │   └─> grok-code-fast-1 model
    │       │
    │       └─> OR HuggingFace API (if use_hf_model=True)
    │
    └─> Return: GenerateReadmeResponse
            └─> repo_url, readme_content, file_count, status
```

## Module Structure

```
app/
├── __init__.py
│   └─> Exports: app (FastAPI instance)
│
├── main.py
│   ├─> Creates FastAPI application
│   ├─> Adds CORS middleware
│   ├─> Includes router
│   └─> Health check endpoint
│
├── config.py
│   └─> Settings class (loads .env)
│       ├─> API keys
│       ├─> Base URLs
│       ├─> File size limits
│       └─> Skip patterns
│
├── models.py
│   ├─> GenerateReadmeRequest (request validation)
│   ├─> GenerateReadmeResponse (response format)
│   └─> HealthResponse (health check)
│
├── api/
│   ├── __init__.py
│   │   └─> Exports: router
│   │
│   └── routes.py
│       ├─> POST /api/generate-readme
│       │   ├─> Fetch repository
│       │   ├─> Summarize files
│       │   ├─> Generate README
│       │   └─> Return response
│       │
│       └─> GET /api/health
│           └─> Return health status
│
└── services/
    ├── __init__.py
    │   └─> Exports all services
    │
    ├── scraper.py
    │   ├─> fetch_repo_code(repo_url)
    │   ├─> chunk_text(text)
    │   └─> compress_python_code(code)
    │
    ├── summarizer.py
    │   └─> CodeSummarizer class
    │       ├─> __init__(use_hf)
    │       └─> summarize_file(path, content)
    │
    └── readme_generator.py
        └─> ReadmeGenerator class
            ├─> __init__(use_hf)
            └─> generate(summaries)
```

## Data Flow Diagram

```
Human Request
      │
      ▼
┌─────────────────────┐
│  Browser/Client     │
│  POST /api/generate │─────────┐
│  {repo_url, use_hf} │         │
└─────────────────────┘         │
                                │
                                ▼
                        ┌──────────────────┐
                        │  FastAPI App     │
                        │  - Validation    │
                        │  - Routing       │
                        │  - Error Handler │
                        └──────────────────┘
                                │
                                ▼
                        ┌──────────────────┐
                        │ Scraper Service  │
                        └──────────────────┘
                                │
                                ├───────────────┐
                                │               │
                                ▼               ▼
                        GitHub API        (GitHub API)
                        [Repo Files]      [Code Content]
                                │               │
                                └───────┬───────┘
                                        │
                                        ▼
                        ┌──────────────────────┐
                        │ Summarizer Service   │
                        │ (for each file)      │
                        └──────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
                OpenRouter API      HuggingFace API
                [LLM Summary]       [LLM Summary]
                    │                       │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼────────────┐
                    │           │           │
                    │    List of Summaries  │
                    │           │           │
                    └───────────┬───────────┘
                                │
                                ▼
                        ┌──────────────────────┐
                        │ README Generator     │
                        │ (Combines summaries) │
                        └──────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
                OpenRouter API      HuggingFace API
                [Generate README]   [Generate README]
                    │                       │
                    └───────────┬───────────┘
                                │
                        ┌───────▼──────┐
                        │ README Text  │
                        └───────┬──────┘
                                │
                                ▼
                        ┌──────────────────────┐
                        │ Response Object      │
                        │ - repo_url           │
                        │ - readme_content     │
                        │ - file_count         │
                        │ - status             │
                        └──────────────────────┘
                                │
                                ▼
                        ┌──────────────────┐
                        │ Browser/Client   │
                        │ (Receives JSON)  │
                        └──────────────────┘
```

## Configuration & Secrets Management

```
┌─────────────────────────────────────────┐
│  backend/.env (Not committed to Git)    │
├─────────────────────────────────────────┤
│ GITHUB_TOKEN = xxxxx                    │
│ OPENROUTER_API_KEY = xxxxx              │
│ HF_TOKEN = xxxxx                        │
│ DEBUG = True                            │
│ PORT = 8000                             │
└─────────────────────────────────────────┘
            │
            │ Loaded by python-dotenv
            │ in config.py
            ▼
┌─────────────────────────────────────────┐
│  Settings class (config.py)             │
├─────────────────────────────────────────┤
│ • OPENROUTER_API_KEY                    │
│ • GITHUB_TOKEN                          │
│ • HF_TOKEN                              │
│ • Base URLs                             │
│ • Model names                           │
│ • File size limits                      │
└─────────────────────────────────────────┘
            │
            │ Used by services
            ▼
┌─────────────────────────────────────────┐
│  Services (scraper, summarizer, etc.)   │
└─────────────────────────────────────────┘
```

## API Response Format

### Success Response (200)
```json
{
  "repo_url": "https://github.com/owner/repo",
  "readme_content": "# Project Title\n\n## Overview\n...",
  "file_count": 15,
  "status": "success"
}
```

### Error Response (400/500)
```json
{
  "detail": "Error message explaining what went wrong"
}
```

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| GitHub fetch | 2-30s | Depends on repo size |
| Per-file summary | 1-5s | Depends on file size, LLM |
| README generation | 2-10s | Combines all summaries |
| **Total** | **5-45s** | From request to response |

---

## Technology Stack Details

### Backend Framework
- **FastAPI**: Modern, async Python web framework
- **Uvicorn**: ASGI web server

### Type Safety
- **Pydantic**: Data validation using Python type hints

### External APIs
- **OpenRouter**: Provides access to various LLMs (grok-code-fast-1)
- **HuggingFace**: Alternative LLM provider (DeepSeek)
- **GitHub API**: Fetch repository contents and metadata

### Configuration
- **python-dotenv**: Load environment variables from .env

### LLM & AI Libraries
- **LangChain**: Prompt management and LLM orchestration
- **LangGraph**: Agentic workflows

---

## Files & Their Purposes

| File | Purpose |
|------|---------|
| `run.py` | Entry point that starts Uvicorn server |
| `main.py` | FastAPI app instance, middleware, routes |
| `config.py` | Load and validate environment settings |
| `models.py` | Pydantic request/response models |
| `routes.py` | API endpoint handlers |
| `scraper.py` | GitHub repository code fetching |
| `summarizer.py` | LLM-based code summarization |
| `readme_generator.py` | README generation from summaries |

---

## Security Considerations

1. **API Keys**: Stored in `.env`, never committed
2. **CORS**: Configurable, currently open (adjust for production)
3. **Rate Limiting**: Not yet implemented (consider for production)
4. **Input Validation**: All inputs validated with Pydantic
5. **Error Messages**: Sanitized (no internal details exposed)

---

## Deployment Diagram

```
┌─────────────────────────────────┐
│  Development (Local)            │
├─────────────────────────────────┤
│ python run.py                   │
│ Host: 127.0.0.1:8000           │
│ Debug: True                     │
│ Auto-reload: Enabled            │
└─────────────────────────────────┘
                │
                │ Deploy to cloud
                ▼
┌─────────────────────────────────┐
│  Production (Cloud)             │
├─────────────────────────────────┤
│ gunicorn + Uvicorn workers      │
│ Host: 0.0.0.0:8000             │
│ Debug: False                    │
│ Multiple workers                │
│ Environment vars via secrets    │
└─────────────────────────────────┘
```

---

*This architecture ensures clean separation of concerns, easy testing, and scalability.*
