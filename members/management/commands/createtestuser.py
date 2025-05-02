from django.core.management.base import BaseCommand
from members.models import User

class Command(BaseCommand):
    help = 'Creates a test user in the database'

    def handle(self, *args, **options):
        try:
            test_email = 'test@example.com'
            test_password = 'testpassword123'
            
            # Check if user already exists
            if User.objects.filter(email=test_email).exists():
                self.stdout.write(self.style.WARNING(f'User {test_email} already exists'))
                return
                
            # Create user
            user = User.objects.create_user(
                email=test_email,
                password=test_password
            )
            user.first_name = 'Test'
            user.last_name = 'User'
            user.mobile = '1234567890'
            user.city = 'Test City'
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully created test user: {test_email}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {str(e)}')) 