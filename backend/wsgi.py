#!/usr/bin/env python3
"""
Main entry point for HomelabWiki Flask application.
"""

import os
from app import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Development server
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )
