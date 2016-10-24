from django import forms

from .models import Team

class TeamForm(forms.ModelForm):
	name = forms.CharField(required=True)

	class Meta:
		model = Team
		fields = ('name',)

class TeamJoinForm(forms.ModelForm):
	team = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label='')

	def __init__(self, request=None, *args, **kwargs):
		super(TeamJoinForm, self).__init__(*args, **kwargs)
		if request is not None:
			self.fields['team'].queryset = self.fields['team'].queryset.exclude(members=request.user)

	class Meta:
		model = Team
		fields = ('team',)

class TeamLeaveForm(forms.ModelForm):
	team = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label='')

	def __init__(self, request=None, *args, **kwargs):
		super(TeamLeaveForm, self).__init__(*args, **kwargs)
		if request is not None:
			self.fields['team'].queryset = self.fields['team'].queryset.filter(members=request.user)

	class Meta:
		model = Team
		fields = ('team',)
