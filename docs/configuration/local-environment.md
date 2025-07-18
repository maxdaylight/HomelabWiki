# Local Environment Configuration Guide

This guide explains how to configure HomelabWiki with your specific server names, IP addresses, and domain information without exposing them in the public repository.

## 🔒 Security First

**Important**: Never commit actual server names, IP addresses, or domain information to version control. This guide shows you how to keep your environment details secure while still being able to deploy and run HomelabWiki.

## 📁 Configuration Files

### 1. Environment Configuration

Copy the local environment template and customize it:

```bash
# Copy the template
cp config/env/.env.local.example .env.local

# Edit with your values
nano .env.local
```

### 2. Required Configuration

Update these key values in your `.env.local` file:

```bash
# Your Domain Controller
LDAP_SERVER=DC01                    # Replace with your DC hostname
LDAP_PORT=389                       # Your LDAP port

# Your Domain Information
LDAP_BASE_DN=DC=company,DC=com      # Replace with your domain
LDAP_BIND_DN=CN=wikisvc,CN=Users,DC=company,DC=com
LDAP_BIND_PASSWORD=YourRealPassword # Your service account password

# Your Search Configuration
LDAP_USER_SEARCH_BASE=CN=Users,DC=company,DC=com
LDAP_GROUP_SEARCH_BASE=CN=Groups,DC=company,DC=com

# Your Groups
LDAP_ADMIN_GROUP=CN=WikiAdmins,CN=Users,DC=company,DC=com
LDAP_USER_GROUP=CN=WikiUsers,CN=Users,DC=company,DC=com
LDAP_READONLY_GROUP=CN=WikiReadOnly,CN=Users,DC=company,DC=com

# Generate a secure secret key
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

## 🖥️ Example Configurations

### Example 1: Small Business Setup

```bash
# Domain Controller
LDAP_SERVER=DC01
LDAP_PORT=389

# Domain: company.local
LDAP_BASE_DN=DC=company,DC=local
LDAP_BIND_DN=CN=wikisvc,CN=Users,DC=company,DC=local
LDAP_USER_SEARCH_BASE=CN=Users,DC=company,DC=local
LDAP_GROUP_SEARCH_BASE=CN=Groups,DC=company,DC=local
```

### Example 2: Multi-Domain Setup

```bash
# Domain Controller
LDAP_SERVER=CORP-DC01
LDAP_PORT=389

# Domain: corp.example.com
LDAP_BASE_DN=DC=corp,DC=example,DC=com
LDAP_BIND_DN=CN=wikisvc,CN=Service Accounts,DC=corp,DC=example,DC=com
LDAP_USER_SEARCH_BASE=CN=Users,DC=corp,DC=example,DC=com
LDAP_GROUP_SEARCH_BASE=CN=Groups,DC=corp,DC=example,DC=com
```

### Example 3: Homelab Setup

```bash
# Domain Controller
LDAP_SERVER=192.168.1.10
LDAP_PORT=389

