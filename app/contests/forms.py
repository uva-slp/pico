from django.forms import Form, ModelForm
from .models import Contest, Submission, Problem
from django import forms
# from bootstrap3_datetime.widgets import DateTimePicker


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
		# widget=DateTimePicker()
	)
	time_penalty = forms.CharField(
		required=True, label="Time Penalty (minutes)", initial=20,
		# widget=DateTimePicker()
	)
	autojudge_enabled = forms.BooleanField(required=False)
	autojudge_review = forms.CharField(
		required=False, label="Judge Review Option",
		widget=forms.Select(choices=REVIEW_LIST)
	)
	problem_description = forms.FileField(required=True, label="Problem Descriptions (.pdf)")
	contest_admins = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':30}))
	contest_participants = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':30}))

	def clean(self):
		upload_to = 'uploads/'
		if not 'problem_description' in self.cleaned_data:
			return self.cleaned_data
		upload_to += self.cleaned_data['problem_description'].name

	class Meta:
		model = Contest
		fields = (
			'title', 'languages', 'contest_length', 'time_penalty',
			'autojudge_enabled', 'autojudge_review', 'problem_description',
			'contest_admins', 'contest_participants')


class CreateProblem(ModelForm):
	solution = forms.FileField(required=True)
	input_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':30}))
	output_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':30}))
	sample_input = forms.FileField(required=False)
	sample_output = forms.FileField(required=False)

	def clean(self):
		upload_to = 'uploads/'
		if not 'solution' in self.cleaned_data:
			return self.cleaned_data
		upload_to += self.cleaned_data['solution'].name

	class Meta:
		model = Problem
		fields = (
			'solution', 'input_description', 'output_description', 'sample_input',
			'sample_output')


'''
class CreateContestForm(forms.Form):
    title = forms.CharField(label='Title', max_length=32)
    languages = forms.CharField(label='Languages', widget=forms.CheckboxSelectMultiple)
    length = forms.ChoiceField(label='Length', choices=CONTEST_LENGTH)
    autojudge = forms.ChoiceField(label='Autojudge', choices=AUTOJUDGE)
    ##file stuff - need group input on how this should be laid out
    ##problems = forms.FileField()
    ##answers = forms.FileField()
'''


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

