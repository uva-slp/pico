from django import forms
from django.urls import reverse_lazy
from dal import autocomplete

from .models import Team

class TeamForm(forms.ModelForm):
	name = forms.CharField(required=True)

	class Meta:
		model = Team
		fields = ('name',)

class TeamJoinForm(forms.ModelForm):
	team = forms.ModelChoiceField(queryset=Team.objects.all(),
		widget=autocomplete.ModelSelect2(url=reverse_lazy('teams:autocomplete', kwargs={'type':1}))
	)

	class Meta:
		model = Team
		fields = ('team',)

class TeamLeaveForm(forms.ModelForm):
	team = forms.ModelChoiceField(queryset=Team.objects.all(),
		widget=autocomplete.ModelSelect2(url=reverse_lazy('teams:autocomplete', kwargs={'type':2}))
	)

	class Meta:
		model = Team
		fields = ('team',)
