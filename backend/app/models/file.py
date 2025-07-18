"""
File model for HomelabWiki application.
Handles file uploads and attachments.
"""

import os
from datetime import datetime
from werkzeug.utils import secure_filename
from app import db

class File(db.Model):
    """File model for uploaded files and attachments."""
    
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # Size in bytes
    mime_type = db.Column(db.String(100), nullable=True)
    file_hash = db.Column(db.String(64), nullable=True)  # SHA-256 hash
    
    # File metadata
    description = db.Column(db.Text, nullable=True)
    alt_text = db.Column(db.String(255), nullable=True)  # For images
    
    # Status
    is_public = db.Column(db.Boolean, default=True)
    is_archived = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=True)
    
    def __repr__(self):
        return f'<File {self.original_filename}>'
    
    @property
    def file_extension(self):
        """Get file extension."""
        return os.path.splitext(self.original_filename)[1].lower()
    
    @property
    def file_type(self):
        """Get general file type category."""
        ext = self.file_extension
        
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']:
            return 'image'
        elif ext in ['.pdf']:
            return 'pdf'
        elif ext in ['.doc', '.docx']:
            return 'document'
        elif ext in ['.xls', '.xlsx']:
            return 'spreadsheet'
        elif ext in ['.txt', '.md', '.rst']:
            return 'text'
        elif ext in ['.zip', '.tar', '.gz', '.bz2', '.7z']:
            return 'archive'
        elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv']:
            return 'video'
        elif ext in ['.mp3', '.wav', '.flac', '.ogg']:
            return 'audio'
        else:
            return 'other'
    
    @property
    def is_image(self):
        """Check if file is an image."""
        return self.file_type == 'image'
    
    @property
    def is_document(self):
        """Check if file is a document."""
        return self.file_type in ['document', 'spreadsheet', 'pdf', 'text']
    
    def get_file_size_formatted(self):
        """Get formatted file size."""
        size = self.file_size
        
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
    
    def get_download_url(self):
        """Get download URL for the file."""
        return f"/api/files/{self.id}/download"
    
    def get_thumbnail_url(self):
        """Get thumbnail URL for images."""
        if self.is_image:
            return f"/api/files/{self.id}/thumbnail"
        return None
    
    def get_absolute_path(self):
        """Get absolute file path."""
        return os.path.abspath(self.file_path)
    
    def file_exists(self):
        """Check if file exists on disk."""
        return os.path.exists(self.get_absolute_path())
    
    def delete_file(self):
        """Delete file from disk."""
        if self.file_exists():
            try:
                os.remove(self.get_absolute_path())
                return True
            except OSError:
                return False
        return False
    
    def to_dict(self):
        """Convert file to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'file_size_formatted': self.get_file_size_formatted(),
            'mime_type': self.mime_type,
            'file_type': self.file_type,
            'file_extension': self.file_extension,
            'is_image': self.is_image,
            'is_document': self.is_document,
            'description': self.description,
            'alt_text': self.alt_text,
            'is_public': self.is_public,
            'is_archived': self.is_archived,
            'download_url': self.get_download_url(),
            'thumbnail_url': self.get_thumbnail_url(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'uploader': {
                'id': self.uploader.id,
                'username': self.uploader.username,
                'display_name': self.uploader.get_display_name()
            } if self.uploader else None,
            'page': {
                'id': self.page.id,
                'title': self.page.title,
                'slug': self.page.slug
            } if self.page else None
        }
    
    @staticmethod
    def create_from_upload(file_obj, uploader_id, page_id=None, description=None):
        """Create file record from uploaded file."""
        import hashlib
        import uuid
        from flask import current_app
        
        # Generate secure filename
        original_filename = secure_filename(file_obj.filename)
        file_extension = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        
        # Create upload directory if it doesn't exist
        upload_dir = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_dir, unique_filename)
        file_obj.save(file_path)
        
        # Calculate file hash
        file_hash = None
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
        except Exception:
            pass
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Create file record
        file_record = File(
            filename=unique_filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file_obj.content_type,
            file_hash=file_hash,
            uploader_id=uploader_id,
            page_id=page_id,
            description=description
        )
        
        return file_record
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed."""
        from flask import current_app
        
        if not filename:
            return False
            
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', set())
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def get_files_by_type(file_type, limit=None):
        """Get files by type."""
        query = File.query
        
        if file_type == 'image':
            query = query.filter(File.mime_type.like('image/%'))
        elif file_type == 'document':
            query = query.filter(File.mime_type.in_([
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'text/plain',
                'text/markdown'
            ]))
        elif file_type == 'archive':
            query = query.filter(File.mime_type.in_([
                'application/zip',
                'application/x-tar',
                'application/gzip',
                'application/x-7z-compressed'
            ]))
        
        query = query.filter_by(is_archived=False).order_by(File.created_at.desc())
        
        if limit:
            query = query.limit(limit)
            
        return query.all()
    
    @staticmethod
    def search_files(query_string, limit=20):
        """Search files by filename or description."""
        search_term = f"%{query_string}%"
        
        results = File.query.filter(
            db.or_(
                File.original_filename.ilike(search_term),
                File.description.ilike(search_term)
            )
        ).filter_by(is_archived=False).order_by(File.created_at.desc()).limit(limit).all()
        
        return results
