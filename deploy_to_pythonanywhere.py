#!/usr/bin/env python
"""
Deployment helper script for PythonAnywhere
Run this script after setting up your PythonAnywhere account and uploading your code.
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a command and print output"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result.returncode

def main():
    """Main deployment function"""
    print("College Event Feedback System - PythonAnywhere Deployment Helper")
    print("=============================================================")
    
    # Collect static files
    print("\n1. Collecting static files...")
    run_command("python manage.py collectstatic --noinput --settings=feedback_system.production_settings")
    
    # Run migrations
    print("\n2. Running database migrations...")
    run_command("python manage.py migrate --settings=feedback_system.production_settings")
    
    # Create superuser if needed
    print("\n3. Do you want to create a superuser? (y/n)")
    if input().lower() == 'y':
        run_command("python manage.py createsuperuser --settings=feedback_system.production_settings")
    
    # Create default user if needed
    print("\n4. Do you want to create the default manager user? (y/n)")
    if input().lower() == 'y':
        from django.contrib.auth.models import User
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_system.production_settings')
        import django
        django.setup()
        
        if not User.objects.filter(username='Ankurrai@gla').exists():
            User.objects.create_user('Ankurrai@gla', 'admin@example.com', 'AnkurRai@010GLA')
            print("Default user created: Ankurrai@gla / AnkurRai@010GLA")
        else:
            print("Default user already exists")
    
    print("\n5. Deployment steps completed!")
    print("\nRemember to:")
    print("- Configure your WSGI file in the PythonAnywhere web app settings")
    print("- Set up static files in the PythonAnywhere web app settings")
    print("- Reload your web app")
    
    print("\nYour app should be available at: https://yourusername.pythonanywhere.com")

if __name__ == "__main__":
    main()
