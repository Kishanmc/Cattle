@echo off
REM Cattle Vision AI - Windows Startup Script

echo ========================================
echo   Cattle Vision AI - Starting Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    echo.
    echo Virtual environment created.
    echo Installing dependencies...
    call venv\Scripts\activate
    pip install -r requirements.txt
    echo.
) else (
    echo Activating virtual environment...
    call venv\Scripts\activate
)

echo.
echo Checking if models exist...
if not exist "best_enhanced_model.pth" (
    echo WARNING: Breed model file 'best_enhanced_model.pth' not found!
)
if not exist "custom_model.h5" (
    echo WARNING: Disease model file 'custom_model.h5' not found!
)

echo.
echo ========================================
echo   Starting FastAPI Server...
echo   Access at: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Press Ctrl+C to stop
echo ========================================
echo.

python app.py
