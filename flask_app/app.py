"""
PySpark Pro Tips Flask Web Application

A simple Flask application to browse PySpark guides and tips.
Designed for easy deployment on PythonAnywhere or Heroku.

Author: Byamba Enkhbat
License: MIT
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import os
import markdown
import sqlite3
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
BASE_DIR = Path(__file__).resolve().parent
GUIDES_DIR = BASE_DIR.parent / 'guides'
DATABASE_PATH = BASE_DIR / 'database' / 'data.sqlite'

# Ensure database directory exists
DATABASE_PATH.parent.mkdir(exist_ok=True)


def get_db():
    """Get database connection."""
    db = sqlite3.connect(str(DATABASE_PATH))
    db.row_factory = sqlite3.Row
    return db


def init_db():
    """Initialize the database with required tables."""
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS guide_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guide_name TEXT NOT NULL,
            view_count INTEGER DEFAULT 0,
            last_viewed TIMESTAMP
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            preference_key TEXT UNIQUE NOT NULL,
            preference_value TEXT NOT NULL
        )
    ''')
    
    # Set default theme if not exists
    try:
        db.execute(
            "INSERT INTO user_preferences (preference_key, preference_value) VALUES (?, ?)",
            ('homepage_design', 'modern')
        )
    except sqlite3.IntegrityError:
        pass  # Already exists
    
    db.commit()
    db.close()


def get_guide_list():
    """Get list of all available guides."""
    guides = []
    if GUIDES_DIR.exists():
        for guide_file in sorted(GUIDES_DIR.glob('*.md')):
            guide_name = guide_file.stem
            # Parse the title from filename (e.g., "01_dataframe_basics" -> "DataFrame Basics")
            title = guide_name.split('_', 1)[1].replace('_', ' ').title()
            guides.append({
                'filename': guide_name,
                'title': title,
                'number': guide_name.split('_')[0]
            })
    return guides


def get_guide_content(guide_name):
    """Read and convert markdown guide to HTML."""
    guide_path = GUIDES_DIR / f"{guide_name}.md"
    if guide_path.exists():
        with open(guide_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Convert markdown to HTML with extensions
        html_content = markdown.markdown(
            content,
            extensions=['fenced_code', 'tables', 'codehilite', 'toc']
        )
        return html_content
    return None


def increment_guide_view(guide_name):
    """Track guide views in database."""
    db = get_db()
    existing = db.execute(
        'SELECT * FROM guide_views WHERE guide_name = ?', (guide_name,)
    ).fetchone()
    
    if existing:
        db.execute(
            'UPDATE guide_views SET view_count = view_count + 1, last_viewed = ? WHERE guide_name = ?',
            (datetime.now(), guide_name)
        )
    else:
        db.execute(
            'INSERT INTO guide_views (guide_name, view_count, last_viewed) VALUES (?, ?, ?)',
            (guide_name, 1, datetime.now())
        )
    db.commit()
    db.close()


def get_current_design():
    """Get the current homepage design preference."""
    db = get_db()
    result = db.execute(
        'SELECT preference_value FROM user_preferences WHERE preference_key = ?',
        ('homepage_design',)
    ).fetchone()
    db.close()
    return result['preference_value'] if result else 'modern'


@app.route('/')
def index():
    """Homepage with selected design."""
    design = get_current_design()
    guides = get_guide_list()
    
    # Route to different design templates
    if design == 'minimalist':
        return render_template('index_minimalist.html', guides=guides)
    elif design == 'dashboard':
        return render_template('index_dashboard.html', guides=guides)
    else:  # default to modern
        return render_template('index_modern.html', guides=guides)


@app.route('/change-design/<design_name>')
def change_design(design_name):
    """Change the homepage design."""
    valid_designs = ['modern', 'minimalist', 'dashboard']
    if design_name in valid_designs:
        db = get_db()
        db.execute(
            'UPDATE user_preferences SET preference_value = ? WHERE preference_key = ?',
            (design_name, 'homepage_design')
        )
        db.commit()
        db.close()
        flash(f'Design changed to {design_name.title()}!', 'success')
    else:
        flash('Invalid design selection.', 'error')
    return redirect(url_for('index'))


@app.route('/guide/<guide_name>')
def view_guide(guide_name):
    """View a specific guide."""
    content = get_guide_content(guide_name)
    if content:
        increment_guide_view(guide_name)
        guides = get_guide_list()
        current_guide = next((g for g in guides if g['filename'] == guide_name), None)
        return render_template('guide.html', 
                             content=content, 
                             guide=current_guide,
                             guides=guides)
    else:
        flash('Guide not found.', 'error')
        return redirect(url_for('index'))


@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')


@app.route('/stats')
def stats():
    """View statistics about guide views."""
    db = get_db()
    stats = db.execute(
        'SELECT guide_name, view_count, last_viewed FROM guide_views ORDER BY view_count DESC'
    ).fetchall()
    db.close()
    return render_template('stats.html', stats=stats)


@app.errorhandler(404)
def not_found(e):
    """404 error handler."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """500 error handler."""
    return render_template('500.html'), 500


# Initialize database on first run
with app.app_context():
    init_db()


if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=5000)
