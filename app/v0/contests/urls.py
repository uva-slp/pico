from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^home$', views.home, name='home'),
	url(r'^diff$', views.diff, name='diff'),
]
