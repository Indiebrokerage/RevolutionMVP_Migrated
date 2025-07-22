#!/usr/bin/env python
"""
Simple script to create admin user for Revolution Realty
This script ensures the admin user exists and can login
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('/app/backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RevolutionMVP_Django.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    username = 'admin'
    email = 'admin@revolutionrealty.com'
    password = 'RevolutionAdmin2024!'
    
    try:
        # Check if admin user exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            print(f"Admin user '{username}' already exists.")
            
            # Ensure user has proper permissions
            if not user.is_superuser or not user.is_staff:
                user.is_superuser = True
                user.is_staff = True
                user.set_password(password)  # Reset password to ensure it's correct
                user.save()
                print(f"Updated admin user permissions and password.")
            else:
                # Reset password to ensure it's correct
                user.set_password(password)
                user.save()
                print(f"Reset admin user password.")
        else:
            # Create new admin user
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"Created new admin user '{username}'")
        
        print(f"Admin login credentials:")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Admin URL: /admin/")
        
        return True
        
    except Exception as e:
        print(f"Error creating/updating admin user: {str(e)}")
        return False

if __name__ == '__main__':
    success = create_admin_user()
    if success:
        print("Admin user setup completed successfully!")
    else:
        print("Admin user setup failed!")
        sys.exit(1)

