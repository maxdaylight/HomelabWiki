"""
Files API endpoints for HomelabWiki.
"""

import os
from flask import request, jsonify, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.api import bp
from app import db
from app.models.file import File
from app.models.page import Page
from PIL import Image
import io

@bp.route('/files', methods=['GET'])
@login_required
def get_files():
    """Get all files with pagination and filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        file_type = request.args.get('type')
        search = request.args.get('search')
        
        query = File.query.filter_by(is_archived=False)
        
        # Apply filters
        if file_type:
            files = File.get_files_by_type(file_type)
            file_ids = [f.id for f in files]
            query = query.filter(File.id.in_(file_ids))
        
        if search:
            files = File.search_files(search)
            file_ids = [f.id for f in files]
            query = query.filter(File.id.in_(file_ids))
        
        # Pagination
        pagination = query.order_by(File.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        files = [file.to_dict() for file in pagination.items]
        
        return jsonify({
            'files': files,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_prev': pagination.has_prev,
                'has_next': pagination.has_next
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get files'}), 500

@bp.route('/files/<int:file_id>', methods=['GET'])
@login_required
def get_file(file_id):
    """Get file information."""
    try:
        file = File.query.get_or_404(file_id)
        return jsonify({'file': file.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get file'}), 500

@bp.route('/files/<int:file_id>/download', methods=['GET'])
@login_required
def download_file(file_id):
    """Download a file."""
    try:
        file = File.query.get_or_404(file_id)
        
        if not file.is_public and file.uploader_id != current_user.id and not current_user.is_admin:
            return jsonify({'error': 'Permission denied'}), 403
        
        if not file.file_exists():
            return jsonify({'error': 'File not found on disk'}), 404
        
        return send_file(
            file.get_absolute_path(),
            mimetype=file.mime_type,
            as_attachment=True,
            download_name=file.original_filename
        )
        
    except Exception as e:
        return jsonify({'error': 'Failed to download file'}), 500

@bp.route('/files/<int:file_id>/thumbnail', methods=['GET'])
@login_required
def get_thumbnail(file_id):
    """Get thumbnail for image files."""
    try:
        file = File.query.get_or_404(file_id)
        
        if not file.is_image:
            return jsonify({'error': 'File is not an image'}), 400
        
        if not file.file_exists():
            return jsonify({'error': 'File not found on disk'}), 404
        
        # Generate thumbnail
        size = request.args.get('size', 200, type=int)
        
        with Image.open(file.get_absolute_path()) as img:
            img.thumbnail((size, size), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save to memory
            img_io = io.BytesIO()
            img.save(img_io, 'JPEG', quality=85)
            img_io.seek(0)
            
            return send_file(
                img_io,
                mimetype='image/jpeg',
                as_attachment=False
            )
        
    except Exception as e:
        return jsonify({'error': 'Failed to generate thumbnail'}), 500

@bp.route('/files', methods=['POST'])
@login_required
def upload_file():
    """Upload a file."""
    try:
        if not current_user.has_permission('upload'):
            return jsonify({'error': 'Permission denied'}), 403
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file_obj = request.files['file']
        if file_obj.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not File.allowed_file(file_obj.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Get optional parameters
        page_id = request.form.get('page_id', type=int)
        description = request.form.get('description')
        
        # Validate page_id if provided
        if page_id:
            page = Page.query.get(page_id)
            if not page:
                return jsonify({'error': 'Page not found'}), 404
        
        # Create file record
        file_record = File.create_from_upload(
            file_obj=file_obj,
            uploader_id=current_user.id,
            page_id=page_id,
            description=description
        )
        
        db.session.add(file_record)
        db.session.commit()
        
        return jsonify({
            'message': 'File uploaded successfully',
            'file': file_record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to upload file'}), 500

@bp.route('/files/<int:file_id>', methods=['PUT'])
@login_required
def update_file(file_id):
    """Update file metadata."""
    try:
        file = File.query.get_or_404(file_id)
        
        if file.uploader_id != current_user.id and not current_user.is_admin:
            return jsonify({'error': 'Permission denied'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields
        if 'description' in data:
            file.description = data['description']
        if 'alt_text' in data:
            file.alt_text = data['alt_text']
        if 'is_public' in data:
            file.is_public = data['is_public']
        
        db.session.commit()
        
        return jsonify({
            'message': 'File updated successfully',
            'file': file.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update file'}), 500

@bp.route('/files/<int:file_id>', methods=['DELETE'])
@login_required
def delete_file(file_id):
    """Delete a file."""
    try:
        file = File.query.get_or_404(file_id)
        
        if not current_user.can_delete_file(file):
            return jsonify({'error': 'Permission denied'}), 403
        
        # Delete file from disk
        file.delete_file()
        
        # Delete from database
        db.session.delete(file)
        db.session.commit()
        
        return jsonify({'message': 'File deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete file'}), 500

@bp.route('/files/stats', methods=['GET'])
@login_required
def get_file_stats():
    """Get file statistics."""
    try:
        if not current_user.has_permission('admin'):
            return jsonify({'error': 'Permission denied'}), 403
        
        # Get file counts by type
        image_count = len(File.get_files_by_type('image'))
        document_count = len(File.get_files_by_type('document'))
        archive_count = len(File.get_files_by_type('archive'))
        
        # Get total file size
        total_size = db.session.query(db.func.sum(File.file_size)).scalar() or 0
        
        # Get file count per user
        user_stats = db.session.query(
            File.uploader_id,
            db.func.count(File.id).label('file_count'),
            db.func.sum(File.file_size).label('total_size')
        ).group_by(File.uploader_id).all()
        
        return jsonify({
            'total_files': File.query.count(),
            'file_types': {
                'images': image_count,
                'documents': document_count,
                'archives': archive_count
            },
            'total_size': total_size,
            'total_size_formatted': File.get_file_size_formatted(total_size) if total_size else '0 B',
            'user_stats': [
                {
                    'uploader_id': stat.uploader_id,
                    'file_count': stat.file_count,
                    'total_size': stat.total_size
                }
                for stat in user_stats
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get file statistics'}), 500

@bp.route('/files/cleanup', methods=['POST'])
@login_required
def cleanup_files():
    """Clean up orphaned files."""
    try:
        if not current_user.has_permission('admin'):
            return jsonify({'error': 'Permission denied'}), 403
        
        # Find files that don't exist on disk
        missing_files = []
        for file in File.query.all():
            if not file.file_exists():
                missing_files.append(file.id)
                db.session.delete(file)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Cleaned up {len(missing_files)} orphaned files',
            'deleted_files': missing_files
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cleanup files'}), 500
