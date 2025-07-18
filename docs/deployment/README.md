# HomelabWiki Deployment Guide

## Overview
This guide provides comprehensive deployment instructions for HomelabWiki in various environments, with a focus on homelab and small business scenarios.

## Deployment Options

### 🐳 Docker Deployment (Recommended)
- **Best for**: All environments
- **Features**: Full containerization, easy management, scalable
- **Guide**: [Docker Deployment Guide](docker.md)

### 🔧 Manual Installation
- **Best for**: Custom environments, learning purposes
- **Features**: Direct control, customizable
- **Guide**: [Manual Installation Guide](manual.md)

### ☁️ Cloud Deployment
- **Best for**: External access, high availability
- **Features**: Auto-scaling, managed services
- **Guide**: [Cloud Deployment Guide](cloud.md)

## Quick Start (Docker)

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- Access to your Active Directory domain controller
- 2GB+ RAM, 10GB+ storage

### 1. Clone and Configure
```bash
git clone <repository-url>
cd HomelabWiki
cp config/env/.env.example .env
```

### 2. Secure Configuration
```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Edit .env with your credentials
nano .env
```

### 3. Deploy
```bash
docker-compose up -d
```

### 4. Access
- **Application**: http://localhost:3000
- **Login**: Use your WYK domain credentials

## System Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 2GB
- **Storage**: 10GB
- **Network**: 1Gbps internal

### Recommended Requirements
- **CPU**: 4 cores
- **RAM**: 4GB
- **Storage**: 50GB SSD
- **Network**: 1Gbps internal

### Supported Platforms
- **Primary**: Debian 11+ Linux Container (Proxmox)
- **Supported**: Ubuntu 20.04+, CentOS 8+, RHEL 8+
- **Docker**: Any Docker-compatible platform

## Active Directory Integration

### Required AD Components
- **Domain Controller**: your-domain-controller (IP: your-dc-ip)
- **Service Account**: LDAP bind account
- **Security Groups**: 
  - `WikiAdmins` (Full access)
  - `WikiUsers` (Read/Write)
  - `WikiReadOnly` (Read only)

### AD Configuration Script
```powershell
# Run on domain controller
New-ADGroup -Name "WikiAdmins" -GroupScope DomainLocal -GroupCategory Security
New-ADGroup -Name "WikiUsers" -GroupScope DomainLocal -GroupCategory Security  
New-ADGroup -Name "WikiReadOnly" -GroupScope DomainLocal -GroupCategory Security

# Create service account
New-ADUser -Name "WikiService" -SamAccountName "wikisvc" -Enabled $true
```

## Security Configuration

### Environment Variables
Never commit these to version control:
```env
SECRET_KEY=your-generated-secret-key
LDAP_BIND_PASSWORD=your-ldap-password
POSTGRES_PASSWORD=your-db-password
```

### File Permissions
```bash
chmod 600 .env
```

### Network Security
- Internal network only by default
- Optional SSL/TLS for external access
- Firewall rules for port management

## Installation Steps

### Docker Deployment (Recommended)

#### 1. Prepare Environment
```bash
# Update system
apt update && apt upgrade -y

# Install Docker
apt install -y docker.io docker-compose

# Enable Docker
systemctl enable docker
systemctl start docker
```

#### 2. Clone and Configure
```bash
# Clone repository
git clone <repository-url>
cd HomelabWiki

# Copy environment template
cp config/env/.env.example .env
```

#### 3. Configure Credentials
```bash
# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Edit .env file
nano .env
```

**Required Variables**:
```env
SECRET_KEY=your-generated-secret-key
LDAP_BIND_PASSWORD=your-ldap-password
POSTGRES_PASSWORD=your-db-password  # If using PostgreSQL
```

#### 4. Deploy Services
```bash
# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

#### 5. Verify Installation
```bash
# Test backend
curl http://localhost:5000/health

# Test frontend
curl http://localhost:3000

# Test LDAP
docker-compose exec backend python -c "from app.auth.ldap_auth import test_ldap_connection; test_ldap_connection()"
```

### Manual Deployment

For manual installation without Docker, see: [Manual Installation Guide](manual.md)

### Cloud Deployment

For cloud providers (AWS, Azure, GCP), see: [Cloud Deployment Guide](cloud.md)

## Post-Installation Configuration

### 1. First Login
- Navigate to http://localhost:3000
- Login with domain credentials: `wyk\username`
- Ensure your account is in `WikiAdmins` group

### 2. SSL Configuration (Optional)
```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/homelab-wiki.key \
  -out ssl/homelab-wiki.crt

