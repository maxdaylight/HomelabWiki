# HomelabWiki Backend

A Flask-based REST API backend for HomelabWiki with enterprise LDAP authentication and comprehensive content management capabilities.

## 🚀 Features

- **🔐 LDAP/Active Directory Authentication**: Enterprise-grade authentication with configurable domain controller integration
- **📝 Content Management**: Full CRUD operations for wiki pages with Markdown support
- **📁 File Management**:     conn = ldap.initialize(f'ldap://{os.getenv("LDAP_SERVER", "your-domain-controller")}:389')ecure file upload, storage, and management system
- **🔍 Full-Text Search**: Advanced search across pages, files, and tags
- **📊 Export System**: PDF and Markdown export capabilities
- **👥 Role-Based Access Control**: LDAP group-based permissions
- **💾 Database Flexibility**: SQLite default with PostgreSQL support
- **🔒 Security Features**: Input validation, session management, and secure file handling

## 📋 Architecture

### Technology Stack
- **Framework**: Flask 2.3+ with SQLAlchemy ORM
- **Database**: SQLite (default) or PostgreSQL
- **Authentication**: LDAP/Active Directory with Flask-Login
- **File Storage**: Local filesystem with secure upload handling
- **Search**: Full-text search with SQLAlchemy
- **Export**: ReportLab for PDF generation

### Application Structure
```
backend/
├── app/
│   ├── __init__.py          # Application factory
│   ├── api/                 # REST API endpoints
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── pages.py         # Page management endpoints
│   │   ├── files.py         # File management endpoints
│   │   └── search.py        # Search endpoints
│   ├── auth/                # Authentication modules
│   │   └── ldap_auth.py     # LDAP authentication logic
│   ├── models/              # Database models
│   │   ├── user.py          # User model
│   │   ├── page.py          # Page and Tag models
│   │   └── file.py          # File model
│   └── services/            # Business logic services
│       ├── page_service.py  # Page operations
│       ├── file_service.py  # File operations
│       └── search_service.py # Search operations
├── config.py                # Configuration classes
├── app.py                   # Application entry point
├── wsgi.py                  # WSGI entry point
├── requirements.txt         # Python dependencies
└── Dockerfile              # Container definition
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- pip and venv
- Access to LDAP/Active Directory server (your domain controller)
- SQLite (default) or PostgreSQL

### Development Setup

1. **Clone and Setup Virtual Environment**:
   ```bash
   git clone <repository-url>
   cd HomelabWiki/backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   ```bash
   # Copy local environment template
   cp config/env/.env.local.example .env.local
   
   # Edit with your actual configuration
   nano .env.local
   ```
   
   **Important**: See [Local Environment Configuration Guide](../docs/configuration/local-environment.md) for detailed setup instructions with your specific server names and domain information.

4. **Database Setup**:
   ```bash
   # Initialize database
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Start Development Server**:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   flask run --host=0.0.0.0 --port=5000
   ```

### Docker Setup

1. **Build Container**:
   ```bash
   docker build -t homelab-wiki-backend .
   ```

2. **Run Container**:
   ```bash
   docker run -d \
     --name wiki-backend \
     -p 5000:5000 \
     -e LDAP_SERVER=your-domain-controller \
     -e LDAP_BIND_PASSWORD=your-password \
     homelab-wiki-backend
   ```

## ⚙️ Configuration

### Environment Variables

#### Core Configuration
```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
DATABASE_URL=sqlite:///homelab_wiki.db

# LDAP Server Configuration
LDAP_SERVER=your-domain-controller
LDAP_PORT=389
LDAP_USE_SSL=false
LDAP_USE_TLS=true

# LDAP Bind Configuration
LDAP_BASE_DN=DC=yourdomain,DC=local
LDAP_BIND_DN=CN=wikisvc,CN=Users,DC=yourdomain,DC=local
LDAP_BIND_PASSWORD=your-service-password

# LDAP Search Configuration
LDAP_USER_SEARCH_BASE=CN=Users,DC=yourdomain,DC=local
LDAP_GROUP_SEARCH_BASE=CN=Groups,DC=yourdomain,DC=local
LDAP_USER_OBJECT_CLASS=user
LDAP_GROUP_OBJECT_CLASS=group

# LDAP Attribute Mapping
LDAP_USERNAME_ATTRIBUTE=sAMAccountName
LDAP_EMAIL_ATTRIBUTE=mail
LDAP_FIRSTNAME_ATTRIBUTE=givenName
LDAP_LASTNAME_ATTRIBUTE=sn
LDAP_GROUP_MEMBER_ATTRIBUTE=member

# File Upload Configuration
UPLOAD_FOLDER=/app/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
BACKUP_FOLDER=/app/backups
```

#### Database Configuration

**SQLite (Default)**:
```env
DATABASE_URL=sqlite:///homelab_wiki.db
```

**PostgreSQL**:
```env
DATABASE_URL=postgresql://username:password@localhost/homelab_wiki
```

### LDAP Group Configuration

The application uses LDAP groups for role-based access control:

- **WikiAdmins**: Full administrative access
- **WikiUsers**: Read/write access to content
- **WikiReadOnly**: Read-only access

## 📡 API Endpoints

### Authentication Endpoints

#### POST /api/auth/login
Login with LDAP credentials.

**Request Body**:
```json
{
  "username": "aegis",
  "password": "password"
}
```

