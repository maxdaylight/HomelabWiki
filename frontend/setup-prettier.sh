#!/bin/bash

# HomelabWiki Frontend - Prettier Setup Script
# This script sets up Prettier for the frontend development environment

echo "🎨 Setting up Prettier for HomelabWiki Frontend..."

# Check if we're in the correct directory
if [[ ! -f "package.json" ]]; then
    echo "❌ Error: package.json not found. Please run this script from the frontend directory."
    exit 1
fi

# Check if Node.js and npm are installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed. Please install npm first."
    exit 1
fi

echo "📦 Installing dependencies..."
npm install

echo "🔧 Running Prettier on existing code..."
npm run format

echo "✅ Prettier setup complete!"
echo ""
echo "Available commands:"
echo "  npm run format       - Format all source files"
echo "  npm run format:check - Check formatting without changes"
echo "  npm run format:all   - Format all files in project"
echo "  npm run lint:fix     - Run ESLint and Prettier together"
echo ""
echo "📝 For VS Code integration:"
echo "  1. Install 'Prettier - Code formatter' extension"
echo "  2. Install 'Vue - Official' extension"
echo "  3. Workspace settings are already configured!"
echo ""
echo "🚀 Happy coding!"
