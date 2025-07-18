"""
User model for HomelabWiki application.
Integrates with LDAP/Active Directory for authentication.
"""

from datetime import datetime
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    """User model for LDAP-authenticated users."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    
    # LDAP/AD attributes
    ldap_dn = db.Column(db.String(255), nullable=True)
    domain = db.Column(db.String(50), nullable=True)
    
    # User roles and permissions
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    can_edit = db.Column(db.Boolean, default=True)
    can_create = db.Column(db.Boolean, default=True)
    can_delete = db.Column(db.Boolean, default=False)
    can_upload = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    pages = db.relationship('Page', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    files = db.relationship('File', backref='uploader', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_full_name(self):
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.username
    
    def get_display_name(self):
        """Get display name for UI."""
        full_name = self.get_full_name()
        if full_name != self.username:
            return f'{full_name} ({self.username})'
        return self.username
    
    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def has_permission(self, permission):
        """Check if user has specific permission."""
        permission_mapping = {
            'read': True,  # All authenticated users can read
            'create': self.can_create,
            'edit': self.can_edit,
            'delete': self.can_delete or self.is_admin,
            'upload': self.can_upload,
            'admin': self.is_admin
        }
        return permission_mapping.get(permission, False)
    
    def can_edit_page(self, page):
        """Check if user can edit a specific page."""
        if self.is_admin:
            return True
        if not self.can_edit:
            return False
        # Users can edit their own pages
        return page.author_id == self.id
    
    def can_delete_page(self, page):
        """Check if user can delete a specific page."""
        if self.is_admin:
            return True
        if not self.can_delete:
            return False
        # Users can delete their own pages
        return page.author_id == self.id
    
    def can_delete_file(self, file):
        """Check if user can delete a specific file."""
        if self.is_admin:
            return True
        # Users can delete their own files
        return file.uploader_id == self.id
    
    def to_dict(self):
        """Convert user to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'display_name': self.get_display_name(),
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'permissions': {
                'can_edit': self.can_edit,
                'can_create': self.can_create,
                'can_delete': self.can_delete,
                'can_upload': self.can_upload
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    @staticmethod
    def create_from_ldap(ldap_user_data):
        """Create user from LDAP data."""
        user = User(
            username=ldap_user_data.get('username'),
            email=ldap_user_data.get('email'),
            first_name=ldap_user_data.get('first_name'),
            last_name=ldap_user_data.get('last_name'),
            ldap_dn=ldap_user_data.get('dn'),
            domain=ldap_user_data.get('domain')
        )
        
        # Set permissions based on LDAP groups
        groups = ldap_user_data.get('groups', [])
        user.is_admin = any('WikiAdmins' in group for group in groups)
        user.can_edit = any('WikiUsers' in group or 'WikiAdmins' in group for group in groups)
        user.can_create = any('WikiUsers' in group or 'WikiAdmins' in group for group in groups)
        user.can_delete = any('WikiAdmins' in group for group in groups)
        user.can_upload = any('WikiUsers' in group or 'WikiAdmins' in group for group in groups)
        
        # Read-only users
        if any('WikiReadOnly' in group for group in groups):
            user.can_edit = False
            user.can_create = False
            user.can_delete = False
            user.can_upload = False
        
        return user
    
    def update_from_ldap(self, ldap_user_data):
        """Update user from LDAP data."""
        self.email = ldap_user_data.get('email') or self.email
        self.first_name = ldap_user_data.get('first_name') or self.first_name
        self.last_name = ldap_user_data.get('last_name') or self.last_name
        self.ldap_dn = ldap_user_data.get('dn') or self.ldap_dn
        self.domain = ldap_user_data.get('domain') or self.domain
        self.updated_at = datetime.utcnow()
        
        # Update permissions based on LDAP groups
        groups = ldap_user_data.get('groups', [])
        self.is_admin = any('WikiAdmins' in group for group in groups)
        self.can_edit = any('WikiUsers' in group or 'WikiAdmins' in group for group in groups)
        self.can_create = any('WikiUsers' in group or 'WikiAdmins' in group for group in groups)
        self.can_delete = any('WikiAdmins' in group for group in groups)
        self.can_upload = any('WikiUsers' in group or 'WikiAdmins' in group for group in groups)
        
        # Read-only users
        if any('WikiReadOnly' in group for group in groups):
            self.can_edit = False
            self.can_create = False
            self.can_delete = False
            self.can_upload = False
