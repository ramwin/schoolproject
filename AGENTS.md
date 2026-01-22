# schoolproject - Django Backend Project

## Project Overview

A Django-based project for school management/testing with REST API capabilities, asynchronous task processing, and comprehensive logging infrastructure. This appears to be both a development testbed and a potential production application for school-related data management.

### Technology Stack

- **Framework**: Django 5.0+ with Python 3.11+
- **Database**: PostgreSQL (multiple database support)
- **API**: Django REST Framework
- **Async Tasks**: Celery with Redis broker
- **WSGI Server**: Gunicorn
- **Caching**: Redis
- **Type Checking**: mypy with django-stubs
- **Linting**: pylint with pylint-django
- **Testing**: pytest with pytest-django
- **Logging**: Comprehensive multi-level file logging with colorlog

## Project Structure

### Core Applications

- **`schoolproject/`** - Main Django project directory
  - Split settings pattern (settings.py + separate config files)
  - Celery configuration
  - URL routing
  
- **`school/`** - Main application
  - Models for Student, Exam, Tag, Klass, School
  - REST API serializers
  - Celery tasks
  - Management commands
  - Tests

### Configuration Files

- **`requirements.txt`** - Python dependencies
- **`pytest.ini`** - Test configuration (DJANGO_SETTINGS_MODULE)
- **`.pylintrc`** - pylint rules with Django plugin
- **`mypy.ini`** - Type checking configuration
- **`gunicorn_config.py`** - Production WSGI server settings
- **`.env.shared`** - Shared environment variables (Redis, DEBUG)

## Build and Development Commands

### Run Development Server
```bash
python3 manage.py runserver
```

### Run Tests
```bash
./run_test.sh
# or directly:
python3 manage.py test django_commands  # Current test target
```

### Run Production Server
```bash
./run_gunicorn.sh
# or directly:
gunicorn schoolproject.wsgi -c gunicorn_config.py
```

### Database Operations
```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```

### Celery Worker
```bash
celery -A schoolproject worker -l info
```

### Code Quality Checks
```bash
# Linting
pylint school/ schoolproject/

# Type checking
mypy school/ schoolproject/
```

### Custom Management Commands
- `python3 manage.py create_lots_of_students`
- `python3 manage.py student_grow`
- `python3 manage.py test_log`

## Code Style Guidelines

### Python Code Style
- **Indentation**: 4 spaces (enforced by pylint)
- **Line Length**: 100 characters maximum
- **Naming Conventions**:
  - Classes: PascalCase
  - Functions/variables: snake_case
  - Constants: UPPER_CASE
- **File Encoding**: UTF-8 with `#!/usr/bin/env python3` and `# -*- coding: utf-8 -*-` headers

### Django Conventions
- Model classes in `models/` subdirectory
- Each model file focuses on specific domain (base.py, relations.py)
- Management commands in `management/commands/`
- Serializers in dedicated `serializers.py`
- Tasks in `tasks.py`

### Documentation
- Author header: `# Xiang Wang <ramwin@qq.com>`
- Module-level docstrings for complex modules
- Follow existing patterns for consistency

### Import Style
- Absolute imports preferred
- Group imports: standard library, third-party, Django, local
- Type hints encouraged (mypy configured)

## Configuration Details

### Settings Architecture
Settings are split across multiple files imported in `settings.py`:
- `logging_settings.py` - Comprehensive logging to `log/` directory
- `cache_settings.py` - Redis cache configuration
- `rest_settings.py` - Django REST Framework settings (currently minimal)
- `database_settings.py` - PostgreSQL with multiple database support

### Logging Infrastructure
- **Log Directory**: `log/` (auto-created)
- **Log Levels**: Separate files for DEBUG, INFO, WARNING, ERROR
- **Rotation**: Timed rotation (hourly for debug, daily for info/error)
- **Format**: Verbose format with timestamp, process ID, function name, line number
- **Color Console**: Colored output for console with colorlog
- **Command Logging**: Separate log files per management command

### Database Configuration
- **Primary DB**: `schoolproject` (PostgreSQL)
- **Secondary DB**: `schoolproject_02` (PostgreSQL)
- **Environment Variables**: `.env.shared` and `.env` for configuration
- **Debug Mode**: Controlled by `DEBUG` environment variable

### Celery Configuration
- **Broker**: Redis (redis://localhost:6379)
- **Backend**: Redis (redis://localhost:6379/)
- **Timezone**: Asia/Shanghai
- **Task Tracking**: Enabled with 30-minute time limit

### API Configuration
- REST Framework installed but minimally configured
- Token authentication available
- Django filters and CORS headers enabled
- Health check endpoints for monitoring

## Testing Strategy

### Test Framework
- **pytest** with django integration
- **Test Location**: `school/tests/`
- **Current Test Focus**: `django_commands` app
- **Monkeypatch Support**: Utilities for mocking (see `test_pytest.py`)

### Test Types
- Unit tests for utilities
- Integration tests for management commands
- Database operation tests
- Template tests
- Fixture tests

### Running Tests
```bash
# Run specific app tests
python3 manage.py test django_commands

# Run with pytest
pytest
```

## Production Deployment

### Gunicorn Configuration
- **Workers**: 4
- **Threads**: 1 per worker
- **Bind**: 0.0.0.0:8000
- **Logs**: `log/gunicorn.access.log` and `log/gunicorn.error.log`
- **PID File**: `gunicorn.pid`
- **Daemon Mode**: Disabled (for systemd/supervisor)

### Supervisor Integration
- **Script**: `deploy/生成supervisord配置.py` generates supervisor configs
- **Log Rotation**: 40MB max with 3 backups
- **Auto-restart**: Enabled with 3 retries
- **Environment**: Configured for virtual environment

### Monitoring
- **Health Checks**: Enabled via django-health-check
- **Database health**: DB, cache, Celery, PSUtil, Redis
- **Logging**: Comprehensive error and performance logging

## Key Features

### Models
- **Student**: Core model with name, code, height, age, info (JSON), timestamps
- **Exam**: Linked to students with scores
- **Tag**: Text-based tagging system
- **Klass**: Class/group organization
- **School**: School organization

### API Endpoints
- Django admin: `/admin/`
- Django commands API: `/api/django-commands/`

### Background Tasks
- `add` task: Async addition with delay and database operations
- Sleep-based demonstration tasks
- Celery beat support (timezone configured)

## Security Considerations

- **Secret Key**: Keep `SECRET_KEY` secure in production
- **Debug Mode**: NEVER run with `DEBUG=true` in production
- **Allowed Hosts**: Configure properly for production
- **Database**: Use environment-specific database credentials
- **CORS**: Configured for API access (review in production)

## Development Workflow

1. **Setup**: Install requirements, configure `.env`, setup PostgreSQL and Redis
2. **Database**: Run migrations, load initial data if needed
3. **Development**: Use `runserver` for development
4. **Testing**: Write tests, ensure they pass
5. **Code Quality**: Run pylint and mypy
6. **Production**: Use Gunicorn with supervisor

## Notes

- Project is configured for Chinese language (`zh-hans`) and Shanghai timezone
- Author: Xiang Wang (ramwin@qq.com)
- Comprehensive logging helps with debugging in development and production
- Multiple database support allows for sharding or separation of concerns
- Celery tasks demonstrate async patterns with proper logging