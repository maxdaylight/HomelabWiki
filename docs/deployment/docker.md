# Docker Deployment Guide

## Overview
HomelabWiki is fully containerized using Docker and Docker Compose for easy deployment and management. This guide covers all deployment scenarios from development to production.

## Prerequisites
- Docker Engine 20.10 or later
- Docker Compose 2.0 or later
- Access to WYK-DC01 Active Directory server
- LDAP service account with read permissions

## Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd HomelabWiki
```

### 2. Configure Environment
```bash
# Copy environment template
cp config/env/.env.example .env

# Edit with your credentials
nano .env
```

### 3. Set Required Variables
Update these critical variables in `.env`:
```env
SECRET_KEY=your-generated-64-character-secret-key
LDAP_BIND_PASSWORD=your-actual-ldap-service-account-password
POSTGRES_PASSWORD=your-secure-database-password  # If using PostgreSQL
```

### 4. Deploy
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 5. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## Architecture

### Services Overview
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Nginx    │    │  Frontend   │    │   Backend   │
│   (Proxy)   │◄──►│   (Vue.js)  │◄──►│   (Flask)   │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
                                              ▼
                                      ┌─────────────┐
                                      │  Database   │
                                      │(PostgreSQL) │
                                      └─────────────┘
```

### Service Details

#### Backend (Flask)
- **Image**: Built from `./backend/Dockerfile`
- **Port**: 5000 (internal)
- **Purpose**: REST API, LDAP authentication, file management
- **Dependencies**: Database, LDAP server

#### Frontend (Vue.js)
- **Image**: Built from `./frontend/Dockerfile`
- **Port**: 3000 (internal)
- **Purpose**: Web interface, user interaction
- **Dependencies**: Backend API

#### Database (PostgreSQL)
- **Image**: postgres:15-alpine
- **Port**: 5432 (internal)
- **Purpose**: Data persistence
- **Alternative**: SQLite (for development)

#### Nginx (Reverse Proxy)
- **Image**: nginx:alpine
- **Ports**: 80, 443
- **Purpose**: SSL termination, load balancing
- **Dependencies**: Frontend, Backend

## Environment Configuration

### Database Options

#### SQLite (Development)
```env
DATABASE_URL=sqlite:///homelab_wiki.db
```

#### PostgreSQL (Production)
```env
DATABASE_URL=postgresql://wiki_user:${POSTGRES_PASSWORD}@database:5432/homelab_wiki
POSTGRES_USER=wiki_user
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=homelab_wiki
```

### LDAP Configuration
```env
LDAP_SERVER=WYK-DC01
LDAP_PORT=389
LDAP_BASE_DN=DC=wyk,DC=local
LDAP_BIND_DN=CN=WikiService,CN=Users,DC=wyk,DC=local
LDAP_BIND_PASSWORD=your-ldap-password
```

### Security Settings
```env
SECRET_KEY=your-generated-secret-key
WTF_CSRF_ENABLED=true
FLASK_ENV=production
```

## Deployment Scenarios

### Development Environment
```bash
# Use development overrides
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

**Features**:
- Source code mounting for live reload
- Debug mode enabled
- Database exposed for development tools
- Detailed logging

### Production Environment
```bash
# Use production overrides
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

**Features**:
- Resource limits and reservations
- Optimized logging
- Performance monitoring
- Security hardening

### High-Security Environment
```bash
# Use Docker secrets
docker-compose -f docker-compose.secrets.yml up -d
```

**Features**:
- Credentials stored as Docker secrets
- No environment variables with passwords
- Enhanced security posture

## Volume Management

### Named Volumes
```yaml
volumes:
  wiki_data:         # Application data
  wiki_uploads:      # User uploaded files
  wiki_backups:      # Automated backups
  wiki_logs:         # Application logs
  postgres_data:     # Database files
```

### Backup Strategy
```bash
# Create backup
docker-compose exec backend python -m app.backup

# Manual database backup
docker-compose exec database pg_dump -U wiki_user homelab_wiki > backup.sql

# Volume backup
docker run --rm -v wiki_data:/data -v $(pwd):/backup alpine tar czf /backup/wiki_data.tar.gz /data
```

## Network Configuration

### Internal Network
- **Name**: `wiki_network`
- **Driver**: bridge
- **Purpose**: Isolate services from host network

### Port Mapping
```yaml
ports:
  - "80:80"     # HTTP (Nginx)
  - "443:443"   # HTTPS (Nginx)
  - "3000:3000" # Frontend (dev only)
  - "5000:5000" # Backend (dev only)
```

## SSL/TLS Configuration

