"""
Pages API endpoints for HomelabWiki.
"""

from flask import request, jsonify, send_file
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.api import bp
from app import db
from app.models.page import Page, Tag
from app.models.user import User
import io
import zipfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import markdown

@bp.route('/pages', methods=['GET'])
@login_required
def get_pages():
    """Get all pages with pagination and filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        tag = request.args.get('tag')
        author = request.args.get('author')
        search = request.args.get('search')
        
        query = Page.query.filter_by(is_published=True, is_archived=False)
        
        # Apply filters
        if tag:
            query = query.join(Page.tags).filter(Tag.name == tag)
        
        if author:
            query = query.join(Page.author).filter(User.username == author)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Page.title.ilike(search_term),
                    Page.content.ilike(search_term)
                )
            )
        
        # Pagination
        pagination = query.order_by(Page.updated_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        pages = [page.to_dict(include_content=False) for page in pagination.items]
        
        return jsonify({
            'pages': pages,
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
        return jsonify({'error': 'Failed to get pages'}), 500

@bp.route('/pages/<int:page_id>', methods=['GET'])
@login_required
def get_page(page_id):
    """Get a specific page."""
    try:
        page = Page.query.get_or_404(page_id)
        
        if not page.is_published and not current_user.can_edit_page(page):
            return jsonify({'error': 'Page not found'}), 404
        
        return jsonify({'page': page.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get page'}), 500

@bp.route('/pages/slug/<slug>', methods=['GET'])
@login_required
def get_page_by_slug(slug):
    """Get a page by slug."""
    try:
        page = Page.query.filter_by(slug=slug, is_published=True, is_archived=False).first_or_404()
        return jsonify({'page': page.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get page'}), 500

@bp.route('/pages', methods=['POST'])
@login_required
def create_page():
    """Create a new page."""
    try:
        if not current_user.has_permission('create'):
            return jsonify({'error': 'Permission denied'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        title = data.get('title')
        content = data.get('content', '')
        tags = data.get('tags', [])
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        # Create page
        page = Page(
            title=title,
            content=content,
            author_id=current_user.id
        )
        
        # Add tags
        for tag_name in tags:
            if tag_name.strip():
                page.add_tag(tag_name.strip())
        
        db.session.add(page)
        db.session.commit()
        
        return jsonify({
            'message': 'Page created successfully',
            'page': page.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create page'}), 500

@bp.route('/pages/<int:page_id>', methods=['PUT'])
@login_required
def update_page(page_id):
    """Update a page."""
    try:
        page = Page.query.get_or_404(page_id)
        
        if not current_user.can_edit_page(page):
            return jsonify({'error': 'Permission denied'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields
        if 'title' in data:
            page.title = data['title']
        if 'content' in data:
            page.content = data['content']
        if 'tags' in data:
            # Clear existing tags
            page.tags.clear()
            # Add new tags
            for tag_name in data['tags']:
                if tag_name.strip():
                    page.add_tag(tag_name.strip())
        
        page.version += 1
        db.session.commit()
        
        return jsonify({
            'message': 'Page updated successfully',
            'page': page.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update page'}), 500

@bp.route('/pages/<int:page_id>', methods=['DELETE'])
@login_required
def delete_page(page_id):
    """Delete a page."""
    try:
        page = Page.query.get_or_404(page_id)
        
        if not current_user.can_delete_page(page):
            return jsonify({'error': 'Permission denied'}), 403
        
        # Delete associated files
        for file in page.files:
            file.delete_file()
        
        db.session.delete(page)
        db.session.commit()
        
        return jsonify({'message': 'Page deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete page'}), 500

@bp.route('/pages/<int:page_id>/export/markdown', methods=['GET'])
@login_required
def export_page_markdown(page_id):
    """Export page as Markdown file."""
    try:
        page = Page.query.get_or_404(page_id)
        
        if not page.is_published and not current_user.can_edit_page(page):
            return jsonify({'error': 'Page not found'}), 404
        
        markdown_content = page.to_markdown()
        
        # Create in-memory file
        file_obj = io.BytesIO()
        file_obj.write(markdown_content.encode('utf-8'))
        file_obj.seek(0)
        
        return send_file(
            file_obj,
            mimetype='text/markdown',
            as_attachment=True,
            download_name=f"{page.slug}.md"
        )
        
    except Exception as e:
        return jsonify({'error': 'Failed to export page'}), 500

@bp.route('/pages/<int:page_id>/export/pdf', methods=['GET'])
@login_required
def export_page_pdf(page_id):
    """Export page as PDF file."""
    try:
        page = Page.query.get_or_404(page_id)
        
        if not page.is_published and not current_user.can_edit_page(page):
            return jsonify({'error': 'Page not found'}), 404
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = Paragraph(page.title, styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Metadata
        metadata = f"Author: {page.author.get_display_name()}<br/>"
        metadata += f"Created: {page.created_at.strftime('%Y-%m-%d %H:%M')}<br/>"
        metadata += f"Updated: {page.updated_at.strftime('%Y-%m-%d %H:%M')}<br/>"
        if page.tags:
            metadata += f"Tags: {', '.join(page.get_tags_list())}<br/>"
        
        meta_para = Paragraph(metadata, styles['Normal'])
        story.append(meta_para)
        story.append(Spacer(1, 12))
        
        # Convert markdown to HTML and then to PDF
        html_content = markdown.markdown(page.content)
        content_para = Paragraph(html_content, styles['Normal'])
        story.append(content_para)
        
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{page.slug}.pdf"
        )
        
    except Exception as e:
        return jsonify({'error': 'Failed to export page as PDF'}), 500

@bp.route('/pages/export/all', methods=['GET'])
@login_required
def export_all_pages():
    """Export all pages as ZIP file."""
    try:
        if not current_user.has_permission('admin'):
            return jsonify({'error': 'Permission denied'}), 403
        
        pages = Page.query.filter_by(is_published=True, is_archived=False).all()
        
        # Create ZIP file in memory
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for page in pages:
                markdown_content = page.to_markdown()
                zip_file.writestr(f"{page.slug}.md", markdown_content.encode('utf-8'))
        
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='wiki-export.zip'
        )
        
    except Exception as e:
        return jsonify({'error': 'Failed to export pages'}), 500

@bp.route('/tags', methods=['GET'])
@login_required
def get_tags():
    """Get all tags."""
    try:
        tags = Tag.query.all()
        return jsonify({
            'tags': [tag.to_dict() for tag in tags]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get tags'}), 500

@bp.route('/tags/<int:tag_id>', methods=['DELETE'])
@login_required
def delete_tag(tag_id):
    """Delete a tag."""
    try:
        if not current_user.has_permission('admin'):
            return jsonify({'error': 'Permission denied'}), 403
        
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        
        return jsonify({'message': 'Tag deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete tag'}), 500