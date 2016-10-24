from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^create-team$', views.create_team, name='create-team'),
	url(r'^join-team$', views.join_team, name='join-team'),
	url(r'^leave-team$', views.leave_team, name='leave-team'),
]