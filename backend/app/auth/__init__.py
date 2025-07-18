"""
Authentication module for HomelabWiki.
Handles LDAP/Active Directory authentication.
"""

from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import ldap_auth
