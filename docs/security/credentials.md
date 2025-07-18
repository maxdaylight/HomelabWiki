# HomelabWiki Credentials Management Guide

## Overview
This guide explains how to securely manage credentials for HomelabWiki deployment without storing sensitive information in the repository.

## 1. Environment Variables Setup

### Create .env file
Copy the example environment file and configure with your actual credentials:

```bash
cp config/env/.env.example .env
nano .env
```

### Required Sensitive Variables
Update these variables in your `.env` file:

```env
# CRITICAL: Generate a strong secret key
SECRET_KEY=your-very-secure-random-secret-key-32-chars-or-more

# LDAP Service Account Password
LDAP_BIND_PASSWORD=your-actual-ldap-service-account-password

# Database Passwords (if using PostgreSQL)
POSTGRES_PASSWORD=your-secure-database-password
```

## 2. Generate Secure Secret Key

Use one of these methods to generate a strong secret key:

### Method 1: Python
```python
import secrets
print(secrets.token_hex(32))
```

### Method 2: OpenSSL
```bash
openssl rand -hex 32
```

### Method 3: PowerShell (Windows)
```powershell
[System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
```

## 3. Secure File Permissions

Set proper permissions on your `.env` file:

```bash
# Linux/Unix
chmod 600 .env
chown $(whoami):$(whoami) .env

# Verify permissions
ls -la .env
# Should show: -rw------- 1 user user
```

## 4. Docker Secrets (Advanced)

For production deployments, consider using Docker secrets:

### Create secrets files
```bash
# Create secrets directory
mkdir -p secrets

# Create secret files
echo "your-secret-key" | docker secret create wiki_secret_key -
echo "your-ldap-password" | docker secret create ldap_password -
echo "your-db-password" | docker secret create db_password -
```

### Update docker-compose.yml for secrets
```yaml
version: '3.8'

services:
  backend:
    # ... other config ...
    secrets:
      - wiki_secret_key
      - ldap_password
    environment:
      - SECRET_KEY_FILE=/run/secrets/wiki_secret_key
      - LDAP_BIND_PASSWORD_FILE=/run/secrets/ldap_password

secrets:
  wiki_secret_key:
    external: true
  ldap_password:
    external: true
  db_password:
    external: true
```

## 5. Environment-Specific Configuration

### Development Environment
```env
# .env.development
FLASK_ENV=development
DATABASE_URL=sqlite:///dev_homelab_wiki.db
LDAP_SERVER=dev-dc.yourdomain.local
# ... other dev-specific settings
```

### Production Environment
```env
# .env.production
FLASK_ENV=production
DATABASE_URL=postgresql://wiki_user:${POSTGRES_PASSWORD}@database:5432/homelab_wiki
LDAP_SERVER=WYK-DC01
# ... other prod-specific settings
```

## 6. Credential Rotation

### Regular Rotation Schedule
- **Secret Key**: Rotate every 90 days
- **LDAP Password**: Follow your organization's policy
- **Database Passwords**: Rotate every 180 days

### Rotation Process
1. Generate new credentials
2. Update `.env` file
3. Restart services: `docker-compose restart`
4. Test authentication
5. Update backup systems

## 7. Security Best Practices

### Never Commit Credentials
- Always use `.env` files for sensitive data
- Never commit `.env` files to version control
- Use `.env.example` as a template only

### Backup Security
- Encrypt backups containing credentials
- Store backups separately from application code
- Use secure storage (encrypted drives, vaults)

### Access Control
- Limit access to `.env` files
- Use principle of least privilege
- Audit access to credential files

### Monitoring
- Monitor failed authentication attempts
- Set up alerts for credential-related errors
- Regular security audits

## 8. Troubleshooting

### Missing Environment Variables
If you see errors about missing environment variables:

1. Check if `.env` file exists
2. Verify file permissions
3. Ensure all required variables are set
4. Check for typos in variable names

### LDAP Authentication Failures
1. Verify LDAP credentials are correct
2. Test LDAP connectivity: `docker-compose exec backend python -c "import ldap; print(ldap.initialize('ldap://WYK-DC01:389').simple_bind_s())"`
3. Check LDAP server accessibility
4. Verify service account permissions

### Database Connection Issues
1. Check database credentials
2. Verify database server is running
3. Test database connectivity
4. Check network connectivity

## 9. Emergency Procedures

### Compromised Credentials
If credentials are compromised:

1. **Immediate Actions**:
   - Change all affected passwords
   - Generate new secret keys
   - Restart all services
   - Check logs for unauthorized access

2. **Investigation**:
   - Review access logs
   - Check for unauthorized changes
   - Audit user activities
   - Document the incident

3. **Recovery**:
   - Update all systems with new credentials
   - Notify affected users
   - Implement additional security measures
   - Review and update security policies

### Locked Out Scenarios
If you're locked out:

1. **Database Access**:
   - Use PostgreSQL/SQLite direct access
   - Reset user permissions via SQL
   - Check user account status

2. **LDAP Issues**:
   - Verify service account status
   - Check LDAP server connectivity
   - Test with different LDAP user
   - Contact AD administrator

## 10. Automation Scripts

### Credential Validation Script
```bash
#!/bin/bash
# validate-credentials.sh

echo "Validating HomelabWiki credentials..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found"
    exit 1
fi

# Check for required variables
required_vars="SECRET_KEY LDAP_BIND_PASSWORD"
for var in $required_vars; do
    if ! grep -q "^$var=" .env; then
        echo "ERROR: $var not found in .env"
        exit 1
    fi
done

# Check secret key length
secret_key=$(grep "^SECRET_KEY=" .env | cut -d'=' -f2)
if [ ${#secret_key} -lt 32 ]; then
    echo "WARNING: SECRET_KEY should be at least 32 characters"
fi

echo "Credential validation complete"
```

### Secure Deployment Script
```bash
#!/bin/bash
# secure-deploy.sh

# Validate credentials
./validate-credentials.sh

# Set secure permissions
chmod 600 .env

# Deploy with security checks
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Verify deployment
sleep 10
curl -f http://localhost:5000/health || echo "Health check failed"

echo "Secure deployment complete"
```

## Summary

By following this guide, you ensure that:
- No sensitive credentials are stored in version control
- All secrets are properly protected with file permissions
- Credential rotation is manageable
- Security best practices are followed
- Emergency procedures are documented

Remember: **Security is an ongoing process, not a one-time setup.**
