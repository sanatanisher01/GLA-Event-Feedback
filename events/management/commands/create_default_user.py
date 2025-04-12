from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates the default admin users'

    def handle(self, *args, **kwargs):
        # Create the primary admin user
        if not User.objects.filter(username='Ankurrai@gla').exists():
            User.objects.create_superuser(
                username='Ankurrai@gla',
                email='admin@example.com',
                password='AnkurRai@010GLA'
            )
            self.stdout.write(self.style.SUCCESS('Primary admin user created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Primary admin user already exists'))

        # Create a backup admin user with simpler credentials
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Backup admin user created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Backup admin user already exists'))
