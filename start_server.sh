#!/bin/bash
# Cattle Vision AI - Linux/Mac Startup Script

echo "========================================"
echo "  Cattle Vision AI - Starting Server"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo ""
    echo "Virtual environment created."
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    echo ""
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo ""
echo "Checking if models exist..."
if [ ! -f "best_enhanced_model.pth" ]; then
    echo "WARNING: Breed model file 'best_enhanced_model.pth' not found!"
fi
if [ ! -f "custom_model.h5" ]; then
    echo "WARNING: Disease model file 'custom_model.h5' not found!"
fi

echo ""
echo "========================================"
echo "  Starting FastAPI Server..."
echo "  Access at: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo "  Press Ctrl+C to stop"
echo "========================================"
echo ""

python app.py
