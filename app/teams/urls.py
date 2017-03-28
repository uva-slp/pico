from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<team_id>[0-9]*)/$', views.index, name='index'),
	url(r'^create$', views.create, name='create'),
	url(r'^join$', views.join, name='join'),
    url(r'^invite/(?P<action>(send|accept|decline|cancel))$', views.invite, name='invite'),
    url(r'^join-request/(?P<action>(accept|decline|cancel))$', views.join_request, name='join-request'),
	url(r'^leave$', views.leave, name='leave'),
    url(r'^public$', views.is_public, name='public'),
    url(r'^get$', views.get, name='get'),
	url(r'^autocomplete$', views.TeamAutocomplete.as_view(), name='autocomplete'),
]