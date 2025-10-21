#!/usr/bin/env python3
"""
QCF Web Service - FIXED Authentication Version
"""

import sys
import os
import time
from flask import Flask, render_template, jsonify, request, redirect, make_response

app = Flask(__name__)
app.secret_key = 'qcf_fixed_auth_2024'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Prevent caching

# Simple session storage
active_sessions = {}

@app.route('/')
def index():
    return redirect('/admin/login')

@app.route('/admin/login')
def admin_login():
    # Clear any existing session
    response = make_response(render_template('admin_login.html'))
    response.set_cookie('qcf_session', '', expires=0)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/admin/dashboard')
def admin_dashboard():
    session_id = request.cookies.get('qcf_session')
    
    # Check if session is valid
    if session_id in active_sessions:
        session_data = active_sessions[session_id]
        # Check if session is not expired (1 hour)
        if time.time() - session_data['login_time'] < 3600:
            response = make_response(render_template('admin_dashboard.html'))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return response
    
    # Invalid session, redirect to login
    return redirect('/admin/login')

@app.route('/api/admin/login', methods=['POST'])
def api_admin_login():
    try:
        data = request.get_json()
        username = data.get('username', '').strip().lower()
        password = data.get('password', '').strip()
        
        print(f"Login attempt for user: {username}")
        
        # Simple authentication
        valid_users = {
            'admin': 'insa2024',
            'insa': 'ethiopia2024'
        }
        
        if username in valid_users and valid_users[username] == password:
            # Create new session
            session_id = f"session_{int(time.time())}_{username}"
            active_sessions[session_id] = {
                'username': username,
                'login_time': time.time(),
                'ip': request.remote_addr
            }
            
            print(f"Login successful for {username}, session created: {session_id}")
            
            response = jsonify({
                'success': True, 
                'message': 'Login successful',
                'user': username
            })
            response.set_cookie('qcf_session', session_id, max_age=3600, httponly=True)
            return response
        else:
            print(f"Login failed for {username}")
            return jsonify({
                'success': False, 
                'error': 'Invalid username or password'
            })
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'error': 'Server error'})

@app.route('/api/admin/threats')
def api_admin_threats():
    session_id = request.cookies.get('qcf_session')
    if session_id not in active_sessions:
        return jsonify({'error': 'Unauthorized'}), 401
    
    threats = [
        {'type': 'Port Scan', 'count': 15, 'severity': 'Medium', 'trend': 'increasing'},
        {'type': 'DDoS Attack', 'count': 3, 'severity': 'High', 'trend': 'stable'},
        {'type': 'SQL Injection', 'count': 8, 'severity': 'High', 'trend': 'decreasing'},
        {'type': 'Malware', 'count': 5, 'severity': 'Critical', 'trend': 'increasing'},
    ]
    return jsonify(threats)

@app.route('/api/admin/users')
def api_admin_users():
    session_id = request.cookies.get('qcf_session')
    if session_id not in active_sessions:
        return jsonify({'error': 'Unauthorized'}), 401
    
    users = [
        {'username': 'admin', 'role': 'superadmin', 'last_login': '2024-01-15 10:30:00', 'status': 'active'},
        {'username': 'insa', 'role': 'admin', 'last_login': '2024-01-15 09:15:00', 'status': 'active'},
    ]
    return jsonify(users)  

@app.route('/api/admin/logout')
def api_admin_logout():
    session_id = request.cookies.get('qcf_session')
    
    if session_id in active_sessions:
        username = active_sessions[session_id]['username']
        del active_sessions[session_id]
        print(f"User {username} logged out")
    
    # Create redirect response with cookie clearing
    response = redirect('/admin/login')
    response.set_cookie('qcf_session', '', expires=0)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

@app.route('/api/admin/check_session')
def api_check_session():
    session_id = request.cookies.get('qcf_session')
    
    if session_id in active_sessions:
        session_data = active_sessions[session_id]
        if time.time() - session_data['login_time'] < 3600:
            return jsonify({'valid': True, 'user': session_data['username']})
    
    return jsonify({'valid': False})

@app.route('/api/admin/stats')
def api_admin_stats():
    session_id = request.cookies.get('qcf_session')
    
    # Verify session
    if session_id not in active_sessions:
        return jsonify({'error': 'Unauthorized'}), 401
    
    session_data = active_sessions[session_id]
    if time.time() - session_data['login_time'] >= 3600:
        return jsonify({'error': 'Session expired'}), 401
    
    return jsonify({
        'total_users': 150,
        'active_threats': 12,
        'system_health': 'Excellent',
        'quantum_accuracy': '98.5%',
        'packets_analyzed': 24567,
        'current_user': session_data['username']
    })

@app.route('/api/admin/logs')
def api_admin_logs():
    session_id = request.cookies.get('qcf_session')
    
    # Verify session
    if session_id not in active_sessions:
        return jsonify({'error': 'Unauthorized'}), 401
    
    logs = [
        {'timestamp': '2024-01-15 10:30:00', 'level': 'INFO', 'message': 'System initialized'},
        {'timestamp': '2024-01-15 10:31:00', 'level': 'WARNING', 'message': 'Suspicious activity detected'},
        {'timestamp': '2024-01-15 10:32:00', 'level': 'INFO', 'message': 'Threat blocked successfully'},
        {'timestamp': '2024-01-15 10:33:00', 'level': 'INFO', 'message': f"User {active_sessions[session_id]['username']} logged in"},
    ]
    return jsonify(logs)

# Clear expired sessions periodically
def clear_expired_sessions():
    current_time = time.time()
    expired_sessions = []
    
    for session_id, session_data in active_sessions.items():
        if current_time - session_data['login_time'] >= 3600:  # 1 hour
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        del active_sessions[session_id]
        print(f"Cleared expired session: {session_id}")

if __name__ == "__main__":
    print("🚀 Starting QCF Web Service - FIXED AUTH")
    print("📊 Admin Login: http://localhost:5000/admin/login")
    print("🔐 Username: admin, Password: insa2024")
    print("🔐 Username: insa, Password: ethiopia2024")
    print("🔄 Session timeout: 1 hour")
    print("⏹️  Press Ctrl+C to stop")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True) 
    