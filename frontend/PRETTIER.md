# Prettier Setup Guide for HomelabWiki Frontend

## Overview

This guide explains the Prettier configuration for the HomelabWiki frontend project. Prettier is set up to ensure consistent code formatting across the entire Vue.js application.

## Configuration Files

### `.prettierrc`
Main Prettier configuration file with Vue.js-optimized settings:

```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "none",
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "avoid",
  "endOfLine": "lf",
  "bracketSameLine": false,
  "singleAttributePerLine": false,
  "vueIndentScriptAndStyle": false,
  "embeddedLanguageFormatting": "auto",
  "plugins": ["prettier-plugin-vue"]
}
```

### `.prettierignore`
Files and directories that should not be formatted:

- Build output (`dist/`, `build/`)
- Dependencies (`node_modules/`)
- Generated files (`*.min.js`, `*.min.css`)
- Configuration files (`nginx*.conf`, `vite.config.js`)
- IDE files (`.vscode/`, `.idea/`)

## Package.json Scripts

The following scripts are available for code formatting:

```json
{
  "scripts": {
    "format": "prettier --write \"src/**/*.{vue,js,jsx,ts,tsx,json,css,scss,md}\"",
    "format:check": "prettier --check \"src/**/*.{vue,js,jsx,ts,tsx,json,css,scss,md}\"",
    "format:all": "prettier --write \"**/*.{vue,js,jsx,ts,tsx,json,css,scss,md}\"",
    "lint:fix": "eslint . --ext .vue,.js,.jsx,.ts,.tsx --fix && npm run format"
  }
}
```

## Usage

### Command Line

```bash
# Format all source files
npm run format

# Check formatting without making changes
npm run format:check

# Format all files in the project (including docs, config, etc.)
npm run format:all

# Run ESLint and Prettier together
npm run lint:fix
```

### VS Code Integration

The project includes VS Code workspace settings (`.vscode/settings.json`) that automatically:

- Format files on save
- Use Prettier as the default formatter for all supported file types
- Integrate with ESLint for comprehensive code quality

#### Required Extensions

1. **Prettier - Code formatter** (`esbenp.prettier-vscode`)
2. **Vue - Official** (`Vue.volar`) or **Vetur** (`octref.vetur`)
3. **ESLint** (`dbaeumer.vscode-eslint`)

#### Manual VS Code Configuration

If you need to configure VS Code manually, add these settings to your `settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "prettier.configPath": "./frontend/.prettierrc",
  "prettier.ignorePath": "./frontend/.prettierignore",
  "prettier.requireConfig": true,
  "prettier.useEditorConfig": false,
  "[vue]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## Code Style Guidelines

### Vue.js Files

```vue
<template>
  <div class="example-component">
    <h1>{{ title }}</h1>
    <button @click="handleClick">Click me</button>
  </div>
</template>

<script>
export default {
  name: 'ExampleComponent',
  data() {
    return {
      title: 'Hello World'
    }
  },
  methods: {
    handleClick() {
      console.log('Button clicked!')
    }
  }
}
</script>

<style scoped>
.example-component {
  padding: 1rem;
}
</style>
```

### JavaScript/TypeScript Files

```javascript
// Use single quotes
const message = 'Hello, World!'

// No semicolons
const calculate = (a, b) => a + b

// Arrow functions without parentheses for single parameters
const double = x => x * 2

// Object spacing
const config = { 
  apiUrl: 'https://api.example.com',
  timeout: 5000 
}

// No trailing commas
const items = [
  'item1',
  'item2',
  'item3'
]
```

### SCSS/CSS Files

```scss
.component {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  
  &__title {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  
  &__content {
    flex: 1;
    overflow-y: auto;
  }
}
```

## Docker Integration

The Prettier configuration is used during the Docker build process:

```dockerfile
# In the frontend Dockerfile
FROM node:20-alpine3.21 as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production --no-audit --no-fund --no-optional

COPY . .
RUN npm run build
```

## CI/CD Integration

For continuous integration, you can add format checking to your pipeline:

```yaml
# Example GitHub Actions workflow
- name: Check code formatting
  run: |
    cd frontend
    npm ci
    npm run format:check
    npm run lint
```

## Troubleshooting

### Common Issues

1. **Prettier not formatting on save**
   - Ensure the Prettier extension is installed and enabled
   - Check that `prettier.requireConfig` is set to `true`
   - Verify the config path is correct

2. **Conflicting formatting between ESLint and Prettier**
   - The project uses `@vue/eslint-config-prettier` to disable conflicting rules
   - Run `npm run lint:fix` to apply both ESLint and Prettier fixes

3. **Files not being formatted**
   - Check if the file type is included in the `.prettierrc` plugins
   - Verify the file is not listed in `.prettierignore`

### Debug Commands

```bash
# Check Prettier configuration
npx prettier --help config

# Test formatting on a specific file
npx prettier --write src/App.vue

# Check if a file would be formatted
npx prettier --check src/App.vue
```

## Best Practices

1. **Always run format before committing**
   ```bash
   npm run lint:fix
   ```

2. **Use the VS Code extension for real-time formatting**
   - Install the Prettier extension
   - Enable format on save

3. **Keep the configuration simple**
   - Only override defaults when necessary
   - Document any non-standard settings

4. **Use consistent formatting in the entire project**
   - Apply the same rules to all file types
   - Use the same configuration across the team

## Setup Scripts

The project includes setup scripts for easy Prettier configuration:

- **Linux/macOS**: `setup-prettier.sh`
- **Windows**: `setup-prettier.bat`

These scripts will:
1. Install dependencies
2. Run initial formatting
3. Provide usage instructions

## Contributing

When contributing to the project:

1. Ensure your code follows the Prettier configuration
2. Run `npm run lint:fix` before committing
3. Use the provided VS Code settings for consistency
4. Update this documentation if you modify the Prettier configuration

## Related Documentation

- [Vue.js Style Guide](https://vuejs.org/style-guide/)
- [Prettier Configuration](https://prettier.io/docs/en/configuration.html)
- [ESLint Vue Plugin](https://eslint.vuejs.org/)
- [VS Code Prettier Extension](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
