from django.forms import ModelForm

from .models import File


class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['title', 'description',
                  'tags', 'owner']

    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
