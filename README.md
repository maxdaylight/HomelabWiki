# HomelabWiki

A Debian-based Dockerized wiki application designed for homelab environments with enterprise authentication integration.

## 🚀 Project Overview

HomelabWiki is a secure, user-friendly platform for documentation management in homelab environments. It provides a modern wiki experience with enterprise-grade authentication through LDAP/Active Directory integration.

### Key Features

- **🔐 Enterprise Authentication**: LDAP/Active Directory integration with configurable directory server
- **📝 Markdown Support**: Native Markdown editing and rendering for all content
- **🔍 Full-Text Search**: Comprehensive search across all wiki content
- **📁 File Management**: Secure file upload and attachment system
- **📊 Export Capabilities**: PDF and Markdown export functionality
- **👥 Role-Based Access**: User management through LDAP groups
- **🐳 Docker Ready**: Fully containerized with Docker Compose orchestration
- **💾 Flexible Database**: SQLite by default with PostgreSQL migration support
- **📱 Responsive Design**: Mobile-friendly interface built with Vue.js

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Vue.js)      │◄──►│   (Flask)       │◄──►│   (SQLite/      │
│   Port: 3000    │    │   Port: 5000    │    │   PostgreSQL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   LDAP/AD       │
                       │   (Domain Controller) │
                       └─────────────────┘
```

### Technology Stack

- **Backend**: Python 3.13+ with Flask framework
- **Frontend**: Vue.js 3 with modern JavaScript (ES6+)
- **Database**: SQLite (default) or PostgreSQL
- **Authentication**: LDAP/Active Directory via python-ldap
- **Containerization**: Docker with docker-compose
- **Web Server**: Nginx (production)

## 🛠️ Quick Start

### Docker Deployment (Recommended)

1. **Clone and Configure**:
   ```bash
   git clone <repository-url>
   cd HomelabWiki
   cp config/env/.env.local.example .env.local
   ```

2. **Configure Your Environment**:
   - Edit `.env.local` with your actual domain controller and credentials
   - See [Local Environment Configuration Guide](docs/configuration/local-environment.md) for details
   - Generate secure secret key: `python -c "import secrets; print(secrets.token_hex(32))"`

3. **Deploy**:
   ```bash
   docker-compose up -d
   ```

4. **Access**:
   - **Application**: http://localhost:3000
   - **Login**: Use your WYK domain credentials
   - **Health Check**: http://localhost:5000/health

### Manual Setup

For development or custom installations without Docker:

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app
flask db upgrade
flask run --host=0.0.0.0 --port=5000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📋 System Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 2GB
- **Storage**: 10GB
- **Network**: 1Gbps internal
- **Docker**: 20.10+ with Compose 2.0+

### Supported Platforms
- **Primary**: Debian 11+ Linux Container (Proxmox)
- **Supported**: Ubuntu 20.04+, CentOS 8+, RHEL 8+
- **Docker**: Any Docker-compatible platform

## 🔐 LDAP/Active Directory Configuration

### Environment Variables

Configure your LDAP/Active Directory connection by setting these environment variables:

```bash
# LDAP Server Configuration
LDAP_SERVER=your-domain-controller          # Your domain controller
LDAP_PORT=389                           # 389 for LDAP, 636 for LDAPS
LDAP_USE_SSL=false                      # Set to true for LDAPS
LDAP_USE_TLS=true                       # Enable StartTLS

# LDAP Bind Configuration
LDAP_BASE_DN=DC=yourdomain,DC=com       # Your domain's base DN
LDAP_BIND_DN=CN=wikisvc,CN=Users,DC=yourdomain,DC=com
LDAP_BIND_PASSWORD=your-service-account-password

# User and Group Configuration
LDAP_USER_SEARCH_BASE=CN=Users,DC=yourdomain,DC=com
LDAP_GROUP_SEARCH_BASE=CN=Groups,DC=yourdomain,DC=com
LDAP_USER_OBJECT_CLASS=user
LDAP_GROUP_OBJECT_CLASS=group

# Attribute Mapping
LDAP_USERNAME_ATTRIBUTE=sAMAccountName
LDAP_EMAIL_ATTRIBUTE=mail
LDAP_FIRSTNAME_ATTRIBUTE=givenName
LDAP_LASTNAME_ATTRIBUTE=sn
LDAP_GROUP_MEMBER_ATTRIBUTE=member
```

### Active Directory Setup

1. **Create a service account** for the wiki application:
   ```powershell
   # On your domain controller
   New-ADUser -Name "WikiService" -SamAccountName "wikisvc" -UserPrincipalName "wikisvc@yourdomain.com" -PasswordNeverExpires $true
   ```

2. **Create security groups** for access control:
   ```powershell
   New-ADGroup -Name "WikiAdmins" -GroupScope DomainLocal
   New-ADGroup -Name "WikiUsers" -GroupScope DomainLocal
   New-ADGroup -Name "WikiReadOnly" -GroupScope DomainLocal
   ```

3. **Grant necessary permissions** to the service account:
   - Read access to user and group objects
   - Query permissions in the directory

### Testing LDAP Connection

Use the built-in LDAP test endpoint:

```bash
# Test LDAP connection
curl -X POST http://localhost:5000/api/auth/test-ldap \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'
```

## 🧪 Running and Testing

### Development Testing

1. **Backend Tests**:
   ```bash
   cd backend
   python -m pytest tests/ -v
   ```

2. **Frontend Tests**:
   ```bash
   cd frontend
   npm run test
   ```

3. **Integration Tests**:
   ```bash
   docker-compose -f docker-compose.test.yml up --abort-on-container-exit
   ```

### Production Deployment

1. **Build and deploy**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

2. **Health checks**:
   ```bash
   # Check container status
   docker-compose ps
   
   # Check application health
   curl http://localhost/health
   ```

### Manual Testing Scenarios

1. **Authentication Flow**:
   - Navigate to http://localhost:3000
   - Click "Login" and enter AD credentials
   - Verify successful authentication and redirect

2. **Wiki Operations**:
   - Create a new page with Markdown content
   - Upload an attachment
   - Search for content
   - Export page as PDF

3. **Permission Testing**:
   - Test with different AD group memberships
   - Verify role-based access restrictions

## 📁 File and Data Layout

### Directory Structure

```
HomelabWiki/
├── backend/                    # Flask backend application
│   ├── app/
│   │   ├── api/               # REST API endpoints
│   │   ├── auth/              # Authentication modules
│   │   ├── models/            # Database models
│   │   └── services/          # Business logic
│   ├── migrations/            # Database migrations
│   ├── tests/                 # Backend tests
│   └── uploads/               # File uploads (volume mounted)
├── frontend/                   # Vue.js frontend
│   ├── src/
│   │   ├── components/        # Vue components
│   │   ├── views/             # Page views
│   │   └── services/          # API services
│   └── dist/                  # Built frontend (production)
├── config/                     # Configuration files
│   ├── env/                   # Environment templates
│   ├── nginx/                 # Nginx configuration
│   └── docker/                # Docker configurations
├── data/                       # Persistent data (volume mounted)
│   ├── database/              # Database files
│   ├── uploads/               # User uploaded files
│   └── backups/               # Database backups
└── docs/                       # Documentation
```

### Data Persistence

**Docker Volumes**:
- `wiki_data`: Database and uploaded files
- `wiki_uploads`: User file uploads
- `wiki_backups`: Automated backups

**Host Paths** (for backup purposes):
- Database: `./data/database/homelab_wiki.db`
- Uploads: `./data/uploads/`
- Backups: `./data/backups/`

### Backup Strategy

1. **Database Backup**:
   ```bash
   # SQLite backup
   docker-compose exec backend sqlite3 /app/data/homelab_wiki.db ".backup /app/data/backups/wiki_backup_$(date +%Y%m%d_%H%M%S).db"
   
   # PostgreSQL backup
   docker-compose exec database pg_dump -U wiki_user wiki_db > ./data/backups/wiki_backup_$(date +%Y%m%d_%H%M%S).sql
   ```

2. **File Backup**:
   ```bash
   # Backup uploads directory
   tar -czf ./data/backups/uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz ./data/uploads/
   ```

3. **Automated Backup Script**:
   ```bash
   #!/bin/bash
   # Add to crontab: 0 2 * * * /path/to/backup.sh
   
   BACKUP_DIR="./data/backups"
   DATE=$(date +%Y%m%d_%H%M%S)
   
   # Database backup
   docker-compose exec -T backend sqlite3 /app/data/homelab_wiki.db ".backup /app/data/backups/wiki_db_${DATE}.db"
   
   # Files backup
   tar -czf "${BACKUP_DIR}/wiki_uploads_${DATE}.tar.gz" ./data/uploads/
   
   # Cleanup old backups (keep last 30 days)
   find ${BACKUP_DIR} -name "wiki_*" -mtime +30 -delete
   ```

## 🔧 Troubleshooting

### Authentication Issues

**Problem**: LDAP authentication failing

**Solutions**:
1. **Test LDAP connectivity**:
   ```bash
   # From the backend container
   docker-compose exec backend python -c "
   import ldap
   import os
   
   server = os.getenv('LDAP_SERVER', 'your-domain-controller')
   port = int(os.getenv('LDAP_PORT', '389'))
   
   try:
       conn = ldap.initialize(f'ldap://{server}:{port}')
       conn.simple_bind_s()
       print('LDAP connection successful')
   except Exception as e:
       print(f'LDAP connection failed: {e}')
   "
   ```

2. **Check DNS resolution**:
   ```bash
   # Verify domain controller is reachable
   docker-compose exec backend nslookup your-domain-controller
   docker-compose exec backend ping -c 3 your-domain-controller
   ```

3. **Validate LDAP configuration**:
   ```bash
   # Check LDAP search
   docker-compose exec backend ldapsearch -x -h your-domain-controller -p 389 -D "CN=wikisvc,CN=Users,DC=yourdomain,DC=com" -w "password" -b "DC=yourdomain,DC=com" "(sAMAccountName=testuser)"
   ```

**Problem**: User permissions not working correctly

**Solutions**:
1. **Check AD group membership**:
   ```bash
   # Verify user is in correct groups
   docker-compose exec backend ldapsearch -x -h your-domain-controller -p 389 -D "CN=wikisvc,CN=Users,DC=yourdomain,DC=com" -w "password" -b "DC=yourdomain,DC=com" "(&(objectClass=group)(member=CN=testuser,CN=Users,DC=yourdomain,DC=com))"
   ```

2. **Review application logs**:
   ```bash
   docker-compose logs backend | grep -i auth
   ```

### Container Deployment Issues

**Problem**: Containers not starting

**Solutions**:
1. **Check Docker daemon**:
   ```bash
   systemctl status docker
   docker --version
   docker-compose --version
   ```

2. **Verify port availability**:
   ```bash
   netstat -tuln | grep -E ':3000|:5000|:80'
   ```

3. **Check container logs**:
   ```bash
   docker-compose logs --tail=50 backend
   docker-compose logs --tail=50 frontend
   ```

4. **Rebuild containers**:
   ```bash
   docker-compose down -v
   docker-compose build --no-cache
   docker-compose up -d
   ```

**Problem**: Database connection errors

**Solutions**:
1. **Check database initialization**:
   ```bash
   docker-compose exec backend flask db current
   docker-compose exec backend flask db upgrade
   ```

2. **Verify database file permissions**:
   ```bash
   ls -la ./data/database/
   chown -R 1000:1000 ./data/database/
   ```

**Problem**: File upload failures

**Solutions**:
1. **Check upload directory permissions**:
   ```bash
   ls -la ./data/uploads/
   chmod 755 ./data/uploads/
   ```

2. **Verify disk space**:
   ```bash
   df -h
   docker system df
   ```

### Performance Issues

**Problem**: Slow response times

**Solutions**:
1. **Check resource usage**:
   ```bash
   docker stats
   htop
   ```

2. **Optimize database**:
   ```bash
   # SQLite optimization
   docker-compose exec backend sqlite3 /app/data/homelab_wiki.db "VACUUM; ANALYZE;"
   ```

3. **Review application logs**:
   ```bash
   docker-compose logs backend | grep -i "slow\|timeout\|error"
   ```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `LDAP connection refused` | Network/firewall issue | Check connectivity to domain controller |
| `Invalid credentials` | Wrong service account | Verify LDAP_BIND_DN and password |
| `Permission denied` | File system permissions | Check data directory ownership |
| `Port already in use` | Conflicting services | Change ports in docker-compose.yml |
| `Database locked` | Concurrent access issue | Restart backend container |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## � Documentation

### Quick References
- **[Docker Quick Start](docs/deployment/docker-quick-reference.md)** - Essential Docker commands
- **[Security Quick Start](docs/security/quick-start.md)** - Fast secure deployment
- **[Docker Troubleshooting](docs/deployment/docker-troubleshooting.md)** - Common issues and solutions

### Comprehensive Guides
- **[Docker Deployment Guide](docs/deployment/docker.md)** - Complete Docker documentation
- **[Docker Compose Guide](docs/deployment/docker-compose-guide.md)** - Configuration details
- **[Local Environment Setup](docs/configuration/local-environment.md)** - Configure your specific environment
- **[Security Guide](docs/security/credentials.md)** - Credential management
- **[API Documentation](docs/api/README.md)** - REST API reference
- **[User Guide](docs/user-guide/README.md)** - End-user documentation

### Security Tools
- **Security Check**: `scripts/security-check.sh` (Linux) or `scripts/security-check.ps1` (Windows)
- **Docker Test**: `scripts/test-docker.sh`
- **Backup Script**: `scripts/backup.sh`

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the documentation in the `docs/` directory

---

**Note**: This application is designed for homelab environments. For production enterprise deployment, additional security hardening and scalability considerations may be required.
