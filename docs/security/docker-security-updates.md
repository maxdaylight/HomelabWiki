# Docker Security Updates

## Overview
This document describes the security improvements made to the HomelabWiki Docker images to address vulnerabilities identified in the base images.

## Changes Made

### Backend Dockerfile (Python)
- **Updated Python version**: `3.11-slim` → `3.12-slim`
  - Reduces high vulnerabilities from 3 to 1
  - Python 3.12 includes security fixes and performance improvements
  
- **Enhanced package management**:
  - Added `--no-install-recommends` to apt-get commands
  - Improved cleanup with `apt-get clean` and temp directory removal
  - Updated pip before installing packages

- **Security hardening**:
  - Added security labels for container scanning
  - Improved user creation with specific UID/GID (1001)
  - Enhanced directory permissions (750 for app, 755 for uploads)
  - Added curl for health checks

### Frontend Dockerfile (Node.js/Nginx)
- **Updated Node.js version**: `18-alpine` → `20-alpine`
  - Node.js 20 is the current LTS version with security fixes
  
- **Updated Nginx version**: `alpine` → `1.26-alpine`
  - Specific version pinning for better security tracking
  - Nginx 1.26 includes security improvements

- **Security improvements**:
  - Added `--no-audit --no-fund` flags to npm install
  - Created dedicated nginx-user with specific UID/GID (1001)
  - Enhanced file permissions for static assets
  - Added security labels for container scanning

## Security Best Practices Implemented

### 1. **Non-Root User Execution**
- Both containers run as non-root users
- Specific UID/GID assignments (1001) for consistency
- Proper file ownership and permissions

### 2. **Minimal Base Images**
- Using slim/alpine variants to reduce attack surface
- Specific version tags instead of 'latest'
- Cleanup of package managers and temporary files

### 3. **Security Labels**
- Added metadata for security scanning tools
- Enables automated vulnerability tracking

### 4. **Dependency Management**
- Updated package managers (pip, npm) before installing
- Reduced recommended packages installation
- Proper cleanup after installation

## Automated Update Scripts

Two scripts have been created to help maintain security:

### PowerShell Script (`scripts/update-docker-images.ps1`)
```powershell
# Dry run to see what would change
.\scripts\update-docker-images.ps1 -DryRun

# Apply updates
.\scripts\update-docker-images.ps1
```

### Bash Script (`scripts/update-docker-images.sh`)
```bash
# Dry run to see what would change
./scripts/update-docker-images.sh --dry-run

# Apply updates
./scripts/update-docker-images.sh
```

## Remaining Vulnerabilities

### Backend (Python 3.12-slim)
- **Status**: 1 high vulnerability remaining
- **Mitigation**: This is significantly improved from 3 high vulnerabilities
- **Recommendation**: Monitor for Python 3.12 security updates

### Frontend (Nginx 1.26-alpine)
- **Status**: May still have some vulnerabilities
- **Mitigation**: Using latest stable version with security fixes
- **Recommendation**: Monitor for Nginx security updates

## Ongoing Security Maintenance

### 1. **Regular Updates**
- Run update scripts monthly or when vulnerabilities are discovered
- Monitor security advisories for base images
- Update dependency versions in requirements.txt and package.json

### 2. **Security Scanning**
- Integrate container scanning in CI/CD pipeline
- Use tools like Trivy, Snyk, or Docker Scout
- Regular vulnerability assessments

### 3. **Version Pinning**
- Always use specific version tags
- Document version update reasons
- Test updates in development environment first

### 4. **Monitoring**
- Subscribe to security mailing lists for:
  - Python security announcements
  - Node.js security releases
  - Nginx security advisories
  - Alpine Linux security updates

## Rebuilding Containers

After making these changes, rebuild and restart your containers:

```bash
# Stop current containers
docker-compose down

# Rebuild with new base images
docker-compose build

# Start with updated images
docker-compose up -d

# Verify the update
docker-compose ps
```

## Security Validation

### 1. **Container Scanning**
```bash
# Scan backend image
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image homelabwiki-backend

# Scan frontend image
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image homelabwiki-frontend
```

### 2. **Runtime Security**
- Verify containers run as non-root users
- Check file permissions are correct
- Test application functionality after updates

## Future Considerations

1. **Multi-stage Build Optimization**
   - Consider using distroless images for production
   - Implement security scanning in build pipeline

2. **Runtime Security**
   - Implement runtime security monitoring
   - Consider using security contexts in Kubernetes

3. **Secrets Management**
   - Use external secret management systems
   - Implement proper credential rotation

4. **Network Security**
   - Use private networks for container communication
   - Implement proper firewall rules
