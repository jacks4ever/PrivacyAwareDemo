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
    
    # Start the scraper in a background thread
    scraper_thread = threading.Thread(target=run_scraper)
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
    
    base_url = request.host_url.rstrip('/')
    
    # Simulate scraper running
    scraper_running = True
    
    try:
        # Step 1: Get all users (demonstrates email leak)
        scraper_results.append({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'action': 'Scraping all users',
            'url': f'{base_url}/api/users',
            'status': 'In progress'
        })
        
        response = requests.get(f'{base_url}/api/users')
        users = response.json()
        
        scraper_results[-1]['status'] = 'Complete'
        scraper_results[-1]['data_collected'] = f'Found {len(users)} users with emails and privacy settings'
        
        time.sleep(2)  # Simulate processing time
        
        # Step 2: Get all posts (demonstrates private post leak)
        scraper_results.append({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'action': 'Scraping all posts',
            'url': f'{base_url}/api/posts',
            'status': 'In progress'
        })
        
        response = requests.get(f'{base_url}/api/posts')
        posts = response.json()
        
        scraper_results[-1]['status'] = 'Complete'
        scraper_results[-1]['data_collected'] = f'Found {len(posts)} posts including private ones'
        
        time.sleep(2)  # Simulate processing time
        
        # Step 3: Get deleted posts (demonstrates deleted data leak)
        scraper_results.append({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'action': 'Scraping deleted posts',
            'url': f'{base_url}/api/posts/all',
            'status': 'In progress'
        })
        
        response = requests.get(f'{base_url}/api/posts/all')
        all_posts = response.json()
        
        deleted_posts = [p for p in all_posts if p.get('is_deleted')]
        
        scraper_results[-1]['status'] = 'Complete'
        scraper_results[-1]['data_collected'] = f'Found {len(deleted_posts)} deleted posts that should be inaccessible'
        
        time.sleep(2)  # Simulate processing time
        
        # Step 4: Get detailed user information for each user
        for user in users[:3]:  # Limit to first 3 users for demo
            user_id = user['id']
            scraper_results.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'action': f'Scraping detailed info for user {user["username"]}',
                'url': f'{base_url}/api/users/{user_id}',
                'status': 'In progress'
            })
            
            response = requests.get(f'{base_url}/api/users/{user_id}')
            user_detail = response.json()
            
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
    
    finally:
        # Mark scraper as complete
        scraper_running = False
        scraper_results.append({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'action': 'Scraper finished',
            'status': 'Complete',
            'data_collected': 'All data collection complete'
        })