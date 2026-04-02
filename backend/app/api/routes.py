"""
API routes for the Agentic AI Application
Provides endpoints for README generation and repository analysis
"""
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List

from ..models import GenerateReadmeRequest, GenerateReadmeResponse, HealthResponse
from ..services import fetch_repo_code, CodeSummarizer, ReadmeGenerator

router = APIRouter()


def _ndjson_line(payload: dict) -> str:
    """Serialize an event payload to NDJSON line format."""
    return json.dumps(payload, ensure_ascii=True) + "\n"


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Health status and version info
    """
    return HealthResponse(status="healthy", version="1.0.0")


@router.post("/generate-readme", response_model=GenerateReadmeResponse, tags=["README Generation"])
async def generate_readme(request: GenerateReadmeRequest):
    """
    Generate a professional README for a GitHub repository
    
    Args:
        request: GenerateReadmeRequest with repo_url and optional use_hf_model flag
        
    Returns:
        GenerateReadmeResponse with generated README content
        
    Raises:
        HTTPException: If repository cannot be accessed or generation fails
    """
    try:
        # Fetch repository code
        print(f"Fetching repository: {request.repo_url}")
        files = fetch_repo_code(request.repo_url)
        
        if not files:
            raise HTTPException(
                status_code=400,
                detail="No files found in repository. Please check the URL and try again."
            )
        
        # Summarize each file
        print(f"Summarizing {len(files)} files...")
        summarizer = CodeSummarizer(use_hf=request.use_hf_model)
        file_summaries: List[str] = []
        
        for file in files:
            summary = summarizer.summarize_file(file["path"], file["content"])
            file_summaries.append(summary)
            print(f"✓ Summarized: {file['path']}")
        
        # Generate README
        print("Generating README...")
        generator = ReadmeGenerator(use_hf=request.use_hf_model)
        readme_content = generator.generate(file_summaries)
        
        print("✅ README generation complete")
        
        return GenerateReadmeResponse(
            repo_url=request.repo_url,
            readme_content=readme_content,
            file_count=len(files),
            status="success"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/generate-readme-stream", tags=["README Generation"])
async def generate_readme_stream(request: GenerateReadmeRequest):
    """
    Generate README while streaming progress logs as NDJSON.

    Response is `application/x-ndjson` where each line is a JSON object.
    """

    async def event_stream():
        try:
            yield _ndjson_line({
                "type": "status",
                "message": f"Fetching repository: {request.repo_url}"
            })

            files = fetch_repo_code(request.repo_url)
            if not files:
                yield _ndjson_line({
                    "type": "error",
                    "message": "No files found in repository. Please check the URL and try again."
                })
                return

            total_files = len(files)
            yield _ndjson_line({
                "type": "status",
                "message": f"Repository loaded. {total_files} files detected."
            })

            summarizer = CodeSummarizer(use_hf=request.use_hf_model)
            file_summaries: List[str] = []

            for index, file in enumerate(files, start=1):
                file_path = file["path"]
                yield _ndjson_line({
                    "type": "scan",
                    "message": f"Scanning file {index}/{total_files}: {file_path}",
                    "current": index,
                    "total": total_files,
                    "file": file_path
                })

                summary = summarizer.summarize_file(file_path, file["content"])
                file_summaries.append(summary)

                yield _ndjson_line({
                    "type": "progress",
                    "message": f"Summarized {file_path}",
                    "current": index,
                    "total": total_files,
                    "file": file_path
                })

            yield _ndjson_line({
                "type": "status",
                "message": "Generating final README.md..."
            })

            generator = ReadmeGenerator(use_hf=request.use_hf_model)
            readme_content = generator.generate(file_summaries)

            yield _ndjson_line({
                "type": "result",
                "repo_url": request.repo_url,
                "readme_content": readme_content,
                "file_count": total_files,
                "status": "success"
            })

            yield _ndjson_line({
                "type": "done",
                "message": "README generation complete"
            })

        except ValueError as e:
            yield _ndjson_line({"type": "error", "message": str(e)})
        except Exception as e:
            yield _ndjson_line({"type": "error", "message": f"Internal error: {str(e)}"})

    return StreamingResponse(event_stream(), media_type="application/x-ndjson")
