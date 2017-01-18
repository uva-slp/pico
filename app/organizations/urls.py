from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),
	url(r'^create$', views.create, name='create'),
	url(r'^join$', views.join, name='join'),
	url(r'^leave$', views.leave, name='leave'),
	url(r'^autocomplete$', views.OrganizationAutocomplete.as_view(), name='autocomplete'),
	url(r'^autocomplete/(?P<type>\d+)$', views.OrganizationAutocomplete.as_view(), name='autocomplete'),
]
