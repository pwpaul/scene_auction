from django import forms
from .models import Scene
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class SceneForm(forms.ModelForm):
    class Meta:
        model = Scene
        fields = ["role", "eligible_bidders", "other_bidders", "title", "short", "long"]
        widgets = {"eligible_bidders": forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Scene Details",
                "role",
                "eligible_bidders",
                "other_bidders",
                "title",
                "short",
                "long",
            ),
            ButtonHolder(Submit("submit", "Save Scene", css_class="btn btn-primary")),
        )
