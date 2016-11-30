from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^home$', views.home, name='home'),
	url(r'^diff/(?P<question_id>[0-9]+)/$', views.diff, name='diff'),
    url(r'^create$', views.create, name='create'),
	url(r'^scoreboard/$', views.scoreboard, name='scoreboard'),
	url(r'^contest/(?P<contest_id>\d+)/$', views.displayContest, name='contest'),
	url(r'^contest/(?P<contest_id>\d+)/scoreboard$', views.scoreboard, name='scoreboard'),
	url(r'^contest/(?P<contest_id>\d+)/judge$', views.displayAllSubmissions, name='contest_judge_submissions'),
	url(r'^contest/(?P<contest_id>\d+)/judge/(?P<run_id>\d+)/$', views.displayJudge, name='contest_judge'),
	url(r'^contest/(?P<contest_id>\d+)/(?P<team_id>\d+)/submissions$',
		views.displayMySubmissions, name='contest_submissions'),
    url(r'^submission$', views.choose_problem, name='choose_problem'),
    url(r'^submission/upload/(?P<problem_id>[0-9]+)/$', views.upload_code, name='upload_code'),
]
