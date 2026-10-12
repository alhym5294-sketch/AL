@echo off
echo ====================================
echo MUQ System - Local Development
echo ====================================
echo.

echo [1/3] Starting Backend...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt -q
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@muq.com --noinput 2>nul || echo Superuser may already exist
python manage.py runserver 8000
