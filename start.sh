#!/bin/bash
# HomelabWiki Startup Script
# This script helps with initial setup and running the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}HomelabWiki Setup Script${NC}"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp config/env/.env.example .env
    echo -e "${YELLOW}Please edit .env file with your configuration before continuing.${NC}"
    echo -e "${YELLOW}Pay special attention to LDAP settings and SECRET_KEY.${NC}"
    read -p "Press Enter to continue after editing .env file..."
fi

# Create necessary directories
echo -e "${GREEN}Creating necessary directories...${NC}"
mkdir -p data/database
mkdir -p data/uploads
mkdir -p data/backups
mkdir -p logs

# Set proper permissions
echo -e "${GREEN}Setting permissions...${NC}"
chmod 755 data/database
chmod 755 data/uploads
chmod 755 data/backups
chmod 755 logs

# Build and start containers
echo -e "${GREEN}Building and starting containers...${NC}"
docker-compose build
docker-compose up -d

echo -e "${GREEN}Waiting for services to start...${NC}"
sleep 10

# Check if services are running
echo -e "${GREEN}Checking service status...${NC}"
docker-compose ps

# Display connection information
echo ""
echo -e "${GREEN}HomelabWiki is now running!${NC}"
echo "=================================="
echo -e "Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "Backend API: ${GREEN}http://localhost:5000${NC}"
echo -e "Health Check: ${GREEN}http://localhost:5000/health${NC}"
echo ""
echo -e "${YELLOW}To view logs:${NC}"
echo "docker-compose logs -f"
echo ""
echo -e "${YELLOW}To stop the application:${NC}"
echo "docker-compose down"
echo ""
echo -e "${YELLOW}To update the application:${NC}"
echo "docker-compose pull && docker-compose up -d --build"
echo ""

# Test backend health
echo -e "${GREEN}Testing backend health...${NC}"
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo -e "${GREEN}Backend is healthy!${NC}"
else
    echo -e "${RED}Backend health check failed. Check logs with: docker-compose logs backend${NC}"
fi

echo ""
echo -e "${GREEN}Setup complete!${NC}"
echo -e "${YELLOW}Don't forget to:${NC}"
echo "1. Configure your LDAP/AD settings in .env"
echo "2. Set up AD security groups (WikiAdmins, WikiUsers, WikiReadOnly)"
echo "3. Create a service account for LDAP binding"
echo "4. Configure SSL certificates if needed"
