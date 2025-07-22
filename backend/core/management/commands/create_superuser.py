from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser for Revolution Realty admin'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Admin username', default='admin')
        parser.add_argument('--email', type=str, help='Admin email', default='admin@revolutionrealty.com')
        parser.add_argument('--password', type=str, help='Admin password', default='RevolutionAdmin2024!')
        parser.add_argument('--force', action='store_true', help='Force recreate user if exists')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        force = options['force']

        try:
            # Check if superuser already exists
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                
                if force:
                    # Delete and recreate user
                    user.delete()
                    self.stdout.write(
                        self.style.WARNING(f'Deleted existing user "{username}"')
                    )
                else:
                    # Update existing user
                    user.is_superuser = True
                    user.is_staff = True
                    user.is_active = True
                    user.email = email
                    user.set_password(password)
                    user.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated existing superuser "{username}"')
                    )
                    self.stdout.write(f'Email: {email}')
                    self.stdout.write(f'Password: {password}')
                    self.stdout.write('User can now login to the admin at /admin/')
                    return

            # Create new superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            # Ensure user is active and has all permissions
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser "{username}"')
            )
            self.stdout.write(f'Email: {email}')
            self.stdout.write(f'Password: {password}')
            self.stdout.write('You can now login to the admin at /admin/')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating/updating superuser: {str(e)}')
            )
            # Try to provide more specific error information
            if 'UNIQUE constraint failed' in str(e):
                self.stdout.write(
                    self.style.WARNING('User might already exist. Try using --force flag to recreate.')
                )
            raise e

