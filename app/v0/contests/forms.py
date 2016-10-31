from django.forms import Form, ModelForm
from .models import User, Contest
from django import forms

LANGAUGES = (('Python','Python'), ('Java', 'Java') , ('C++', 'C++'))
CONTEST_LENGTH = (('1', '1 Hour'), ('2','2 Hours'), ('5','5 Hours'), ('10', '10 Hours'), ('24','24 Hours'))
AUTOJUDGE = (('1','Enabled'), ('0','Disabled'))

# class CreateContestForm(ModelForm):
#     class Meta:
#         model = Contest
#         fields = ['title']

class CreateContestForm(forms.Form):
    title = forms.CharField(label='Title', max_length=32)
    languages = forms.CharField(label='Languages', widget=forms.CheckboxSelectMultiple)
    length = forms.CharField(label='Length', choices=CONTEST_LENGTH)
    autojudge = forms.CharField(label='Autojudge', choices=AUTOJUDGE)
    ##file stuff - need group input on how this should be laid out
    ##problems = forms.FileField()
    ##answers = forms.FileField()
