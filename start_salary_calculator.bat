@echo off
chcp 65001 >nul
echo ================================
echo    Salary Calculator Launcher
echo ================================
echo.

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found
    echo Please install Python from: https://python.org/downloads
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit
)

echo [OK] Python is installed

:: Check and install dependencies
echo [INFO] Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install packages
        pause
        exit
    )
) else (
    echo [OK] Packages already installed
)

:: Start application
echo.
echo [INFO] Starting Salary Calculator...
echo.
echo Browser will open automatically at: http://localhost:8501
echo If it doesn't open automatically, please open the URL above manually
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run streamlit_salary_calculator.py

pause