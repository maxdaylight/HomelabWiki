# HomelabWiki API Documentation

Comprehensive REST API documentation for HomelabWiki backend services.

## 🚀 API Overview

The HomelabWiki API provides a complete REST interface for managing wiki content, user authentication, file operations, and search functionality. All endpoints require authentication except for the health check.

### Base URL
```
http://localhost:5000/api
```

### Authentication
The API uses session-based authentication with LDAP/Active Directory integration. Users must authenticate via the `/auth/login` endpoint before accessing protected resources.

### Response Format
All API responses follow a consistent JSON format:

**Success Response**:
```json
{
  "data": {...},
  "message": "Operation successful"
}
```

**Error Response**:
```json
{
  "error": "Error description",
  "code": "ERROR_CODE"
}
```

### HTTP Status Codes
- `200 OK`: Successful GET, PUT, PATCH requests
- `201 Created`: Successful POST requests
- `204 No Content`: Successful DELETE requests
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## 🔐 Authentication Endpoints

### POST /api/auth/login
Authenticate user with LDAP credentials.

**Request Body**:
```json
{
  "username": "aegis",
  "password": "password123"
}
```

**Response** (200 OK):
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "aegis",
    "email": "user@yourdomain.local",
    "first_name": "John",
    "last_name": "Doe",
    "roles": ["WikiAdmins"],
    "created_at": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-01T12:00:00Z"
  }
}
```

### POST /api/auth/logout
Logout current user and invalidate session.

**Response** (200 OK):
```json
{
  "message": "Logout successful"
}
```

### GET /api/auth/me
Get current user information.

**Response** (200 OK):
```json
{
  "user": {
    "id": 1,
    "username": "aegis",
    "email": "user@yourdomain.local",
    "first_name": "John",
    "last_name": "Doe",
    "roles": ["WikiAdmins"],
    "created_at": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-01T12:00:00Z"
  }
}
```

## 📝 Pages Endpoints

### GET /api/pages
Get all pages with pagination and filtering.

**Query Parameters**:
- `page` (integer): Page number (default: 1)
- `per_page` (integer): Items per page (default: 20, max: 100)
- `tag` (string): Filter by tag name
- `author` (string): Filter by author username
- `search` (string): Search in title and content

**Response** (200 OK):
```json
{
  "pages": [
    {
      "id": 1,
      "title": "Welcome to HomelabWiki",
      "slug": "welcome-to-homelabwiki",
      "content": "# Welcome\n\nThis is the homepage...",
      "summary": "Welcome page for new users",
      "author": {
        "id": 1,
        "username": "aegis",
        "email": "user@yourdomain.local"
      },
      "tags": ["welcome", "introduction"],
      "is_published": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
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

### POST /api/pages
Create a new page.

**Request Body**:
```json
{
  "title": "New Page Title",
  "content": "# New Page\n\nThis is the content in Markdown format.",
  "summary": "Brief description of the page",
  "tags": ["tag1", "tag2"],
  "is_published": true
}
```

### GET /api/pages/{id}
Get a specific page by ID.

### PUT /api/pages/{id}
Update a specific page.

### DELETE /api/pages/{id}
Delete a specific page.

### POST /api/pages/{id}/export
Export a page as PDF or Markdown.

**Request Body**:
```json
{
  "format": "pdf"
}
```

## 📁 Files Endpoints

### GET /api/files
Get all files with pagination and filtering.

**Query Parameters**:
- `page` (integer): Page number (default: 1)
- `per_page` (integer): Items per page (default: 20, max: 100)
- `type` (string): Filter by file type (`image`, `document`, `archive`)
- `search` (string): Search in filename and description

### POST /api/files
Upload a new file.

**Request**: Multipart form data with file and metadata.

### GET /api/files/{id}
Get file metadata.

### GET /api/files/{id}/download
Download a file.

### DELETE /api/files/{id}
Delete a file.

## 🔍 Search Endpoints

### GET /api/search
Global search across pages, files, and tags.

**Query Parameters**:
- `q` (string): Search query (required)
- `type` (string): Search type (`all`, `pages`, `files`, `tags`)
- `limit` (integer): Maximum results (default: 20)

**Response** (200 OK):
```json
{
  "query": "search term",
  "results": {
    "pages": [...],
    "files": [...],
    "tags": [...]
  }
}
```

## 🔧 Utility Endpoints

### GET /health
Application health check (No authentication required).

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "HomelabWiki",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🚨 Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "error": "Invalid request data",
  "code": "INVALID_REQUEST"
}
```

#### 401 Unauthorized
```json
{
  "error": "Authentication required",
  "code": "UNAUTHORIZED"
}
```

#### 403 Forbidden
```json
{
  "error": "Insufficient permissions",
  "code": "FORBIDDEN"
}
```

#### 404 Not Found
```json
{
  "error": "Resource not found",
  "code": "NOT_FOUND"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "code": "INTERNAL_ERROR"
}
```

## 🧪 Testing the API

### Authentication Testing
```bash
# Login
curl -X POST "http://localhost:5000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "aegis", "password": "password123"}' \
  -c cookies.txt

# Use session cookie for subsequent requests
curl -X GET "http://localhost:5000/api/auth/me" -b cookies.txt
```

### Example API Calls

**Create a page**:
```bash
curl -X POST "http://localhost:5000/api/pages" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Docker Guide",
    "content": "# Docker\n\nThis is a Docker guide...",
    "tags": ["docker", "containers"]
  }'
```

**Upload a file**:
```bash
curl -X POST "http://localhost:5000/api/files" \
  -b cookies.txt \
  -F "file=@document.pdf" \
  -F "description=Important document"
```

**Search content**:
```bash
curl -X GET "http://localhost:5000/api/search?q=docker&type=all" \
  -b cookies.txt
```

## 📚 Additional Resources

### Related Documentation
- [Backend README](../../backend/README.md) - Backend setup and development
- [Deployment Guide](../deployment/README.md) - Deployment instructions
- [User Guide](../user-guide/README.md) - End-user documentation
- [Security Guide](../security/README.md) - Security best practices

### Support
- **GitHub Issues**: Report bugs and request features
- **API Status**: Monitor API health and status
- **Community**: Join the HomelabWiki community for support

---

**Note**: This API documentation is for HomelabWiki version 1.0.0. For the latest updates and changes, please refer to the changelog and release notes.
