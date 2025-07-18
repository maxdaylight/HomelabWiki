"""
Authentication API endpoints for HomelabWiki.
"""

from flask import request, jsonify, session
from flask_login import login_required, current_user
from app.api import bp
from app.auth.ldap_auth import login_user_with_ldap, logout_current_user, test_ldap_connection

@bp.route('/auth/login', methods=['POST'])
def login():
    """Login endpoint."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Strip domain prefix if present (e.g., wyk\aegis -> aegis)
        if '\\' in username:
            username = username.split('\\')[1]
        
        success, message = login_user_with_ldap(username, password)
        
        if success:
            return jsonify({
                'message': message,
                'user': current_user.to_dict()
            }), 200
        else:
            return jsonify({'error': message}), 401
            
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

@bp.route('/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout endpoint."""
    try:
        success, message = logout_current_user()
        return jsonify({'message': message}), 200
    except Exception as e:
        return jsonify({'error': 'Logout failed'}), 500

@bp.route('/auth/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current user information."""
    try:
        return jsonify({'user': current_user.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get user info'}), 500

@bp.route('/auth/test-ldap', methods=['POST'])
def test_ldap():
    """Test LDAP connection."""
    try:
        if test_ldap_connection():
            return jsonify({'message': 'LDAP connection successful'}), 200
        else:
            return jsonify({'error': 'LDAP connection failed'}), 500
    except Exception as e:
        return jsonify({'error': 'LDAP test failed'}), 500

@bp.route('/auth/check', methods=['GET'])
def check_auth():
    """Check authentication status."""
    try:
        if current_user.is_authenticated:
            return jsonify({
                'authenticated': True,
                'user': current_user.to_dict()
            }), 200
        else:
            return jsonify({'authenticated': False}), 200
    except Exception as e:
        return jsonify({'error': 'Authentication check failed'}), 500