from django import forms
from .models import DocFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = DocFile
        fields = ('title', 'agreement')


class VariablesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        variables = kwargs.pop('variables')
        super().__init__(*args, **kwargs)

        for i, variable in enumerate(variables):
            self.fields['custom_%s' % i] = forms.CharField(label=variable)

    def get_input_text(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)