# Domain: homelab.internal
LDAP_BASE_DN=DC=homelab,DC=internal
LDAP_BIND_DN=CN=wikisvc,CN=Users,DC=homelab,DC=internal
LDAP_USER_SEARCH_BASE=CN=Users,DC=homelab,DC=internal
LDAP_GROUP_SEARCH_BASE=CN=Users,DC=homelab,DC=internal
```

## 🔧 Setup Steps

### Step 1: Prepare Your Environment

1. **Create your local configuration**:
   ```bash
   cd HomelabWiki
   cp config/env/.env.local.example .env.local
   ```

2. **Generate a secure secret key**:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Update your `.env.local` file** with your actual values

### Step 2: Active Directory Setup

1. **Create the service account** in Active Directory:
   ```powershell
   # Replace with your domain
   New-ADUser -Name "WikiService" -SamAccountName "wikisvc" -UserPrincipalName "wikisvc@yourdomain.com" -PasswordNeverExpires $true
   ```

2. **Create the security groups**:
   ```powershell
   New-ADGroup -Name "WikiAdmins" -GroupScope DomainLocal
   New-ADGroup -Name "WikiUsers" -GroupScope DomainLocal
   New-ADGroup -Name "WikiReadOnly" -GroupScope DomainLocal
   ```

3. **Add users to appropriate groups**:
   ```powershell
   Add-ADGroupMember -Identity "WikiAdmins" -Members "your-username"
   ```

### Step 3: Test Your Configuration

1. **Start the services**:
   ```bash
   docker-compose up -d
   ```

2. **Test LDAP connectivity**:
   ```bash
   docker-compose exec backend python -c "
   import ldap
   import os
   
   server = os.getenv('LDAP_SERVER')
   port = int(os.getenv('LDAP_PORT', '389'))
   
   try:
       conn = ldap.initialize(f'ldap://{server}:{port}')
       conn.simple_bind_s()
       print('LDAP connection successful')
   except Exception as e:
       print(f'LDAP connection failed: {e}')
   "
   ```

3. **Test authentication**:
   ```bash
   curl -X POST http://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "your-username", "password": "your-password"}'
   ```

## 📋 Configuration Reference

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `LDAP_SERVER` | Your domain controller hostname/IP | `DC01` or `192.168.1.10` |
| `LDAP_PORT` | LDAP port | `389` (standard) or `636` (SSL) |
| `LDAP_BASE_DN` | Base distinguished name | `DC=company,DC=local` |
| `LDAP_BIND_DN` | Service account DN | `CN=wikisvc,CN=Users,DC=company,DC=local` |
| `LDAP_BIND_PASSWORD` | Service account password | `YourSecurePassword` |
| `LDAP_USER_SEARCH_BASE` | Where to search for users | `CN=Users,DC=company,DC=local` |
| `LDAP_GROUP_SEARCH_BASE` | Where to search for groups | `CN=Groups,DC=company,DC=local` |

### Common Domain Patterns

| Domain Type | Example | Base DN |
|-------------|---------|---------|
| Simple | `company.local` | `DC=company,DC=local` |
| Multi-level | `dept.company.com` | `DC=dept,DC=company,DC=com` |
| Homelab | `homelab.internal` | `DC=homelab,DC=internal` |

## 🛠️ Troubleshooting

### Common Issues

1. **LDAP Connection Refused**:
   - Check if your domain controller is reachable
   - Verify firewall settings
   - Test connectivity: `ping your-domain-controller`

2. **Authentication Fails**:
   - Verify service account credentials
   - Check if account is enabled and not locked
   - Test manual LDAP bind

3. **Users Not Found**:
   - Verify search base DNs are correct
   - Check object class filters
   - Ensure users exist in specified OUs

### Testing Commands

```bash
# Test connectivity
docker-compose exec backend nslookup your-domain-controller
docker-compose exec backend ping -c 3 your-domain-controller

# Test LDAP search
docker-compose exec backend ldapsearch -x -h your-domain-controller -p 389 \
  -D "CN=wikisvc,CN=Users,DC=yourdomain,DC=com" \
  -w "password" \
  -b "DC=yourdomain,DC=com" \
  "(sAMAccountName=testuser)"
```

## 🔐 Security Best Practices

1. **Use Strong Passwords**:
   - Service account passwords should be complex
   - Use different passwords for each environment

2. **Restrict Service Account**:
   - Grant only necessary permissions
   - Use dedicated service account for the application

3. **Network Security**:
   - Restrict network access to domain controllers
   - Use firewall rules to limit access

4. **Regular Maintenance**:
   - Rotate service account passwords regularly
   - Monitor authentication logs
   - Review group memberships periodically

## 📝 Documentation Updates

When updating your deployment:

1. **Never commit real values** to the repository
2. **Update your local `.env.local`** with any new variables
3. **Test changes** in development first
4. **Document custom configurations** for your team (in a separate, secure location)

## 🆘 Support

If you encounter issues:

1. Check the main troubleshooting guide
2. Verify all environment variables are set correctly
3. Test LDAP connectivity manually
4. Check application logs for specific error messages

Remember: Keep your actual configuration secure and never commit it to version control!
