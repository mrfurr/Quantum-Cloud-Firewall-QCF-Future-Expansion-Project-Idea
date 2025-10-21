import time

class AdminAuth:
    def __init__(self):
        self.sessions = {}
        self.users = {
            'admin': {'password': 'insa2024', 'role': 'superadmin'},
            'insa': {'password': 'ethiopia2024', 'role': 'admin'}
        }
    
    def login(self, username, password):
        username = username.lower()
        if username in self.users and self.users[username]['password'] == password:
            session_id = f"session_{int(time.time())}_{username}"
            self.sessions[session_id] = {
                'username': username,
                'role': self.users[username]['role'],
                'login_time': time.time()
            }
            return session_id
        return None
    
    def validate_session(self, session_id):
        if session_id in self.sessions:
            # Check if session is not expired (24 hours)
            if time.time() - self.sessions[session_id]['login_time'] < 86400:
                return self.sessions[session_id]
        return None
    
    def logout(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

# Global instance
auth_manager = AdminAuth() 