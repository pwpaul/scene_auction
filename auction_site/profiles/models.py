import os
from io import BytesIO
from PIL import Image

from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver


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
    name = models.CharField(max_length=100, help_text="This is your diplay name on this site.  It is not your login name.")
    fet = models.CharField("fet name", max_length=100, blank=True, help_text="This is your Fetlife Username, if you have one.")
    pronouns = models.CharField(max_length=50, blank=True)

    # Image fields
    pic_original = models.ImageField("Profile Picture",
        upload_to=profile_original_upload_to, blank=True, null=True,
        help_text="This will be used during the auction")
    pic = models.ImageField(upload_to=profile_resized_upload_to, blank=True, null=True)
    pic_thumb = models.ImageField(
        upload_to=profile_thumb_upload_to, blank=True, null=True
    )

    # Auctioneer references
    ref_phys = models.BooleanField("ok to mention physical?", default=False)
    ref_words = models.TextField("preferred words", blank=True, help_text="Words you might like used to describe you in an auction")
    ref_no_words = models.TextField("words to avoid", blank=True, help_text="Words you prefer not to be used in an auction")

    ready = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_avatar_url(self):
        try:
            if self.pic_thumb and self.pic_thumb.name:
                return self.pic_thumb.url
            elif self.pic and self.pic.name:
                return self.pic.url
            elif self.pic_original and self.pic_original.name:
                return self.pic_original.url
        except ValueError:
            # happens if file is missing on disk
            pass
        return "/static/img/default_profile.png"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.pic_original:
            # Always create resized & thumb after saving original
            self._generate_image_version(self.pic_original, (800, 800), "resized")
            self._generate_image_version(self.pic_original, (400, 400), "thumb")

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

    def delete(self, *args, **kwargs):
        # Manual delete safeguard
        if self.pic_thumb and os.path.isfile(self.pic_thumb.path):
            os.remove(self.pic_thumb.path)
        if self.pic and os.path.isfile(self.pic.path):
            os.remove(self.pic.path)
        if self.pic_original and os.path.isfile(self.pic_original.path):
            os.remove(self.pic_original.path)
        super().delete(*args, **kwargs)


# Signal to always clean up files on delete
@receiver(pre_delete, sender=Profile)
def delete_profile_images(sender, instance, **kwargs):
    if instance.pic_thumb and os.path.isfile(instance.pic_thumb.path):
        os.remove(instance.pic_thumb.path)
    if instance.pic and os.path.isfile(instance.pic.path):
        os.remove(instance.pic.path)
    if instance.pic_original and os.path.isfile(instance.pic_original.path):
        os.remove(instance.pic_original.path)
