#!/bin/bash

echo "================================"
echo "    Salary Calculator Launcher"
echo "================================"
echo

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found"
    echo "Please install Python3:"
    echo "  macOS: brew install python"
    echo "  Ubuntu: sudo apt install python3 python3-pip"
    read -p "Press Enter to exit..."
    exit 1
fi

echo "[OK] Python3 is installed"

# Check and install dependencies
echo "[INFO] Checking dependencies..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "[INFO] Installing required packages..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install packages"
        read -p "Press Enter to exit..."
        exit 1
    fi
else
    echo "[OK] Packages already installed"
fi

# Start application
echo
echo "[INFO] Starting Salary Calculator..."
echo
echo "Browser will open automatically at: http://localhost:8501"
echo "If it doesn't open automatically, please open the URL above manually"
echo
echo "Press Ctrl+C to stop the application"
echo

python3 -m streamlit run streamlit_salary_calculator.py