# HomelabWiki Frontend

A modern Vue.js 3 frontend for HomelabWiki - a comprehensive self-hosted Knowledge Base application.

## Features

- **Modern Vue.js 3** with Composition API
- **Responsive Design** with mobile-first approach
- **Rich Markdown Editor** with live preview
- **File Upload & Management** with drag-and-drop support
- **Full-text Search** across all content
- **LDAP Authentication** integration
- **Export Capabilities** (PDF and Markdown)
- **Dark/Light Theme** support

## Development Setup

### Prerequisites

- Node.js 18+ and npm
- Docker (for containerized development)

### Local Development

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Open browser at `http://localhost:5173`

### Docker Development

```bash
# Build and run with docker-compose
docker-compose -f docker-compose.dev.yml up --build
```

## Code Quality & Formatting

This project uses **Prettier** for code formatting and **ESLint** for linting.

### Prettier Configuration

The project includes a comprehensive Prettier setup with Vue.js optimizations:

- **Semi-colons**: Disabled for cleaner code
- **Single quotes**: Preferred for consistency
- **Tab width**: 2 spaces
- **Print width**: 100 characters
- **Vue.js support**: Enhanced with prettier-plugin-vue

### Available Scripts

```bash
# Format all source files
npm run format

# Check formatting without making changes
npm run format:check

# Format all files in the project
npm run format:all

# Run linting with auto-fix
npm run lint

# Run both linting and formatting
npm run lint:fix
```

### VS Code Integration

For the best development experience, install these VS Code extensions:

1. **Prettier - Code formatter** (`esbenp.prettier-vscode`)
2. **Vetur** or **Vue - Official** (`vue.volar`)
3. **ESLint** (`dbaeumer.vscode-eslint`)

#### VS Code Settings

Add these settings to your VS Code settings.json:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "[vue]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### Git Hooks (Optional)

To ensure code quality, you can set up pre-commit hooks:

```bash
# Install husky for git hooks
npm install --save-dev husky lint-staged

# Add to package.json
"lint-staged": {
  "*.{vue,js,jsx,ts,tsx}": [
    "eslint --fix",
    "prettier --write"
  ]
}
```

## Build Process

### Development Build
```bash
npm run dev
```

### Production Build
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## Docker Production

The frontend uses a multi-stage Docker build for optimal security and performance:

- **Builder stage**: Node.js 20 Alpine for building
- **Runtime stage**: Nginx Alpine for serving static files
- **Security**: Runs as non-root user with minimal attack surface
- **Health checks**: Built-in health monitoring

## Project Structure

```
src/
├── components/          # Reusable Vue components
├── views/              # Page components
├── services/           # API and authentication services
├── stores/             # Pinia state management
├── styles/             # Global styles and themes
├── router.js           # Vue Router configuration
├── main.js             # Application entry point
└── App.vue             # Root component
```

## Security Features

- **Non-root container** execution
- **Minimal base images** (Alpine Linux)
- **Security headers** via Nginx configuration
- **Content Security Policy** implementation
- **Input validation** and sanitization
- **HTTPS enforcement** in production

## Contributing

1. Follow the existing code style
2. Run `npm run lint:fix` before committing
3. Ensure all tests pass
4. Update documentation as needed

## Technology Stack

- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Fast build tool and dev server
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Axios** - HTTP client
- **Marked** - Markdown parsing
- **PrismJS** - Syntax highlighting
- **Sass** - CSS preprocessing
- **Prettier** - Code formatting
- **ESLint** - Code linting

## License

MIT - See LICENSE file for details