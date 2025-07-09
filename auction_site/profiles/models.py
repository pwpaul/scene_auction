from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


class User(AbstractUser):
    must_change_password = models.BooleanField(default=True)

    def __str__(self):
        return self.username


def profile_original_upload_to(instance, filename):
    return f"profile_pics/{instance.user.username}/original/{filename}"


def profile_resized_upload_to(instance, filename):
    return f"profile_pics/{instance.user.username}/resized/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # general info
    name = models.CharField(max_length=100)
    fet = models.CharField("fet name", max_length=100, blank=True)
    pronouns = models.CharField(max_length=50, blank=True)

    # updated image system
    pic_original = models.ImageField(
        upload_to=profile_original_upload_to, blank=True, null=True
    )
    pic = models.ImageField(upload_to=profile_resized_upload_to, blank=True, null=True)

    # auctioneer references
    ref_pronouns = models.CharField("auction pronouns", max_length=50, blank=True)
    ref_name = models.CharField("auction name", max_length=100, blank=True)
    ref_phys = models.BooleanField("ok to mention physical?", default=False)
    ref_words = models.TextField("preferred words", blank=True)
    ref_no_words = models.TextField("words to avoid", blank=True)

    ready = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pic_original:
            img = Image.open(self.pic_original.path)
            img = img.convert("RGB")
            img.thumbnail((400, 400))
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            buffer.seek(0)
            basename, ext = os.path.splitext(os.path.basename(self.pic_original.name))
            new_filename = f"{basename}_resized.jpg"
            self.pic.save(new_filename, ContentFile(buffer.read()), save=False)
            buffer.close()
            super().save(update_fields=["pic"])