**Response**:
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "aegis",
    "email": "user@yourdomain.local",
    "roles": ["WikiAdmins"]
  }
}
```

#### POST /api/auth/logout
Logout current user.

#### GET /api/auth/me
Get current user information.

### Pages Endpoints

#### GET /api/pages
Get all pages with pagination and filtering.

**Query Parameters**:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `tag`: Filter by tag name
- `author`: Filter by author username
- `search`: Search in title and content

**Response**:
```json
{
  "pages": [
    {
      "id": 1,
      "title": "Welcome to HomelabWiki",
      "slug": "welcome",
      "author": "aegis",
      "tags": ["welcome", "introduction"],
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 1,
    "pages": 1
  }
}
```

#### POST /api/pages
Create a new page.

**Request Body**:
```json
{
  "title": "New Page",
  "content": "# New Page\n\nThis is the content.",
  "tags": ["tag1", "tag2"]
}
```

#### GET /api/pages/{id}
Get a specific page by ID.

#### PUT /api/pages/{id}
Update a specific page.

#### DELETE /api/pages/{id}
Delete a specific page.

#### POST /api/pages/{id}/export
Export a page as PDF or Markdown.

**Request Body**:
```json
{
  "format": "pdf"
}
```

### Files Endpoints

#### GET /api/files
Get all files with pagination and filtering.

**Query Parameters**:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `type`: Filter by file type (image, document, archive)
- `search`: Search in filename and description

#### POST /api/files
Upload a new file.

**Request**: Multipart form data with file and metadata.

#### GET /api/files/{id}
Get file metadata.

#### GET /api/files/{id}/download
Download a file.

#### DELETE /api/files/{id}
Delete a file.

### Search Endpoints

#### GET /api/search
Global search across pages, files, and tags.

**Query Parameters**:
- `q`: Search query (required)
- `type`: Search type (all, pages, files, tags)
- `limit`: Maximum results (default: 20)

**Response**:
```json
{
  "query": "search term",
  "pages": [...],
  "files": [...],
  "tags": [...]
}
```

## 🧪 Testing

### Unit Tests

Run the test suite:
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_auth.py -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html
```

### Manual Testing

#### Test LDAP Authentication
```bash
# Test LDAP connection
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'
```

#### Test Page Operations
```bash
# Create a page
curl -X POST http://localhost:5000/api/pages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{"title": "Test Page", "content": "# Test\n\nContent"}'

# Get all pages
curl -X GET http://localhost:5000/api/pages \
  -H "Authorization: Bearer your-token"
```

#### Test File Upload
```bash
# Upload a file
curl -X POST http://localhost:5000/api/files \
  -H "Authorization: Bearer your-token" \
  -F "file=@test.pdf" \
  -F "description=Test file"
```

### Integration Tests

Run integration tests with Docker:
```bash
# Start test environment
docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# Run specific integration test
docker-compose exec backend python -m pytest tests/integration/
```

## 🔍 Monitoring & Logging

### Health Check
```bash
# Application health
curl http://localhost:5000/health
```

### Logging Configuration

The application uses Python's logging module with different levels:

- **Development**: DEBUG level to console
- **Production**: INFO level to file and console

Log files are stored in `/app/logs/homelab_wiki.log`

### Monitoring Endpoints

#### GET /health
Application health check.

**Response**:
```json
{
  "status": "healthy",
  "service": "HomelabWiki"
}
```

## 🔧 Troubleshooting

### Common Issues

#### LDAP Connection Issues
```bash
# Test LDAP connectivity
python -c "
import ldap
import os
try:
    conn = ldap.initialize(f'ldap://{os.getenv(\"LDAP_SERVER\", \"WYK-DC01\")}:389')
    conn.simple_bind_s()
    print('LDAP connection successful')
except Exception as e:
    print(f'LDAP connection failed: {e}')
"
```

#### Database Issues
```bash
# Check database connection
flask shell
>>> from app import db
>>> db.engine.execute('SELECT 1')

# Reset database (WARNING: Deletes all data)
flask db downgrade
flask db upgrade
```

#### File Upload Issues
```bash
# Check upload directory permissions
ls -la /app/uploads/
chmod 755 /app/uploads/

# Check disk space
df -h
```

### Debug Mode

Enable debug mode for development:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run
```

### Performance Optimization

#### Database Optimization
```python
# SQLite optimization
import sqlite3
conn = sqlite3.connect('homelab_wiki.db')
conn.execute('VACUUM')
conn.execute('ANALYZE')
conn.close()
```

#### Memory Usage
```bash
# Monitor memory usage
ps aux | grep python
top -p $(pgrep -f "flask run")
```

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret
   ```

2. **Database Migration**:
   ```bash
   flask db upgrade
   ```

3. **WSGI Server**:
   ```bash
   # Using Gunicorn
   gunicorn --bind 0.0.0.0:5000 wsgi:app
   
   # Using uWSGI
   uwsgi --http 0.0.0.0:5000 --module wsgi:app
   ```

### Docker Production

```bash
# Build production image
docker build -t homelab-wiki-backend:latest .

# Run production container
docker run -d \
  --name wiki-backend \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-production-secret \
  -e DATABASE_URL=postgresql://user:pass@db/wiki \
  -v /opt/wiki/uploads:/app/uploads \
  homelab-wiki-backend:latest
```

## 📚 Development Guidelines

### Code Style
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write comprehensive docstrings
- Include error handling and logging

### Security Practices
- Validate all user inputs
- Use parameterized queries
- Implement proper authentication
- Handle sensitive data securely
- Regular security updates

### Performance Considerations
- Use database indexing
- Implement caching where appropriate
- Optimize file handling
- Monitor resource usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Follow code style guidelines
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review logs: `/app/logs/homelab_wiki.log`
- Test LDAP connectivity
- Verify configuration settings
- Create GitHub issue with logs and configuration details