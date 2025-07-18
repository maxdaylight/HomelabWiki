# Docker Quick Reference

## Essential Commands

### Basic Operations
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# View status
docker-compose ps

# View logs
docker-compose logs -f

# Update and rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Service Management
```bash
# Start specific service
docker-compose up -d backend

# Stop specific service
docker-compose stop frontend

# Restart specific service
docker-compose restart database

# View service logs
docker-compose logs -f backend
```

### Development Commands
```bash
# Development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Production mode
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# High-security mode
docker-compose -f docker-compose.secrets.yml up -d
```

## Environment Files

### .env (Main Configuration)
```env
# Required
SECRET_KEY=your-generated-secret-key
LDAP_BIND_PASSWORD=your-ldap-password

# Optional (with defaults)
LDAP_SERVER=WYK-DC01
LDAP_PORT=389
DATABASE_URL=sqlite:///homelab_wiki.db
```

### docker-compose.yml (Main)
- Base configuration
- Production-ready defaults
- Environment variable substitution

### docker-compose.dev.yml (Development)
- Debug mode enabled
- Source code mounting
- Additional port exposure

### docker-compose.prod.yml (Production)
- Resource limits
- Performance optimization
- Security hardening

### docker-compose.secrets.yml (High Security)
- Docker secrets integration
- No environment variable passwords
- Enhanced security posture

## Service Ports

### Default Ports
- **Frontend**: 3000 (internal), 80 (external)
- **Backend**: 5000 (internal)
- **Database**: 5432 (internal)
- **Nginx**: 80, 443 (external)

### Development Ports
- **Frontend**: 3000 (exposed)
- **Backend**: 5000 (exposed)
- **Database**: 5432 (exposed)

## Volume Management

### Named Volumes
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect homelab-wiki_wiki_data

# Backup volume
docker run --rm -v homelab-wiki_wiki_data:/data -v $(pwd):/backup alpine tar czf /backup/wiki_data.tar.gz /data

# Restore volume
docker run --rm -v homelab-wiki_wiki_data:/data -v $(pwd):/backup alpine tar xzf /backup/wiki_data.tar.gz -C /
```

### Volume Locations
- **wiki_data**: Application data
- **wiki_uploads**: User uploads
- **wiki_backups**: Automated backups
- **wiki_logs**: Application logs
- **postgres_data**: Database files

## Troubleshooting

### Common Issues
```bash
# Check service health
curl http://localhost:5000/health

# View container resources
docker stats

# Check disk usage
docker system df

# Clean up unused resources
docker system prune -f
```

### Log Analysis
```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# Filter logs by service
docker-compose logs backend

# Search logs
docker-compose logs backend | grep ERROR
```

### Database Issues
```bash
# Test database connection
docker-compose exec database psql -U wiki_user -d homelab_wiki -c "SELECT 1;"

# Database shell
docker-compose exec database psql -U wiki_user -d homelab_wiki

# Reset database (WARNING: Deletes all data)
docker-compose down -v
docker-compose up -d
```

### LDAP Issues
```bash
# Test LDAP connection
docker-compose exec backend python -c "
from app.auth.ldap_auth import test_ldap_connection
test_ldap_connection()
"

# Check LDAP configuration
docker-compose exec backend env | grep LDAP
```

## Security Commands

### Credential Management
```bash
# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Check file permissions
ls -la .env

# Set secure permissions
chmod 600 .env
```

### Security Validation
```bash
# Run security check
./scripts/security-check.sh

# Windows security check
.\scripts\security-check.ps1

# Docker configuration test
./scripts/test-docker.sh
```

## Maintenance

### Updates
```bash
# Update from git
git pull origin main

# Rebuild containers
docker-compose build --no-cache

# Update running services
docker-compose up -d

# Clean up old images
docker image prune -f
```

### Backups
```bash
# Manual backup
./scripts/backup.sh

# Database backup
docker-compose exec backend python -m app.backup

# Volume backup
docker run --rm -v homelab-wiki_wiki_data:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz /data
```

### Health Checks
```bash
# Application health
curl http://localhost:5000/health

# Service status
docker-compose ps

# Container statistics
docker stats --no-stream

# System resources
df -h
free -h
```

## Advanced Operations

### Scaling Services
```bash
# Scale frontend (multiple instances)
docker-compose up -d --scale frontend=3

# Scale with resource limits
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --scale backend=2
```

### Database Migration
```bash
# Run migrations
docker-compose exec backend flask db upgrade

# Create migration
docker-compose exec backend flask db migrate -m "Description"

# Database shell
docker-compose exec database psql -U wiki_user -d homelab_wiki
```

### SSL/TLS Setup
```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/homelab-wiki.key \
  -out ssl/homelab-wiki.crt

# Set certificate permissions
chmod 600 ssl/homelab-wiki.key
chmod 644 ssl/homelab-wiki.crt
```

## Performance Monitoring

### Resource Usage
```bash
# Container resources
docker stats

# Disk usage
docker system df

# Network usage
docker network ls
```

### Application Metrics
```bash
# Backend metrics
curl http://localhost:5000/metrics

# Database performance
docker-compose exec database psql -U wiki_user -d homelab_wiki -c "
SELECT schemaname,tablename,attname,n_distinct,correlation 
FROM pg_stats 
WHERE tablename = 'pages';"
```

## Configuration Examples

### SQLite Configuration
```env
DATABASE_URL=sqlite:///homelab_wiki.db
```

### PostgreSQL Configuration
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

## Emergency Procedures

### Complete Reset
```bash
# WARNING: This will delete all data
docker-compose down -v --remove-orphans
docker system prune -af
docker volume prune -f
docker-compose up -d
```

### Service Recovery
```bash
# Restart failed service
docker-compose restart backend

# Recreate service
docker-compose up -d --force-recreate backend

# Check service logs
docker-compose logs -f backend
```

### Data Recovery
```bash
# Stop services
docker-compose down

# Restore from backup
cp /path/to/backup/wiki_data.tar.gz .
tar -xzf wiki_data.tar.gz -C data/

# Fix permissions
chown -R 1000:1000 data/

# Start services
docker-compose up -d
```

---

This quick reference covers the most common Docker operations for HomelabWiki. For detailed documentation, see the [Docker Deployment Guide](docker.md).
