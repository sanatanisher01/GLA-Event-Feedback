from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates the default admin user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='Ankurrai@gla').exists():
            User.objects.create_superuser(
                username='Ankurrai@gla',
                email='admin@example.com',
                password='AnkurRai@010GLA'
            )
            self.stdout.write(self.style.SUCCESS('Default admin user created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Default admin user already exists'))
