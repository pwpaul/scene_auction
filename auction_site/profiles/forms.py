from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
import os

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB


class ForcedPasswordChangeForm(PasswordChangeForm):
    # Could customize labels if you want
    pass


# Custom widget to rename "Clear" to "Delete"
class CustomClearableFileInput(forms.ClearableFileInput):
    clear_checkbox_label = "Delete"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name",
            "fet",
            "pronouns",
            "pic_original",
            "ref_phys",
            "ref_words",
            "ref_no_words",
        ]
        widgets = {
            "pic_original": CustomClearableFileInput,
        }

    def clean_pic_original(self):
        pic = self.cleaned_data.get("pic_original")
        if pic:
            if pic.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                    "Profile picture file size must be under 10 MB."
                )
        return pic

    def save(self, commit=True):
        instance = super().save(commit=False)

        if "pic_original" in self.changed_data:
            try:
                old_instance = Profile.objects.get(pk=instance.pk)
                if old_instance.pic_original and os.path.isfile(
                    old_instance.pic_original.path
                ):
                    os.remove(old_instance.pic_original.path)
                if old_instance.pic and os.path.isfile(old_instance.pic.path):
                    os.remove(old_instance.pic.path)
                if old_instance.pic_thumb and os.path.isfile(
                    old_instance.pic_thumb.path
                ):
                    os.remove(old_instance.pic_thumb.path)
            except Profile.DoesNotExist:
                # No old profile exists yet (creating new)
                pass

        if commit:
            instance.save()
        return instance
