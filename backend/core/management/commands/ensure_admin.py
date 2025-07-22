from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Ensure admin user exists'

    def handle(self, *args, **options):
        username = 'admin'
        password = 'admin123'
        email = 'admin@revolutionrealty.com'
        
        try:
            # Delete existing admin user if exists
            if User.objects.filter(username=username).exists():
                User.objects.filter(username=username).delete()
                self.stdout.write(f'Deleted existing user: {username}')
            
            # Create new admin user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user: {username}')
            )
            self.stdout.write(f'Username: {username}')
            self.stdout.write(f'Password: {password}')
            self.stdout.write(f'Email: {email}')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
            # Create with basic method
            try:
                user = User(username=username, email=email)
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.is_active = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created admin user with fallback method')
                )
            except Exception as e2:
                self.stdout.write(
                    self.style.ERROR(f'Fallback failed: {str(e2)}')
                )

