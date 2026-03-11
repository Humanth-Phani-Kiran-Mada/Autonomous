@echo off
REM Setup script for Self-Evolving AI System (Windows)

echo.
echo =====================================================
echo SELF-EVOLVING AI SYSTEM - SETUP (Windows)
echo =====================================================
echo.

REM Check Python version
echo Checking Python version...
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo. ✓ Created .env file - update with your API keys if needed
)

REM Create necessary directories
echo Creating data directories...
if not exist "data\memory" mkdir "data\memory"
if not exist "data\knowledge" mkdir "data\knowledge"
if not exist "data\cache" mkdir "data\cache"
if not exist "logs" mkdir "logs"

echo.
echo =====================================================
echo ✓ SETUP COMPLETE
echo =====================================================
echo.
echo To start the system, run:
echo   python main.py
echo.
echo Or activate the virtual environment first:
echo   venv\Scripts\activate.bat
echo.
