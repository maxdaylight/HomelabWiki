#!/bin/bash

# HomelabWiki Security Validation Script
# This script validates that your HomelabWiki deployment follows security best practices

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Security check functions
print_status() {
    if [ "$1" = "OK" ]; then
        echo -e "${GREEN}✅ $2${NC}"
    elif [ "$1" = "WARN" ]; then
        echo -e "${YELLOW}⚠️  $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

print_header() {
    echo -e "\n${GREEN}=== $1 ===${NC}"
}

check_env_file() {
    print_header "Environment File Security"
    
    if [ ! -f .env ]; then
        print_status "FAIL" ".env file not found. Copy from config/env/.env.example"
        return 1
    fi
    
    print_status "OK" ".env file exists"
    
    # Check file permissions
    if [ "$(stat -c %a .env 2>/dev/null)" = "600" ]; then
        print_status "OK" ".env file has secure permissions (600)"
    else
        print_status "WARN" ".env file permissions should be 600 (current: $(stat -c %a .env 2>/dev/null || echo 'unknown'))"
    fi
}

check_secret_key() {
    print_header "Secret Key Security"
    
    if ! grep -q "^SECRET_KEY=" .env; then
        print_status "FAIL" "SECRET_KEY not found in .env"
        return 1
    fi
    
    SECRET_KEY=$(grep "^SECRET_KEY=" .env | cut -d'=' -f2)
    
    if [ "$SECRET_KEY" = "REPLACE_WITH_SECURE_32_CHAR_SECRET_KEY" ]; then
        print_status "FAIL" "SECRET_KEY still contains placeholder value"
        return 1
    fi
    
    if [ ${#SECRET_KEY} -lt 32 ]; then
        print_status "FAIL" "SECRET_KEY is too short (${#SECRET_KEY} characters, minimum 32)"
        return 1
    fi
    
    print_status "OK" "SECRET_KEY is properly configured (${#SECRET_KEY} characters)"
}

check_ldap_password() {
    print_header "LDAP Password Security"
    
    if ! grep -q "^LDAP_BIND_PASSWORD=" .env; then
        print_status "FAIL" "LDAP_BIND_PASSWORD not found in .env"
        return 1
    fi
    
    LDAP_PASSWORD=$(grep "^LDAP_BIND_PASSWORD=" .env | cut -d'=' -f2)
    
    if [ "$LDAP_PASSWORD" = "REPLACE_WITH_ACTUAL_LDAP_PASSWORD" ]; then
        print_status "FAIL" "LDAP_BIND_PASSWORD still contains placeholder value"
        return 1
    fi
    
    if [ ${#LDAP_PASSWORD} -lt 8 ]; then
        print_status "WARN" "LDAP_BIND_PASSWORD is shorter than 8 characters"
    else
        print_status "OK" "LDAP_BIND_PASSWORD is configured"
    fi
}

check_database_password() {
    print_header "Database Password Security"
    
    if grep -q "^POSTGRES_PASSWORD=" .env; then
        POSTGRES_PASSWORD=$(grep "^POSTGRES_PASSWORD=" .env | cut -d'=' -f2)
        
        if [ "$POSTGRES_PASSWORD" = "REPLACE_WITH_SECURE_DB_PASSWORD" ]; then
            print_status "FAIL" "POSTGRES_PASSWORD still contains placeholder value"
            return 1
        fi
        
        if [ ${#POSTGRES_PASSWORD} -lt 8 ]; then
            print_status "WARN" "POSTGRES_PASSWORD is shorter than 8 characters"
        else
            print_status "OK" "POSTGRES_PASSWORD is configured"
        fi
    else
        print_status "OK" "Using SQLite (no PostgreSQL password required)"
    fi
}

check_docker_compose() {
    print_header "Docker Compose Security"
    
    if [ ! -f docker-compose.yml ]; then
        print_status "FAIL" "docker-compose.yml not found"
        return 1
    fi
    
    # Check for hardcoded passwords
    if grep -q "WikiService123!" docker-compose.yml; then
        print_status "FAIL" "Hardcoded password found in docker-compose.yml"
        return 1
    fi
    
    if grep -q "change-this-in-production" docker-compose.yml; then
        print_status "FAIL" "Default secret key found in docker-compose.yml"
        return 1
    fi
    
    if grep -q "wiki_password" docker-compose.yml; then
        print_status "FAIL" "Default database password found in docker-compose.yml"
        return 1
    fi
    
    print_status "OK" "No hardcoded credentials found in docker-compose.yml"
}

check_gitignore() {
    print_header "Git Security"
    
    if [ ! -f .gitignore ]; then
        print_status "WARN" ".gitignore file not found"
        return 1
    fi
    
    if grep -q "^\.env$" .gitignore; then
        print_status "OK" ".env file is properly ignored by git"
    else
        print_status "FAIL" ".env file is NOT ignored by git (security risk!)"
        return 1
    fi
    
    if grep -q "^.*\.env$" .gitignore; then
        print_status "OK" "All .env files are ignored by git"
    else
        print_status "WARN" "Consider adding *.env to .gitignore for additional protection"
    fi
}

check_services() {
    print_header "Service Security"
    
    if command -v docker-compose &> /dev/null; then
        if docker-compose ps | grep -q "Up"; then
            print_status "OK" "Docker services are running"
            
            # Check if health endpoint is accessible
            if curl -s -f http://localhost:5000/health > /dev/null 2>&1; then
                print_status "OK" "Backend health check passed"
            else
                print_status "WARN" "Backend health check failed (service may be starting)"
            fi
        else
            print_status "WARN" "Docker services are not running"
        fi
    else
        print_status "WARN" "docker-compose not found"
    fi
}

generate_recommendations() {
    print_header "Security Recommendations"
    
    echo "1. Regularly rotate credentials (every 90 days)"
    echo "2. Monitor authentication logs for suspicious activity"
    echo "3. Use strong, unique passwords for all services"
    echo "4. Keep .env file permissions at 600"
    echo "5. Never commit .env files to version control"
    echo "6. Use HTTPS in production with reverse proxy"
    echo "7. Regular security audits and updates"
    echo "8. Implement network segmentation"
    echo "9. Configure automated backups"
    echo "10. Set up monitoring and alerting"
}

# Main execution
main() {
    echo -e "${GREEN}HomelabWiki Security Validation${NC}"
    echo "================================="
    
    CHECKS_PASSED=0
    TOTAL_CHECKS=6
    
    # Run all security checks
    if check_env_file; then ((CHECKS_PASSED++)); fi
    if check_secret_key; then ((CHECKS_PASSED++)); fi
    if check_ldap_password; then ((CHECKS_PASSED++)); fi
    if check_database_password; then ((CHECKS_PASSED++)); fi
    if check_docker_compose; then ((CHECKS_PASSED++)); fi
    if check_gitignore; then ((CHECKS_PASSED++)); fi
    
    # Optional service check (doesn't count toward total)
    check_services
    
    # Generate recommendations
    generate_recommendations
    
    # Final summary
    print_header "Security Summary"
    echo -e "Checks passed: ${CHECKS_PASSED}/${TOTAL_CHECKS}"
    
    if [ $CHECKS_PASSED -eq $TOTAL_CHECKS ]; then
        print_status "OK" "All security checks passed! ✨"
        exit 0
    else
        print_status "FAIL" "Some security checks failed. Please review and fix issues above."
        exit 1
    fi
}

# Run main function
main "$@"
