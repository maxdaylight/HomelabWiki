"""
LDAP/Active Directory authentication for HomelabWiki.
Handles user authentication and group membership validation.
"""

import ldap
import ldap.filter
from flask import current_app, session
from flask_login import login_user, logout_user
from app import db
from app.models.user import User
import logging

logger = logging.getLogger(__name__)

class LDAPAuthenticator:
    """LDAP authentication handler."""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize LDAP configuration."""
        self.server = app.config.get('LDAP_SERVER', 'WYK-DC01')
        self.port = app.config.get('LDAP_PORT', 389)
        self.use_ssl = app.config.get('LDAP_USE_SSL', False)
        self.use_tls = app.config.get('LDAP_USE_TLS', True)
        self.base_dn = app.config.get('LDAP_BASE_DN', 'DC=homelab,DC=local')
        self.bind_dn = app.config.get('LDAP_BIND_DN')
        self.bind_password = app.config.get('LDAP_BIND_PASSWORD')
        self.user_search_base = app.config.get('LDAP_USER_SEARCH_BASE', 'CN=Users,DC=homelab,DC=local')
        self.group_search_base = app.config.get('LDAP_GROUP_SEARCH_BASE', 'CN=Groups,DC=homelab,DC=local')
        self.username_attribute = app.config.get('LDAP_USERNAME_ATTRIBUTE', 'sAMAccountName')
        self.email_attribute = app.config.get('LDAP_EMAIL_ATTRIBUTE', 'mail')
        self.firstname_attribute = app.config.get('LDAP_FIRSTNAME_ATTRIBUTE', 'givenName')
        self.lastname_attribute = app.config.get('LDAP_LASTNAME_ATTRIBUTE', 'sn')
    
    def _get_ldap_connection(self):
        """Create LDAP connection."""
        protocol = 'ldaps' if self.use_ssl else 'ldap'
        ldap_url = f"{protocol}://{self.server}:{self.port}"
        
        try:
            connection = ldap.initialize(ldap_url)
            connection.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            connection.set_option(ldap.OPT_REFERRALS, 0)
            
            if self.use_tls and not self.use_ssl:
                connection.start_tls_s()
            
            return connection
        except ldap.LDAPError as e:
            logger.error(f"Failed to create LDAP connection: {e}")
            raise
    
    def _bind_service_account(self, connection):
        """Bind with service account."""
        try:
            if self.bind_dn and self.bind_password:
                connection.simple_bind_s(self.bind_dn, self.bind_password)
            else:
                connection.simple_bind_s()  # Anonymous bind
        except ldap.INVALID_CREDENTIALS:
            logger.error("Invalid service account credentials")
            raise
        except ldap.LDAPError as e:
            logger.error(f"Failed to bind service account: {e}")
            raise
    
    def _search_user(self, connection, username):
        """Search for user in LDAP."""
        search_filter = f"({self.username_attribute}={ldap.filter.escape_filter_chars(username)})"
        
        try:
            result = connection.search_s(
                self.user_search_base,
                ldap.SCOPE_SUBTREE,
                search_filter,
                [self.username_attribute, self.email_attribute, 
                 self.firstname_attribute, self.lastname_attribute, 'memberOf']
            )
            
            if result:
                return result[0]  # Return first match
            return None
        except ldap.LDAPError as e:
            logger.error(f"Failed to search user {username}: {e}")
            raise
    
    def _get_user_groups(self, connection, user_dn):
        """Get user's group memberships."""
        try:
            # Search for groups where user is a member
            search_filter = f"(member={ldap.filter.escape_filter_chars(user_dn)})"
            
            result = connection.search_s(
                self.group_search_base,
                ldap.SCOPE_SUBTREE,
                search_filter,
                ['cn', 'description']
            )
            
            groups = []
            for group_dn, group_attrs in result:
                if 'cn' in group_attrs:
                    groups.append(group_attrs['cn'][0].decode('utf-8'))
            
            return groups
        except ldap.LDAPError as e:
            logger.error(f"Failed to get user groups: {e}")
            return []
    
    def _extract_user_data(self, user_dn, user_attrs):
        """Extract user data from LDAP attributes."""
        def get_attr_value(attr_name):
            """Get attribute value safely."""
            if attr_name in user_attrs and user_attrs[attr_name]:
                return user_attrs[attr_name][0].decode('utf-8')
            return None
        
        username = get_attr_value(self.username_attribute)
        email = get_attr_value(self.email_attribute)
        first_name = get_attr_value(self.firstname_attribute)
        last_name = get_attr_value(self.lastname_attribute)
        
        # Extract domain from DN
        domain = None
        if user_dn:
            dn_parts = user_dn.split(',')
            dc_parts = [part.strip() for part in dn_parts if part.strip().startswith('DC=')]
            if dc_parts:
                domain = '.'.join([part.split('=')[1] for part in dc_parts])
        
        return {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'dn': user_dn,
            'domain': domain
        }
    
    def authenticate(self, username, password):
        """Authenticate user against LDAP."""
        if not username or not password:
            return None
        
        connection = None
        try:
            # Create connection and bind service account
            connection = self._get_ldap_connection()
            self._bind_service_account(connection)
            
            # Search for user
            user_result = self._search_user(connection, username)
            if not user_result:
                logger.warning(f"User {username} not found in LDAP")
                return None
            
            user_dn, user_attrs = user_result
            
            # Try to bind with user credentials
            user_connection = self._get_ldap_connection()
            try:
                user_connection.simple_bind_s(user_dn, password)
            except ldap.INVALID_CREDENTIALS:
                logger.warning(f"Invalid credentials for user {username}")
                return None
            finally:
                user_connection.unbind_s()
            
            # Extract user data
            user_data = self._extract_user_data(user_dn, user_attrs)
            
            # Get user groups
            groups = self._get_user_groups(connection, user_dn)
            user_data['groups'] = groups
            
            logger.info(f"User {username} authenticated successfully")
            return user_data
            
        except ldap.LDAPError as e:
            logger.error(f"LDAP authentication failed for {username}: {e}")
            return None
        finally:
            if connection:
                connection.unbind_s()
    
    def test_connection(self):
        """Test LDAP connection."""
        try:
            connection = self._get_ldap_connection()
            self._bind_service_account(connection)
            connection.unbind_s()
            return True
        except Exception as e:
            logger.error(f"LDAP connection test failed: {e}")
            return False

