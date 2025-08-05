from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.post import Post
from app.models.access_log import AccessLog
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get all public posts
    posts = Post.query.filter_by(is_public=True, is_deleted=False).order_by(Post.created_at.desc()).all()
    
    # Log the access (not a privacy leak since these are public posts)
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None
        
    log = AccessLog(
        endpoint='/',
        method='GET',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        accessed_data=json.dumps({'action': 'view_public_posts'}),
        user_id=user_id
    )
    db.session.add(log)
    db.session.commit()
    
    return render_template('main/index.html', posts=posts)

@main_bp.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    # Get public posts by this user
    posts = Post.query.filter_by(user_id=user.id, is_public=True, is_deleted=False).order_by(Post.created_at.desc()).all()
    
    # Determine what data to show based on privacy settings
    show_email = user.email_public
    show_bio = user.bio_public
    
    # Log the access
    if current_user.is_authenticated:
        viewer_id = current_user.id
    else:
        viewer_id = None
        
    log = AccessLog(
        endpoint=f'/user/{username}',
        method='GET',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        accessed_data=json.dumps({
            'username': username,
            'show_email': show_email,
            'show_bio': show_bio
        }),
        user_id=viewer_id
    )
    db.session.add(log)
    db.session.commit()
    
    return render_template('main/user_profile.html', user=user, posts=posts, 
                          show_email=show_email, show_bio=show_bio)

@main_bp.route('/my-posts')
@login_required
def my_posts():
    # Get all posts by the current user, including private ones
    posts = Post.query.filter_by(user_id=current_user.id, is_deleted=False).order_by(Post.created_at.desc()).all()
    
    # Log the access (not a privacy leak since users are viewing their own posts)
    log = AccessLog(
        endpoint='/my-posts',
        method='GET',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        accessed_data=json.dumps({'action': 'view_own_posts'}),
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()
    
    return render_template('main/my_posts.html', posts=posts)

@main_bp.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        is_public = 'is_public' in request.form
        
        post = Post(title=title, content=content, user_id=current_user.id, is_public=is_public)
        db.session.add(post)
        db.session.commit()
        
        flash('Post created successfully', 'success')
        return redirect(url_for('main.my_posts'))
    
    return render_template('main/create_post.html')

@main_bp.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Check if the current user is the author
    if post.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to edit this post', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.is_public = 'is_public' in request.form
        
        db.session.commit()
        flash('Post updated successfully', 'success')
        return redirect(url_for('main.my_posts'))
    
    return render_template('main/edit_post.html', post=post)

@main_bp.route('/delete-post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Check if the current user is the author
    if post.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this post', 'danger')
        return redirect(url_for('main.index'))
    
    # Soft delete the post
    post.is_deleted = True
    db.session.commit()
    
    flash('Post deleted successfully', 'success')
    return redirect(url_for('main.my_posts'))

@main_bp.route('/access-logs')
@login_required
def access_logs():
    # Only show logs for the current user unless they're an admin
    if current_user.is_admin:
        logs = AccessLog.query.order_by(AccessLog.timestamp.desc()).limit(100).all()
    else:
        logs = AccessLog.query.filter_by(user_id=current_user.id).order_by(AccessLog.timestamp.desc()).limit(50).all()
    
    return render_template('main/access_logs.html', logs=logs)