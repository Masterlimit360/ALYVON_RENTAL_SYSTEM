# 🚨 Remove Secrets from Git History

If you accidentally committed secrets to Git, follow these steps to remove them.

## ⚠️ Important

**Before starting:** Rotate your Twilio credentials in the Twilio console, as they may have been exposed.

## 🔧 Method 1: Remove from Last Commit (If Not Pushed Yet)

If you haven't pushed yet:

```cmd
# Remove secrets from staging
git reset HEAD~1

# Fix the files (remove secrets)
# Edit sms_config.py and TWILIO_SETUP_COMPLETE.md

# Commit again
git add .
git commit -m "Remove secrets from config"
```

## 🔧 Method 2: Remove from History (If Already Pushed)

If you already pushed to GitHub:

### Step 1: Install git-filter-repo (Recommended)

```cmd
python -m pip install git-filter-repo
```

### Step 2: Remove Secrets from History

```cmd
# Remove Twilio Account SID (replace with your actual SID if different)
git filter-repo --replace-text <(echo "YOUR_ACCOUNT_SID==>REMOVED")

# Remove Auth Token (replace with your actual token if different)
git filter-repo --replace-text <(echo "YOUR_AUTH_TOKEN==>REMOVED")
```

### Step 3: Force Push (⚠️ WARNING: This rewrites history)

```cmd
git push origin main --force
```

**⚠️ WARNING:** This will rewrite Git history. Coordinate with anyone else using the repository.

## 🔧 Method 3: Manual File Edit + New Commit

Simpler approach if you just want to fix going forward:

1. **Edit files to remove secrets** (already done)
2. **Commit the fix:**
   ```cmd
   git add sms_config.py TWILIO_SETUP_COMPLETE.md
   git commit -m "Remove secrets - use .env file instead"
   git push origin main
   ```

3. **Note:** Old commits still contain secrets, but new code is clean.

## ✅ After Removing Secrets

1. **Rotate credentials** in Twilio console
2. **Update `.env`** with new credentials
3. **Verify `.env` is in `.gitignore`**
4. **Test the app** to ensure it works

---

## 📚 Alternative: Use GitHub's Secret Scanning

GitHub may have already detected and revoked the secrets. Check:
- GitHub → Your Repo → Security → Secret scanning

---

**Remember:** Always use `.env` files for secrets, never commit them! 🔒

