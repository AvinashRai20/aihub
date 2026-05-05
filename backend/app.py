from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, 
            static_folder='../frontend', 
            template_folder='../frontend',
            static_url_path='')

app.secret_key = 'ai_hub_pro_secret_key' # For session management

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_FILE = os.path.join(BASE_DIR, 'tools.json')
USERS_FILE = os.path.join(BASE_DIR, 'users.json')

# Ensure users file exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([], f)

# Helper function to get tools
def get_tools_data():
    with open(TOOLS_FILE, 'r') as f:
        return json.load(f)

# Helper function to get users
def get_users_data():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    # Basic admin protection
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

# API Endpoints
@app.route('/api/tools', methods=['GET'])
def get_tools():
    return jsonify(get_tools_data())

@app.route('/api/tools', methods=['POST'])
def add_tool():
    if not session.get('is_admin'):
        return jsonify({"error": "Unauthorized"}), 401
    new_tool = request.json
    tools = get_tools_data()
    tools.append(new_tool)
    with open(TOOLS_FILE, 'w') as f:
        json.dump(tools, f, indent=4)
    return jsonify({"message": "Tool added successfully!"})

@app.route('/api/tools/<string:name>', methods=['DELETE'])
def delete_tool(name):
    if not session.get('is_admin'):
        return jsonify({"error": "Unauthorized"}), 401
    tools = get_tools_data()
    tools = [t for t in tools if t['name'] != name]
    with open(TOOLS_FILE, 'w') as f:
        json.dump(tools, f, indent=4)
    return jsonify({"message": "Tool deleted successfully!"})

@app.route('/api/stats')
def get_stats():
    tools = get_tools_data()
    users = get_users_data()
    return jsonify({
        "toolCount": len(tools),
        "userCount": 50000 + len(users) # Base 50k + new users
    })

# Auth Logic
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    users = get_users_data()
    if any(u['username'] == username for u in users):
        return jsonify({"error": "User already exists"}), 400
    
    hashed_password = generate_password_hash(password)
    users.append({"username": username, "password": hashed_password})
    
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)
    
    return jsonify({"message": "Registration successful!"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Special Admin Account
    if username == "admin" and password == "admin123":
        session['is_admin'] = True
        session['user'] = "Admin"
        return jsonify({"message": "Admin Login Successful!", "redirect": "/admin"})

    users = get_users_data()
    user = next((u for u in users if u['username'] == username), None)
    
    if user and check_password_hash(user['password'], password):
        session['user'] = username
        return jsonify({"message": "Login successful!", "redirect": "/"})
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
