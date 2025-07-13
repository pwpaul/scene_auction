import os
from io import BytesIO
from PIL import Image

from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractUser


# Your custom User model
class User(AbstractUser):
    must_change_password = models.BooleanField(default=True)

    def __str__(self):
        return self.username


# Helpers to create organized file paths
def user_upload_path(instance, filename, subfolder):
    username_or_id = instance.user.username or f"user_{instance.user.id}"
    return f"profile_pics/{username_or_id}/{subfolder}/{filename}"


def profile_original_upload_to(instance, filename):
    username_or_id = instance.user.username or f"user_{instance.user.id}"
    return f"profile_pics/{username_or_id}/original/{username_or_id}_original.jpg"


def profile_resized_upload_to(instance, filename):
    username_or_id = instance.user.username or f"user_{instance.user.id}"
    return f"profile_pics/{username_or_id}/resized/{username_or_id}_resized.jpg"


def profile_thumb_upload_to(instance, filename):
    username_or_id = instance.user.username or f"user_{instance.user.id}"
    return f"profile_pics/{username_or_id}/thumb/{username_or_id}_thumb.jpg"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # General info
    name = models.CharField(max_length=100)
    fet = models.CharField("fet name", max_length=100, blank=True)
    pronouns = models.CharField(max_length=50, blank=True)

    # Image fields
    pic_original = models.ImageField(
        upload_to=profile_original_upload_to, blank=True, null=True
    )
    pic = models.ImageField(upload_to=profile_resized_upload_to, blank=True, null=True)
    pic_thumb = models.ImageField(
        upload_to=profile_thumb_upload_to, blank=True, null=True
    )

    # Auctioneer references
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
            # Always create resized & thumb after saving original
            self._generate_image_version(self.pic_original, (800, 800), "resized")
            self._generate_image_version(self.pic_original, (150, 150), "thumb")

    def _generate_image_version(self, source_field, size, version_name):
        img = Image.open(source_field.path)
        img = img.convert("RGB")
        img.thumbnail(size)

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)

        new_filename = (
            f"{self.user.username or f'user_{self.user.id}'}_{version_name}.jpg"
        )

        if version_name == "resized":
            self.pic.save(new_filename, ContentFile(buffer.read()), save=False)
        elif version_name == "thumb":
            self.pic_thumb.save(new_filename, ContentFile(buffer.read()), save=False)

        buffer.close()
        super().save(update_fields=["pic", "pic_thumb"])
