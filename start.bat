@echo off
REM HomelabWiki Startup Script for Windows
REM This script helps with initial setup and running the application

echo HomelabWiki Setup Script
echo ==================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy config\env\.env.example .env
    echo Please edit .env file with your configuration before continuing.
    echo Pay special attention to LDAP settings and SECRET_KEY.
    pause
)

REM Create necessary directories
echo Creating necessary directories...
if not exist data\database mkdir data\database
if not exist data\uploads mkdir data\uploads
if not exist data\backups mkdir data\backups
if not exist logs mkdir logs

REM Build and start containers
echo Building and starting containers...
docker-compose build
docker-compose up -d

echo Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are running
echo Checking service status...
docker-compose ps

REM Display connection information
echo.
echo HomelabWiki is now running!
echo ==================================
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:5000
echo Health Check: http://localhost:5000/health
echo.
echo To view logs:
echo docker-compose logs -f
echo.
echo To stop the application:
echo docker-compose down
echo.
echo To update the application:
echo docker-compose pull && docker-compose up -d --build
echo.

REM Test backend health
echo Testing backend health...
curl -f http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo Backend is healthy!
) else (
    echo Backend health check failed. Check logs with: docker-compose logs backend
)

echo.
echo Setup complete!
echo Don't forget to:
echo 1. Configure your LDAP/AD settings in .env
echo 2. Set up AD security groups (WikiAdmins, WikiUsers, WikiReadOnly)
echo 3. Create a service account for LDAP binding
echo 4. Configure SSL certificates if needed

pause
