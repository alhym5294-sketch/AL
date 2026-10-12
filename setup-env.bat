@echo off
echo ====================================
echo Setup Environment for MUQ System
echo ====================================
echo.

cd backend
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo .env file created successfully!
) else (
    echo .env file already exists.
)

echo.
echo Setup complete!
echo You can now run: start.bat
