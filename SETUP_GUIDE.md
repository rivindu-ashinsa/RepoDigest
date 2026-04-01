# Setup and Deployment Guide

## Project Overview

This is a reorganized FastAPI-based backend application for GitHub repository analysis and README generation. The project is now properly structured with separated backend and frontend for easy deployment via GitHub Pages.

## Directory Structure

```
Agentic-ai-application/
├── backend/                      # FastAPI Backend Application
│   ├── app/
│   │   ├── __init__.py          # Package initialization
│   │   ├── main.py              # FastAPI application setup
│   │   ├── config.py            # Configuration and settings
│   │   ├── models.py            # Pydantic models for validation
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py        # API endpoint definitions
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── scraper.py       # GitHub repository scraper
│   │       ├── summarizer.py    # Code summarization service
│   │       └── readme_generator.py  # README generation logic
│   ├── run.py                   # Application entry point
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment variables template
│   ├── .gitignore              # Git ignore rules
│   ├── setup_and_run.bat       # Windows setup script
│   ├── setup_and_run.sh        # Unix setup script
│   └── README.md               # Backend documentation
├── frontend/                     # Frontend (to be created)
├── archived/                     # Old and generated files
│   ├── DEMENTIA.md
│   ├── GENERATED_README.md
│   ├── GENERATED_README_OPTIMIZED.md
│   ├── hf_models.py
│   ├── main.py
│   ├── READMEE.md
│   ├── scraper.py
│   ├── test.ipynb
│   └── walkie_genie_readme.md
├── .env                         # Local environment configuration (not tracked)
├── .gitignore                   # Global git ignore
├── requirements.txt             # Root-level readme for dependencies
└── README.md                    # Main project README
```

## Quick Start (Windows)

### Option 1: Using Setup Script (Recommended)

```bash
cd backend
setup_and_run.bat
```

This script will:
1. Create virtual environment if needed
2. Activate it
3. Install dependencies
4. Check for .env configuration
5. Start the FastAPI server

### Option 2: Manual Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your API keys

# Run the application
python run.py
```

## Quick Start (macOS/Linux)

### Option 1: Using Setup Script (Recommended)

```bash
cd backend
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### Option 2: Manual Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the application
python run.py
```

## Configuration (Important!)

Before running, you must configure the `.env` file:

1. **Copy the template**:
   ```bash
   cp backend/.env.example backend/.env
   ```

2. **Edit `backend/.env`** and set:

   ```env
   # Required: GitHub Token
   GITHUB_TOKEN=your_github_personal_access_token
   
   # Choose ONE of the following:
   # Option A: OpenRouter (Recommended for fast responses)
   OPENROUTER_API_KEY=your_openrouter_api_key
   
   # Option B: HuggingFace
   HF_TOKEN=your_huggingface_token
   
   # Optional: Site information for OpenRouter ranking
   SITE_URL=http://localhost:8000
   SITE_NAME=Agentic AI Application
   
   # Application settings
   DEBUG=True
   PORT=8000
   ```

## Obtaining API Keys

### GitHub Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `public_repo`, `repo`
4. Copy and save the token to `.env`

### OpenRouter API Key
1. Go to https://openrouter.ai/keys
2. Create a new API key
3. Copy and save to `.env`

### HuggingFace Token
1. Go to https://huggingface.co/settings/tokens
2. Create a new token with "read" access
3. Copy and save to `.env`

## Running the Application

After setup and configuration:

```bash
cd backend
python run.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## Accessing the API

### Interactive Documentation (Swagger UI)
```
http://127.0.0.1:8000/docs
```

### Alternative Documentation (ReDoc)
```
http://127.0.0.1:8000/redoc
```

### API Endpoints

**Health Check:**
```
GET /api/health
```

**Generate README:**
```
POST /api/generate-readme

{
  "repo_url": "https://github.com/owner/repo",
  "use_hf_model": false
}
```

## Example Requests

### Using cURL
```bash
curl -X POST "http://127.0.0.1:8000/api/generate-readme" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/owner/repository",
    "use_hf_model": false
  }'
```

### Using Python
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/api/generate-readme",
    json={
        "repo_url": "https://github.com/owner/repository",
        "use_hf_model": False
    }
)

data = response.json()
if response.status_code == 200:
    print(data['readme_content'])
else:
    print(f"Error: {data['detail']}")
```

## Troubleshooting

### Issue: "GITHUB_TOKEN not set"
- **Solution**: Check that `.env` file exists in backend directory and `GITHUB_TOKEN` is set

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
- **Solution**: Ensure virtual environment is activated and dependencies installed
  ```bash
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  pip install -r requirements.txt
  ```

### Issue: "Port 8000 already in use"
- **Solution**: Change PORT in `.env` file or kill the process using port 8000

### Issue: "Invalid API key"
- **Solution**: Verify your API keys are correct and have necessary permissions

## Project Features

✅ **FastAPI Backend** - Modern, fast API framework  
✅ **GitHub Integration** - Fetch and analyze repositories  
✅ **AI-Powered Summarization** - Multiple LLM options  
✅ **README Generation** - Professional documentation  
✅ **RESTful API** - Clean, documented endpoints  
✅ **Error Handling** - Comprehensive validation  
✅ **Type Safety** - Pydantic models  
✅ **API Documentation** - Auto-generated docs (Swagger, ReDoc)  

## Next Steps

1. ✅ Backend is set up and ready to run
2. ⏳ Frontend development (when ready)
   - Create `frontend/` directory
   - Build UI to interact with API
   - Deploy to GitHub Pages
3. 🚀 Production deployment
   - Deploy backend to cloud platform
   - Configure CORS for frontend domain
   - Set up proper environment variables

## Code Quality & Standards

- **Type Hints**: All functions have proper type annotations
- **Documentation**: Comprehensive docstrings for all modules
- **Error Handling**: Proper exception handling and user-friendly messages
- **Configuration**: Centralized settings management
- **Modularity**: Clean separation of concerns
- **API Validation**: Pydantic models for request/response validation

## Development Tips

### Running in Debug Mode
The app runs in debug/reload mode by default when `DEBUG=True` in `.env`. This means:
- Server restarts on code changes
- Better error messages
- Slower performance

For production, set `DEBUG=False`.

### Adding New Endpoints
1. Create route handler in `backend/app/api/routes.py`
2. Add Pydantic models in `backend/app/models.py` if needed
3. Add business logic in appropriate service module
4. Route automatically available at next restart

## Support & Documentation

- **Backend README**: [backend/README.md](backend/README.md)
- **Main README**: [README.md](README.md)
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **OpenRouter Docs**: https://openrouter.ai/docs
- **HuggingFace Docs**: https://huggingface.co/docs

---

**Happy Coding! 🚀**
