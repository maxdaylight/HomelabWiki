# HomelabWiki Backend Dockerfile
# Multi-stage build for optimized production image with minimal vulnerabilities

# Build stage using Alpine for minimal attack surface
FROM python:3.13-alpine3.21 AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    openssl-dev \
    openldap-dev \
    cyrus-sasl-dev \
    python3-dev \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    make \
    pkgconfig \
    libwebp-dev \
    libxcb-dev \
    libffi-dev \
    && apk add --no-cache \
    libmagic \
    curl \
    libldap \
    libsasl \
    libpq \
    jpeg \
    zlib \
    freetype \
    lcms2 \
    openjpeg \
    tiff \
    libwebp \
    libxcb

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Clean up build dependencies
RUN apk del .build-deps

# Production stage - using minimal Alpine with only runtime dependencies
FROM python:3.13-alpine3.21

# Add security labels
LABEL maintainer="HomelabWiki" \
    security.scan="enabled" \
    security.non-root="true" \
    security.alpine="true"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app
ENV FLASK_ENV=production

# Install only runtime dependencies (no dev packages)
RUN apk add --no-cache \
    libldap \
    libsasl \
    libssl3 \
    libmagic \
    libpq \
    jpeg \
    zlib \
    freetype \
    lcms2 \
    openjpeg \
    tiff \
    libwebp \
    libxcb \
    curl \
    ca-certificates \
    && apk upgrade --no-cache \
    && addgroup -g 1001 -S appuser \
    && adduser -u 1001 -D -S -G appuser appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p /app/uploads /app/backups /app/logs \
    && chown -R appuser:appuser /app \
    && chmod -R 750 /app \
    && chmod -R 755 /app/uploads

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--worker-class", "gevent", "--timeout", "120", "app:create_app()"]