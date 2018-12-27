from django import forms
from .models import DocFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = DocFile
        fields = ('title', 'agreement')
