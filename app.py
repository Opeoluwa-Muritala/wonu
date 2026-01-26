from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
from flask_cors import CORS
import os
import json
from functools import wraps

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

DATA_FILE = 'content.json'

# --- 1. Load/Save Logic ---
# In app.py - Replace the default return in load_content() or the content.json structure

def load_content():
    if not os.path.exists(DATA_FILE):
        return {
            "site": { "brand": "Wonuola Ogundana", "badgeYear": "2026" },
            "hero": {
                "firstName": "Wonuola", 
                "lastName": "Ogundana",
                "subtitle": "A UI/UX designer passionate about designing meaningful products."
            },
            "social": {
                "email": "Wonuolaogundana@gmail.com",
                "linkedin": "#", "behance": "#", "resumeUrl": "#" 
            },
            # DATA FED FROM HERE
            "projects": [
                {
                    "id": "p01",
                    "number": "01",
                    "title": "Airxplora",
                    "category": "Travel Booking Platform",
                    "overview": "A seamless travel planning platform for flights and hotels.",
                    # Note: We use 'filename' for static images
                    "image": "User Dashboard Flights.png",
                    "color": "pink" 
                },
                {
                    "id": "p02",
                    "number": "02",
                    "title": "Arcabill",
                    "category": "Utility Payment Dashboard",
                    "overview": "Manage electricity, airtime, and subscriptions in one place.",
                    "image": "Dashboard (2).png",
                    "color": "blue"
                },
                {
                    "id": "p03",
                    "number": "03",
                    "title": "AV Card",
                    "category": "Virtual Banking App",
                    "overview": "Smarter virtual cards for online payments.",
                    "image": "DASHBOARD (1).png",
                    "color": "purple"
                },
                {
                    "id": "p04",
                    "number": "04",
                    "title": "Datafrik",
                    "category": "Tech Analytics Landing",
                    "overview": "Empowering businesses with data-driven insights.",
                    "image": "Landing page Redesign (1).png",
                    "color": "green"
                }
            ]
        }
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def save_content(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# --- 2. Context Processor (MAKES DATA AVAILABLE EVERYWHERE) ---
@app.context_processor
def inject_content():
    # This runs before every template render
    content = load_content()
    return dict(content=content)

# --- 3. Auth Decorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login_view'))
        return f(*args, **kwargs)
    return decorated_function

# --- 4. Routes ---

@app.route('/', methods=['GET'])
def home_view():
    content = load_content()
    # pass projects explicitly for the loop
    return render_template('index.html', projects=content.get('projects', []))

@app.route('/project/<projectid>', methods=['GET'])
def project_view_id(projectid):
    content = load_content()
    projects = content.get('projects', [])
    project = next((p for p in projects if p['id'] == projectid), None)
    if project is None: abort(404)
    return render_template('project-view.html', project=project)

# --- Admin & API ---

@app.route('/admin', methods=['GET'])
def login_view():
    return render_template('admin-login.html')

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard_view():
    return render_template('admin-edit.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    req = request.json
    if req.get('username') == 'admin' and req.get('password') == 'password':
        session['logged_in'] = True
        return jsonify({"success": True})
    return jsonify({"error": "Invalid"}), 401

@app.route('/api/content', methods=['GET', 'POST'])
@login_required
def handle_content():
    if request.method == 'POST':
        save_content(request.json)
        return jsonify({"success": True})
    return jsonify(load_content())

@app.route('/api/project/add', methods=['POST'])
@login_required
def add_project():
    content = load_content()
    req = request.json
    projects = content.get('projects', [])

    count = len(projects) + 1
    new_id = f"p{count:02d}"
    new_number = f"{count:02d}"

    new_proj = {
        "id": new_id,
        "number": new_number,
        "category": req.get('category', 'New Category'),
        "title": req.get('title', 'New Project'),
        "overview": req.get('overview', 'Description...'),
        "image": req.get('image', ''),
        "deliverables": ["UI Design", "UX Research"] 
    }
    
    projects.insert(0, new_proj)
    content['projects'] = projects
    save_content(content)
    return jsonify({"success": True})

# --- Static Pages ---
@app.route('/projects')
def project_view(): return render_template('projects.html', projects=load_content().get('projects', []))
@app.route('/about')
def about_view(): return render_template('about.html')
@app.route('/contact')
def contact_view(): return render_template('contact.html')
@app.route('/resume')
def resume_view(): return render_template('resume.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)