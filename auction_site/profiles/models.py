from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    must_change_password = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # general info
    name = models.CharField(max_length=100)
    fet = models.CharField("fet name", max_length=100, blank=True)
    pronouns = models.CharField(max_length=50, blank=True)
    pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    # auctioneer references
    ref_pronouns = models.CharField("auction pronouns", max_length=50, blank=True)
    ref_name = models.CharField("auction name", max_length=100, blank=True)
    ref_phys = models.BooleanField("ok to mention physical?", default=False)
    ref_words = models.TextField("preferred words", blank=True)
    ref_no_words = models.TextField("words to avoid", blank=True)

    ready = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"
