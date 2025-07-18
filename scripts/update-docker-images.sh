#!/bin/bash

# HomelabWiki Docker Image Update Script
# This script helps keep Docker base images updated to address security vulnerabilities

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Default options
DRY_RUN=false
FORCE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--dry-run] [--force] [--help]"
            echo "  --dry-run    Show what would be changed without making changes"
            echo "  --force      Force update even if images are already latest"
            echo "  --help       Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}HomelabWiki Docker Image Update Script${NC}"
echo -e "${GREEN}=====================================${NC}"

# Function to check if Docker is available
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker is not installed or not in PATH${NC}"
        exit 1
    fi
    
    if ! docker version &> /dev/null; then
        echo -e "${RED}Docker is not running or not accessible${NC}"
        exit 1
    fi
}

# Function to get latest stable versions
get_latest_versions() {
    # These should be updated regularly
    PYTHON_VERSION="3.12"
    NODE_VERSION="20"
    NGINX_VERSION="1.26"
}

# Function to update Dockerfile
update_dockerfile() {
    local filepath="$1"
    local base_image="$2"
    local new_version="$3"
    
    if [[ ! -f "$filepath" ]]; then
        echo -e "${YELLOW}Warning: Dockerfile not found: $filepath${NC}"
        return
    fi
    
    local old_pattern="FROM ${base_image}:[0-9]+(\.[0-9]+)*(-[a-zA-Z0-9]+)*"
    local new_image="FROM ${base_image}:${new_version}"
    
    if grep -qE "$old_pattern" "$filepath"; then
        local old_image=$(grep -E "$old_pattern" "$filepath" | head -1)
        echo -e "${YELLOW}Updating $filepath${NC}"
        echo -e "  ${RED}Old: $old_image${NC}"
        echo -e "  ${GREEN}New: $new_image${NC}"
        
        if [[ "$DRY_RUN" == "false" ]]; then
            sed -i.bak -E "s|$old_pattern|$new_image|g" "$filepath"
            echo -e "  ${GREEN}Updated!${NC}"
        else
            echo -e "  ${YELLOW}(Dry run - no changes made)${NC}"
        fi
    else
        echo -e "${YELLOW}No matching pattern found in $filepath${NC}"
    fi
}

# Function to run security scan
run_security_scan() {
    local image_name="$1"
    
    if command -v docker &> /dev/null; then
        echo -e "${YELLOW}Running security scan for $image_name...${NC}"
        if docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
            -v "$(pwd):/app" aquasec/trivy image "$image_name" 2>/dev/null; then
            echo -e "${GREEN}Security scan completed for $image_name${NC}"
        else
            echo -e "${YELLOW}Warning: Security scan failed for $image_name${NC}"
        fi
    else
        echo -e "${YELLOW}Warning: Docker not available for security scanning${NC}"
    fi
}

# Main execution
check_docker

echo -e "${CYAN}Checking for Docker image updates...${NC}"

get_latest_versions

BACKEND_DOCKERFILE="backend/Dockerfile"
FRONTEND_DOCKERFILE="frontend/Dockerfile"

# Update backend Dockerfile
if [[ -f "$BACKEND_DOCKERFILE" ]]; then
    update_dockerfile "$BACKEND_DOCKERFILE" "python" "${PYTHON_VERSION}-slim"
else
    echo -e "${YELLOW}Warning: Backend Dockerfile not found${NC}"
fi

# Update frontend Dockerfile
if [[ -f "$FRONTEND_DOCKERFILE" ]]; then
    update_dockerfile "$FRONTEND_DOCKERFILE" "node" "${NODE_VERSION}-alpine"
    update_dockerfile "$FRONTEND_DOCKERFILE" "nginx" "${NGINX_VERSION}-alpine"
else
    echo -e "${YELLOW}Warning: Frontend Dockerfile not found${NC}"
fi

if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "\n${YELLOW}Dry run completed. No changes were made.${NC}"
    echo -e "${YELLOW}Run without --dry-run to apply changes.${NC}"
else
    echo -e "\n${GREEN}Docker images updated successfully!${NC}"
    echo -e "${CYAN}Remember to rebuild your containers:${NC}"
    echo -e "${WHITE}  docker-compose build${NC}"
    echo -e "${WHITE}  docker-compose up -d${NC}"
fi

echo -e "\n${CYAN}Security recommendations:${NC}"
echo -e "${WHITE}1. Run security scans regularly${NC}"
echo -e "${WHITE}2. Keep base images updated${NC}"
echo -e "${WHITE}3. Use specific version tags (avoid 'latest')${NC}"
echo -e "${WHITE}4. Review and update dependencies${NC}"

# Make script executable
chmod +x "$0" 2>/dev/null || true
