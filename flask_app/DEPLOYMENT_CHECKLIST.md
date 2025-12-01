# ✅ Pre-Deployment Checklist

Use this checklist before deploying to ensure everything is ready!

---

## 📋 Files Checklist

### Core Application Files
- [ ] `app.py` - Main Flask application exists
- [ ] `requirements.txt` - All dependencies listed
- [ ] `.gitignore` - Git ignore file present
- [ ] `Procfile` - Heroku configuration (for Heroku deployment)
- [ ] `runtime.txt` - Python version specified (for Heroku)

### Template Files
- [ ] `templates/base.html` - Base template
- [ ] `templates/index_modern.html` - Modern design
- [ ] `templates/index_minimalist.html` - Minimalist design
- [ ] `templates/index_dashboard.html` - Dashboard design
- [ ] `templates/guide.html` - Guide viewing page
- [ ] `templates/about.html` - About page
- [ ] `templates/stats.html` - Statistics page
- [ ] `templates/404.html` - Error page
- [ ] `templates/500.html` - Error page

### Static Files
- [ ] `static/css/styles.css` - Main stylesheet

### Documentation Files
- [ ] `README.md` - Main documentation
- [ ] `QUICKSTART.md` - Quick start guide
- [ ] `deployment_guides/DEPLOY_PYTHONANYWHERE.md` - PythonAnywhere guide
- [ ] `deployment_guides/DEPLOY_HEROKU.md` - Heroku guide
- [ ] `.env.example` - Environment variables example

### Content Files
- [ ] `../guides/` folder exists with `.md` files
- [ ] At least one guide file present

---

## 🧪 Local Testing Checklist

### Before Deployment, Test These:

- [ ] App runs locally without errors (`python app.py`)
- [ ] Homepage loads successfully
- [ ] Can switch between all three designs
- [ ] Design preference is saved
- [ ] At least one guide displays correctly
- [ ] Guide navigation (Previous/Next) works
- [ ] Sidebar navigation works
- [ ] About page loads
- [ ] Stats page loads
- [ ] 404 page shows for invalid URLs
- [ ] Code syntax highlighting works
- [ ] Tables render properly in guides
- [ ] Responsive design works (resize browser)

---

## 🔐 Security Checklist

- [ ] Change `SECRET_KEY` in production (use `.env` file)
- [ ] `.env` file is in `.gitignore`
- [ ] No sensitive data hardcoded in `app.py`
- [ ] Database file (`data.sqlite`) is in `.gitignore`

---

## 🌐 Pre-Deployment Setup

### For PythonAnywhere:
- [ ] PythonAnywhere account created
- [ ] Know your username
- [ ] Have repository URL (if using Git)

### For Heroku:
- [ ] Heroku account created
- [ ] Heroku CLI installed
- [ ] Git repository initialized
- [ ] All changes committed to Git
- [ ] Chosen app name (or will use random)

---

## 📝 Configuration Checklist

- [ ] `GUIDES_DIR` path in `app.py` is correct
- [ ] `DATABASE_PATH` in `app.py` is correct
- [ ] All template paths are correct
- [ ] Static file paths are correct

---

## 🚀 Ready to Deploy!

### Choose Your Platform:

**Option A: PythonAnywhere** (Recommended for Beginners)
- ✅ All checkboxes above are checked
- 📖 Follow [DEPLOY_PYTHONANYWHERE.md](deployment_guides/DEPLOY_PYTHONANYWHERE.md)

**Option B: Heroku** (More Technical)
- ✅ All checkboxes above are checked
- ✅ Git repository is ready
- 📖 Follow [DEPLOY_HEROKU.md](deployment_guides/DEPLOY_HEROKU.md)

---

## 🎯 Post-Deployment Checklist

After deploying, verify these:

- [ ] Website loads without errors
- [ ] Homepage displays correctly
- [ ] Can view at least one guide
- [ ] Design switcher works
- [ ] Navigation works
- [ ] About page loads
- [ ] Stats page loads (may be empty initially)
- [ ] No console errors (press F12 in browser)
- [ ] Mobile view works (test on phone or resize browser)

---

## 🐛 If Something Goes Wrong

### First Steps:
1. Check error logs (platform specific)
2. Verify all files uploaded correctly
3. Check that folder structure is maintained
4. Ensure all dependencies installed

### Platform-Specific Help:
- **PythonAnywhere**: Check Error Log in Web tab
- **Heroku**: Run `heroku logs --tail`

### Common Issues:
- **Guides don't show**: Check `GUIDES_DIR` path
- **No styling**: Verify static files deployed
- **Database errors**: Database may need initialization
- **Import errors**: Re-install requirements

---

## 📊 Success Metrics

Your deployment is successful when:
- ✅ Website is accessible via public URL
- ✅ All pages load without errors
- ✅ Guides display with formatting
- ✅ Design switching works
- ✅ Stats are tracked
- ✅ Mobile-friendly

---

## 🎉 Deployment Complete!

Once all checks pass:
1. Share your URL with others
2. Test from different devices
3. Monitor error logs first few days
4. Enjoy your live website!

---

## 📞 Need Help?

- Review deployment guides
- Check troubleshooting sections
- Create GitHub issue
- Check platform documentation

---

**Last updated**: December 1, 2025
