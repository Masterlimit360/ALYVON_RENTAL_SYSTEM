# 🔒 Secure Setup Guide - Multi-PC Configuration

This guide helps you securely set up credentials on both PCs without exposing secrets to GitHub.

## 🎯 Overview

- **Credentials are stored in `.env` file** (not committed to Git)
- **Each PC has its own `.env` file** with credentials
- **Code is synced via GitHub** (without secrets)
- **Secrets stay local** on each PC

---

## 📋 Setup on PC 1 (Main PC - Where You Write Code)

### Step 1: Install python-dotenv

```cmd
python -m pip install python-dotenv
```

### Step 2: Create .env File

The `.env` file should already exist with your Twilio credentials. If not, create it:

1. Copy `.env.example` to `.env`:
   ```cmd
   copy .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   SMS_GATEWAY=twilio
   TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
   TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
   TWILIO_PHONE_NUMBER=your_twilio_phone_number_here
   ```
   
   **Or run the setup script:**
   ```cmd
   python setup_env.py
   ```

### Step 3: Verify .env is Ignored

Check that `.env` is in `.gitignore` (it should be already).

### Step 4: Test the App

```cmd
python rental_manager_improved.py
```

The app should load credentials from `.env` automatically.

---

## 📋 Setup on PC 2 (Other PC)

### Step 1: Pull Latest Code

```cmd
cd "C:\path\to\ALYVON-rental"
git pull
```

### Step 2: Install Dependencies

```cmd
python -m pip install -r requirements.txt
```

### Step 3: Create .env File

1. Copy the example file:
   ```cmd
   copy .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   SMS_GATEWAY=twilio
   TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
   TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
   TWILIO_PHONE_NUMBER=your_twilio_phone_number_here
   ```
   
   **Or run the setup script:**
   ```cmd
   python setup_env.py
   ```

   **Note:** Both PCs can use the same Twilio credentials, or you can create separate Twilio accounts.

### Step 4: Test the App

```cmd
python rental_manager_improved.py
```

---

## 🔄 Workflow: Syncing Code Without Secrets

### On PC 1 (After Making Code Changes):

1. **Make your code changes**

2. **Commit and push** (credentials are NOT included):
   ```cmd
   git add .
   git commit -m "Your changes"
   git push origin main
   ```

### On PC 2 (To Get Latest Code):

1. **Pull latest code:**
   ```cmd
   git pull
   ```

2. **Your `.env` file stays untouched** - credentials remain local

---

## ✅ Security Checklist

- [x] `.env` file is in `.gitignore`
- [x] `.env.example` is committed (template only, no real credentials)
- [x] `sms_config.py` has no hardcoded credentials
- [x] Credentials loaded from environment variables
- [x] Both PCs can have their own `.env` files

---

## 🔧 Troubleshooting

### "Credentials not found" or SMS not working:

1. **Check `.env` file exists:**
   ```cmd
   dir .env
   ```

2. **Verify `.env` has correct format:**
   - No spaces around `=`
   - No quotes needed
   - One variable per line

3. **Check python-dotenv is installed:**
   ```cmd
   python -m pip install python-dotenv
   ```

4. **Restart the app** after creating/editing `.env`

### "Module 'dotenv' not found":

```cmd
python -m pip install python-dotenv
```

### Credentials still in Git history:

If you accidentally committed credentials before, see `REMOVE_SECRETS_FROM_GIT.md`

---

## 📝 File Structure

```
ALYVON rental/
├── .env                    ← Your credentials (NOT in Git)
├── .env.example            ← Template (in Git, safe)
├── sms_config.py           ← Loads from .env (in Git, safe)
├── .gitignore              ← Ignores .env (in Git)
└── ...
```

---

## 💡 Tips

1. **Never commit `.env`** - It's already in `.gitignore`
2. **Share credentials securely** - Use secure methods (not email/GitHub) to share credentials with team
3. **Different credentials per PC** - Each PC can have different credentials if needed
4. **Backup `.env`** - Keep a secure backup of your `.env` file (not in Git!)

---

## 🚨 If Credentials Are Exposed

If you accidentally pushed credentials to GitHub:

1. **Immediately rotate credentials** in Twilio console
2. **Remove from Git history** (see `REMOVE_SECRETS_FROM_GIT.md`)
3. **Update `.env`** with new credentials
4. **Never commit `.env` again**

---

**Your setup is now secure!** Credentials stay local, code syncs via GitHub. 🔒

