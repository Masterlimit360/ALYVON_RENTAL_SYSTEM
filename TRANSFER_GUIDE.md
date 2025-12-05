# Step-by-Step Guide: Transferring ALYVON Rental App to Another PC

This guide will help you transfer the ALYVON Rental Management System to a different PC and set it up with a desktop icon.

---

## 📦 PART 1: Preparing Files for Transfer

### Step 1: Gather All Application Files
On your **current PC**, make sure you have all these files and folders:

```
ALYVON rental/
├── ALYVON logo.ico
├── ALYVON logo.png
├── ALYVON_Rental_Manager.bat
├── config.py
├── create_shortcut.py
├── database.py
├── rental_manager_improved.py
├── requirements.txt
├── README.md
└── web/
    ├── index.html
    ├── logo.png
    └── data/
        ├── active_rentals.json
        └── rental_history.json
```

### Step 2: Create a Transfer Package
1. **Copy the entire folder** `ALYVON rental` to a USB drive, external hard drive, or cloud storage (Google Drive, OneDrive, etc.)
2. Make sure the folder structure is preserved exactly as shown above

---

## 🚀 PART 2: Setting Up on the New PC

### Step 3: Install Python
1. Download Python 3.7 or higher from [python.org](https://www.python.org/downloads/)
2. **Important**: During installation, check the box **"Add Python to PATH"**
3. Complete the installation

### Step 4: Install PostgreSQL
1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Install PostgreSQL (remember the password you set for the 'postgres' user)
3. Make sure the PostgreSQL service is running (it should start automatically)

### Step 5: Transfer Files to New PC
1. Copy the `ALYVON rental` folder from your USB/cloud storage to the new PC
2. Place it in a convenient location (e.g., `C:\Users\YourName\Desktop\` or `C:\Program Files\ALYVON\`)
3. **Note the full path** where you placed the folder (you'll need this later)

### Step 6: Update Database Configuration
1. Open the `config.py` file in the `ALYVON rental` folder
2. Update the database password to match your PostgreSQL password:
   ```python
   DB_PASSWORD = "your_postgres_password_here"  # Replace with your actual password
   ```
3. Save the file

### Step 7: Install Python Dependencies
1. Open **Command Prompt** or **PowerShell**
2. Navigate to the application folder:
   ```cmd
   cd "C:\path\to\ALYVON rental"
   ```
   (Replace with your actual path)
3. Install required packages:
   ```cmd
   pip install -r requirements.txt
   ```
4. Wait for installation to complete

### Step 8: Setup Database
1. Still in the Command Prompt, run:
   ```cmd
   python database.py
   ```
   (This will create the database tables if they don't exist)

---

## 🖥️ PART 3: Creating Desktop Icon

### Method 1: Using the Automated Script (Recommended)

1. Open Command Prompt in the application folder:
   ```cmd
   cd "C:\path\to\ALYVON rental"
   ```

2. Run the shortcut creation script:
   ```cmd
   python create_shortcut.py
   ```

3. If it asks to install packages, type `y` and press Enter. The script will:
   - Install `winshell` and `pywin32` if needed
   - Create a desktop shortcut automatically
   - Use the ALYVON logo as the icon

4. You should see: **"✅ Desktop shortcut created successfully!"**

5. Check your desktop for **"ALYVON Rental Manager"** icon

### Method 2: Manual Creation (Alternative)

If the automated script doesn't work, create the shortcut manually:

1. **Right-click** on your desktop → **New** → **Shortcut**

2. In the location field, enter:
   ```
   pythonw.exe "C:\path\to\ALYVON rental\rental_manager_improved.py"
   ```
   (Replace with your actual path)

3. Click **Next**

4. Name it: **ALYVON Rental Manager**

5. Click **Finish**

6. **Right-click** the new shortcut → **Properties**

7. Click **Change Icon** → **Browse**

8. Navigate to your `ALYVON rental` folder and select **ALYVON logo.ico**

9. Click **OK** → **OK**

10. In the Properties window, update the "Start in" field to:
    ```
    C:\path\to\ALYVON rental
    ```
    (Replace with your actual path)

11. Click **OK**

### Method 3: Using the Batch File (Quick Test)

1. Double-click `ALYVON_Rental_Manager.bat` to test if the app runs
2. If it works, you can create a shortcut to this batch file instead:
   - Right-click `ALYVON_Rental_Manager.bat` → **Create Shortcut**
   - Move the shortcut to your desktop
   - Right-click the shortcut → **Properties** → **Change Icon** → Select `ALYVON logo.ico`

---

## ✅ PART 4: Verification

### Test the Application
1. Double-click the desktop icon (or the batch file)
2. The application should open
3. If you see any errors:
   - Check that PostgreSQL is running
   - Verify the database password in `config.py` is correct
   - Make sure all Python packages are installed: `pip install -r requirements.txt`

---

## 🔧 Troubleshooting

### Issue: "Python is not recognized"
**Solution**: 
- Reinstall Python and make sure "Add Python to PATH" is checked
- Or add Python manually to PATH in System Environment Variables

### Issue: "Module not found" errors
**Solution**: 
- Run: `pip install -r requirements.txt`
- Make sure you're in the correct directory

### Issue: "Database connection failed"
**Solution**: 
- Check PostgreSQL is running (Services → PostgreSQL)
- Verify password in `config.py` matches your PostgreSQL password
- Make sure database `rental_system` exists

### Issue: Shortcut doesn't work
**Solution**: 
- Check the path in the shortcut properties is correct
- Make sure Python is in your PATH
- Try using the batch file method instead

### Issue: Icon doesn't show
**Solution**: 
- Make sure `ALYVON logo.ico` is in the same folder
- Try refreshing the desktop (F5)
- The icon should appear after a few seconds

---

## 📝 Quick Reference Checklist

- [ ] Python 3.7+ installed with PATH enabled
- [ ] PostgreSQL installed and running
- [ ] All application files copied to new PC
- [ ] `config.py` updated with correct database password
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Database initialized
- [ ] Desktop shortcut created
- [ ] Application tested and working

---

## 💡 Tips

1. **Keep a backup**: Always keep a backup of your `web/data/` folder as it contains your rental data
2. **Portable option**: You can place the app on a USB drive and run it from there (just update paths accordingly)
3. **Multiple users**: If multiple people will use this, consider placing it in a shared location like `C:\Program Files\ALYVON\`
4. **Database backup**: Regularly backup your PostgreSQL database for safety

---

**Need Help?** Check the `README.md` file for more detailed information about the application features and usage.




