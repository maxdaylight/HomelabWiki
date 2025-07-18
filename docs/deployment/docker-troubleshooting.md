# HomelabWiki Docker Troubleshooting Guide

## Common Issues and Solutions

### 1. Service Won't Start

#### Symptoms
- Container exits immediately
- Service status shows "Exited (1)"
- Error messages in logs

#### Diagnosis
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs service_name

# Check configuration
docker-compose config
```

#### Solutions

**Missing Environment Variables**
```bash
# Check if .env file exists
ls -la .env

# Verify required variables
grep -E "SECRET_KEY|LDAP_BIND_PASSWORD" .env

# Copy from template if missing
cp config/env/.env.example .env
```

**Port Conflicts**
```bash
# Check port usage
netstat -tlnp | grep -E ":(80|443|3000|5000|5432)"

# Use alternative ports
# Edit docker-compose.yml:
ports:
  - "8080:80"  # Alternative HTTP port
  - "8443:443" # Alternative HTTPS port
```

**Permission Issues**
```bash
# Fix .env permissions
chmod 600 .env

# Fix data directory permissions
sudo chown -R 1000:1000 data/
```

### 2. Database Connection Issues

#### Symptoms
- Backend can't connect to database
- Database connection errors in logs
- Tables not created

#### Diagnosis
```bash
# Check database logs
docker-compose logs database

# Test database connectivity
docker-compose exec database psql -U wiki_user -d homelab_wiki -c "SELECT 1;"

# Check database process
docker-compose exec database ps aux
```

#### Solutions

**PostgreSQL Not Ready**
```bash
# Wait for database to initialize
sleep 30
docker-compose restart backend

# Check PostgreSQL logs
docker-compose logs database | grep "ready to accept connections"
```

**Wrong Database Credentials**
```bash
# Verify database environment variables
docker-compose exec database env | grep POSTGRES

# Check .env file
grep -E "POSTGRES_" .env

# Reset database (WARNING: deletes data)
docker-compose down -v
docker-compose up -d
```

**Database Corruption**
```bash
# Check database integrity
docker-compose exec database psql -U wiki_user -d homelab_wiki -c "SELECT pg_database_size(current_database());"

# Restore from backup
docker-compose down
# Restore backup files
docker-compose up -d
```

### 3. LDAP Authentication Issues

#### Symptoms
- Cannot login with AD credentials
- LDAP connection errors
- Authentication timeout

#### Diagnosis
```bash
# Test LDAP connectivity
docker-compose exec backend python -c "
import ldap
try:
    conn = ldap.initialize('ldap://WYK-DC01:389')
    conn.simple_bind_s()
    print('LDAP connection successful')
except Exception as e:
    print(f'LDAP error: {e}')
"

# Check LDAP configuration
docker-compose exec backend env | grep LDAP
```

#### Solutions

**LDAP Server Unreachable**
```bash
# Test network connectivity
docker-compose exec backend ping WYK-DC01

# Check DNS resolution
docker-compose exec backend nslookup WYK-DC01

# Test LDAP port
docker-compose exec backend telnet WYK-DC01 389
```

**Invalid LDAP Credentials**
```bash
# Verify service account
# Check .env file
grep LDAP_BIND_PASSWORD .env

# Test credentials manually
# (Run on domain controller)
dsquery user -samid wikisvc
```

**LDAP Configuration Issues**
```bash
# Check base DN
docker-compose exec backend python -c "
import ldap
conn = ldap.initialize('ldap://WYK-DC01:389')
conn.simple_bind_s('CN=WikiService,CN=Users,DC=wyk,DC=local', 'password')
result = conn.search_s('DC=wyk,DC=local', ldap.SCOPE_BASE)
print(result)
"
```

### 4. Frontend Issues

#### Symptoms
- Frontend not loading
- API connection errors
- Blank white page

#### Diagnosis
```bash
# Check frontend logs
docker-compose logs frontend

# Test frontend directly
curl http://localhost:3000

# Check API connectivity
curl http://localhost:5000/health
```

#### Solutions

**API Connection Issues**
```bash
# Check backend status
docker-compose ps backend

# Verify API URL configuration
docker-compose exec frontend env | grep VITE_API_URL

# Test API from frontend container
docker-compose exec frontend curl http://backend:5000/health
```

**Build Issues**
```bash
# Rebuild frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend

# Check build logs
docker-compose logs frontend
```

**Network Issues**
```bash
# Check Docker network
docker network ls
docker network inspect homelab-wiki_wiki_network

# Restart network
docker-compose down
docker-compose up -d
```

### 5. SSL/TLS Issues

#### Symptoms
- SSL certificate errors
- HTTPS not working
- Mixed content warnings

#### Diagnosis
```bash
# Check SSL configuration
docker-compose exec nginx nginx -t

# Verify certificate files
ls -la ssl/

# Test SSL connection
openssl s_client -connect localhost:443
```

#### Solutions

**Missing SSL Certificates**
```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/homelab-wiki.key \
  -out ssl/homelab-wiki.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=homelab-wiki.local"

# Set permissions
chmod 600 ssl/homelab-wiki.key
chmod 644 ssl/homelab-wiki.crt
```

**Nginx SSL Configuration**
```bash
# Check nginx configuration
docker-compose exec nginx cat /etc/nginx/conf.d/default.conf

# Reload nginx
docker-compose exec nginx nginx -s reload
```

### 6. Performance Issues

#### Symptoms
- Slow response times
- High CPU/memory usage
- Database timeouts

#### Diagnosis
```bash
# Check resource usage
docker stats

