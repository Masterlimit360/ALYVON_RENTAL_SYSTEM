"""
Create desktop shortcut for ALYVON Rental Management System.
"""
import os
import sys

def create_desktop_shortcut():
    """Create a desktop shortcut for the rental management system"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_path = os.path.join(current_dir, "rental_manager_improved.py")
        icon_path = os.path.join(current_dir, "ALYVON logo.ico")
        
        # Get desktop path
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "ALYVON Rental Manager.lnk")
        
        # Create shortcut
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{app_path}"'
        shortcut.WorkingDirectory = current_dir
        shortcut.IconLocation = icon_path
        shortcut.Description = "ALYVON Rental Management System - Professional Rental Management"
        shortcut.save()
        
        print(f"Desktop shortcut created successfully!")
        print(f"Shortcut location: {shortcut_path}")
        print(f"Application: {app_path}")
        print(f"Icon: {icon_path}")
        return True
        
    except ImportError:
        print("Installing required packages...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "winshell", "pywin32"])
            print("Packages installed. Please run this script again.")
            return False
        except Exception as e:
            print(f"Failed to install packages: {e}")
            return False
    except Exception as e:
        print(f"Failed to create shortcut: {e}")
        return False

if __name__ == "__main__":
    print("Creating ALYVON Rental Manager desktop shortcut...")
    success = create_desktop_shortcut()
    
    if success:
        print("\n✅ Desktop shortcut created successfully!")
        print("You can now double-click 'ALYVON Rental Manager' on your desktop to start the application.")
    else:
        print("\n❌ Failed to create shortcut.")
        print("You can still run the application using the batch file: ALYVON_Rental_Manager.bat")
