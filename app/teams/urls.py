from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<team_id>[0-9]*)/$', views.index, name='index'),
	url(r'^create$', views.create, name='create'),
	url(r'^join$', views.join, name='join'),
    url(r'^invite$', views.invite, name='invite'),
    url(r'^join-request/(?P<action>(approve|reject))$', views.join_request, name='join-request'),
    url(r'^invite/cancel$', views.cancel_invite, name='cancel-invite'),
	url(r'^leave$', views.leave, name='leave'),
    url(r'^get$', views.get, name='get'),
	url(r'^autocomplete$', views.TeamAutocomplete.as_view(), name='autocomplete'),
]