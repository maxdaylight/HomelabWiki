# Copilot Instructions for HomelabWiki

## Project Overview
HomelabWiki is a comprehensive self-hosted Knowledge Base (Wiki) web application designed for homelab environments. It provides a secure, user-friendly platform for documentation management with enterprise-grade authentication through LDAP/Active Directory integration.

### Project Status: FULLY IMPLEMENTED ✅
- **Backend**: Complete Flask application with LDAP authentication, REST API, and database models
- **Frontend**: Modern Vue.js 3 application with responsive design and rich markdown editing
- **Database**: SQLite (default) with PostgreSQL support and comprehensive models
- **Authentication**: Full LDAP/Active Directory integration with group-based permissions
- **File Management**: Complete file upload, storage, and management system
- **Search**: Full-text search across pages, files, and tags
- **Export**: PDF and Markdown export capabilities
- **Deployment**: Docker containerization with docker-compose orchestration
- **Security**: Comprehensive security implementation with proper session management
- **Documentation**: Complete user and deployment documentation

### Key Features Implemented ✅
- **🔐 Enterprise Authentication**: LDAP/Active Directory integration with WYK-DC01
- **📝 Markdown Support**: Full markdown editing with live preview and syntax highlighting
- **🔍 Full-Text Search**: Comprehensive search across all wiki content and files
- **📁 File Management**: Secure file upload with support for images, documents, and archives
- **📊 Export Capabilities**: PDF and Markdown export for individual pages and bulk operations
- **👥 Role-Based Access**: User management through LDAP groups (WikiAdmins, WikiUsers, WikiReadOnly)
- **🐳 Docker Ready**: Fully containerized with production-ready docker-compose setup
- **💾 Database Flexibility**: SQLite by default with easy PostgreSQL migration
- **📱 Responsive Design**: Mobile-friendly interface with modern UI components
- **🔒 Security**: Comprehensive security implementation with proper input validation

### Target Environment: Debian Linux Container (CT) in Proxmox ✅
- **Deployment Method**: Docker containers within Debian CT
- **Network Configuration**: Static internal IP support
- **LDAP Integration**: Pre-configured for WYK-DC01 domain controller at 192.168.0.5
- **User Authentication**: Support for domain login format (wyk\username)
- **Resource Optimization**: Optimized for homelab hardware constraints

## Core Requirements

### Authentication & Security
- **LDAP/Active Directory Integration**: All user authentication MUST be through environment-configurable LDAP/Active Directory
- **Default LDAP Server**: WYK-DC01 (configurable via environment variables)
- **Security Best Practices**: 
  - Use secure session management
  - Implement proper input validation and sanitization
  - Follow OWASP security guidelines
  - Use HTTPS in production environments
  - Implement proper error handling without exposing sensitive information

### Technology Stack
- **Backend**: Python with Flask framework
- **Frontend**: Modern JavaScript (ES6+) with Vue.js
- **Database**: SQLite by default, with easy PostgreSQL migration capability
- **Content Format**: Markdown support for all wiki content
- **Containerization**: Docker with docker-compose for orchestration

### Core Features
- **Content Management**: Full CRUD operations for wiki pages
- **Markdown Support**: Native Markdown rendering and editing
- **Export Capabilities**: PDF and Markdown export functionality
- **File Management**: File upload and attachment system
- **Search**: Full-text search across all content
- **User Management**: Role-based access control via LDAP groups

### Database Architecture
- **Default**: SQLite for simplicity and portability
- **Production**: Easy switch to PostgreSQL via environment configuration
- **Migration**: Provide clear migration path between database systems
- **Models**: User, Page, File entities with proper relationships

## Development Guidelines

### Code Quality & Practices
- **Code Legibility**: Write self-documenting code with clear variable and function names
- **Documentation**: Document all non-obvious decisions directly in code comments
- **Error Handling**: Implement comprehensive error handling with user-friendly messages
- **Testing**: Include unit tests for critical functionality
- **API Design**: RESTful API design with proper HTTP status codes

### Security Considerations
- **Environment Variables**: Use environment variables for all sensitive configuration
- **Input Validation**: Validate and sanitize all user inputs
- **File Uploads**: Implement secure file upload with type validation and size limits
- **Session Management**: Use secure session handling with proper timeout
- **LDAP Configuration**: Secure LDAP connection with proper certificate validation

