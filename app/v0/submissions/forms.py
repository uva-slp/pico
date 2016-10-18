from django import forms
from .models import Submission

class UploadCodeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code_file', 'question']
        widgets = {'question': forms.HiddenInput()}
