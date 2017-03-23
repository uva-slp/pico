
from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^create$', views.create, name='create'),
	url(r'^edit/(?P<contest_id>\d+)/$', views.edit, name='edit_contest'),
	url(r'^create_template$', views.create_template, name='create_template'),
	url(r'^scoreboard/$', views.scoreboard, name='scoreboard'),
	url(r'^contest/(?P<contest_id>\d+)/$', views.displayContest, name='contest'),
	url(r'^contest/(?P<contest_id>\d+)/problemDescription$', views.displayProblemDescription, name='problem_description'),
	url(r'^contest/(?P<contest_id>\d+)/scoreboard$', views.scoreboard, name='scoreboard'),
	url(r'^contest/(?P<contest_id>\d+)/judge$', views.displayAllSubmissions, name='contest_judge_submissions'),
	url(r'^contest/(?P<contest_id>\d+)/judge/(?P<run_id>\d+)/$', views.displayJudge, name='contest_judge'),
	url(r'^contest/(?P<contest_id>\d+)/(?P<team_id>\d+)/submissions$',
		views.displayMySubmissions, name='contest_submissions'),
	url(r'^api/get_notification/$', views.show_notification, name='show_notification'),
	url(r'^api/close_notification/$', views.close_notification, name='close_notification'),
	url(r'^api/refresh_submission/$', views.refresh_submission, name='refresh_submission'),
	url(r'^api/refresh_scoreboard/$', views.refresh_scoreboard, name='refresh_scoreboard'),
]
