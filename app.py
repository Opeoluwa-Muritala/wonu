from flask import Flask, render_template, request, redirect, flash, url_for, session, jsonify, abort
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY')

PROJECTS = [
    {
        "id": "p05",
        "number": "05",
        "title": "SNP Website Redesign",
        "category": "Website Design",
        "overview": "A redesign concept focused on showcasing spaces...",
        "deliverables": ["Homepage layout", "Team section", "Responsive behavior"],
        # NEW: Background Image URL
        "image": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=1600&q=80"
    },
    {
        "id": "p04",
        "number": "04",
        "title": "JobID",
        "category": "Product Design",
        "overview": "A comprehensive case study regarding job identification...",
        "deliverables": ["User Research", "Wireframing", "UI Design"],
        # NEW: Background Image URL
        "image": "https://images.unsplash.com/photo-1545239351-1141bd82e8a6?auto=format&fit=crop&w=1600&q=80"
    }
]

@app.route('/', methods=['GET'])
def home_view():
    return render_template('index.html', projects=PROJECTS)
@app.route('/projects', methods=['GET'])
def project_view():
    return render_template('projects.html', projects=PROJECTS)
@app.route('/about', methods=['GET'])
def about_view():
    return render_template('about.html')

@app.route('/contact', methods=['GET'])
def contact_view():
    return render_template('contact.html')

@app.route('/resume', methods=['GET'])
def resume_view():
    return render_template('resume.html')

@app.route('/project/<projectid>', methods=['GET', 'POST'])
def project_view_id(projectid):
    project = next((p for p in PROJECTS if p['id'] == projectid), None)
    
    if project is None:
        abort(404) 

    return render_template('project-view.html', project=project)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug=True)