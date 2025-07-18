# Configuration Documentation

This directory contains configuration guides and documentation for HomelabWiki.

## 📁 Contents

- **[local-environment.md](local-environment.md)** - Complete guide for configuring your local environment with your specific server names, IP addresses, and domain information

## 🔒 Security Notice

The configuration files in this directory provide templates and examples using generic placeholders. **Never commit actual server names, IP addresses, passwords, or domain information to version control.**

## 📋 Quick Start

1. **Copy the environment template**:
   ```bash
   cp config/env/.env.local.example .env.local
   ```

2. **Follow the local environment guide**: [local-environment.md](local-environment.md)

3. **Test your configuration**:
   ```bash
   docker-compose up -d
   ```

## 📚 Related Documentation

- [Deployment Guide](../deployment/README.md) - General deployment instructions
- [Security Guide](../security/README.md) - Security best practices
- [API Documentation](../api/README.md) - API reference

## 🆘 Support

If you need help with configuration:

1. Check the [local environment guide](local-environment.md)
2. Review the [troubleshooting section](../deployment/README.md#troubleshooting)
3. Create an issue in the repository (without including sensitive information)