# Global authenticator instance
ldap_auth = LDAPAuthenticator()

def login_user_with_ldap(username, password):
    """Login user with LDAP authentication."""
    try:
        # Authenticate with LDAP
        ldap_user_data = ldap_auth.authenticate(username, password)
        if not ldap_user_data:
            return False, "Invalid username or password"
        
        # Check if user exists in database
        user = User.query.filter_by(username=username).first()
        
        if user:
            # Update existing user from LDAP
            user.update_from_ldap(ldap_user_data)
            user.update_last_login()
        else:
            # Create new user from LDAP
            user = User.create_from_ldap(ldap_user_data)
            db.session.add(user)
        
        db.session.commit()
        
        # Login user
        login_user(user, remember=True)
        logger.info(f"User {username} logged in successfully")
        
        return True, "Login successful"
        
    except Exception as e:
        logger.error(f"Login failed for {username}: {e}")
        db.session.rollback()
        return False, "Login failed due to server error"

def logout_current_user():
    """Logout current user."""
    try:
        logout_user()
        session.clear()
        return True, "Logout successful"
    except Exception as e:
        logger.error(f"Logout failed: {e}")
        return False, "Logout failed"

def test_ldap_connection():
    """Test LDAP connection."""
    try:
        return ldap_auth.test_connection()
    except Exception as e:
        logger.error(f"LDAP connection test failed: {e}")
        return False

def get_ldap_user_info(username):
    """Get user information from LDAP without authentication."""
    connection = None
    try:
        connection = ldap_auth._get_ldap_connection()
        ldap_auth._bind_service_account(connection)
        
        user_result = ldap_auth._search_user(connection, username)
        if not user_result:
            return None
        
        user_dn, user_attrs = user_result
        user_data = ldap_auth._extract_user_data(user_dn, user_attrs)
        
        # Get user groups
        groups = ldap_auth._get_user_groups(connection, user_dn)
        user_data['groups'] = groups
        
        return user_data
        
    except Exception as e:
        logger.error(f"Failed to get LDAP user info for {username}: {e}")
        return None
    finally:
        if connection:
            connection.unbind_s()

def sync_user_from_ldap(username):
    """Sync user data from LDAP."""
    try:
        ldap_user_data = get_ldap_user_info(username)
        if not ldap_user_data:
            return False, "User not found in LDAP"
        
        user = User.query.filter_by(username=username).first()
        if user:
            user.update_from_ldap(ldap_user_data)
            db.session.commit()
            return True, "User synchronized successfully"
        else:
            return False, "User not found in database"
            
    except Exception as e:
        logger.error(f"Failed to sync user {username}: {e}")
        db.session.rollback()
        return False, "Synchronization failed"