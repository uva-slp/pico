from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^home$', views.home, name='home'),
	url(r'^diff$', views.diff, name='diff'),
	url(r'^create$', views.create, name='create'),
	url(r'^createTemplate$', views.createTemplate, name='createTemplate'),
]
