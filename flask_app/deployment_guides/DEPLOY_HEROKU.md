# 🚀 Deploy to Heroku - Step by Step Guide

This guide will help you deploy your PySpark Pro Tips Flask app to Heroku, even if you've never done it before!

---

## 📋 What You'll Need

- A free Heroku account (sign up at [www.heroku.com](https://www.heroku.com))
- Git installed on your computer
- Your code in a Git repository (GitHub recommended)
- About 20-25 minutes

---

## 🎯 Step-by-Step Instructions

### Step 1: Create a Heroku Account

1. Go to [www.heroku.com](https://www.heroku.com)
2. Click **"Sign Up"** in the top right
3. Fill in your information:
   - First Name
   - Last Name
   - Email Address
   - Country
   - Role (choose "Student" or "Professional")
   - Primary Development Language (choose "Python")
4. Click **"Create Free Account"**
5. Check your email and click the confirmation link
6. Set a password when prompted

> 💡 **Tip**: Heroku is completely free for learning and small projects!

---

### Step 2: Install Heroku CLI (Command Line Interface)

The Heroku CLI lets you control Heroku from your computer's command line.

**For Windows:**
1. Go to [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
2. Download the Windows installer
3. Run the installer (just keep clicking "Next")
4. After installation, open **PowerShell** or **Command Prompt**
5. Test it by typing: `heroku --version`
   - You should see a version number

**For Mac:**
1. Open **Terminal**
2. Type: `brew tap heroku/brew && brew install heroku`
3. Test it by typing: `heroku --version`

**For Linux:**
1. Open **Terminal**
2. Type: `curl https://cli-assets.heroku.com/install.sh | sh`
3. Test it by typing: `heroku --version`

---

### Step 3: Prepare Your Files

Make sure you have all these files in your `flask_app` folder:

✅ `app.py` - Your Flask application  
✅ `requirements.txt` - Python packages  
✅ `Procfile` - Tells Heroku how to run your app  
✅ `runtime.txt` - Specifies Python version  
✅ `.gitignore` - Lists files to not upload  

**These files are already created for you!** But let's verify:

1. Open PowerShell or Terminal
2. Navigate to your flask_app folder:
```bash
cd c:\Users\Byamba\byamba\github_pin\useful_pyspark\flask_app
```

3. List the files:
```bash
dir  # On Windows
ls   # On Mac/Linux
```

You should see all the files listed above.

---

### Step 4: Initialize Git (If Not Already Done)

If your project isn't already in Git:

1. In your flask_app folder, type:
```bash
git init
git add .
git commit -m "Initial commit for Flask app"
```

If you already have Git set up, just make sure everything is committed:
```bash
git add .
git commit -m "Prepare for Heroku deployment"
```

---

### Step 5: Login to Heroku

1. In your terminal/PowerShell, type:
```bash
heroku login
```

2. Press any key (it will open your web browser)
3. Click **"Log In"** in the browser
4. Return to your terminal

You should see a message like "Logged in as your-email@example.com"

---

### Step 6: Create a Heroku App

1. In your terminal, type:
```bash
heroku create your-app-name-here
```

Replace `your-app-name-here` with a unique name. For example:
- `pyspark-tips-byamba`
- `my-pyspark-guide`
- `awesome-spark-tutorial`

> 💡 **Tips for naming:**
> - Use only lowercase letters, numbers, and hyphens
> - The name must be unique across all of Heroku
> - If the name is taken, try adding numbers: `pyspark-tips-2025`

**Or** just type `heroku create` without a name, and Heroku will create a random name for you!

You'll see output like:
```
Creating app... done, ⬢ your-app-name
https://your-app-name.herokuapp.com/ | https://git.heroku.com/your-app-name.git
```

**Save that URL!** That's your website address!

---

### Step 7: Configure Environment Variables

Set your secret key for Flask:

```bash
heroku config:set SECRET_KEY=your-super-secret-random-key-here-change-this
```

You can generate a random key using Python:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as your SECRET_KEY.

---

### Step 8: Deploy to Heroku! 🚀

Now for the magic moment:

```bash
git push heroku main
```

Or if your branch is called "master":
```bash
git push heroku master
```

> ⏰ **This will take 2-3 minutes.** You'll see lots of text scrolling by. This is normal! Heroku is:
> - Receiving your code
> - Installing Python
> - Installing all your packages from requirements.txt
> - Starting your web server

Look for these messages at the end:
```
remote: -----> Launching...
remote:        Released v1
remote:        https://your-app-name.herokuapp.com/ deployed to Heroku
```

---

### Step 9: Open Your Website! 🎉

Type:
```bash
heroku open
```

Your web browser will open your new website!

**Or** just visit: `https://your-app-name.herokuapp.com/`

---

## ✅ Testing Your Deployment

Check these things:

- [ ] Homepage loads with one of the designs
- [ ] You can switch between designs (Modern, Minimalist, Dashboard)
- [ ] Clicking on guides shows the guide content
- [ ] Navigation works
- [ ] About and Stats pages load
- [ ] No error messages

---

## 🔧 Troubleshooting

### Problem: "Application Error" page appears

**Solution**:
```bash
heroku logs --tail
```

This shows you what went wrong. Look for lines with "Error" in red.

Common fixes:
- Make sure Procfile has no .txt extension
- Check that app.py is in the root of your repository
- Verify all files are committed to git

### Problem: Guides don't show up

**Solution**:
The guides folder needs to be one level up from flask_app. Check your folder structure:
```
useful_pyspark/
├── guides/          ← Guide files here
│   ├── 01_dataframe_basics.md
│   └── ...
└── flask_app/       ← Flask app here
    ├── app.py
    └── ...
```

If the structure is different, update the `GUIDES_DIR` path in `app.py`.

### Problem: Can't push to Heroku

**Solution**:
```bash
heroku git:remote -a your-app-name
git push heroku main
```

### Problem: Website is slow to load

**Solution**:
- Free Heroku apps "sleep" after 30 minutes of inactivity
- They wake up automatically (takes ~10 seconds on first visit)
- This is normal for free accounts!

### Problem: Changes don't appear

**Solution**:
After making changes, you need to:
```bash
git add .
git commit -m "Describe your changes"
git push heroku main
```

---

## 📊 Viewing Your App Information

**Check your app status:**
```bash
heroku info
```

**View recent logs:**
```bash
heroku logs --tail
```

**Open your app:**
```bash
heroku open
```

**Restart your app:**
```bash
heroku restart
```

---

## 🔄 Updating Your Website

When you make changes to your code:

1. **Save your changes**
2. **Commit to Git:**
   ```bash
   git add .
   git commit -m "Description of what you changed"
   ```
3. **Deploy to Heroku:**
   ```bash
   git push heroku main
   ```
4. **Wait about 1-2 minutes for deployment**
5. **Refresh your website**

---

## 🎨 Managing Your Database

The SQLite database is stored on Heroku's filesystem. Note:
- Database is created automatically on first run
- Stats and preferences are saved
- **IMPORTANT**: On Heroku's free tier, the database resets every 24 hours
- For persistent storage, consider upgrading or using a Heroku Postgres addon

To add Postgres (optional, more persistent):
```bash
heroku addons:create heroku-postgresql:mini
```

---

## 📱 Advanced: Custom Domain (Optional)

Want your own domain name instead of `.herokuapp.com`?

1. Buy a domain from a domain registrar (like Namecheap, GoDaddy)
2. In Heroku:
   ```bash
   heroku domains:add www.yourdomain.com
   ```
3. Follow the instructions to update your domain's DNS settings
4. Note: This requires a paid Heroku account

---

## 💰 About Free Tier Limits

Heroku free tier includes:
- ✅ 550-1000 free hours per month (enough for 1 app running 24/7)
- ✅ App sleeps after 30 min of inactivity (wakes automatically)
- ✅ Custom domain support
- ❌ Database may not persist across restarts
- ❌ Limited to certain number of apps

---

## 🔍 Useful Heroku Commands

| Command | What It Does |
|---------|--------------|
| `heroku logs --tail` | View live logs (Ctrl+C to exit) |
| `heroku restart` | Restart your app |
| `heroku info` | See app details |
| `heroku open` | Open app in browser |
| `heroku ps` | Check app status |
| `heroku config` | View environment variables |
| `heroku config:set KEY=value` | Set environment variable |
| `heroku releases` | See deployment history |
| `heroku rollback` | Revert to previous version |

---

## 🎓 What You've Learned

Congratulations! You've:
- ✅ Created a Heroku account
- ✅ Installed and used the Heroku CLI
- ✅ Deployed a Flask app to the cloud
- ✅ Configured environment variables
- ✅ Learned how to update and troubleshoot your app

Your PySpark Pro Tips website is now live on the internet! 🚀

---

## 🆘 Getting Help

- **Heroku Dev Center**: [devcenter.heroku.com](https://devcenter.heroku.com/)
- **Heroku Support**: [help.heroku.com](https://help.heroku.com/)
- **Check logs first**: `heroku logs --tail` usually explains the problem

---

## 📝 Quick Reference

**Initial Setup:**
```bash
heroku login
heroku create app-name
git push heroku main
heroku open
```

**Update Code:**
```bash
git add .
git commit -m "Your changes"
git push heroku main
```

**Debug Issues:**
```bash
heroku logs --tail
heroku restart
```

---

**Your app URL**: `https://your-app-name.herokuapp.com`

Share it with the world and help others learn PySpark! 🎉

---

## 🔄 Switching Between PythonAnywhere and Heroku

You can deploy to both platforms! They're independent:
- **PythonAnywhere**: `yourusername.pythonanywhere.com`
- **Heroku**: `your-app-name.herokuapp.com`

Both will work simultaneously with the same code!

---

**Need help?** Create an issue on GitHub or check Heroku's documentation!
