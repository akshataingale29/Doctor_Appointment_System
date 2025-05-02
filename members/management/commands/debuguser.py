from django.core.management.base import BaseCommand
from members.models import User
from django.db import connection

class Command(BaseCommand):
    help = 'Debugging user creation process'

    def handle(self, *args, **options):
        try:
            # Print all existing users first
            self.stdout.write(self.style.SUCCESS('Checking existing users...'))
            users = User.objects.all()
            self.stdout.write(self.style.SUCCESS(f'Total users: {users.count()}'))
            
            # List tables in the database
            self.stdout.write(self.style.SUCCESS('Listing database tables...'))
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                for table in tables:
                    self.stdout.write(self.style.SUCCESS(f'- {table[0]}'))
            
            # Create a test user
            self.stdout.write(self.style.SUCCESS('Creating test user...'))
            test_email = 'test@example.com'
            test_password = 'testpassword123'
            
            # Delete existing user if it exists
            if User.objects.filter(email=test_email).exists():
                User.objects.filter(email=test_email).delete()
                self.stdout.write(self.style.SUCCESS(f'Deleted existing user with email {test_email}'))
            
            # Create user with verbose logging
            self.stdout.write(self.style.SUCCESS('About to call User.objects.create_user()'))
            user = User.objects.create_user(
                email=test_email,
                password=test_password
            )
            self.stdout.write(self.style.SUCCESS(f'User created with ID: {user.id}'))
            
            self.stdout.write(self.style.SUCCESS('Setting additional fields'))
            user.first_name = 'Test'
            user.last_name = 'User'
            user.mobile = '1234567890'
            user.city = 'Test City'
            
            self.stdout.write(self.style.SUCCESS('About to save user'))
            user.save()
            self.stdout.write(self.style.SUCCESS('User saved'))
            
            # Verify the user was created
            self.stdout.write(self.style.SUCCESS('Verifying user creation...'))
            created_user = User.objects.filter(email=test_email).first()
            if created_user:
                self.stdout.write(self.style.SUCCESS(f'Success! User created with ID: {created_user.id}'))
                self.stdout.write(self.style.SUCCESS(f'Email: {created_user.email}'))
                self.stdout.write(self.style.SUCCESS(f'First name: {created_user.first_name}'))
                self.stdout.write(self.style.SUCCESS(f'Is superuser: {created_user.is_superuser}'))
                self.stdout.write(self.style.SUCCESS(f'Is staff: {created_user.is_staff}'))
                self.stdout.write(self.style.SUCCESS(f'Is active: {created_user.is_active}'))
            else:
                self.stdout.write(self.style.ERROR('Failed to retrieve created user!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}')) 