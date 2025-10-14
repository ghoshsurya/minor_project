#!/usr/bin/env python
"""
Single command to start the ATS CV Optimizer project locally
Usage: python start.py
"""
import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Starting ATS CV Optimizer Project...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        sys.exit(1)
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("⚠️  Static files collection failed, continuing...")
    
    # Create superuser if needed
    print("🔧 Creating superuser (skip if exists)...")
    subprocess.run("python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@atsoptimizer.com', 'admin123')\"", shell=True)
    
    print("\n" + "=" * 50)
    print("🎉 Project setup completed!")
    print("📊 Access flowchart: http://127.0.0.1:8000/flowchart/")
    print("🔐 Admin panel: http://127.0.0.1:8000/admin/ (admin/admin123)")
    print("🏠 Main site: http://127.0.0.1:8000/")
    print("=" * 50)
    
    # Start development server
    print("🌐 Starting development server...")
    os.system("python manage.py runserver")

if __name__ == "__main__":
    main()