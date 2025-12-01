# 🚀 Quick Start - 5 Minutes to Running!

Get your Flask app running locally in just 5 minutes!

---

## For Complete Beginners 👶

### Step 1: Open PowerShell (Windows) or Terminal (Mac/Linux)

**Windows:**
- Press `Windows Key + X`
- Click "Windows PowerShell" or "Terminal"

**Mac:**
- Press `Command + Space`
- Type "Terminal" and press Enter

**Linux:**
- Press `Ctrl + Alt + T`

### Step 2: Navigate to the Flask App Folder

Copy and paste this command (replace with your actual path):

**Windows:**
```powershell
cd c:\Users\Byamba\byamba\github_pin\useful_pyspark\flask_app
```

**Mac/Linux:**
```bash
cd /path/to/useful_pyspark/flask_app
```

### Step 3: Create a Virtual Environment

Copy and paste:

**Windows:**
```powershell
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

⏰ Wait about 10 seconds...

### Step 4: Activate the Virtual Environment

**Windows:**
```powershell
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your command line.

### Step 5: Install Required Packages

```bash
pip install -r requirements.txt
```

⏰ Wait about 30 seconds while packages install...

### Step 6: Run the App!

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 7: Open Your Browser

Open your web browser and go to:
```
http://localhost:5000
```

🎉 **You should see your PySpark Pro Tips website!**

---

## Testing the Designs

1. Click the **"Change Design"** dropdown in the navigation
2. Try each design:
   - 🎨 Modern
   - ✨ Minimalist
   - 📊 Dashboard
3. Click on any guide to view it
4. Check the **Stats** page to see view counts

---

## Stopping the App

Press `Ctrl + C` in the terminal/PowerShell to stop the server.

---

## Running Again Later

1. Open terminal/PowerShell
2. Navigate to flask_app folder
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Run: `python app.py`

---

## What's Next?

Now that it's running locally, deploy it online:

- 📖 [Deploy to PythonAnywhere](deployment_guides/DEPLOY_PYTHONANYWHERE.md) - **Recommended for beginners**
- 📖 [Deploy to Heroku](deployment_guides/DEPLOY_HEROKU.md) - For those comfortable with command line

---

## Troubleshooting

### "python is not recognized"

**Solution:**
- Make sure Python is installed
- Try `python3` instead of `python`
- Download Python from [python.org](https://python.org)

### "pip is not recognized"

**Solution:**
Try `python -m pip` instead of just `pip`

### Port already in use

**Solution:**
Another app is using port 5000. Either:
- Stop the other app, or
- Edit `app.py` and change port 5000 to 5001

### Can't see guides

**Solution:**
Make sure the `guides` folder with `.md` files is one level up from `flask_app`

---

## Need Help?

- Check the main [README.md](README.md)
- Review the [deployment guides](deployment_guides/)
- Create an issue on GitHub

---

**Happy coding!** 🚀
