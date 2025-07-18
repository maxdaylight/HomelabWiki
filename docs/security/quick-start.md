# Quick Start: Secure HomelabWiki Deployment

## 🚨 Security Alert
Before deploying HomelabWiki, ensure you've properly secured your credentials. This guide provides the fastest path to a secure deployment.

## 1. Prerequisites
- Docker and docker-compose installed
- Access to your WYK-DC01 Active Directory server
- LDAP service account with read permissions

## 2. Create Environment File (CRITICAL)

### Copy Example File
```bash
cp config/env/.env.example .env
```

### Generate Secure Secret Key
Run ONE of these commands to generate a secure secret key:

**Python:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**PowerShell (Windows):**
```powershell
[System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
```

**OpenSSL:**
```bash
openssl rand -hex 32
```

### Edit .env File
Open `.env` in your text editor and update these **CRITICAL** values:

```env
# Replace with your generated secret key
SECRET_KEY=your-generated-64-character-secret-key-here

# Replace with your LDAP service account password
LDAP_BIND_PASSWORD=your-actual-ldap-service-account-password

# If using PostgreSQL, replace with secure password
POSTGRES_PASSWORD=your-secure-database-password
```

## 3. Secure File Permissions

### Linux/Unix:
```bash
chmod 600 .env
```

### Windows:
```powershell
icacls .env /grant:r "$($env:USERNAME):(R,W)" /inheritance:r
```

## 4. Verify Security

### Check .env File
Ensure these values are NOT in your `.env` file:
- ❌ `SECRET_KEY=REPLACE_WITH_SECURE_32_CHAR_SECRET_KEY`
- ❌ `LDAP_BIND_PASSWORD=REPLACE_WITH_ACTUAL_LDAP_PASSWORD`
- ❌ `POSTGRES_PASSWORD=REPLACE_WITH_SECURE_DB_PASSWORD`

### Check .gitignore
Verify `.env` is in your `.gitignore` file:
```bash
grep -q "^\.env$" .gitignore && echo "✅ .env is ignored" || echo "❌ .env NOT ignored"
```

## 5. Deploy

### Start Services
```bash
docker-compose up -d
```

### Verify Health
```bash
# Check if services are running
docker-compose ps

# Test health endpoint
curl http://localhost:5000/health
```

### View Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 6. Initial Access

### Access the Application
- **URL**: http://localhost:3000
- **Login**: Use your WYK domain credentials (e.g., `wyk\username`)
- **Password**: Your Active Directory password

### First Login
1. Navigate to http://localhost:3000
2. Click "Login"
3. Enter your AD credentials:
   - Username: `wyk\yourusername` or `yourusername@wyk.local`
   - Password: Your AD password

### Admin Access
Ensure your AD account is in the `WikiAdmins` group for full access.

## 7. Post-Deployment Security

### Monitor Logs
```bash
# Check for authentication errors
docker-compose logs backend | grep -i "auth\|ldap\|error"

# Check for failed logins
docker-compose logs backend | grep -i "failed\|unauthorized"
```

### Test LDAP Connection
```bash
# Test LDAP connectivity
docker-compose exec backend python -c "
from app.auth.ldap_auth import test_ldap_connection
test_ldap_connection()
"
```

## 8. Troubleshooting

### Common Issues

**Can't login:**
- Check LDAP service account password
- Verify user is in correct AD groups
- Check LDAP server connectivity

**Secret key errors:**
- Ensure SECRET_KEY is set in .env
- Verify key is at least 32 characters
- Restart services after changing key

**Database connection errors:**
- Check database passwords in .env
- Verify database service is running
- Check database connection string

### Get Help
```bash
# View service status
docker-compose ps

# Check service logs
docker-compose logs [service_name]

# Restart specific service
docker-compose restart [service_name]

# Full restart
docker-compose down && docker-compose up -d
```

## 9. Security Checklist

Before going live, verify:

- [ ] `.env` file contains unique, strong passwords
- [ ] `.env` file has proper permissions (600)
- [ ] `.env` file is in `.gitignore`
- [ ] No hardcoded credentials in docker-compose.yml
- [ ] SECRET_KEY is 32+ characters and randomly generated
- [ ] LDAP service account has minimal required permissions
- [ ] Database passwords are strong and unique
- [ ] Application is accessible only on intended network
- [ ] Regular backup schedule is configured
- [ ] Log monitoring is in place

## 10. Next Steps

After successful deployment:
1. Configure regular backups
2. Set up monitoring and alerting
3. Configure SSL/TLS with reverse proxy
4. Review and adjust LDAP group permissions
5. Test disaster recovery procedures

## Need Help?

Refer to the comprehensive guides:
- [Full Credentials Management Guide](./credentials.md)
- [Deployment Guide](../deployment/README.md)
- [User Guide](../user-guide/README.md)

---

**⚠️ IMPORTANT**: Never commit your `.env` file to version control. Always use strong, unique passwords for all services.
