from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from profiles.models import Profile

User = get_user_model()

class Command(BaseCommand):
    help = "Create a new auction user with random password and blank profile"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the new user')

    def handle(self, *args, **options):
        username = options['username']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))
            return

        password = get_random_string(10)
        user = User.objects.create_user(username=username, password=password)
        user.must_change_password = True
        user.save()

        profile, created = Profile.objects.get_or_create(user=user)

        if created:
            self.stdout.write(self.style.SUCCESS(f"Profile created for '{username}'"))
        else:
            self.stdout.write(self.style.WARNING(f"Profile already exists for '{username}'"))

        self.stdout.write(self.style.SUCCESS(f"User '{username}' created."))
        self.stdout.write(f"Login URL: http://127.0.0.1:8000/accounts/login/")
        self.stdout.write(f"Username: {username}")
        self.stdout.write(f"Password: {password}")
