@echo off
echo ====================================
echo MUQ Frontend - Local Development
echo ====================================
echo.

echo Starting Frontend Server...
cd frontend
python -m http.server 8010
