from datetime import datetime
from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Soft delete flag
    is_deleted = db.Column(db.Boolean, default=False)
    
    def __init__(self, title, content, user_id, is_public=True):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.is_public = is_public
    
    def to_dict(self, include_private=False):
        """Convert post to dictionary, optionally including private data"""
        # Don't include deleted posts unless specifically requested
        if self.is_deleted and not include_private:
            return None
            
        data = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': self.user_id,
            'author_username': self.author.username if self.author else None
        }
        
        # Include private fields if requested
        if include_private:
            data['is_public'] = self.is_public
            data['is_deleted'] = self.is_deleted
            
        return data