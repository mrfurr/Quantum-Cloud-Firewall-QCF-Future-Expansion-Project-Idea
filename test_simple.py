from flask import Flask, render_template, jsonify, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/admin/login')

@app.route('/admin/login')
def login():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>QCF Test</title>
        <style>
            body { background: #0c0c0c; color: white; font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; }
            .login-box { background: rgba(255,255,255,0.1); padding: 40px; border-radius: 10px; }
            input { display: block; margin: 10px 0; padding: 10px; width: 200px; }
            button { padding: 10px 20px; background: #00ff88; border: none; border-radius: 5px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>QCF Test Login</h2>
            <form id="loginForm">
                <input type="text" id="username" placeholder="Username" value="admin">
                <input type="password" id="password" placeholder="Password" value="insa2024">
                <button type="submit">Login</button>
            </form>
            <div id="message" style="margin-top: 10px;"></div>
        </div>
        
        <script>
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, password})
                });
                
                const data = await response.json();
                document.getElementById('message').textContent = data.message;
                
                if (data.success) {
                    setTimeout(() => window.location.href = '/dashboard', 1000);
                }
            });
        </script>
    </body>
    </html>
    """

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if data.get('username') == 'admin' and data.get('password') == 'insa2024':
        return jsonify({'success': True, 'message': 'Login successful! Redirecting...'})
    return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/dashboard')
def dashboard():
    return "<h1>Dashboard - Login Successful!</h1><p><a href='/'>Back to login</a></p>"

if __name__ == '__main__':
    print("🔧 Testing simple login...")
    print("🌐 http://localhost:5000")
    app.run(debug=True)  