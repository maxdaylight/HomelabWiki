#!/bin/bash

# Docker Environment Test Script
# This script validates your Docker configuration and credentials

set -e

echo "🐳 Testing HomelabWiki Docker Configuration"
echo "=========================================="

# Test 1: Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "Run: cp config/env/.env.example .env"
    exit 1
fi
echo "✅ .env file found"

# Test 2: Check required environment variables
echo "🔍 Checking required environment variables..."
source .env

if [ -z "$SECRET_KEY" ]; then
    echo "❌ SECRET_KEY not set in .env"
    exit 1
fi
echo "✅ SECRET_KEY is set"

if [ -z "$LDAP_BIND_PASSWORD" ]; then
    echo "❌ LDAP_BIND_PASSWORD not set in .env"
    exit 1
fi
echo "✅ LDAP_BIND_PASSWORD is set"

# Test 3: Check Docker Compose syntax
echo "🔍 Validating docker-compose.yml syntax..."
if docker-compose config > /dev/null 2>&1; then
    echo "✅ docker-compose.yml syntax is valid"
else
    echo "❌ docker-compose.yml syntax error"
    exit 1
fi

# Test 4: Check if Docker is running
echo "🔍 Checking Docker daemon..."
if docker info > /dev/null 2>&1; then
    echo "✅ Docker daemon is running"
else
    echo "❌ Docker daemon is not running"
    exit 1
fi

# Test 5: Test environment variable substitution
echo "🔍 Testing environment variable substitution..."
docker-compose config | grep -q "SECRET_KEY" && echo "✅ Environment variables are being substituted"

# Test 6: Build and start services (optional)
echo "🚀 Starting services for testing..."
docker-compose up -d

echo "⏱️  Waiting for services to start..."
sleep 15

# Test 7: Check service health
echo "🔍 Checking service health..."
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Backend service is healthy"
else
    echo "⚠️  Backend service may still be starting"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend service is accessible"
else
    echo "⚠️  Frontend service may still be starting"
fi

# Test 8: Check logs for errors
echo "🔍 Checking logs for errors..."
if docker-compose logs backend | grep -i error | head -5; then
    echo "⚠️  Found errors in backend logs (check above)"
else
    echo "✅ No errors found in backend logs"
fi

echo ""
echo "🎉 Docker configuration test complete!"
echo "Access your wiki at: http://localhost:3000"
echo "Backend API at: http://localhost:5000"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs: docker-compose logs -f"
