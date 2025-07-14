from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile


MAX_UPLOAD_SIZE = 10 * 1024 * 1024 #10MB
class ForcedPasswordChangeForm(PasswordChangeForm):
    # Could customize labels if you want
    pass

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name', 'fet', 'pronouns', 'pic_original',
            'ref_pronouns', 'ref_name', 'ref_phys', 'ref_words', 'ref_no_words'
        ]


class ForcedPasswordChangeForm(PasswordChangeForm):
    pass
    def clean_pic_original(self):
        pic = self.cleaned_data.get('pic_original')
        if pic:
            if pic.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Profile picture file size must be under 10 MB.")
        return pic
