#!/bin/bash
# Setup and run script for Agentic AI Application Backend
# This script sets up the virtual environment and runs the FastAPI server

echo "========================================"
echo "Agentic AI Application - Backend Setup"
echo "========================================"
echo ""

# Check if in correct directory
if [ ! -d "app" ]; then
    echo "Error: Please run this script from the backend directory"
    exit 1
fi

# Create/activate virtual environment
echo "Step 1: Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating new virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "Step 2: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for .env file
echo ""
echo "Step 3: Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Please create .env file by copying .env.example and filling in your API keys:"
    echo "  - GITHUB_TOKEN"
    echo "  - OPENROUTER_API_KEY or HF_TOKEN"
    echo ""
    read -p "Do you want to continue? (y/n) " response
    if [ "$response" != "y" ] && [ "$response" != "Y" ]; then
        exit 1
    fi
else
    echo ".env file found"
fi

# Run the application
echo ""
echo "========================================"
echo "Starting FastAPI Server..."
echo "========================================"
echo ""
echo "API Documentation available at: http://127.0.0.1:8000/docs"
echo ""
python run.py
