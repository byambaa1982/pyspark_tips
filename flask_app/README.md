# ⚡ PySpark Pro Tips - Flask Web Application

A beautiful, easy-to-deploy Flask web application that showcases your PySpark guides and tips. Perfect for sharing your knowledge with the community!

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](../LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-green)](https://flask.palletsprojects.com/)

---

## 🌟 Features

### 🎨 Three Beautiful Design Themes
Choose from three professionally designed homepage layouts:

1. **Modern Design** - Vibrant cards with gradient hero section
2. **Minimalist Design** - Clean, focused, distraction-free layout  
3. **Dashboard Design** - Organized by difficulty level with sidebar navigation

Switch between designs with a single click! Your preference is saved automatically.

### 📚 Guide Management
- Browse all 10 PySpark guides
- Beautiful markdown rendering with syntax highlighting
- Navigation sidebar for easy guide switching
- Previous/Next navigation between guides
- Responsive design works on all devices

### 📊 Analytics & Tracking
- SQLite database tracks guide views
- Statistics page shows most popular guides
- Preference management for design choices
- All data stored locally in `data.sqlite`

### 🚀 Easy Deployment
- Deploy to **PythonAnywhere** (free hosting!)
- Deploy to **Heroku** (also free!)
- Detailed step-by-step guides for non-technical users
- No prior deployment experience needed

---

## 📋 Prerequisites

- Python 3.11 or higher
- Git (for deployment)
- A PythonAnywhere or Heroku account (both have free tiers)

---

## 🚀 Quick Start - Local Development

### 1. Clone or Download This Repository

```bash
git clone https://github.com/YOUR-USERNAME/useful_pyspark.git
cd useful_pyspark/flask_app
```

### 2. Create a Virtual Environment

**On Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables (Optional)

```bash
# Copy the example file
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# Edit .env and add your secret key
```

### 5. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your web browser! 🎉

---

## 📁 Project Structure

```
flask_app/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Procfile                    # Heroku configuration
├── runtime.txt                 # Python version for Heroku
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── index_modern.html      # Modern design homepage
│   ├── index_minimalist.html  # Minimalist design homepage
│   ├── index_dashboard.html   # Dashboard design homepage
│   ├── guide.html             # Guide viewing page
│   ├── about.html             # About page
│   ├── stats.html             # Statistics page
│   ├── 404.html               # Error pages
│   └── 500.html
│
├── static/                     # Static files
│   ├── css/
│   │   └── styles.css         # Complete stylesheet for all designs
│   └── js/
│       └── (future JS files)
│
├── database/                   # SQLite database location
│   └── data.sqlite            # Auto-created on first run
│
├── deployment_guides/          # Step-by-step deployment guides
│   ├── DEPLOY_PYTHONANYWHERE.md
│   └── DEPLOY_HEROKU.md
│
└── README.md                   # This file!
```

---

## 🎨 Choosing Your Homepage Design

The application includes three distinct homepage designs:

### 🌈 Modern Design (Default)
- **Best for**: Professional presentation
- **Features**: Gradient hero, card-based layout, feature highlights
- **Color scheme**: Vibrant oranges and blues
- **Perfect for**: Public-facing educational sites

### ✨ Minimalist Design
- **Best for**: Focused learning experience
- **Features**: Clean lines, lots of whitespace, simple list layout
- **Color scheme**: Black, white, and gray
- **Perfect for**: Distraction-free browsing

### 📊 Dashboard Design
- **Best for**: Structured learning paths
- **Features**: Sidebar navigation, organized by difficulty level
- **Color scheme**: Purple gradients with level badges
- **Perfect for**: Course-like progression

**To change design**: Use the "Change Design" dropdown in the navigation menu.

---

## 🗄️ Database Schema

The app uses SQLite with two tables:

### `guide_views`
Tracks how many times each guide has been viewed.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| guide_name | TEXT | Name of the guide file |
| view_count | INTEGER | Number of views |
| last_viewed | TIMESTAMP | Last view date/time |

### `user_preferences`
Stores user preferences like selected design theme.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| preference_key | TEXT | Setting name (e.g., 'homepage_design') |
| preference_value | TEXT | Setting value (e.g., 'modern') |

---

## 🌐 Deployment Options

### Option 1: PythonAnywhere (Recommended for Beginners)

**Pros:**
- ✅ Completely free forever
- ✅ No credit card required
- ✅ Simple web-based interface
- ✅ Perfect for Python projects
- ✅ Persistent file storage

**Cons:**
- ❌ App URL includes "pythonanywhere.com"
- ❌ App may sleep after inactivity (free tier)

📖 **[Full PythonAnywhere Deployment Guide](deployment_guides/DEPLOY_PYTHONANYWHERE.md)**

### Option 2: Heroku

**Pros:**
- ✅ Free tier available
- ✅ Professional deployment platform
- ✅ Git-based deployments
- ✅ Easy to scale later
- ✅ Clean herokuapp.com URLs

**Cons:**
- ❌ App sleeps after 30 minutes of inactivity (free tier)
- ❌ Free tier database doesn't persist
- ❌ Requires command line usage

📖 **[Full Heroku Deployment Guide](deployment_guides/DEPLOY_HEROKU.md)**

---

## 🛠️ Customization Guide

### Change the App Name and Branding

Edit `templates/base.html`:
```html
<a href="{{ url_for('index') }}" class="logo">⚡ Your App Name</a>
```

### Modify Colors

Edit `static/css/styles.css` - change CSS variables:
```css
:root {
    --primary-color: #FF6B35;      /* Main accent color */
    --secondary-color: #004E89;    /* Secondary accent */
    --accent-color: #F7931E;       /* Highlights */
}
```

### Add More Pages

1. Create a new template in `templates/`
2. Add a route in `app.py`:
```python
@app.route('/mypage')
def my_page():
    return render_template('mypage.html')
```
3. Add a link in `templates/base.html`

### Customize Database

Add more tables by editing the `init_db()` function in `app.py`.

---

## 📊 Monitoring Your App

### View Statistics

Visit `/stats` on your deployed app to see:
- Which guides are most popular
- Total view counts
- Last viewed dates

### Check Logs

**PythonAnywhere:**
- Go to Web tab → Error log

**Heroku:**
```bash
heroku logs --tail
```

---

## 🔧 Troubleshooting

### Guides Don't Show Up

**Problem**: No guides displayed on homepage.

**Solution**: 
1. Verify the guides folder path in `app.py`
2. Check that `.md` files exist in `../guides/`
3. Ensure folder structure matches expected layout

### Database Errors

**Problem**: "Database locked" or similar errors.

**Solution**:
```python
# In a Python console
from app import init_db
init_db()
```

### CSS Not Loading

**Problem**: Website has no styling.

**Solution**:
1. Check that `static/css/styles.css` exists
2. Verify static files are properly deployed
3. Clear browser cache (Ctrl + F5)

### Import Errors

**Problem**: `ModuleNotFoundError` or import issues.

**Solution**:
```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test locally
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Create a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

## 👨‍💻 Author

**Byamba Enkhbat**  
Data Engineer & Analytics Professional

- Website: [DataLogicHub.com](https://www.datalogichub.com)
- Website: [DataLogicHub.net](https://www.datalogichub.net)
- GitHub: [@byambaa1982](https://github.com/byambaa1982)

---

## 🙏 Acknowledgments

- Flask web framework
- Python-Markdown for markdown rendering
- Highlight.js for code syntax highlighting
- The PySpark community

---

## 📚 Related Projects

- **Main Repository**: [useful_pyspark](https://github.com/byambaa1982/useful_pyspark)
- **PySpark Documentation**: [spark.apache.org](https://spark.apache.org/docs/latest/api/python/)

---

## 🎓 Learning Resources

After deploying this app, you'll have learned:
- ✅ Flask web development
- ✅ SQLite database integration
- ✅ Template rendering with Jinja2
- ✅ Static file management
- ✅ Markdown processing
- ✅ Web deployment to cloud platforms
- ✅ Environment configuration
- ✅ Git-based workflows

---

## 📞 Support

- **Issues**: Create an issue on GitHub
- **Questions**: Check deployment guides first
- **Updates**: Watch the repository for updates

---

## 🎯 Roadmap

Future enhancements (contributions welcome!):

- [ ] User authentication and accounts
- [ ] Bookmarking favorite guides
- [ ] Search functionality
- [ ] Comments section for guides
- [ ] Code snippet testing in-browser
- [ ] Dark mode toggle
- [ ] More design themes
- [ ] Export guides as PDF
- [ ] API endpoints for guide content
- [ ] Mobile app version

---

## 🎉 Quick Start Summary

**For Local Development:**
```bash
cd flask_app
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux
pip install -r requirements.txt
python app.py
```

**For Deployment:**
- 📖 Read [DEPLOY_PYTHONANYWHERE.md](deployment_guides/DEPLOY_PYTHONANYWHERE.md) or
- 📖 Read [DEPLOY_HEROKU.md](deployment_guides/DEPLOY_HEROKU.md)

---

**Ready to deploy?** Choose your platform and follow the detailed guides!

**Questions?** Open an issue or check the deployment guides!

**Happy deploying!** 🚀✨
