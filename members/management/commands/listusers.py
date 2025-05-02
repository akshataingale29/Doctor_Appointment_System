from django.core.management.base import BaseCommand
from members.models import User

class Command(BaseCommand):
    help = 'Lists all users in the database with detailed information'

    def handle(self, *args, **options):
        users = User.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Total users: {users.count()}'))
        
        for i, user in enumerate(users, 1):
            self.stdout.write(self.style.SUCCESS(f'\nUser #{i}:'))
            self.stdout.write(self.style.SUCCESS(f'ID: {user.id}'))
            self.stdout.write(self.style.SUCCESS(f'Email: {user.email}'))
            self.stdout.write(self.style.SUCCESS(f'First name: {user.first_name}'))
            self.stdout.write(self.style.SUCCESS(f'Last name: {user.last_name}'))
            self.stdout.write(self.style.SUCCESS(f'Mobile: {user.mobile}'))
            self.stdout.write(self.style.SUCCESS(f'City: {user.city}'))
            self.stdout.write(self.style.SUCCESS(f'Is active: {user.is_active}'))
            self.stdout.write(self.style.SUCCESS(f'Is staff: {user.is_staff}'))
            self.stdout.write(self.style.SUCCESS(f'Is superuser: {user.is_superuser}'))
            self.stdout.write(self.style.SUCCESS(f'Last login: {user.last_login}'))
            self.stdout.write(self.style.SUCCESS(f'Date joined: {user.date_joined}')) 