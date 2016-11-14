from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^home$', views.home, name='home'),
	url(r'^diff/(?P<question_id>[0-9]+)/$', views.diff, name='diff'),
    url(r'^create$', views.create, name='create'),
	url(r'^scoreboard$', views.scoreboard, name='scoreboard'),
	url(r'^createTemplate$', views.createTemplate, name='createTemplate'),
	url(r'^contest/(?P<contest_id>\d+)/$', views.displayContest, name='contest'),
    url(r'^submission$', views.choose_question, name='choose_question'),
    url(r'^submission/upload/(?P<question_id>[0-9]+)/$', views.upload_code, name='upload_code'),
]
