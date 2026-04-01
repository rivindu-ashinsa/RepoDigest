@echo off
REM Setup and run script for Agentic AI Application Backend
REM This script sets up the virtual environment and runs the FastAPI server

echo ========================================
echo Agentic AI Application - Backend Setup
echo ========================================
echo.

REM Check if in correct directory
if not exist "app\" (
    echo Error: Please run this script from the backend directory
    exit /b 1
)

REM Create/activate virtual environment
echo Step 1: Setting up Python virtual environment...
if not exist "venv\" (
    echo Creating new virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo.
echo Step 2: Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Check for .env file
echo.
echo Step 3: Checking environment configuration...
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create .env file by copying .env.example and filling in your API keys:
    echo   - GITHUB_TOKEN
    echo   - OPENROUTER_API_KEY or HF_TOKEN
    echo.
    echo Do you want to continue? (y/n)
    set /p response=
    if /i not "%response%"=="y" exit /b 1
) else (
    echo .env file found
)

REM Run the application
echo.
echo ========================================
echo Starting FastAPI Server...
echo ========================================
echo.
echo API Documentation available at: http://127.0.0.1:8000/docs
echo.
python run.py

pause
