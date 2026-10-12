from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser interactively (replaces the hardcoded admin)'

    def handle(self, *args, **options):
        self.stdout.write('Creating a superuser interactively...')
        username = input('Username: ')
        email = input('Email (optional): ') or ''
        password = input('Password: ')
        
        if not username or not password:
            self.stdout.write(self.style.ERROR('Username and password are required'))
            return
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User {username} already exists'))
            return
        
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            name=username,
            user_type='admin'
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully'))
