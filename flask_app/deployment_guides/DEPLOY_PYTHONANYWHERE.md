# 🚀 Deploy to PythonAnywhere - Step by Step Guide

This guide will help you deploy your PySpark Pro Tips Flask app to PythonAnywhere, even if you've never done it before!

---

## 📋 What You'll Need

- A free PythonAnywhere account (sign up at [www.pythonanywhere.com](https://www.pythonanywhere.com))
- Your GitHub repository URL (if using Git) OR your files ready to upload
- About 15-20 minutes

---

## 🎯 Step-by-Step Instructions

### Step 1: Create a PythonAnywhere Account

1. Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Click the **"Pricing & signup"** button at the top
3. Choose the **"Create a Beginner account"** (it's FREE!)
4. Fill in your details:
   - Username (this will be part of your website URL)
   - Email address
   - Password
5. Click **"Register"**
6. Check your email and verify your account

> 💡 **Tip**: Choose a good username because your website will be at `yourusername.pythonanywhere.com`

---

### Step 2: Upload Your Files

**Option A: Using Git (Recommended)**

1. After logging in, click on **"Consoles"** in the top menu
2. Click **"Bash"** to open a new console
3. In the console, type these commands one by one:

```bash
git clone https://github.com/YOUR-USERNAME/useful_pyspark.git
cd useful_pyspark/flask_app
```

Replace `YOUR-USERNAME` with your actual GitHub username.

**Option B: Upload Files Manually**

1. Click on **"Files"** in the top menu
2. Navigate to `/home/yourusername/`
3. Click **"Upload a file"** button
4. Upload all your Flask app files
5. Make sure to maintain the folder structure:
   ```
   flask_app/
   ├── app.py
   ├── requirements.txt
   ├── templates/
   ├── static/
   └── database/
   ```

---

### Step 3: Set Up a Virtual Environment

1. Go to **"Consoles"** → Open a **"Bash"** console
2. Type these commands:

```bash
cd useful_pyspark/flask_app
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Wait for all packages to install (this might take 2-3 minutes).

> ⏰ **What's happening?** These commands create a separate space for your app's packages so they don't conflict with other projects.

---

### Step 4: Create a Web App

1. Click on **"Web"** in the top menu
2. Click **"Add a new web app"** button
3. Click **"Next"** on the domain name page (it shows your free domain)
4. Select **"Manual configuration"** (NOT the Flask option!)
5. Choose **"Python 3.11"**
6. Click **"Next"**

---

### Step 5: Configure the Web App

Now you'll see a configuration page with several sections:

#### A. Set the Source Code Directory

1. Find the **"Code"** section
2. Click on the path next to **"Source code:"**
3. Change it to: `/home/yourusername/useful_pyspark/flask_app`
   (Replace `yourusername` with your actual username)

#### B. Set the Working Directory

1. In the same section, find **"Working directory:"**
2. Set it to: `/home/yourusername/useful_pyspark/flask_app`

#### C. Configure the Virtual Environment

1. Find the **"Virtualenv"** section
2. Click the link that says **"Enter path to a virtualenv"**
3. Type: `/home/yourusername/useful_pyspark/flask_app/venv`
4. Click the checkmark to save

#### D. Edit the WSGI File

1. Find the **"Code"** section again
2. Click on the **"WSGI configuration file"** link (something like `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. You'll see a file editor. **Delete everything** in the file
4. Copy and paste this code:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/useful_pyspark/flask_app'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set up environment
os.chdir(project_home)

# Import flask app
from app import app as application
```

5. **IMPORTANT**: Replace `yourusername` with your actual PythonAnywhere username
6. Click **"Save"** at the top

---

### Step 6: Copy the Guides Folder Path

Since your guides are in a different folder, you need to make sure the path is correct:

1. Go back to **"Consoles"** → **"Bash"**
2. Type:
```bash
ls /home/yourusername/useful_pyspark/guides/
```

This should show all your guide files. If it does, the path is correct!

---

### Step 7: Launch Your Website! 🎉

1. Go back to the **"Web"** tab
2. Scroll to the top
3. Click the big green **"Reload"** button
4. Wait about 10 seconds
5. Click on your website link at the top (something like `yourusername.pythonanywhere.com`)

**Your website should now be live!** 🎊

---

## ✅ Testing Your Deployment

Check these things to make sure everything works:

- [ ] Homepage loads and shows the design selector
- [ ] You can switch between Modern, Minimalist, and Dashboard designs
- [ ] Clicking on a guide shows the guide content
- [ ] Navigation sidebar works
- [ ] "About" and "Stats" pages load

---

## 🔧 Troubleshooting

### Problem: Website shows "Something went wrong"

**Solution**:
1. Go to **"Web"** tab
2. Scroll down to **"Log files"**
3. Click on **"Error log"**
4. Look for red error messages
5. Most common issue: Check that all paths use your correct username

### Problem: Guides don't show up

**Solution**:
1. Check that the guides folder exists at `/home/yourusername/useful_pyspark/guides/`
2. Make sure the folder contains `.md` files
3. In the WSGI file, make sure the path is correct

### Problem: Can't see the CSS styling

**Solution**:
1. Go to **"Web"** tab
2. Scroll to **"Static files"**
3. Add a new entry:
   - URL: `/static/`
   - Directory: `/home/yourusername/useful_pyspark/flask_app/static/`
4. Click checkmark to save
5. Click **"Reload"** button

### Problem: Database errors

**Solution**:
The database is created automatically. If you see errors:
1. Go to Bash console
2. Type:
```bash
cd /home/yourusername/useful_pyspark/flask_app
python3
```
3. Then type:
```python
from app import init_db
init_db()
exit()
```
4. Reload your web app

---

## 🎨 Changing the Default Design

To set which design shows by default:

1. Visit your website
2. Use the **"Change Design"** dropdown menu
3. Select your preferred design
4. The choice is saved in the database and will persist

---

## 📊 Viewing Your Stats

1. Visit: `yourusername.pythonanywhere.com/stats`
2. See which guides are most viewed
3. Stats are tracked automatically in the SQLite database

---

## 🔄 Updating Your Website

When you make changes to your code:

**If using Git:**
```bash
cd /home/yourusername/useful_pyspark/flask_app
git pull origin main
```

**If uploading manually:**
1. Upload the changed files via the "Files" tab

**Then always:**
1. Go to "Web" tab
2. Click "Reload" button

---

## 💡 Tips for Success

1. **Bookmark your Web tab**: You'll use the Reload button often
2. **Check Error logs**: If something breaks, the error log tells you why
3. **Free account limits**: 
   - Your site will sleep if not visited for a while (it wakes up automatically)
   - Limited to 512 MB disk space
   - One web app on free account
4. **Custom domain**: Upgrade to paid account if you want your own domain name

---

## 🆘 Getting Help

- **PythonAnywhere Forums**: [www.pythonanywhere.com/forums/](https://www.pythonanywhere.com/forums/)
- **PythonAnywhere Help**: Click "Help" at the top of PythonAnywhere
- **Check the error log**: Most issues are explained there

---

## 🎓 What You've Learned

Congratulations! You've:
- ✅ Created a PythonAnywhere account
- ✅ Set up a Python virtual environment
- ✅ Configured a Flask web application
- ✅ Deployed a live website to the internet
- ✅ Learned how to troubleshoot common issues

Your PySpark Pro Tips website is now accessible to anyone in the world! Share your URL with others and help them learn PySpark! 🚀

---

## 📝 Quick Reference

| Task | Location | Action |
|------|----------|--------|
| Update code | Bash Console | `git pull` or upload files |
| Apply changes | Web tab | Click "Reload" |
| Check errors | Web tab | View "Error log" |
| View files | Files tab | Browse and edit |
| Change settings | Web tab | Edit configuration |

---

**Need help?** Create an issue on GitHub or check the PythonAnywhere forums!
