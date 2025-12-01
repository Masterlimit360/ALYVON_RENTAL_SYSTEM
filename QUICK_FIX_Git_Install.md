# Quick Fix: Installing Git on the Other PC

## ❌ Error You're Seeing:
```
'git' is not recognized as an internal or external command,
operable program or batch file.
```

## ✅ Solution: Install Git

### Step 1: Download Git
1. Go to: **https://git-scm.com/download/win**
2. The download should start automatically
3. Or click the download button if it appears

### Step 2: Install Git
1. **Run the downloaded file** (usually `Git-2.x.x-64-bit.exe`)
2. Click **"Next"** through the installation wizard
3. **Important**: On the "Adjusting your PATH environment" screen:
   - Select: **"Git from the command line and also from 3rd-party software"** (usually selected by default)
4. Click **"Next"** on all other screens (defaults are fine)
5. Click **"Install"**
6. Wait for installation to complete
7. Click **"Finish"**

### Step 3: Restart Command Prompt
⚠️ **IMPORTANT**: You **must** close and reopen Command Prompt/PowerShell after installing Git!

1. **Close** all Command Prompt or PowerShell windows
2. **Open a NEW** Command Prompt or PowerShell window
3. Test Git by typing:
   ```cmd
   git --version
   ```
4. You should see something like: `git version 2.43.0`

### Step 4: Navigate to Your App Folder
1. Open Command Prompt
2. Navigate to your ALYVON rental folder:
   ```cmd
   cd "C:\path\to\ALYVON-rental"
   ```
   (Replace with your actual folder path)

### Step 5: Now You Can Pull Changes
Once Git is installed, you can pull the latest changes:
```cmd
git pull
```

---

## 🎯 Quick Summary

1. **Download Git**: https://git-scm.com/download/win
2. **Install Git**: Run installer, use defaults
3. **Restart Command Prompt**: Close and reopen it
4. **Test**: Run `git --version`
5. **Pull**: Run `git pull` in your app folder

---

## 💡 Alternative: Use GitHub Desktop (Easier)

If you prefer a visual interface instead of command line:

1. Download **GitHub Desktop** from: https://desktop.github.com
2. Install and sign in with your GitHub account
3. Open your repository folder in GitHub Desktop
4. Click the **"Pull origin"** or **"Fetch origin"** button
5. Much easier - no command line needed!

---

**After installing Git, you should be able to use `git pull` successfully!** 🎉

