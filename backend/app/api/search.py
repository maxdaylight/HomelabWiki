"""
Search API endpoints for HomelabWiki.
"""

from flask import request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.api import bp
from app.models.page import Page, Tag
from app.models.file import File
from app.models.user import User

@bp.route('/search', methods=['GET'])
@login_required
def search():
    """Global search across pages, files, and tags."""
    try:
        query = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'all')  # all, pages, files, tags
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        results = {
            'query': query,
            'pages': [],
            'files': [],
            'tags': []
        }
        
        # Search pages
        if search_type in ['all', 'pages']:
            pages = search_pages(query, limit)
            results['pages'] = [page.to_dict(include_content=False) for page in pages]
        
        # Search files
        if search_type in ['all', 'files']:
            files = File.search_files(query, limit)
            results['files'] = [file.to_dict() for file in files]
        
        # Search tags
        if search_type in ['all', 'tags']:
            tags = search_tags(query, limit)
            results['tags'] = [tag.to_dict() for tag in tags]
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({'error': 'Search failed'}), 500

@bp.route('/search/pages', methods=['GET'])
@login_required
def search_pages_endpoint():
    """Search pages specifically."""
    try:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        pages = search_pages(query, limit)
        
        return jsonify({
            'query': query,
            'pages': [page.to_dict(include_content=False) for page in pages]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Page search failed'}), 500

@bp.route('/search/files', methods=['GET'])
@login_required
def search_files_endpoint():
    """Search files specifically."""
    try:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        files = File.search_files(query, limit)
        
        return jsonify({
            'query': query,
            'files': [file.to_dict() for file in files]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'File search failed'}), 500

@bp.route('/search/tags', methods=['GET'])
@login_required
def search_tags_endpoint():
    """Search tags specifically."""
    try:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        tags = search_tags(query, limit)
        
        return jsonify({
            'query': query,
            'tags': [tag.to_dict() for tag in tags]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Tag search failed'}), 500

@bp.route('/search/suggestions', methods=['GET'])
@login_required
def search_suggestions():
    """Get search suggestions."""
    try:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 10, type=int)
        
        if not query or len(query) < 2:
            return jsonify({'suggestions': []}), 200
        
        suggestions = []
        
        # Get page title suggestions
        page_titles = Page.query.filter(
            Page.title.ilike(f"%{query}%"),
            Page.is_published == True,
            Page.is_archived == False
        ).limit(limit // 2).all()
        
        for page in page_titles:
            suggestions.append({
                'text': page.title,
                'type': 'page',
                'url': f'/pages/{page.slug}'
            })
        
        # Get tag suggestions
        tag_names = Tag.query.filter(
            Tag.name.ilike(f"%{query}%")
        ).limit(limit // 2).all()
        
        for tag in tag_names:
            suggestions.append({
                'text': tag.name,
                'type': 'tag',
                'url': f'/pages?tag={tag.name}'
            })
        
        return jsonify({'suggestions': suggestions}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get suggestions'}), 500

@bp.route('/search/recent', methods=['GET'])
@login_required
def recent_searches():
    """Get recent searches (placeholder for future implementation)."""
    try:
        # This would typically store user search history
        # For now, return empty list
        return jsonify({'recent_searches': []}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get recent searches'}), 500

def search_pages(query, limit=20):
    """Search pages by title and content."""
    search_term = f"%{query}%"
    
    # Search in title and content
    pages = Page.query.filter(
        or_(
            Page.title.ilike(search_term),
            Page.content.ilike(search_term)
        ),
        Page.is_published == True,
        Page.is_archived == False
    ).order_by(
        # Prioritize title matches
        Page.title.ilike(search_term).desc(),
        Page.updated_at.desc()
    ).limit(limit).all()
    
    return pages

def search_tags(query, limit=20):
    """Search tags by name."""
    search_term = f"%{query}%"
    
    tags = Tag.query.filter(
        Tag.name.ilike(search_term)
    ).limit(limit).all()
    
    return tags

@bp.route('/search/advanced', methods=['POST'])
@login_required
def advanced_search():
    """Advanced search with multiple criteria."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No search criteria provided'}), 400
        
        # Extract search criteria
        title_query = data.get('title', '').strip()
        content_query = data.get('content', '').strip()
        author_query = data.get('author', '').strip()
        tags_query = data.get('tags', [])
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        
        # Build query
        query = Page.query.filter(
            Page.is_published == True,
            Page.is_archived == False
        )
        
        # Apply filters
        if title_query:
            query = query.filter(Page.title.ilike(f"%{title_query}%"))
        
        if content_query:
            query = query.filter(Page.content.ilike(f"%{content_query}%"))
        
        if author_query:
            query = query.join(Page.author).filter(
                or_(
                    User.username.ilike(f"%{author_query}%"),
                    User.first_name.ilike(f"%{author_query}%"),
                    User.last_name.ilike(f"%{author_query}%")
                )
            )
        
        if tags_query:
            query = query.join(Page.tags).filter(Tag.name.in_(tags_query))
        
        if date_from:
            query = query.filter(Page.created_at >= date_from)
        
        if date_to:
            query = query.filter(Page.created_at <= date_to)
        
        # Execute query
        pages = query.order_by(Page.updated_at.desc()).limit(50).all()
        
        return jsonify({
            'pages': [page.to_dict(include_content=False) for page in pages],
            'total': len(pages)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Advanced search failed'}), 500
