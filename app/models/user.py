from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    bio = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Privacy settings
    email_public = db.Column(db.Boolean, default=False)
    bio_public = db.Column(db.Boolean, default=True)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, username, email, password, bio=None, is_admin=False):
        self.username = username
        self.email = email
        self.set_password(password)
        self.bio = bio
        self.is_admin = is_admin
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_private=False):
        """Convert user to dictionary, optionally including private data"""
        data = {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat(),
            'is_admin': self.is_admin
        }
        
        # Include bio if public or if private data is requested
        if self.bio_public or include_private:
            data['bio'] = self.bio
            
        # Include email if public or if private data is requested
        if self.email_public or include_private:
            data['email'] = self.email
            
        # Always include privacy settings if private data is requested
        if include_private:
            data['email_public'] = self.email_public
            data['bio_public'] = self.bio_public
            
        return data

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))