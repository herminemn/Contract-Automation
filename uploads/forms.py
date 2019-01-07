from django import forms
from .models import DocFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = DocFile
        fields = ('title', 'agreement')


class EditFileForm(forms.Form):
    text = forms.CharField(label='', required=False)
