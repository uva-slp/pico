from django.forms import Form, ModelForm
from .models import User, Contest
from django import forms

class CreateContestForm(ModelForm):
    class Meta:
        model = Contest
        fields = ['title']

