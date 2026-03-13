@echo off
echo ==================================
echo Intelli-Credit Quick Setup ^& Demo
echo For Windows
echo ==================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python not found. Please install Python 3.9+ and try again.
    pause
    exit /b 1
)

echo + Python found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo + Virtual environment created
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip >nul 2>&1

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ~ Some dependencies may have installation warnings. Check requirements.txt
) else (
    echo + Dependencies installed
)

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo To run the pipeline:
echo   venv\Scripts\activate    ^<-- Activate virtual environment
echo   python main.py           ^<-- Run complete pipeline
echo   python main.py --help    ^<-- See all options
echo.
echo To view the dashboard:
echo   Open frontend/dashboard.html in your browser
echo.
echo Documentation:
echo   README.md     - Full project documentation
echo   aboutus.txt   - Complete project overview
echo   docs/         - Detailed architecture docs
echo.
pause

REM Ask if user wants to run now
set /p RUN_NOW="Run the pipeline now? (y/n): "
if /i "%RUN_NOW%"=="y" (
    python main.py
    pause
)
