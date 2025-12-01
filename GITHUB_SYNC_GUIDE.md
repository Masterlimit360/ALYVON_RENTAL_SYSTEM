# GitHub Sync Guide: Keeping Multiple PCs Updated

## 🔄 How GitHub Works

**Important**: Pushing changes to GitHub does **NOT** automatically update other PCs. You need to **pull** the changes on each PC.

### The Workflow:
1. **PC 1** (Your main PC): Make changes → **Push** to GitHub
2. **PC 2** (Other PC): **Pull** from GitHub to get the latest changes

---

## 📤 PART 1: Setting Up GitHub (First Time)

### Step 1: Create a GitHub Repository
1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon → **"New repository"**
3. Name it: `ALYVON-rental` (or any name you prefer)
4. Choose **Private** (recommended for business apps)
5. **Don't** initialize with README (you already have files)
6. Click **"Create repository"**

### Step 2: Initialize Git on Your Main PC
1. Open **Command Prompt** or **PowerShell** in your `ALYVON rental` folder
2. Run these commands:

```cmd
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ALYVON-rental.git
git push -u origin main
```

(Replace `YOUR_USERNAME` with your actual GitHub username)

---

## 📥 PART 2: Setting Up the Other PC

### Step 3: Install Git on the Other PC (REQUIRED FIRST!)

**If you get "git is not recognized" error, you need to install Git first:**

1. Download Git for Windows from: [git-scm.com/download/win](https://git-scm.com/download/win)
2. Run the installer
3. **Important settings during installation:**
   - Choose "Use Git from the Windows Command Prompt" (recommended)
   - Choose "Checkout Windows-style, commit Unix-style line endings"
   - Click "Next" through the rest (defaults are fine)
4. After installation, **restart Command Prompt or PowerShell** (close and reopen)
5. Verify Git is installed by running:
   ```cmd
   git --version
   ```
   You should see something like `git version 2.x.x`

### Step 4: Clone Repository on Other PC
1. On the **other PC**, open Command Prompt
2. Navigate to where you want the app (e.g., `cd Desktop`)
3. Clone the repository:

```cmd
git clone https://github.com/YOUR_USERNAME/ALYVON-rental.git
```

4. This will create a folder called `ALYVON-rental` with all your files

### Step 5: Setup on Other PC
1. Follow the setup steps from `TRANSFER_GUIDE.md`:
   - Install Python dependencies: `pip install -r requirements.txt`
   - Update `config.py` with the correct database password
   - Create desktop shortcut: `python create_shortcut.py`

---

## 🔄 PART 3: Daily Sync Workflow

### When You Make Changes on PC 1 (Main PC):

1. **Make your code changes** in the files

2. **Commit and push** to GitHub:
   ```cmd
   cd "C:\path\to\ALYVON rental"
   git add .
   git commit -m "Description of changes"
   git push
   ```

### When You Want to Update PC 2 (Other PC):

1. **Pull the latest changes**:
   ```cmd
   cd "C:\path\to\ALYVON-rental"
   git pull
   ```

2. **If you made changes to dependencies**, reinstall:
   ```cmd
   pip install -r requirements.txt
   ```

3. **Restart the application** to see the changes

---

## ⚠️ Important Notes

### What Gets Synced:
✅ Code files (`.py`, `.html`, `.bat`, etc.)  
✅ Configuration templates (`config.py`)  
✅ Documentation files  
✅ Requirements file  

### What Does NOT Get Synced:
❌ Database files (PostgreSQL data stays on each PC)  
❌ `config.py` passwords (each PC has its own database password)  
❌ `__pycache__` folders (auto-generated)  
❌ Local data files (if any)  

### Database Considerations:
- **Each PC has its own database** - they don't share data
- If you need to sync database data, you'll need to export/import separately
- The code structure syncs, but the actual rental data stays local to each PC

---

## 🔧 Troubleshooting

### Issue: "Repository not found"
**Solution**: 
- Check the repository URL is correct
- Make sure you're logged into GitHub
- Verify the repository exists and you have access

### Issue: "Local changes would be overwritten by merge"
**Solution**: 
- Your local files have changes that conflict with GitHub
- **Option 1 (Recommended)**: Discard local changes to match GitHub:
  ```cmd
  git reset --hard HEAD
  git clean -fd
  git pull
  ```
- **Option 2**: Save your changes temporarily:
  ```cmd
  git stash
  git pull
  git stash pop
  ```
- See `FIX_Git_Conflict.md` for detailed instructions

### Issue: "Merge conflicts"
**Solution**: 
- This happens when both PCs have different changes
- Git will mark conflicts in files
- You'll need to manually resolve them or choose which version to keep

### Issue: "Changes not appearing after pull"
**Solution**: 
- Make sure you saved files before committing
- Check that you're in the correct directory
- Try: `git status` to see what's happening
- Restart the application after pulling

### Issue: "Authentication failed"
**Solution**: 
- Use a Personal Access Token instead of password
- Or use GitHub Desktop app (easier for beginners)

### Issue: "git is not recognized" or "git: command not found"
**Solution**: 
- **Git is not installed** on this PC
- Install Git from [git-scm.com/download/win](https://git-scm.com/download/win)
- After installation, **restart Command Prompt** (close and reopen)
- Verify with: `git --version`
- If you already have the app folder, you don't need to clone again - just use `git pull` after installing Git

---

## 💡 Best Practices

1. **Commit often**: Commit changes after each feature or fix
2. **Write clear commit messages**: "Fixed rental calculation bug" is better than "update"
3. **Pull before making changes**: Always pull latest changes before starting work
4. **Test before pushing**: Make sure your code works before pushing
5. **Keep config.py local**: Don't commit passwords (use `.gitignore`)

---

## 🚀 Quick Commands Reference

### On PC 1 (After making changes):
```cmd
git add .
git commit -m "Your change description"
git push
```

### On PC 2 (To get updates):
```cmd
git pull
```

### Check status:
```cmd
git status
```

### See what changed:
```cmd
git log
```

---

## 📝 Alternative: Using GitHub Desktop

If command line seems complicated, use **GitHub Desktop**:

1. Download from [desktop.github.com](https://desktop.github.com)
2. Sign in with your GitHub account
3. Clone your repository
4. Use the GUI to commit, push, and pull changes
5. Much easier for beginners!

---

**Remember**: GitHub syncs **code**, not **data**. Each PC maintains its own database and configuration.