### Frontend Guidelines
- **Modern JavaScript**: Use ES6+ features and modern development practices
- **Vue.js**: Follow Vue.js best practices and component architecture
- **Responsive Design**: Ensure mobile-friendly responsive design
- **User Experience**: Focus on intuitive navigation and clear user feedback
- **Performance**: Optimize for fast loading and smooth interactions

### Backend Guidelines
- **Flask Structure**: Follow Flask application factory pattern
- **Database ORM**: Use SQLAlchemy for database operations
- **API Endpoints**: Implement clear, RESTful API endpoints
- **Authentication**: Integrate LDAP authentication with Flask-Login
- **Configuration**: Use Flask configuration classes for different environments

## Deployment Environment

### Proxmox Container (CT)
- **No sudo**: Assume deployment within Proxmox CT where sudo is not available
- **Shell Commands**: All command examples should work without sudo privileges
- **System Integration**: Consider CT-specific networking and storage configurations
- **Resource Management**: Optimize for container resource constraints

### Docker Configuration
- **Multi-stage Builds**: Use multi-stage Dockerfiles for optimized images
- **Environment Variables**: All configuration through environment variables
- **Volume Management**: Proper volume mounting for persistent data
- **Network Configuration**: Secure container networking setup

## File Structure Guidelines

### Backend Structure
```
backend/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── api/                 # API endpoints
│   ├── auth/                # Authentication modules
│   ├── models/              # Database models
│   └── services/            # Business logic services
├── config.py                # Configuration classes
├── requirements.txt         # Python dependencies
└── Dockerfile              # Backend container definition
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/          # Vue.js components
│   ├── views/              # Page components
│   ├── services/           # API and auth services
│   └── router.js           # Vue Router configuration
├── public/                 # Static assets
├── package.json            # Node.js dependencies
└── Dockerfile             # Frontend container definition
```

## Configuration Management

### Environment Variables
- `LDAP_SERVER`: LDAP server hostname (default: WYK-DC01)
- `LDAP_PORT`: LDAP server port (default: 389)
- `LDAP_BASE_DN`: Base distinguished name for LDAP queries
- `LDAP_BIND_DN`: Service account for LDAP binding
- `LDAP_BIND_PASSWORD`: Password for LDAP service account
- `DATABASE_URL`: Database connection string (SQLite or PostgreSQL)
- `SECRET_KEY`: Flask secret key for session management
- `UPLOAD_FOLDER`: Directory for file uploads
- `MAX_CONTENT_LENGTH`: Maximum file upload size

### Database Configuration
- **SQLite**: Default for development and small deployments
- **PostgreSQL**: Production-ready option with environment variable switch
- **Migration Scripts**: Provide database migration utilities
- **Backup Strategy**: Document backup procedures for both database types

## Implementation Priorities

1. **Authentication System**: Implement LDAP authentication first
2. **Core Wiki Functions**: Basic CRUD operations for pages
3. **Markdown Support**: Rich text editing and rendering
4. **File Management**: Upload and attachment system
5. **Search Functionality**: Full-text search implementation
6. **Export Features**: PDF and Markdown export capabilities
7. **User Interface**: Responsive, intuitive frontend
8. **Security Hardening**: Comprehensive security review and testing

## Testing Strategy
- **Unit Tests**: Backend service and model testing
- **Integration Tests**: API endpoint testing
- **Frontend Tests**: Component and user interaction testing
- **Security Tests**: Authentication and authorization testing
- **Performance Tests**: Load testing for typical homelab usage

## Documentation Standards
- **API Documentation**: OpenAPI/Swagger documentation
- **User Guide**: Comprehensive user documentation
- **Deployment Guide**: Step-by-step deployment instructions
- **Development Setup**: Local development environment setup
- **Code Comments**: Explain complex logic and business decisions

## Performance Considerations
- **Database Optimization**: Proper indexing and query optimization
- **Caching Strategy**: Implement appropriate caching for frequently accessed data
- **File Handling**: Efficient file upload and storage management
- **Frontend Optimization**: Minimize bundle size and optimize loading times
- **Container Resources**: Optimize for typical homelab hardware constraints

Remember: This is a homelab-focused application, so prioritize simplicity, security, and ease of deployment over enterprise-scale features. All code should be production-ready but appropriate for small-scale homelab environments.
