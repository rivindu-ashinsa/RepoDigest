"""
Pydantic models for request/response validation
"""
from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class GenerateReadmeRequest(BaseModel):
    """Request model for README generation endpoint"""
    repo_url: str
    use_hf_model: bool = False  # Use HuggingFace model instead of OpenRouter
    
    class Config:
        json_schema_extra = {
            "example": {
                "repo_url": "https://github.com/username/repo",
                "use_hf_model": False
            }
        }


class FileSummary(BaseModel):
    """Individual file summary"""
    file_path: str
    summary: str


class GenerateReadmeResponse(BaseModel):
    """Response model for README generation endpoint"""
    repo_url: str
    readme_content: str
    file_count: int
    status: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "repo_url": "https://github.com/username/repo",
                "readme_content": "# Project Title\n\n## Overview\n...",
                "file_count": 10,
                "status": "success"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str = "1.0.0"
