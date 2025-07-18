@echo off
REM HomelabWiki Frontend - Prettier Setup Script (Windows)
REM This script sets up Prettier for the frontend development environment

echo 🎨 Setting up Prettier for HomelabWiki Frontend...

REM Check if we're in the correct directory
if not exist "package.json" (
    echo ❌ Error: package.json not found. Please run this script from the frontend directory.
    exit /b 1
)

REM Check if Node.js and npm are installed
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Node.js is not installed. Please install Node.js 18+ first.
    exit /b 1
)

where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: npm is not installed. Please install npm first.
    exit /b 1
)

echo 📦 Installing dependencies...
npm install

echo 🔧 Running Prettier on existing code...
npm run format

echo ✅ Prettier setup complete!
echo.
echo Available commands:
echo   npm run format       - Format all source files
echo   npm run format:check - Check formatting without changes
echo   npm run format:all   - Format all files in project
echo   npm run lint:fix     - Run ESLint and Prettier together
echo.
echo 📝 For VS Code integration:
echo   1. Install 'Prettier - Code formatter' extension
echo   2. Install 'Vue - Official' extension
echo   3. Workspace settings are already configured!
echo.
echo 🚀 Happy coding!

pause
