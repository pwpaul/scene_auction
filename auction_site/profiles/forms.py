from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile


class ForcedPasswordChangeForm(PasswordChangeForm):
    # Could customize labels if you want
    pass


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name",
            "fet",
            "pronouns",
            "pic_original",
            "ref_pronouns",
            "ref_name",
            "ref_phys",
            "ref_words",
            "ref_no_words",
        ]
