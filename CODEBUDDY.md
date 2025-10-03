# Django Hub - CODEBUDDY Guide

## Project Overview
Django Hub is an enterprise-level user management system built with Django 4.2+. The project features modular architecture, RESTful API endpoints, and comprehensive logging system.

## Essential Development Commands

### Django Management Commands
```bash
# Start development server
python manage.py runserver 0.0.0.0:8000

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test
python manage.py test demo

# Collect static files (production)
python manage.py collectstatic

# Django shell
python manage.py shell
```

### Docker Commands
```bash
# Build Docker image
docker build -t django-hub .

# Run container (development)
docker run -p 8000:8000 django-hub

# Run with volume mounts (production)
docker run -d --name django-hub -p 8000:8000 -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs django-hub
```

### Code Quality Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Code formatting (if Black is configured)
black .

# Import sorting (if isort is configured)
isort .
```

## Project Architecture

### Directory Structure
```
demo-django-hub/
├── DjangoProject/           # Project configuration
│   ├── settings.py         # Main settings (Django 5.2+)
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py           # WSGI configuration
├── demo/                  # Main application
│   ├── views/            # Modular view layer
│   │   ├── auth_views.py    # Authentication views
│   │   ├── user_views.py     # User management views
│   │   ├── group_views.py    # Group management views
│   │   └── system_views.py   # System initialization
│   ├── api/              # RESTful API layer
│   │   ├── user_api.py       # User API endpoints
│   │   ├── group_api.py      # Group API endpoints
│   │   └── serializers.py    # API serializers
│   ├── views.py          # Backward compatibility layer
│   ├── logger.py         # Loguru-based logging system
│   └── urls.py           # App URL routing
├── data/                 # Data directory
│   └── db.sqlite3        # SQLite database file
├── logs/                 # Log files directory
├── staticfiles/          # Collected static files
└── templates/            # HTML templates
```

### Key Architectural Patterns

#### 1. Modular View Architecture
- Views are organized by functionality in `demo/views/` directory
- `demo/views.py` provides backward compatibility for existing URLs
- API endpoints are separated into `demo/api/` directory

#### 2. Logging System (`demo/logger.py`)
- Uses Loguru for advanced logging
- Four log handlers: django.log, error.log, security.log, audit.log
- Automatic rotation at 500MB, retention for 30 days
- Client IP and browser information logging
- Async logging with error backtraces

#### 3. API Design
- RESTful endpoints return JSON with consistent format:
```json
{
  "status": "success|error",
  "message": "string",
  "data": "object|array|null",
  "errors": "object|null"
}
```

### Database Configuration
- Development: SQLite at `data/db.sqlite3`
- Production: PostgreSQL support via psycopg2-binary
- All database operations logged for audit purposes

## Critical Development Information

### URL Routing Structure
- Main app namespace: `demo`
- API endpoints under `/demo/` prefix
- System initialization: `/demo/init/<password>/`
- Authentication endpoints: `/demo/login/`, `/demo/register/`

### Authentication & Permissions
- Three-level permission system: superuser, admin, regular user
- CSRF protection enabled
- CORS configured for all origins (development)
- User management requires appropriate permissions

### System Initialization
- Initialize system via `/demo/init/admin123/` endpoint
- Creates default user groups and superuser account
- Default admin credentials: admin/admin

### Logging Best Practices
- Use `log_operation()` for general operations
- Use `log_security()` for security-related events
- Use `log_audit()` for important system changes
- All functions support client context from request objects

## Important Configuration Details

### Settings (`DjangoProject/settings.py`)
- `DEBUG = True` (development)
- `ALLOWED_HOSTS = ['*']`
- CORS enabled for all origins
- Static files collected to `staticfiles/` directory
- Database path: `data/db.sqlite3`

### Dependencies (`requirements.txt`)
- Django >=4.2,<5.0
- gunicorn >=21.2.0 (production)
- django-cors-headers >=4.7.0
- loguru >=0.7.0
- psycopg2-binary >=2.9.1 (PostgreSQL support)

## Development Workflow

### Adding New Features
1. Create views in appropriate module under `demo/views/`
2. Add API endpoints in `demo/api/` if needed
3. Update URL routing in `demo/urls.py`
4. Add proper logging using logger functions
5. Test with appropriate user permissions

### Database Changes
1. Update models in `demo/models.py`
2. Generate migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Test with sample data

### Deployment Considerations
- Set `DEBUG = False` in production
- Configure proper `ALLOWED_HOSTS`
- Use PostgreSQL for production database
- Ensure `logs/` directory has write permissions
- Run `collectstatic` before deployment

## Common Issues & Solutions

### Database Connection Issues
- Check `data/db.sqlite3` file permissions
- Ensure `data/` directory exists and is writable

### Permission Errors
- Verify user has appropriate permissions in Django admin
- Check group assignments for non-superusers

### Logging Problems
- Ensure `logs/` directory exists and is writable
- Check log file permissions and disk space

### API Endpoint Issues
- Verify CSRF tokens for POST requests
- Check CORS configuration for cross-domain requests
- Validate JSON request format and parameters