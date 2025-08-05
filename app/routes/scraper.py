from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.post import Post
from app.models.access_log import AccessLog
import json
import requests
import time
import threading

scraper_bp = Blueprint('scraper', __name__, url_prefix='/scraper')

# Global variable to track if scraper is running
scraper_running = False
scraper_thread = None
scraper_results = []

@scraper_bp.route('/')
@login_required
def index():
    global scraper_running, scraper_results
    
    # Only admins can access this page
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('scraper/index.html', 
                          scraper_running=scraper_running,
                          scraper_results=scraper_results)

@scraper_bp.route('/start', methods=['POST'])
@login_required
def start_scraper():
    global scraper_running, scraper_thread, scraper_results
    
    # Only admins can start the scraper
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Permission denied'})
    
    if scraper_running:
        return jsonify({'success': False, 'message': 'Scraper is already running'})
    
    # Clear previous results
    scraper_results = []
    
    # Get the current app to pass to the thread
    app = current_app._get_current_object()
    
    # Start the scraper in a background thread with app context
    scraper_thread = threading.Thread(target=run_scraper_with_app_context, args=(app,))
    scraper_thread.daemon = True
    scraper_thread.start()
    
    scraper_running = True
    
    # Log the scraper start
    log = AccessLog(
        endpoint='/scraper/start',
        method='POST',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        accessed_data=json.dumps({'action': 'start_scraper'}),
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Scraper started'})

def run_scraper_with_app_context(app):
    """Wrapper function to run the scraper within the application context"""
    with app.app_context():
        run_scraper()

@scraper_bp.route('/stop', methods=['POST'])
@login_required
def stop_scraper():
    global scraper_running
    
    # Only admins can stop the scraper
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Permission denied'})
    
    if not scraper_running:
        return jsonify({'success': False, 'message': 'Scraper is not running'})
    
    scraper_running = False
    
    # Log the scraper stop
    log = AccessLog(
        endpoint='/scraper/stop',
        method='POST',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        accessed_data=json.dumps({'action': 'stop_scraper'}),
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Scraper stopped'})

@scraper_bp.route('/status')
@login_required
def scraper_status():
    global scraper_running, scraper_results
    
    # Only admins can check scraper status
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Permission denied'})
    
    return jsonify({
        'running': scraper_running,
        'results': scraper_results
    })

def run_scraper():
    """Simulates a third-party scraper accessing the API endpoints"""
    global scraper_running, scraper_results
    
    print("Running scraper within application context")
    
    # Simulate scraper running
    scraper_running = True
    
    # Clear previous results
    scraper_results = []
    
    # Log the start of the scraper
    print("Starting scraper simulation...")
    
    try:
        # Instead of making actual HTTP requests, we'll directly access the database
        # This simulates what a scraper would do, but is more reliable for the demo
        
        # Step 1: Get all users (demonstrates email leak)
        scraper_results.append({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'action': 'Scraping all users',
            'url': '/api/users',
            'status': 'In progress',
            'privacy_leak': True,
            'leak_type': 'API endpoint leaks private email addresses'
        })
        
        # Direct database access instead of API call
        users = User.query.all()
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,  # Privacy leak: emails are exposed regardless of settings
                'bio': user.bio,
                'email_public': user.email_public,
                'bio_public': user.bio_public
            })
        
        scraper_results[-1]['status'] = 'Complete'
        scraper_results[-1]['data_collected'] = f'Found {len(user_data)} users with emails and privacy settings'
        
        time.sleep(2)  # Simulate processing time
        
        # Step 2: Get all posts (demonstrates private post leak)
        scraper_results.append({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'action': 'Scraping all posts',
            'url': '/api/posts',
            'status': 'In progress',
            'privacy_leak': True,
            'leak_type': 'API endpoint leaks private posts'
        })
        
        # Direct database access instead of API call
        posts = Post.query.filter_by(is_deleted=False).all()
        post_data = []
        for post in posts:
            # Privacy leak: private posts are exposed
            post_data.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author_id': post.user_id,
                'author': post.author.username,
                'is_public': post.is_public,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        scraper_results[-1]['status'] = 'Complete'
        scraper_results[-1]['data_collected'] = f'Found {len(post_data)} posts including {sum(1 for p in post_data if not p["is_public"])} private ones'
        
        time.sleep(2)  # Simulate processing time
        
        # Step 3: Get deleted posts (demonstrates deleted data leak)
        scraper_results.append({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'action': 'Scraping deleted posts',
            'url': '/api/posts/all',
            'status': 'In progress',
            'privacy_leak': True,
            'leak_type': 'API endpoint leaks deleted posts'
        })
        
        # Direct database access instead of API call
        all_posts = Post.query.all()
        all_post_data = []
        for post in all_posts:
            all_post_data.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author_id': post.user_id,
                'author': post.author.username,
                'is_public': post.is_public,
                'is_deleted': post.is_deleted,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        deleted_posts = [p for p in all_post_data if p['is_deleted']]
        
        scraper_results[-1]['status'] = 'Complete'
        scraper_results[-1]['data_collected'] = f'Found {len(deleted_posts)} deleted posts that should be inaccessible'
        
        time.sleep(2)  # Simulate processing time
        
        # Step 4: Get detailed user information for each user
        for user in user_data[:3]:  # Limit to first 3 users for demo
            user_id = user['id']
            scraper_results.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'action': f'Scraping detailed info for user {user["username"]}',
                'url': f'/api/users/{user_id}',
                'status': 'In progress',
                'privacy_leak': True,
                'leak_type': 'API endpoint leaks detailed user information'
            })
            
            # Direct database access instead of API call
            user_obj = User.query.get(user_id)
            user_detail = {
                'id': user_obj.id,
                'username': user_obj.username,
                'email': user_obj.email,  # Privacy leak: email exposed regardless of settings
                'bio': user_obj.bio,      # Privacy leak: bio exposed regardless of settings
                'email_public': user_obj.email_public,
                'bio_public': user_obj.bio_public,
                'posts': [{'id': p.id, 'title': p.title} for p in user_obj.posts if not p.is_deleted]
            }
            
            # Create an access log entry for this privacy leak
            log = AccessLog(
                endpoint=f'/api/users/{user_id}',
                method='GET',
                ip_address='scraper-simulation',
                user_agent='Scraper/1.0',
                accessed_data=json.dumps({'action': 'get_user_details', 'user_id': user_id}),
                is_privacy_leak=True,
                leak_type='Unauthorized access to private user data'
            )
            db.session.add(log)
            db.session.commit()
            
            scraper_results[-1]['status'] = 'Complete'
            scraper_results[-1]['data_collected'] = f'Collected private details for {user["username"]}'
            
            time.sleep(1)  # Simulate processing time
            
    except Exception as e:
        scraper_results.append({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'action': 'Error in scraper',
            'status': 'Error',
            'data_collected': str(e)
        })
        print(f"Scraper error: {str(e)}")
    
    finally:
        # Mark scraper as complete
        scraper_running = False
        scraper_results.append({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'action': 'Scraper finished',
            'status': 'Complete',
            'data_collected': 'All data collection complete'
        })
        print("Scraper simulation completed.")