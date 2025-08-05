from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.models.post import Post
from app.models.access_log import AccessLog
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            
            # Log the access
            log = AccessLog(
                endpoint='/login',
                method='POST',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string,
                accessed_data=json.dumps({'username': username}),
                user_id=user.id
            )
            db.session.add(log)
            db.session.commit()
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        bio = request.form.get('bio')
        email_public = 'email_public' in request.form
        bio_public = 'bio_public' in request.form
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return render_template('auth/register.html')
            
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return render_template('auth/register.html')
        
        # Create new user
        user = User(username=username, email=email, password=password, bio=bio)
        user.email_public = email_public
        user.bio_public = bio_public
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Update user profile
        current_user.bio = request.form.get('bio')
        current_user.email_public = 'email_public' in request.form
        current_user.bio_public = 'bio_public' in request.form
        
        # Update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            current_user.set_password(new_password)
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        
    return render_template('auth/profile.html')

@auth_bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    password = request.form.get('password')
    
    # Verify password
    if not current_user.check_password(password):
        flash('Incorrect password. Account deletion canceled.', 'danger')
        return redirect(url_for('main.user_profile', username=current_user.username))
    
    # Store username for confirmation message
    username = current_user.username
    
    # Get user posts
    user_posts = Post.query.filter_by(user_id=current_user.id).all()
    
    # Delete all user posts
    for post in user_posts:
        db.session.delete(post)
    
    # Delete access logs
    access_logs = AccessLog.query.filter_by(user_id=current_user.id).all()
    for log in access_logs:
        db.session.delete(log)
    
    # Delete the user
    db.session.delete(current_user)
    db.session.commit()
    
    # Log out the user
    logout_user()
    
    flash(f'Account "{username}" has been permanently deleted along with all associated data.', 'success')
    
    # Redirect to account deletion confirmation page
    return redirect(url_for('auth.account_deleted', username=username))

@auth_bp.route('/account-deleted/<username>')
def account_deleted(username):
    return render_template('auth/account_deleted.html', username=username)