### Certificate Setup
```bash
# Create SSL directory
mkdir -p ssl

# Generate self-signed certificate (development)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/homelab-wiki.key \
  -out ssl/homelab-wiki.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=homelab-wiki.local"

# Set permissions
chmod 600 ssl/homelab-wiki.key
chmod 644 ssl/homelab-wiki.crt
```

### Nginx SSL Configuration
The nginx configuration in `config/nginx/default.conf` handles SSL termination.

## Monitoring and Logging

### Health Checks
```bash
# Backend health
curl http://localhost:5000/health

# Service status
docker-compose ps

# Resource usage
docker stats
```

### Log Management
```bash
# View all logs
docker-compose logs -f

# Service-specific logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database

# Follow logs with timestamps
docker-compose logs -f -t

# Filter logs
docker-compose logs backend | grep ERROR
```

### Log Rotation
Logs are automatically rotated by Docker's logging driver. Configure in `docker-compose.yml`:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check logs
docker-compose logs service_name

# Verify environment variables
docker-compose config

# Check resource usage
docker system df
```

#### Database Connection Issues
```bash
# Test database connectivity
docker-compose exec backend python -c "
import os
from app import create_app
app = create_app()
with app.app_context():
    from app.models import db
    db.create_all()
    print('Database connection successful')
"
```

#### LDAP Authentication Issues
```bash
# Test LDAP connectivity
docker-compose exec backend python -c "
from app.auth.ldap_auth import test_ldap_connection
test_ldap_connection()
"
```

#### Port Conflicts
```bash
# Check port usage
netstat -tlnp | grep :80
netstat -tlnp | grep :443

# Use different ports
docker-compose down
# Edit docker-compose.yml ports
docker-compose up -d
```

### Performance Issues

#### Memory Usage
```bash
# Monitor memory
docker stats --no-stream

# Limit memory usage
# Edit docker-compose.yml with deploy.resources.limits
```

#### Database Performance
```bash
# Check database size
docker-compose exec database du -sh /var/lib/postgresql/data

# Optimize database
docker-compose exec database psql -U wiki_user -d homelab_wiki -c "VACUUM ANALYZE;"
```

## Security Best Practices

### Container Security
1. **Non-root user**: All containers run as non-root
2. **Read-only filesystem**: Where possible
3. **Resource limits**: Prevent resource exhaustion
4. **Network isolation**: Private Docker network

### Credential Security
1. **Environment variables**: Never hardcode credentials
2. **File permissions**: Secure `.env` file (600)
3. **Secret rotation**: Regular credential updates
4. **Audit logging**: Monitor authentication events

### Network Security
1. **Firewall rules**: Restrict access to necessary ports
2. **SSL/TLS**: Encrypt all communications
3. **Reverse proxy**: Hide backend services
4. **Rate limiting**: Prevent abuse

## Maintenance

### Regular Tasks
```bash
# Update containers
docker-compose pull
docker-compose up -d

# Clean up unused resources
docker system prune -f

# Backup volumes
./scripts/backup.sh

# Check security
./scripts/security-check.sh
```

### Updates and Patches
```bash
# Update application
git pull origin main
docker-compose build --no-cache
docker-compose up -d

# Database migrations
docker-compose exec backend flask db upgrade
```

## Production Deployment Checklist

### Pre-deployment
- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Firewall rules configured
- [ ] DNS records updated
- [ ] Backup strategy implemented

### Security
- [ ] Strong passwords generated
- [ ] File permissions set (600 for .env)
- [ ] No hardcoded credentials
- [ ] LDAP service account configured
- [ ] SSL/TLS enabled

### Performance
- [ ] Resource limits configured
- [ ] Database optimized
- [ ] Log rotation enabled
- [ ] Monitoring configured

### Testing
- [ ] Health checks passing
- [ ] LDAP authentication working
- [ ] File uploads functional
- [ ] Export features working
- [ ] Search functionality active

## Support and Resources

### Log Files
- **Backend**: `docker-compose logs backend`
- **Frontend**: `docker-compose logs frontend`
- **Database**: `docker-compose logs database`
- **Nginx**: `docker-compose logs nginx`

### Configuration Files
- **Main**: `docker-compose.yml`
- **Development**: `docker-compose.dev.yml`
- **Production**: `docker-compose.prod.yml`
- **Secrets**: `docker-compose.secrets.yml`
- **Environment**: `.env`

### Scripts
- **Security Check**: `scripts/security-check.sh`
- **Docker Test**: `scripts/test-docker.sh`
- **Backup**: `scripts/backup.sh`

For additional support, refer to the main documentation or check the project's issue tracker.
