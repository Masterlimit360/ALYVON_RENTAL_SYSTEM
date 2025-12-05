# Quick Fix: pip Command Not Recognized

## ❌ Issue:
```
pip : The term 'pip' is not recognized...
```

## ✅ Solution:

On Windows, use `python -m pip` instead of just `pip`:

### Install Dependencies:
```cmd
python -m pip install -r requirements.txt
```

### Or use py launcher:
```cmd
py -m pip install -r requirements.txt
```

---

## Why This Happens:

On Windows, `pip` might not be in your PATH. Using `python -m pip` works because:
- It uses Python directly to run pip
- Python is already recognized (you have Python 3.13.2 installed)
- More reliable on Windows

---

## Alternative: Add pip to PATH

If you want to use just `pip` in the future:

1. Find Python's Scripts folder (usually: `C:\Users\YourName\AppData\Local\Programs\Python\Python313\Scripts`)
2. Add it to your System PATH environment variable
3. Restart Command Prompt

But `python -m pip` works without any changes!


