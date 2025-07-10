from django.core.management.base import BaseCommand
from scenes.models import EligibleBidder

class Command(BaseCommand):
    help = "Seed EligibleBidder table with common orientation / identity terms"

    def handle(self, *args, **options):
        bidders = [
            ("Heterosexual", "Attracted to people of the opposite binary gender."),
            ("Gay", "Man attracted to men."),
            ("Lesbian", "Woman attracted to women."),
            ("Bisexual", "Attracted to more than one gender."),
            ("Pansexual", "Attracted to people regardless of their gender."),
            ("Queer", "Umbrella term for non-heterosexual, non-cisgender identities."),
            ("Asexual", "Experiences little or no sexual attraction."),
            ("Demisexual", "Only experiences sexual attraction after forming an emotional bond."),
            ("Graysexual", "Rarely experiences sexual attraction or under specific circumstances."),
            ("Polysexual", "Attracted to multiple, but not all, genders."),
            ("Sapiosexual", "Primarily attracted to intelligence."),
            ("Skoliosexual", "Attracted to non-binary or gender non-conforming people."),
            ("Androsexual", "Attracted to masculinity, regardless of gender."),
            ("Gynesexual", "Attracted to femininity, regardless of gender."),
        ]

        for code, desc in bidders:
            obj, created = EligibleBidder.objects.get_or_create(code=code, defaults={"desc": desc})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added: {code}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {code}"))
