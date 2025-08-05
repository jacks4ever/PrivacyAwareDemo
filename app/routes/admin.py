from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.post import Post
from app.models.access_log import AccessLog
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin access decorator
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin_bp.route('/users')
@admin_required
def users():
    all_users = User.query.all()
    
    # Log the access (not a privacy leak since admin has permission)
    log = AccessLog(
        endpoint='/admin/users',
        method='GET',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        accessed_data=json.dumps({'action': 'view_all_users'}),
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()
    
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/posts')
@admin_required
def posts():
    all_posts = Post.query.all()
    
    # Log the access (not a privacy leak since admin has permission)
    log = AccessLog(
        endpoint='/admin/posts',
        method='GET',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        accessed_data=json.dumps({'action': 'view_all_posts'}),
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()
    
    return render_template('admin/posts.html', posts=all_posts)

@admin_bp.route('/logs')
@admin_required
def logs():
    all_logs = AccessLog.query.order_by(AccessLog.timestamp.desc()).all()
    
    # Count privacy leaks
    privacy_leaks = AccessLog.query.filter_by(is_privacy_leak=True).count()
    
    return render_template('admin/logs.html', logs=all_logs, privacy_leaks=privacy_leaks)

@admin_bp.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.bio = request.form.get('bio')
        user.email_public = 'email_public' in request.form
        user.bio_public = 'bio_public' in request.form
        user.is_admin = 'is_admin' in request.form
        
        # Update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            user.set_password(new_password)
        
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/edit_user.html', user=user)