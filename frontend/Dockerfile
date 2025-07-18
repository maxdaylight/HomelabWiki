# HomelabWiki Frontend Dockerfile
# Multi-stage build for optimized production image with minimal vulnerabilities

# Build stage using Node.js 22 LTS Alpine for minimal attack surface
FROM node:22-alpine as builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (production only, no dev dependencies)
RUN npm ci --only=production --no-audit --no-fund --no-optional

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage - using minimal Alpine with Nginx
FROM nginx:1.27-alpine

# Add security labels
LABEL maintainer="HomelabWiki" \
    security.scan="enabled" \
    security.non-root="true" \
    security.alpine="true"

# Install security updates and create non-root user
RUN apk upgrade --no-cache \
    && apk add --no-cache curl \
    && addgroup -g 1001 -S nginx-user \
    && adduser -u 1001 -D -S -G nginx-user nginx-user

# Copy built application from builder
COPY --from=builder --chown=nginx-user:nginx-user /app/dist /usr/share/nginx/html

# Copy custom nginx configuration for non-root operation
COPY nginx-nonroot.conf /etc/nginx/nginx.conf

# Create temporary directories for nginx non-root operation
RUN mkdir -p /tmp/client_temp /tmp/proxy_temp_path /tmp/fastcgi_temp /tmp/uwsgi_temp /tmp/scgi_temp \
    && chown -R nginx-user:nginx-user /tmp/client_temp /tmp/proxy_temp_path /tmp/fastcgi_temp /tmp/uwsgi_temp /tmp/scgi_temp \
    && chown -R nginx-user:nginx-user /var/cache/nginx \
    && chown -R nginx-user:nginx-user /usr/share/nginx/html \
    && chmod -R 755 /usr/share/nginx/html

# Switch to non-root user
USER nginx-user

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Start nginx (run on port 8080 as non-root user)
CMD ["nginx", "-g", "daemon off;"]