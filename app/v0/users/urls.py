from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^login', views.login),
	url(r'^register', views.register),
]