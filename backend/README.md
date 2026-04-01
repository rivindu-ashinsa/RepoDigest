# Agentic AI Application - Backend

A FastAPI-based backend for analyzing GitHub repositories and generating professional README files using AI models.

## Features

- **GitHub Repository Analysis**: Fetch and analyze code from GitHub repositories
- **Code Summarization**: Automatically summarize code files using OpenRouter or HuggingFace APIs
- **README Generation**: Generate professional README files from code analysis
- **Multiple LLM Support**: Use either OpenRouter or HuggingFace models
- **RESTful API**: Clean, documented API endpoints with FastAPI
- **Production Ready**: Error handling, validation, and proper logging

## Tech Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **API Clients**: OpenAI Python SDK, Requests
- **AI Models**: OpenRouter, HuggingFace
- **Configuration**: Python-dotenv
- **Type Validation**: Pydantic

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app setup
│   ├── config.py            # Configuration and settings
│   ├── models.py            # Pydantic request/response models
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API endpoints
│   └── services/
│       ├── __init__.py
│       ├── scraper.py       # GitHub repository scraper
│       ├── summarizer.py    # Code summarization service
│       └── readme_generator.py  # README generation service
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- GitHub Token (for accessing repositories)
- OpenRouter API key OR HuggingFace token

### Setup Steps

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and fill in your API keys:
     - `GITHUB_TOKEN`: Your GitHub personal access token
     - `OPENROUTER_API_KEY`: Your OpenRouter API key (if using OpenRouter)
     - `HF_TOKEN`: Your HuggingFace token (if using HuggingFace)
     - `SITE_URL` and `SITE_NAME`: Optional (for OpenRouter ranking)

## Usage

### Running the Server

```bash
python run.py
```

The API will be available at `http://127.0.0.1:8000`

### API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://127.0.0.1:8000/docs (Swagger UI)
- **Alternative API docs**: http://127.0.0.1:8000/redoc (ReDoc)

### API Endpoints

#### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

#### Generate README
```http
POST /api/generate-readme
```

**Request Body:**
```json
{
  "repo_url": "https://github.com/username/repository",
  "use_hf_model": false
}
```

**Parameters:**
- `repo_url` (required): Full GitHub repository URL
- `use_hf_model` (optional): Use HuggingFace model instead of OpenRouter (default: false)

**Response (on success):**
```json
{
  "repo_url": "https://github.com/username/repository",
  "readme_content": "# Project Title\n\n## Overview\n...",
  "file_count": 15,
  "status": "success"
}
```

**Error Response (on failure):**
```json
{
  "detail": "Error message explaining what went wrong"
}
```

### Example Usage with cURL

```bash
curl -X POST "http://127.0.0.1:8000/api/generate-readme" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/owner/repo",
    "use_hf_model": false
  }'
```

### Example Usage with Python

```python
import requests

url = "http://127.0.0.1:8000/api/generate-readme"
payload = {
    "repo_url": "https://github.com/owner/repo",
    "use_hf_model": False
}

response = requests.post(url, json=payload)
data = response.json()

if response.status_code == 200:
    print(data['readme_content'])
else:
    print(f"Error: {data['detail']}")
```

## Configuration

### Environment Variables

All configuration is managed through the `.env` file. See `.env.example` for all available options.

**Key Variables:**
- `GITHUB_TOKEN`: Required for accessing private repositories
- `OPENROUTER_API_KEY`: Required if using OpenRouter (default)
- `HF_TOKEN`: Required if using HuggingFace models
- `DEBUG`: Set to `True` for development, `False` for production
- `HOST`: Server host (default: 127.0.0.1)
- `PORT`: Server port (default: 8000)

## Development

### Code Structure

- **Services**: Modular services for different functionalities
  - `scraper.py`: GitHub repository interaction
  - `summarizer.py`: Code summarization using LLMs
  - `readme_generator.py`: README generation logic

- **API Layer**: FastAPI routes with request/response validation
- **Configuration**: Centralized settings management
- **Models**: Pydantic models for data validation

### Error Handling

The API includes comprehensive error handling:
- Invalid repository URLs
- Missing API credentials
- API rate limits
- Network errors
- LLM generation failures

## Deployment

### Production Considerations

1. **Set `DEBUG=False`** in `.env`
2. **Use a production ASGI server** (uvicorn with multiple workers, gunicorn, etc.)
3. **Configure CORS** for your frontend domain
4. **Set proper HOST and PORT** for your infrastructure
5. **Use environment-specific `.env` files**
6. **Implement rate limiting** if needed
7. **Add authentication** if exposing publicly

### Example Production Run

```bash
# Using gunicorn (install with: pip install gunicorn)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

## Troubleshooting

### Common Issues

1. **"GITHUB_TOKEN not set"**
   - Ensure `.env` file exists and has `GITHUB_TOKEN` set
   - Restart the server after editing `.env`

2. **"API key not configured"**
   - Check that `OPENROUTER_API_KEY` or `HF_TOKEN` is set in `.env`
   - Verify the API key is correct and has necessary permissions

3. **Repository not found**
   - Verify the GitHub repository URL is correct
   - Check that your GITHUB_TOKEN has access to the repository

4. **LLM API errors**
   - Check API key validity
   - Verify API rate limits haven't been exceeded
   - Check internet connection

## License

This project is licensed under the MIT License.

## Support

For issues, feature requests, or suggestions, please create an issue in the repository.
