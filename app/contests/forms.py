from django.forms import Form, ModelForm
from .models import Contest, ContestTemplate
from django import forms
# from bootstrap3_datetime.widgets import DateTimePicker


class CreateContestForm(ModelForm):
	class Meta:
		model = Contest
		fields = ['title']

LANG_LIST = (
	('1', 'Java'),
	('2', 'C++'),
	('3', 'Python')
)

REVIEW_LIST = (
	('1', 'Manual review incorrect submissions'),
	('2', 'Manual review all submissions')
)


class CreateContestTemplate(ModelForm):
	title = forms.CharField(required=True)
	languages = forms.CharField(required=True, widget=forms.CheckboxSelectMultiple(choices=LANG_LIST))
	contest_length = forms.CharField(
										required=True,
										label="Contest Length (hours & minutes)",
										initial='02:00',
										# widget=DateTimePicker()
									)
	time_penalty = forms.CharField(
										required=True,
										label="Time Penalty (minutes)",
										initial=20,
										# widget=DateTimePicker()
									)
	autojudge_enabled = forms.BooleanField(required=False)
	autojudge_review = forms.CharField(
											required=False,
											label="Judge Review Option",
											widget=forms.Select(choices=REVIEW_LIST)
										)
	# problem_descriptions = forms.CharField(required=True)
	# solutions = forms.CharField(required=True)
	contest_admins = forms.CharField(required=False, widget=forms.Textarea)
	contest_participants = forms.CharField(required=False, widget=forms.Textarea)

	class Meta:
		model = ContestTemplate
		fields = ('title', 'languages', 'contest_length', 'time_penalty', 'autojudge_enabled',
					'autojudge_review', 'contest_admins', 'contest_participants')


class CreateQuestionAnswer(Form):
	problem_desc = forms.FileField(required=True)
	solution = forms.FileField(required=True)



