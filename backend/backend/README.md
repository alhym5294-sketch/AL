# MUQ System - Django REST Framework Backend

## Overview
This is the Django REST Framework backend for the MUQ attendance system with face recognition. It provides a secure API with JWT authentication and PostgreSQL database support.

## Features
- JWT-based authentication with token refresh
- Role-based access control (Admin, Teacher, Student, Staff)
- Face profile management with versioning
- Attendance tracking and reporting
- Schedule management
- Department, Stage, and Branch hierarchy
- CORS support for frontend integration
- PostgreSQL production database

## Tech Stack
- Django 5.1.1
- Django REST Framework 3.15.2
- Django REST Framework SimpleJWT 5.3.1
- PostgreSQL
- Gunicorn (production server)
- Whitenoise (static file serving)

## Local Development

### Prerequisites
- Python 3.8+
- PostgreSQL (optional, defaults to SQLite for local dev)

### Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py create_superuser
   ```

6. **Run development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/logout/` - Logout (blacklist refresh token)
- `GET /api/auth/me/` - Get current user info
- `POST /api/auth/token/refresh/` - Refresh access token

### Users
- `GET /api/users/` - List users (admin only)
- `POST /api/users/` - Create user (admin only)
- `GET /api/users/{id}/` - Get user details
- `PATCH /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user (admin only)
- `POST /api/users/{id}/deactivate/` - Deactivate user (admin only)
- `POST /api/users/{id}/reactivate/` - Reactivate user (admin only)
- `POST /api/users/{id}/reset_password/` - Reset password (admin only)

### Departments
- `GET /api/departments/` - List departments
- `POST /api/departments/` - Create department
- `GET /api/departments/{id}/` - Get department details
- `PATCH /api/departments/{id}/` - Update department
- `DELETE /api/departments/{id}/` - Delete department

### Stages
- `GET /api/stages/` - List stages
- `POST /api/stages/` - Create stage
- `GET /api/stages/{id}/` - Get stage details
- `PATCH /api/stages/{id}/` - Update stage
- `DELETE /api/stages/{id}/` - Delete stage

### Branches
- `GET /api/branches/` - List branches
- `POST /api/branches/` - Create branch
- `GET /api/branches/{id}/` - Get branch details
- `PATCH /api/branches/{id}/` - Update branch
- `DELETE /api/branches/{id}/` - Delete branch

### Attendance
- `GET /api/attendance/` - List attendance records
- `POST /api/attendance/` - Create attendance record
- `GET /api/attendance/{id}/` - Get attendance details
- `PATCH /api/attendance/{id}/` - Update attendance
- `DELETE /api/attendance/{id}/` - Delete attendance

### Schedule
- `GET /api/schedule/` - List schedule items
- `POST /api/schedule/` - Create schedule item
- `GET /api/schedule/{id}/` - Get schedule details
- `PATCH /api/schedule/{id}/` - Update schedule
- `DELETE /api/schedule/{id}/` - Delete schedule

### Face Profiles
- `GET /api/face-profiles/` - List face profiles
- `POST /api/face-profiles/` - Create face profile (admin only)
- `GET /api/face-profiles/{id}/` - Get face profile details
- `PATCH /api/face-profiles/{id}/` - Update face profile (admin only)
- `DELETE /api/face-profiles/{id}/` - Delete face profile (admin only)

### Health Check
- `GET /api/health/` - Health check endpoint

## Environment Variables

See `.env.example` for all available variables. Key variables:

- `DEBUG` - Set to `False` in production
- `SECRET_KEY` - Django secret key (generate with `python manage.py generatesecretkey`)
- `DB_ENGINE` - `sqlite` for local, `postgresql` for production
- `CORS_ALLOWED_ORIGINS` - Frontend domains allowed to access API
- `JWT_ACCESS_TOKEN_HOURS` - Access token lifetime
- `JWT_REFRESH_TOKEN_DAYS` - Refresh token lifetime

## Security Features

- JWT authentication with automatic token refresh
- Token blacklisting on logout
- Password hashing with Django's default validators
- CORS configuration
- Session security settings
- HSTS and SSL redirect in production

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Railway deployment instructions.

## Project Structure

```
Django/
├── attendance/          # Attendance and schedule models/views
├── departments/         # Department, Stage, Branch models/views
├── users/              # User and FaceProfile models/views
├── muq_system/         # Django project settings
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── Procfile           # Railway deployment config
├── railway.json       # Railway project config
├── .env.example       # Environment variables template
└── DEPLOYMENT.md      # Deployment guide
```

## Testing

Run tests with:
```bash
python manage.py test
```

## Admin Panel

Access Django admin at `/admin/` with your superuser credentials.

## License

Proprietary - MUQ System
