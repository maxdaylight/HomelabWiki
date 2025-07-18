"""
API module for HomelabWiki.
RESTful API endpoints for the application.
"""

from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import auth, pages, files, search