# Update nginx configuration
nano config/nginx/default.conf
```

### 3. Backup Configuration
```bash
# Create backup script
cp scripts/backup.sh /usr/local/bin/
chmod +x /usr/local/bin/backup.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /usr/local/bin/backup.sh
```

## Maintenance and Monitoring

### Health Checks
```bash
# Application health
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
docker-compose logs backend
docker-compose logs frontend
docker-compose logs database
```

### Updates
```bash
# Update application
git pull origin main
docker-compose build --no-cache
docker-compose up -d

# Clean up
docker system prune -f
```

## Troubleshooting

### Common Issues

#### LDAP Authentication Failed
```bash
# Test LDAP connectivity
docker-compose exec backend python -c "
import ldap
conn = ldap.initialize('ldap://your-domain-controller:389')
conn.simple_bind_s()
print('LDAP connection successful')
"
```

#### Database Connection Issues
```bash
# Test database
docker-compose exec database psql -U wiki_user -d homelab_wiki -c "SELECT 1;"

# Reset database (WARNING: Deletes all data)
docker-compose down -v
docker-compose up -d
```

#### Permission Errors
```bash
# Fix file permissions
chown -R 1000:1000 data/
chmod -R 755 data/
```

#### Port Conflicts
```bash
# Check port usage
netstat -tlnp | grep :80
netstat -tlnp | grep :443

# Use alternative ports
# Edit docker-compose.yml ports section
```

### Performance Optimization

#### Database Optimization
```bash
# SQLite optimization
docker-compose exec backend sqlite3 /app/data/homelab_wiki.db "VACUUM; ANALYZE;"

# PostgreSQL optimization
docker-compose exec database psql -U wiki_user -d homelab_wiki -c "VACUUM ANALYZE;"
```

#### Resource Monitoring
```bash
# Monitor containers
docker stats --no-stream

# Check disk usage
df -h
du -sh data/
```

## Security Hardening

### Network Security
```bash
# Firewall rules (UFW)
ufw allow 80/tcp
ufw allow 443/tcp
ufw deny 22/tcp  # Restrict SSH if needed

# Internal network only
# No additional rules needed for internal-only access
```

### File Security
```bash
# Secure environment file
chmod 600 .env
chown root:root .env

# Secure SSL certificates
chmod 600 ssl/*.key
chmod 644 ssl/*.crt
```

### Access Control
- Use strong passwords
- Enable 2FA on AD accounts
- Regular access reviews
- Principle of least privilege

## Backup and Recovery

### Automated Backup
```bash
#!/bin/bash
# /usr/local/bin/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/homelab-wiki"

mkdir -p $BACKUP_DIR

# Database backup
docker-compose exec -T backend sqlite3 /app/data/homelab_wiki.db ".backup /app/data/backups/wiki_db_${DATE}.db"

# File backup
tar -czf $BACKUP_DIR/wiki_files_${DATE}.tar.gz -C data uploads

# Cleanup old backups (30 days)
find $BACKUP_DIR -name "wiki_*" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### Recovery Process
```bash
# Stop services
docker-compose down

# Restore database
cp /opt/backups/wiki_db_YYYYMMDD_HHMMSS.db data/homelab_wiki.db

# Restore files
tar -xzf /opt/backups/wiki_files_YYYYMMDD_HHMMSS.tar.gz -C data/

# Fix permissions
chown -R 1000:1000 data/

# Start services
docker-compose up -d
```

## Environment-Specific Guides

### Development Environment
```bash
# Use development configuration
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### Production Environment
```bash
# Use production configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### High-Security Environment
```bash
# Use Docker secrets
docker-compose -f docker-compose.secrets.yml up -d
```

## Support and Resources

### Documentation
- [Docker Deployment Guide](docker.md) - Comprehensive Docker documentation
- [Security Guide](../security/README.md) - Security best practices
- [User Guide](../user-guide/README.md) - User documentation
- [API Documentation](../api/README.md) - API reference

### Scripts
- `scripts/security-check.sh` - Security validation
- `scripts/test-docker.sh` - Docker testing
- `scripts/backup.sh` - Backup automation

### Logs and Monitoring
- Application logs: `docker-compose logs`
- Health endpoint: `http://localhost:5000/health`
- Metrics: `docker stats`

For additional support:
1. Check troubleshooting section
2. Review logs with `docker-compose logs -f`
3. Run security check: `scripts/security-check.sh`
4. Create GitHub issue with logs and configuration

---

**Note**: This deployment guide is optimized for homelab environments with trusted internal networks. For production enterprise deployment, additional security hardening may be required.
