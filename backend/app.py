#!/usr/bin/env python3
"""
Flask application entry point for HomelabWiki.
This file is used by gunicorn and other WSGI servers.
"""

from app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    app.run()
