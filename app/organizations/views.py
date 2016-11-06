from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from dal import autocomplete

from .models import Organization
from .forms import OrganizationForm, OrganizationJoinForm, OrganizationLeaveForm

@login_required
def create(request):
	if request.method == 'POST':
		organization_form = OrganizationForm(data=request.POST)

		if organization_form.is_valid():
			organization = organization_form.save()
			organization.members.add(request.user)
	
	return redirect(reverse('contests:home'))

@login_required
def join(request):
	if request.method == 'POST':
		organization_join_form = OrganizationJoinForm(data=request.POST)

		if organization_join_form.is_valid():
			organization = organization_join_form.cleaned_data['organization']
			request.user.organization_set.add(organization)

	return redirect(reverse('contests:home'))

@login_required
def leave(request):
	if request.method == 'POST':
		organization_leave_form = OrganizationLeaveForm(data=request.POST)

		if organization_leave_form.is_valid():
			organization = organization_leave_form.cleaned_data['organization']
			request.user.organization_set.remove(organization)
			if organization.members.count() == 0:
				organization.delete()

	return redirect(reverse('contests:home'))

class OrganizationAutocomplete(autocomplete.Select2QuerySetView):

	def get_queryset(self):		
		if not self.request.user.is_authenticated():
			return Organization.objects.none()
		
		qs = Organization.objects.all()
		if self.q:
			qs = qs.filter(name__istartswith=self.q)


		queryType = int(self.kwargs.get('type', 0))
		if queryType == 0:
			return qs
		if queryType == 1: # join
			return qs.exclude(members=self.request.user)
		if queryType == 2: # leave
			return qs.filter(members=self.request.user)
		
		return qs
