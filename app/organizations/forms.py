from django import forms
from django.urls import reverse_lazy
from dal import autocomplete

from .models import Organization

class OrganizationForm(forms.ModelForm):
	name = forms.CharField(required=True)

	class Meta:
		model = Organization
		fields = ('name',)

class OrganizationJoinForm(forms.ModelForm):
	organization = forms.ModelChoiceField(queryset=Organization.objects.all(),
		widget=autocomplete.ModelSelect2(url=reverse_lazy('organizations:autocomplete', kwargs={'type':1}))
	)

	class Meta:
		model = Organization
		fields = ('organization',)

class OrganizationLeaveForm(forms.ModelForm):
	organization = forms.ModelChoiceField(queryset=Organization.objects.all(),
		widget=autocomplete.ModelSelect2(url=reverse_lazy('organizations:autocomplete', kwargs={'type':2}))
	)

	class Meta:
		model = Organization
		fields = ('organization',)
