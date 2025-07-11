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

def profile_thumb_upload_to(instance, filename):
    username_or_id = instance.user.username or f"user_{instance.user.id}"
    return f"profile_pics/{username_or_id}/thumb/{username_or_id}_thumb.jpg"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # general info
    name = models.CharField(max_length=100)
    fet = models.CharField("fet name", max_length=100, blank=True)
    pronouns = models.CharField(max_length=50, blank=True)

    # updated image system
    pic_original = models.ImageField(upload_to=profile_original_upload_to, blank=True, null=True)
    pic = models.ImageField(upload_to=profile_resized_upload_to, blank=True, null=True)
    pic_thumb = models.ImageField(upload_to=profile_thumb_upload_to, blank=True, null=True)

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
            # If clearing the original image on form, also remove the files
            if self.pk:
                old = Profile.objects.filter(pk=self.pk).first()
                if old and old.pic_original and not self.pic_original:
                    old.delete_images()

            super().save(*args, **kwargs)

            # If there is a new pic_original, generate resized & thumb
            if self.pic_original:
                self._generate_image_version(self.pic_original, (800, 800), 'resized')
                self._generate_image_version(self.pic_original, (150, 150), 'thumb')

    def _generate_image_version(self, source_field, size, version_name):
        img = Image.open(source_field.path)
        img = img.convert("RGB")
        img.thumbnail(size)

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)

        new_filename = f"{self.user.username or f'user_{self.user.id}'}_{version_name}.jpg"
        if version_name == "resized":
            self.pic.save(new_filename, ContentFile(buffer.read()), save=False)
        elif version_name == "thumb":
            self.pic_thumb.save(new_filename, ContentFile(buffer.read()), save=False)

        buffer.close()
        super().save(update_fields=["pic", "pic_thumb"])

    def delete_images(self):
        """Delete all associated image files from storage."""
        storage = self.pic_original.storage if self.pic_original else None
        if storage:
            for image_field in [self.pic_original, self.pic, self.pic_thumb]:
                if image_field:
                    try:
                        storage.delete(image_field.name)
                    except Exception:
                        pass
        # Also clear from DB
        self.pic_original = None
        self.pic = None
        self.pic_thumb = None
        super().save(update_fields=["pic_original", "pic", "pic_thumb"])
    
    def get_avatar_url(self):
        """
        Returns the URL to the thumbnail if it exists,
        otherwise returns a default avatar.
        """
        if self.pic_thumb and self.pic_thumb.url:
            return self.pic_thumb.url
        return '/static/img/default_avatar.jpg'  # adjust to wherever your fallback image is