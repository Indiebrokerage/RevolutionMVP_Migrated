from django.apps import AppConfig
from django.db import transaction
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        This method is called when Django starts up.
        It ensures the admin user exists every time the application runs.
        """
        # Only run this in production or when explicitly enabled
        if os.environ.get('DJANGO_SETTINGS_MODULE') and 'test' not in os.environ.get('DJANGO_SETTINGS_MODULE', ''):
            self.ensure_admin_user()

    def ensure_admin_user(self):
        """
        Ensures that an admin user exists in the database.
        This runs automatically when Django starts up.
        """
        try:
            # Import here to avoid circular imports
            from django.contrib.auth.models import User
            from django.db import connection
            
            # Check if database is ready (tables exist)
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='auth_user';
                """)
                if not cursor.fetchone():
                    # Database tables don't exist yet, skip
                    return

            # Use transaction to ensure atomicity
            with transaction.atomic():
                username = 'admin'
                password = 'admin123'
                email = 'admin@revolutionrealty.com'
                
                # Check if admin user exists
                admin_user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': email,
                        'is_staff': True,
                        'is_superuser': True,
                        'is_active': True,
                    }
                )
                
                if created:
                    # Set password for new user
                    admin_user.set_password(password)
                    admin_user.save()
                    print(f"✅ Created admin user: {username}")
                else:
                    # Update existing user to ensure proper permissions and password
                    admin_user.email = email
                    admin_user.is_staff = True
                    admin_user.is_superuser = True
                    admin_user.is_active = True
                    admin_user.set_password(password)
                    admin_user.save()
                    print(f"✅ Updated admin user: {username}")
                
                print(f"🔑 Admin credentials: {username} / {password}")
                print(f"📧 Admin email: {email}")
                print(f"🌐 Admin URL: /admin/")
                
        except Exception as e:
            # Don't crash the application if admin creation fails
            print(f"⚠️ Admin user creation failed: {str(e)}")
            # This is expected during migrations or when database isn't ready
            pass

