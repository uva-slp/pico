from django.forms import Form, ModelForm
from .models import Contest, Submission, Problem, ContestTemplate
from users.models import User
from django import forms
#from bootstrap3_datetime.widgets import DateTimePicker
from datetime import datetime


'''
class CreateContestForm(ModelForm):
    class Meta:
        model = Contest
        fields = ['title']
'''

LANGAUGES = (
    ('Python','Python'),
    ('Java', 'Java') ,
    ('C++', 'C++'))
CONTEST_LENGTH = (
    ('1', '1 Hour'),
    ('2','2 Hours'),
    ('5','5 Hours'),
    ('10', '10 Hours'),
    ('24','24 Hours'))
AUTOJUDGE = (
    ('1','Enabled'),
    ('0','Disabled'))

LANG_LIST = (
    ('1', 'Java'),
    ('2', 'C++'),
    ('3', 'Python')
)

REVIEW_LIST = (
    ('1', 'Manual review incorrect submissions'),
    ('2', 'Manual review all submissions')
)


class CreateContestForm(ModelForm):
    title = forms.CharField(required=True)
    languages = forms.CharField(
        required=True,
        widget=forms.CheckboxSelectMultiple(choices=LANG_LIST)
    )
    contest_length = forms.CharField(
        required=True, label="Contest Length (hours & minutes)", initial='02:00',
        #widget=DateTimePicker()
    )
    time_penalty = forms.CharField(
        required=True, label="Time Penalty (minutes)", initial=20,
        #widget=DateTimePicker()
    )
    autojudge_enabled = forms.BooleanField(required=False)
    autojudge_review = forms.CharField(
        required=False, label="Judge Review Option",
        widget=forms.Select(choices=REVIEW_LIST, attrs={'disabled':'disabled'})
    )
    problem_description = forms.FileField(required=True, label="Problem Descriptions (.pdf)")
    contest_admins = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
    # contest_admins = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':30}))
    contest_participants = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':30}))

    def clean(self):
        upload_to = 'uploads/'
        if not 'problem_description' in self.cleaned_data:
            return self.cleaned_data
        upload_to += self.cleaned_data['problem_description'].name

    def clean_contest_length(self):
        data = self.cleaned_data['contest_length']
        separator = data.find(":")
        cl_hours = int(data[0:separator])
        cl_minutes = int(data[separator + 1:])
        time = datetime.now()
        data = time.replace(hour=cl_hours, minute=cl_minutes)
        return data

    def clean_time_penalty(self):
        data = self.cleaned_data['time_penalty']
        time = datetime.now()
        data = time.replace(minute=int(data))
        return data

    class Meta:
        model = Contest
        fields = (
            'title', 'languages', 'contest_length', 'time_penalty',
            'autojudge_enabled', 'autojudge_review', 'problem_description',
            'contest_admins', 'contest_participants')


class CreateProblem(ModelForm):
    solution = forms.FileField(required=True, label='Solution (.txt)')
    program_input = forms.FileField(required=False, label= 'Program Input (.txt)')
    input_description = forms.CharField(required=False, label='Description of Input',
        widget=forms.Textarea(attrs={'rows':4, 'cols':30}))
    output_description = forms.CharField(required=False, label='Description of Output',
        widget=forms.Textarea(attrs={'rows':4, 'cols':30}))
    sample_input = forms.FileField(required=False, label='Sample Input (.txt)')
    sample_output = forms.FileField(required=False, label='Sample Output (.txt)')

    def clean(self):
        upload_to = 'uploads/'
        if not 'solution' in self.cleaned_data:
            return self.cleaned_data
        upload_to += self.cleaned_data['solution'].name

    class Meta:
        model = Problem
        fields = (
            'solution', 'program_input', 'input_description', 'output_description', 'sample_input',
            'sample_output')


class CreateContestTemplateForm(ModelForm):
    title = forms.CharField(required=True)
    languages = forms.CharField(
        required=True,
        widget=forms.CheckboxSelectMultiple(choices=LANG_LIST)
    )
    contest_length = forms.CharField(
        required=True, label="Contest Length (hours & minutes)", initial='02:00',
        # widget=DateTimePicker()
    )
    time_penalty = forms.CharField(
        required=True, label="Time Penalty (minutes)", initial=20,
        # widget=DateTimePicker()
    )
    autojudge_enabled = forms.BooleanField(required=False)
    autojudge_review = forms.CharField(
        required=False, label="Judge Review Option",
        widget=forms.Select(choices=REVIEW_LIST, attrs={'disabled':'disabled'})
    )
    # contest_admins = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':30}))
    contest_admins = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
    contest_participants = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':30}))

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = ContestTemplate
        fields = (
            'title', 'languages', 'contest_length', 'time_penalty',
            'autojudge_enabled', 'autojudge_review',
            'contest_admins', 'contest_participants')


class UploadCodeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code_file', 'problem']
        widgets = {'problem': forms.HiddenInput()}


class ReturnJudgeResultForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['result', 'state']
        widgets = {'state': forms.HiddenInput()}

    def clean(self):
        cleaned_data = super(ReturnJudgeResultForm, self).clean()
        result = cleaned_data.get('result')
        if result:
            if result == 'YES':
                cleaned_data['state'] = 'YES'
            else:
                cleaned_data['state'] = 'NO'
        else:
            cleaned_data['state'] = 'NEW'
        return cleaned_data

