# Agentic AI Application

An AI-powered application for analyzing GitHub repositories and generating professional README files.

## Project Structure

This project is organized with **backend** and **frontend** separated for easy deployment via GitHub Pages.

```
Agentic-ai-application/
├── backend/                 # FastAPI backend application
│   ├── app/                # Application code
│   │   ├── api/           # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── main.py        # FastAPI app
│   │   ├── config.py      # Configuration
│   │   └── models.py      # Data models
│   ├── run.py             # Entry point
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example       # Environment template
│   └── README.md          # Backend documentation
├── frontend/               # Frontend application (create when needed)
├── archived/              # Old/generated files
└── README.md             # This file
```

## Quick Start

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. Run the server:
   ```bash
   python run.py
   ```

The API will be available at `http://127.0.0.1:8000`

### API Documentation

Once running, access the interactive documentation at:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Generate README
```
POST /api/generate-readme
```

**Request:**
```json
{
  "repo_url": "https://github.com/username/repository",
  "use_hf_model": false
}
```

**Response:**
```json
{
  "repo_url": "https://github.com/username/repository",
  "readme_content": "# Generated README content...",
  "file_count": 15,
  "status": "success"
}
```

### Health Check
```
GET /api/health
```

## Features

✅ **GitHub Repository Analysis** - Fetch and analyze code from repositories  
✅ **AI-Powered Summarization** - Automatic code summarization  
✅ **README Generation** - Professional README creation  
✅ **Multiple LLM Support** - OpenRouter or HuggingFace models  
✅ **RESTful API** - Clean, documented endpoints  
✅ **Error Handling** - Comprehensive error management  

## Requirements

- **Python 3.9+**
- **GitHub Token** (for accessing repositories)
- **OpenRouter API Key** OR **HuggingFace Token** (for LLM services)

## Configuration

All configuration is done via environment variables in the `.env` file. See `backend/.env.example` for all available options.

**Essential Variables:**
- `GITHUB_TOKEN` - GitHub personal access token
- `OPENROUTER_API_KEY` - OpenRouter API key
- `HF_TOKEN` - HuggingFace API token
- `DEBUG` - Development/Production mode

## Next Steps

1. **Frontend Development**: Create frontend in the `frontend/` directory
2. **Deployment**: Deploy backend to your preferred platform (Heroku, AWS, etc.)
3. **GitHub Pages**: Set up frontend for GitHub Pages deployment
4. **Integration**: Connect frontend to backend API

## Project Structure Benefits

- **Separation of Concerns**: Backend and frontend are independent
- **Easy Deployment**: Deploy backend and frontend separately
- **Scalability**: Each component can scale independently
- **Maintainability**: Clear organization and file structure
- **Frontend Friendly**: GitHub Pages compatible frontend

## Documentation

- **Backend**: See [backend/README.md](backend/README.md) for detailed backend documentation
- **Frontend**: Create frontend documentation when implementing

## Troubleshooting

### Backend won't start
1. Check that all required API keys are set in `.env`
2. Verify Python version is 3.9 or higher
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Check for port conflicts on port 8000

### API returns errors
1. Verify GITHUB_TOKEN is valid and has correct permissions
2. Check that OpenRouter or HuggingFace API keys are correct
3. Ensure repository URL is valid and accessible

## License

MIT License

## Support

For issues or feature requests, please open an issue in the repository.

## Setup
1. Clone and navigate:
```bash
git clone <repository-url>
cd Agentic-ai-application
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```
OPEN_AI_KEY=<your_openai_key>
GITHUB_TOKEN=<your_github_token>
HF_TOKEN=<your_huggingface_token>
```

## Usage
Execute:
```bash
python main.py
```
Note: Configure repository URL in main.py's app.invoke method.

## Contributing
Issues and pull requests welcome.

## License
MIT License
