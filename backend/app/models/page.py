"""
Page model for HomelabWiki application.
Stores wiki pages with Markdown content and metadata.
"""

from datetime import datetime
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property
import re
from app import db

# Association table for page tags
page_tags = db.Table('page_tags',
    db.Column('page_id', db.Integer, db.ForeignKey('pages.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Page(db.Model):
    """Page model for wiki pages."""
    
    __tablename__ = 'pages'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(500), nullable=True)
    
    # Versioning
    version = db.Column(db.Integer, default=1)
    
    # Status
    is_published = db.Column(db.Boolean, default=True)
    is_archived = db.Column(db.Boolean, default=False)
    
    # Metadata
    meta_description = db.Column(db.String(300), nullable=True)
    meta_keywords = db.Column(db.String(500), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    tags = db.relationship('Tag', secondary=page_tags, lazy='subquery',
                          backref=db.backref('pages', lazy=True))
    files = db.relationship('File', backref='page', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Page {self.title}>'
    
    @hybrid_property
    def word_count(self):
        """Calculate word count of the content."""
        if not self.content:
            return 0
        # Remove markdown formatting and count words
        text = re.sub(r'[#*`\[\]()]', '', self.content)
        words = text.split()
        return len(words)
    
    @hybrid_property
    def reading_time(self):
        """Estimate reading time in minutes (assuming 200 words per minute)."""
        return max(1, self.word_count // 200)
    
    def generate_slug(self):
        """Generate URL-friendly slug from title."""
        if not self.title:
            return None
        
        # Convert to lowercase and replace spaces with hyphens
        slug = re.sub(r'[^\w\s-]', '', self.title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')
        
        # Ensure uniqueness
        base_slug = slug
        counter = 1
        while Page.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        return slug
    
    def extract_summary(self, length=200):
        """Extract summary from content."""
        if not self.content:
            return ''
        
        # Remove markdown formatting
        text = re.sub(r'[#*`\[\]()]', '', self.content)
        text = re.sub(r'\n+', ' ', text)
        text = text.strip()
        
        if len(text) <= length:
            return text
        
        # Find the last space before the length limit
        truncated = text[:length]
        last_space = truncated.rfind(' ')
        
        if last_space > 0:
            return truncated[:last_space] + '...'
        else:
            return truncated + '...'
    
    def get_headings(self):
        """Extract headings from markdown content."""
        if not self.content:
            return []
        
        headings = []
        lines = self.content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                if level <= 6:  # H1 to H6
                    text = line.lstrip('#').strip()
                    if text:
                        headings.append({
                            'level': level,
                            'text': text,
                            'id': re.sub(r'[^\w\s-]', '', text.lower()).replace(' ', '-')
                        })
        
        return headings
    
    def get_tags_list(self):
        """Get list of tag names."""
        return [tag.name for tag in self.tags]
    
    def add_tag(self, tag_name):
        """Add a tag to the page."""
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag_name):
        """Remove a tag from the page."""
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag and tag in self.tags:
            self.tags.remove(tag)
    
    def to_dict(self, include_content=True):
        """Convert page to dictionary for JSON serialization."""
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'summary': self.summary or self.extract_summary(),
            'version': self.version,
            'is_published': self.is_published,
            'is_archived': self.is_archived,
            'word_count': self.word_count,
            'reading_time': self.reading_time,
            'tags': self.get_tags_list(),
            'headings': self.get_headings(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author': {
                'id': self.author.id,
                'username': self.author.username,
                'display_name': self.author.get_display_name()
            } if self.author else None
        }
        
        if include_content:
            data['content'] = self.content
            
        return data
    
    def to_markdown(self):
        """Export page as markdown with metadata."""
        metadata = f"""---
title: {self.title}
slug: {self.slug}
author: {self.author.username if self.author else 'Unknown'}
created: {self.created_at.isoformat() if self.created_at else 'Unknown'}
updated: {self.updated_at.isoformat() if self.updated_at else 'Unknown'}
tags: {', '.join(self.get_tags_list())}
---

"""
        return metadata + self.content
    
    @staticmethod
    def create_from_markdown(markdown_content, author_id):
        """Create page from markdown content with metadata."""
        # Extract metadata if present
        if markdown_content.startswith('---'):
            try:
                _, metadata_str, content = markdown_content.split('---', 2)
                metadata = {}
                for line in metadata_str.strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()
                
                page = Page(
                    title=metadata.get('title', 'Untitled'),
                    content=content.strip(),
                    author_id=author_id
                )
                
                # Add tags if present
                if 'tags' in metadata:
                    tag_names = [tag.strip() for tag in metadata['tags'].split(',')]
                    for tag_name in tag_names:
                        if tag_name:
                            page.add_tag(tag_name)
                
                return page
            except ValueError:
                # If metadata parsing fails, treat as regular content
                pass
        
        # Create page without metadata
        return Page(
            title='Untitled',
            content=markdown_content,
            author_id=author_id
        )

class Tag(db.Model):
    """Tag model for categorizing pages."""
    
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(200), nullable=True)
    color = db.Column(db.String(7), nullable=True)  # Hex color code
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tag {self.name}>'
    
    def to_dict(self):
        """Convert tag to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'page_count': len(self.pages),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Event listeners
@event.listens_for(Page, 'before_insert')
def generate_slug_on_insert(mapper, connection, target):
    """Generate slug before inserting a new page."""
    if not target.slug:
        target.slug = target.generate_slug()

@event.listens_for(Page, 'before_update')
def update_summary_on_update(mapper, connection, target):
    """Update summary when content changes."""
    if not target.summary:
        target.summary = target.extract_summary()