# Monitor logs
docker-compose logs -f | grep -i "slow\|timeout\|error"

# Check disk space
df -h
docker system df
```

#### Solutions

**Resource Limits**
```bash
# Use production configuration with limits
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Monitor resource usage
docker stats --no-stream
```

**Database Performance**
```bash
# Optimize database
docker-compose exec database psql -U wiki_user -d homelab_wiki -c "VACUUM ANALYZE;"

# Check slow queries
docker-compose exec database psql -U wiki_user -d homelab_wiki -c "
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;"
```

**Clean Up Resources**
```bash
# Remove unused containers
docker container prune -f

# Remove unused images
docker image prune -f

# Remove unused volumes
docker volume prune -f

# Full cleanup
docker system prune -af
```

### 7. File Upload Issues

#### Symptoms
- File uploads fail
- Permission denied errors
- Disk space errors

#### Diagnosis
```bash
# Check upload directory permissions
docker-compose exec backend ls -la /app/uploads/

# Check disk space
df -h
docker-compose exec backend df -h

# Check file limits
docker-compose exec backend env | grep MAX_CONTENT_LENGTH
```

#### Solutions

**Permission Issues**
```bash
# Fix upload directory permissions
docker-compose exec backend chown -R app:app /app/uploads/
docker-compose exec backend chmod -R 755 /app/uploads/
```

**Disk Space Issues**
```bash
# Clean up old files
docker-compose exec backend find /app/uploads/ -type f -mtime +90 -delete

# Check volume usage
docker system df
```

### 8. Backup and Recovery Issues

#### Symptoms
- Backup failures
- Cannot restore data
- Missing backup files

#### Diagnosis
```bash
# Check backup directory
docker-compose exec backend ls -la /app/backups/

# Test backup script
./scripts/backup.sh

# Check backup logs
docker-compose logs backend | grep backup
```

#### Solutions

**Backup Script Issues**
```bash
# Make backup script executable
chmod +x scripts/backup.sh

# Test backup manually
docker-compose exec backend python -m app.backup
```

**Recovery Process**
```bash
# Stop services
docker-compose down

# Restore database
cp backup/wiki_db_20250718.db data/homelab_wiki.db

# Restore uploads
tar -xzf backup/wiki_uploads_20250718.tar.gz -C data/

# Fix permissions
sudo chown -R 1000:1000 data/

# Start services
docker-compose up -d
```

## Diagnostic Commands

### System Information
```bash
# Docker version
docker --version
docker-compose --version

# System resources
free -h
df -h
lscpu

# Network information
ip addr show
netstat -tlnp
```

### Service Health
```bash
# All services status
docker-compose ps

# Resource usage
docker stats --no-stream

# Health checks
curl http://localhost:5000/health
curl http://localhost:3000

# Service logs
docker-compose logs -f --tail=50
```

### Configuration Validation
```bash
# Validate docker-compose.yml
docker-compose config

# Check environment variables
docker-compose exec backend env | grep -E "SECRET_KEY|LDAP|DATABASE"

# Verify file permissions
ls -la .env
ls -la ssl/
```

## Log Analysis

### Important Log Patterns
```bash
# Authentication errors
docker-compose logs backend | grep -i "auth\|ldap\|login"

# Database errors
docker-compose logs database | grep -i "error\|fail"

# Application errors
docker-compose logs backend | grep -i "error\|exception\|traceback"

# Performance issues
docker-compose logs | grep -i "slow\|timeout\|memory"
```

### Log Locations
- **Application logs**: `docker-compose logs`
- **Container logs**: `/var/lib/docker/containers/`
- **System logs**: `/var/log/syslog`
- **Nginx logs**: Inside nginx container

## Emergency Procedures

### Complete Reset (WARNING: Deletes all data)
```bash
# Stop and remove everything
docker-compose down -v --remove-orphans

# Clean up Docker resources
docker system prune -af
docker volume prune -f

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

### Service Recovery
```bash
# Restart single service
docker-compose restart backend

# Recreate service
docker-compose up -d --force-recreate backend

# Scale service
docker-compose up -d --scale backend=2
```

### Data Recovery
```bash
# Restore from backup
docker-compose down
# Copy backup files to data/
docker-compose up -d

# Check data integrity
docker-compose exec backend python -c "
from app import create_app
app = create_app()
with app.app_context():
    from app.models import db, Page
    print(f'Pages count: {Page.query.count()}')
"
```

## Prevention Tips

### Regular Maintenance
```bash
# Weekly tasks
docker-compose logs --since 7d | grep -i error
docker system df
docker-compose exec database psql -U wiki_user -d homelab_wiki -c "VACUUM ANALYZE;"

# Monthly tasks
docker system prune -f
./scripts/backup.sh
```

### Monitoring Setup
```bash
# Set up log rotation
# Edit /etc/logrotate.d/docker-compose

# Monitor disk space
# Add to crontab: 0 0 * * * df -h | mail -s "Disk Space" admin@example.com

# Health check monitoring
# Add to crontab: */5 * * * * curl -f http://localhost:5000/health || echo "Health check failed"
```

### Security Monitoring
```bash
# Monitor authentication failures
docker-compose logs backend | grep -i "auth.*fail\|invalid.*login"

# Check for suspicious activity
docker-compose logs nginx | grep -E "POST|PUT|DELETE"

# Verify file integrity
find data/ -type f -name "*.db" -exec md5sum {} \;
```

For additional help, see:
- [Docker Deployment Guide](docker.md)
- [Security Documentation](../security/README.md)
- [User Guide](../user-guide/README.md)
