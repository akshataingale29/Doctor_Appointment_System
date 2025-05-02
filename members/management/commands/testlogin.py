from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from members.models import User

class Command(BaseCommand):
    help = 'Test authentication for a user'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email of the user to test')
        parser.add_argument('password', type=str, help='Password of the user to test')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        
        # Check if user exists
        self.stdout.write(self.style.SUCCESS(f'Checking if user exists with email: {email}'))
        try:
            user = User.objects.get(email=email)
            self.stdout.write(self.style.SUCCESS(f'User found: {user.email}, ID: {user.id}'))
            
            # Test password verification directly
            self.stdout.write(self.style.SUCCESS('Testing password verification directly...'))
            if user.check_password(password):
                self.stdout.write(self.style.SUCCESS('Password check successful directly!'))
            else:
                self.stdout.write(self.style.ERROR('Password check failed directly!'))
            
            # Test authentication
            self.stdout.write(self.style.SUCCESS('Testing authenticate() function...'))
            authenticated_user = authenticate(username=email, password=password)
            
            if authenticated_user is not None:
                self.stdout.write(self.style.SUCCESS(f'Authentication successful! User ID: {authenticated_user.id}'))
            else:
                self.stdout.write(self.style.ERROR('Authentication failed!'))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No user found with email: {email}')) 