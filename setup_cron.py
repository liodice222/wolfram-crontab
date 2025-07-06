#!/usr/bin/env python3
"""
Cron Job Setup Script for Daily Questions System
"""
import os
import subprocess
import sys
from pathlib import Path

def get_script_path():
    """Get the absolute path to the script.py file"""
    return str(Path(__file__).parent / "script.py")

def check_cron_installed():
    """Check if crontab is available"""
    try:
        subprocess.run(["which", "crontab"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_current_crontab():
    """Get the current crontab entries"""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return ""
    except subprocess.CalledProcessError:
        return ""

def add_cron_job(script_path, time="9:00"):
    """Add a cron job to run the script daily"""
    current_crontab = get_current_crontab()
    
    # Parse the time (default format: "9:00")
    try:
        hour, minute = map(int, time.split(":"))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Invalid time format")
    except ValueError:
        print("Invalid time format. Please use HH:MM format (e.g., 9:00)")
        return False
    
    # Create the cron job entry
    cron_entry = f"{minute} {hour} * * * /usr/bin/python3 {script_path}"
    
    # Check if the job already exists
    if cron_entry in current_crontab:
        print("Cron job already exists!")
        return True
    
    # Add the new job
    new_crontab = current_crontab.strip() + "\n" + cron_entry + "\n"
    
    # Write the new crontab
    try:
        process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
        process.communicate(input=new_crontab)
        
        if process.returncode == 0:
            print(f"Cron job added successfully! Script will run daily at {time}")
            return True
        else:
            print("Failed to add cron job")
            return False
    except Exception as e:
        print(f"Error adding cron job: {e}")
        return False

def remove_cron_job(script_path):
    """Remove the cron job for this script"""
    current_crontab = get_current_crontab()
    
    # Find and remove the line containing our script
    lines = current_crontab.split('\n')
    new_lines = [line for line in lines if script_path not in line]
    
    if len(new_lines) == len(lines):
        print("No cron job found for this script")
        return True
    
    # Write the updated crontab
    new_crontab = '\n'.join(new_lines) + '\n'
    
    try:
        process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
        process.communicate(input=new_crontab)
        
        if process.returncode == 0:
            print("Cron job removed successfully!")
            return True
        else:
            print("Failed to remove cron job")
            return False
    except Exception as e:
        print(f"Error removing cron job: {e}")
        return False

def list_cron_jobs():
    """List all current cron jobs"""
    current_crontab = get_current_crontab()
    
    if not current_crontab.strip():
        print("No cron jobs found")
        return
    
    print("Current cron jobs:")
    print("-" * 50)
    for line in current_crontab.strip().split('\n'):
        if line.strip() and not line.startswith('#'):
            print(line)

def test_script():
    """Test the script to make sure it works"""
    script_path = get_script_path()
    print(f"Testing script: {script_path}")
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Script test successful!")
            print("Output:")
            print(result.stdout)
        else:
            print("❌ Script test failed!")
            print("Error:")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("❌ Script test timed out (took longer than 30 seconds)")
        return False
    except Exception as e:
        print(f"❌ Script test failed with error: {e}")
        return False
    
    return True

def main():
    """Main setup menu"""
    script_path = get_script_path()
    
    print("="*60)
    print("Daily Questions Cron Job Setup")
    print("="*60)
    print(f"Script path: {script_path}")
    
    if not check_cron_installed():
        print("❌ crontab is not available on this system")
        return
    
    while True:
        print("\nOptions:")
        print("1. Test the script")
        print("2. Add daily cron job (default: 9:00 AM)")
        print("3. Add custom time cron job")
        print("4. Remove cron job")
        print("5. List current cron jobs")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            test_script()
            
        elif choice == '2':
            if add_cron_job(script_path, "9:00"):
                print("✅ Daily cron job added for 9:00 AM")
            
        elif choice == '3':
            time = input("Enter time (HH:MM format, e.g., 14:30 for 2:30 PM): ")
            if add_cron_job(script_path, time):
                print(f"✅ Daily cron job added for {time}")
            
        elif choice == '4':
            remove_cron_job(script_path)
            
        elif choice == '5':
            list_cron_jobs()
            
        elif choice == '6':
            print("Setup complete!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 