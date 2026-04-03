# Agentic AI Application

AI-powered GitHub repository analyzer that generates a polished `README.md` using LLMs.

The project includes:
- A FastAPI backend for repository scanning, summarization, and README generation
- A dark, glass-style frontend with real-time scan logs and GitHub-style markdown preview

## Architecture

```
Agentic-ai-application/
├── backend/
│   ├── app/
│   │   ├── api/routes.py
│   │   ├── services/scraper.py
│   │   ├── services/summarizer.py
│   │   ├── services/readme_generator.py
│   │   ├── config.py
│   │   └── main.py
│   ├── run.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── archived/
```

## Features

- Generate README from a GitHub repository URL
- Live progress stream (`scanning file...`) in the UI
- GitHub-style rendered markdown preview (not raw markdown syntax view)
- Multi-provider LLM support: OpenRouter or Hugging Face
- Cost-aware token budgeting and aggressive file filtering
- Ignores irrelevant files (including common data/model artifact folders)

## Quick Start

### 1. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

Create `.env` from template:

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
```

Set at least:

```env
GITHUB_TOKEN=your_github_token
OPENROUTER_API_KEY=your_openrouter_key
# OR HF_TOKEN=your_huggingface_token
```

Run backend:

```bash
python run.py
```

Backend URL: `http://127.0.0.1:8000`

### 2. Frontend Setup

```bash
cd frontend
python -m http.server 5500
```

Frontend URL: `http://127.0.0.1:5500`

For local development, the frontend reads its API base URL from `frontend/config.js`.

## API Endpoints

- `GET /api/health`
- `POST /api/generate-readme` (standard JSON response)
- `POST /api/generate-readme-stream` (NDJSON stream for live logs)

### Stream Endpoint Payload

```json
{
   "repo_url": "https://github.com/owner/repo",
   "use_hf_model": true
}
```

### Stream Event Types

- `status`
- `scan`
- `progress`
- `result`
- `done`
- `error`

## Efficiency and Filtering

To reduce cost and avoid irrelevant context, the backend:

- Includes only high-signal source/config files
- Skips common noisy directories (`tests`, `docs`, `examples`, etc.)
- Skips data/model directories (`data`, `datasets`, `artifacts`, `checkpoints`, `weights`)
- Skips data/model files (`.csv`, `.parquet`, `.npy`, `.pt`, `.onnx`, `.safetensors`, etc.)
- Enforces prompt/token budgets for both summarization and final README generation

Tune these in `backend/.env`:

- `MAX_FILES_TO_SUMMARIZE`
- `MAX_FILE_CONTENT_CHARS`
- `SUMMARIZER_MAX_OUTPUT_TOKENS`
- `README_MAX_SUMMARY_CHARS`
- `README_MAX_OUTPUT_TOKENS`

## Troubleshooting

- `GITHUB_TOKEN not set in environment`
   - Ensure `backend/.env` exists and has `GITHUB_TOKEN`
- `API key not configured`
   - Set `HF_TOKEN` in `backend/.env` (default path)
   - Optional fallback: set `OPENROUTER_API_KEY` and send `use_hf_model: false`
- `402` from OpenRouter (credits/token budget)
   - Lower token/file limits in `backend/.env`
   - Or switch to Hugging Face model in UI

## Deployment Notes

- Frontend is static and can be deployed on GitHub Pages
- Backend should be deployed separately on Render (or similar)
- Update `frontend/config.js` so `API_BASE_URL` points to your deployed backend URL
- If you use GitHub Pages, the frontend must call the Render URL over HTTPS
- A GitHub Actions workflow is included at `.github/workflows/deploy-pages.yml`

## License

MIT
