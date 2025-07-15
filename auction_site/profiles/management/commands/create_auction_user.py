from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles.models import Profile
from django.utils.crypto import get_random_string
from pathlib import Path
import platform


class Command(BaseCommand):
    help = "Creates users & profiles from a comma-separated list. Outputs: username, password if created, or username, already exists."

    def add_arguments(self, parser):
        parser.add_argument(
            "--users", type=str, help="Comma-separated list of usernames", required=True
        )

    def handle(self, *args, **options):
        User = get_user_model()
        user_list = options["users"].split(",")

        system = platform.system()
        home = Path.home()

        if system == "Windows":
            output_file = home / "Documents" / "auction" / "users" / "created_users.txt"
        else:
            output_file = home / "created_users.txt"

        output_file.parent.mkdir(parents=True, exist_ok=True)

        self.stdout.write(self.style.NOTICE(f"Logging results to: {output_file}"))

        with open(output_file, "a") as f:
            for username in user_list:
                username = username.strip()
                if not username:
                    continue

                user, created = User.objects.get_or_create(username=username)

                if created:
                    # Generate random password
                    password = get_random_string(10)
                    user.set_password(password)
                    user.save()

                    # Ensure Profile exists
                    Profile.objects.get_or_create(user=user)

                    line = f"{username}, {password}"
                    self.stdout.write(self.style.SUCCESS(f"Created: {line}"))
                else:
                    line = f"{username}, already exists"
                    self.stdout.write(self.style.WARNING(f"{line}"))

                f.write(line + "\n")
