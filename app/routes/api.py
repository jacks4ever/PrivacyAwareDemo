from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user, login_required
from app import db
from app.models.user import User
from app.models.post import Post
from app.models.access_log import AccessLog
import json

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Helper function to log API access
def log_api_access(endpoint, data, is_privacy_leak=False, leak_type=None):
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None
        
    log = AccessLog(
        endpoint=endpoint,
        method=request.method,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        accessed_data=json.dumps(data),
        user_id=user_id,
        is_privacy_leak=is_privacy_leak,
        leak_type=leak_type
    )
    db.session.add(log)
    db.session.commit()

# Secure API endpoints (require authentication)
@api_bp.route('/users/me')
@login_required
def get_current_user():
    user_data = current_user.to_dict(include_private=True)
    
    log_api_access(
        endpoint='/api/users/me',
        data={'user_id': current_user.id}
    )
    
    return jsonify(user_data)

@api_bp.route('/posts/me')
@login_required
def get_current_user_posts():
    posts = Post.query.filter_by(user_id=current_user.id, is_deleted=False).all()
    posts_data = [post.to_dict(include_private=True) for post in posts]
    
    log_api_access(
        endpoint='/api/posts/me',
        data={'user_id': current_user.id, 'post_count': len(posts_data)}
    )
    
    return jsonify(posts_data)

# Insecure API endpoints (demonstrate privacy leaks)

# 1. Insecure user endpoint that leaks private emails
@api_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    
    # This endpoint leaks all user data including private emails
    users_data = [user.to_dict(include_private=True) for user in users]
    
    # Log this as a privacy leak
    log_api_access(
        endpoint='/api/users',
        data={'user_count': len(users_data)},
        is_privacy_leak=True,
        leak_type='email_leak'
    )
    
    return jsonify(users_data)

# 2. Insecure post endpoint that leaks private posts
@api_bp.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.filter_by(is_deleted=False).all()
    
    # This endpoint leaks all posts including private ones
    posts_data = [post.to_dict(include_private=True) for post in posts]
    
    # Log this as a privacy leak
    log_api_access(
        endpoint='/api/posts',
        data={'post_count': len(posts_data)},
        is_privacy_leak=True,
        leak_type='private_post_leak'
    )
    
    return jsonify(posts_data)

# 3. Insecure user detail endpoint with no authentication
@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    
    # This endpoint leaks user details without checking permissions
    user_data = user.to_dict(include_private=True)
    
    # Log this as a privacy leak
    log_api_access(
        endpoint=f'/api/users/{user_id}',
        data={'user_id': user_id},
        is_privacy_leak=True,
        leak_type='user_detail_leak'
    )
    
    return jsonify(user_data)

# 4. Insecure endpoint that leaks "deleted" posts
@api_bp.route('/posts/all', methods=['GET'])
def get_all_posts_including_deleted():
    posts = Post.query.all()  # This includes deleted posts
    
    # This endpoint leaks all posts including deleted ones
    posts_data = [post.to_dict(include_private=True) for post in posts]
    
    # Log this as a privacy leak
    log_api_access(
        endpoint='/api/posts/all',
        data={'post_count': len(posts_data)},
        is_privacy_leak=True,
        leak_type='deleted_post_leak'
    )
    
    return jsonify(posts_data)