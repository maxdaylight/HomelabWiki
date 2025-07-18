# HomelabWiki Docker Compose Configuration

## Overview
This directory contains Docker Compose configurations for different deployment scenarios. Each configuration is designed for specific use cases and environments.

## Configuration Files

### 📋 docker-compose.yml
**Main configuration file**
- **Purpose**: Base configuration for all environments
- **Features**: Environment variable substitution, secure defaults
- **Usage**: `docker-compose up -d`

### 🛠️ docker-compose.dev.yml
**Development environment override**
- **Purpose**: Development and debugging
- **Features**: Source code mounting, debug ports exposed, verbose logging
- **Usage**: `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d`

### 🚀 docker-compose.prod.yml
**Production environment override**
- **Purpose**: Production deployment
- **Features**: Resource limits, performance optimization, security hardening
- **Usage**: `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d`

### 🔐 docker-compose.secrets.yml
**High-security configuration**
- **Purpose**: Maximum security deployment
- **Features**: Docker secrets, no environment variable passwords
- **Usage**: `docker-compose -f docker-compose.secrets.yml up -d`

## Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        External Access                      │
├─────────────────────────────────────────────────────────────┤
│  Port 80/443 (HTTP/HTTPS)                                  │
│  ┌─────────────────┐                                       │
│  │     Nginx       │  ← Reverse Proxy, SSL Termination     │
│  │   (nginx:alpine) │                                       │
│  └─────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Internal Network                         │
│                     (wiki_network)                          │
│                                                             │
│  ┌─────────────────┐           ┌─────────────────┐         │
│  │    Frontend     │◄─────────►│    Backend      │         │
│  │   (Vue.js 3)    │           │   (Flask)       │         │
│  │  Port 3000      │           │  Port 5000      │         │
│  └─────────────────┘           └─────────────────┘         │
│                                          │                  │
│                                          ▼                  │
│                                 ┌─────────────────┐         │
│                                 │   Database      │         │
│                                 │ (PostgreSQL)    │         │
│                                 │  Port 5432      │         │
│                                 └─────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   External Services                         │
│                                                             │
│  ┌─────────────────┐                                       │
│  │   WYK-DC01      │  ← LDAP Authentication                │
│  │(Active Directory│                                       │
│  │  Port 389/636   │                                       │
│  └─────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

## Environment Variables

### Required Variables
These must be set in your `.env` file:

```env
SECRET_KEY=your-generated-secret-key
LDAP_BIND_PASSWORD=your-ldap-service-account-password
```

### Optional Variables
These have sensible defaults but can be overridden:

```env
LDAP_SERVER=WYK-DC01
LDAP_PORT=389
LDAP_BASE_DN=DC=wyk,DC=local
DATABASE_URL=sqlite:///homelab_wiki.db
```

### PostgreSQL Variables
Only required if using PostgreSQL:

```env
POSTGRES_USER=wiki_user
POSTGRES_PASSWORD=your-database-password
POSTGRES_DB=homelab_wiki
```

## Volume Management

### Named Volumes
```yaml
volumes:
  wiki_data:        # Application data and configuration
  wiki_uploads:     # User uploaded files
  wiki_backups:     # Automated backup files
  wiki_logs:        # Application log files
  postgres_data:    # Database files (PostgreSQL only)
```

### Volume Locations
- **Host**: Named volumes managed by Docker
- **Container**: Mounted at `/app/data`, `/app/uploads`, etc.
- **Backup**: Can be backed up using `docker run` commands

## Network Configuration

### Internal Network
```yaml
networks:
  wiki_network:
    driver: bridge
```

- **Purpose**: Isolate services from external access
- **Security**: Only nginx proxy exposed to host
- **Communication**: Services communicate internally

### Port Mapping
```yaml
# Production (nginx proxy)
ports:
  - "80:80"
  - "443:443"

# Development (direct access)
ports:
  - "3000:3000"  # Frontend
  - "5000:5000"  # Backend
  - "5432:5432"  # Database
```

## Configuration Examples

### Basic Deployment
```bash
# 1. Create environment file
cp config/env/.env.example .env

# 2. Edit credentials
nano .env

# 3. Start services
docker-compose up -d
```

### Development Environment
```bash
# Start with development overrides
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Access services directly
curl http://localhost:5000/health  # Backend
curl http://localhost:3000         # Frontend
```

### Production Environment
```bash
# Start with production overrides
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Access through nginx proxy
curl http://localhost/health       # Backend (proxied)
curl http://localhost              # Frontend (proxied)
```

### High-Security Environment
```bash
# 1. Create secrets directory
mkdir -p secrets

# 2. Create secret files
echo "your-secret-key" > secrets/secret_key.txt
echo "your-ldap-password" > secrets/ldap_password.txt
echo "your-db-password" > secrets/db_password.txt

# 3. Set permissions
chmod 600 secrets/*.txt

# 4. Start with secrets
docker-compose -f docker-compose.secrets.yml up -d
```

## Service Dependencies

### Startup Order
1. **Database** - PostgreSQL container starts first
2. **Backend** - Waits for database to be ready
3. **Frontend** - Waits for backend to be ready
4. **Nginx** - Waits for frontend and backend

### Health Checks
```bash
# Backend health check
curl http://localhost:5000/health

# Database connection test
docker-compose exec database psql -U wiki_user -d homelab_wiki -c "SELECT 1;"

# LDAP connection test
docker-compose exec backend python -c "from app.auth.ldap_auth import test_ldap_connection; test_ldap_connection()"
```

## Security Configuration

### Container Security
- **Non-root users**: All containers run as non-root
- **Resource limits**: Configured in production mode
- **Network isolation**: Services isolated in private network
- **Read-only filesystem**: Where applicable

### Data Security
- **Environment variables**: Sensitive data from `.env` file
- **Docker secrets**: Available for high-security deployments
- **Volume encryption**: Can be configured at host level
- **SSL/TLS**: Configured in nginx proxy

### Access Control
- **Internal network**: Database not exposed to host
- **Reverse proxy**: Only nginx exposed externally
- **LDAP authentication**: All users authenticated via Active Directory
- **Role-based access**: Based on AD group membership

## Monitoring and Logging

### Log Configuration
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### Log Locations
- **Application logs**: `/app/logs` volume
- **Container logs**: `docker-compose logs`
- **System logs**: Docker daemon logs

### Monitoring Commands
```bash
# Service status
docker-compose ps

# Resource usage
docker stats

# Log viewing
docker-compose logs -f

# Health checks
curl http://localhost:5000/health
```

## Troubleshooting

### Common Issues
1. **Port conflicts**: Check if ports 80/443 are available
2. **Permission errors**: Ensure `.env` file has correct permissions
3. **LDAP connectivity**: Verify WYK-DC01 is accessible
4. **Database issues**: Check database logs and connectivity

### Debugging Commands
```bash
# Check configuration
docker-compose config

# View environment variables
docker-compose exec backend env

# Test database connection
docker-compose exec database psql -U wiki_user -d homelab_wiki

# Check nginx configuration
docker-compose exec nginx nginx -t
```

### Recovery Procedures
```bash
# Restart failed service
docker-compose restart backend

# Recreate service
docker-compose up -d --force-recreate backend

# Complete reset (WARNING: deletes data)
docker-compose down -v
docker-compose up -d
```

## Best Practices

### Development
- Use `docker-compose.dev.yml` for development
- Mount source code for live reload
- Enable debug logging
- Expose service ports for direct access

### Production
- Use `docker-compose.prod.yml` for production
- Configure resource limits
- Enable SSL/TLS
- Use nginx reverse proxy
- Implement log rotation

### Security
- Never commit `.env` files
- Use strong, unique passwords
- Regular credential rotation
- Monitor authentication logs
- Keep containers updated

### Maintenance
- Regular backups
- Log monitoring
- Performance monitoring
- Security updates
- Cleanup unused resources

## File Structure
```
HomelabWiki/
├── docker-compose.yml           # Main configuration
├── docker-compose.dev.yml       # Development overrides
├── docker-compose.prod.yml      # Production overrides
├── docker-compose.secrets.yml   # High-security configuration
├── .env                        # Environment variables (create from .env.example)
├── config/
│   ├── nginx/
│   │   └── default.conf        # Nginx configuration
│   └── env/
│       └── .env.example        # Environment template
├── backend/
│   └── Dockerfile              # Backend container definition
├── frontend/
│   └── Dockerfile              # Frontend container definition
└── ssl/                        # SSL certificates (optional)
    ├── homelab-wiki.crt
    └── homelab-wiki.key
```

For detailed deployment instructions, see the [Docker Deployment Guide](docker.md).
