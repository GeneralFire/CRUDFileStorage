from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = []

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
