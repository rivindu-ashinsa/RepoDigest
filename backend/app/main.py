"""
Main FastAPI application
Core application setup and configuration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router
from .config import settings

# Create FastAPI app
app = FastAPI(
    title="Agentic AI Application",
    description="AI-powered GitHub repository analysis and README generation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["API"])


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Agentic AI Application API",
        "version": "1.0.0",
        "docs": "/docs",
        "debug": settings.DEBUG
    }
