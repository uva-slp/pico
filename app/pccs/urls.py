from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^', include('users.urls', namespace='users')),
	url(r'^teams/', include('teams.urls', namespace='teams')),
	url(r'^organizations/', include('organizations.urls', namespace='organizations')),
	url(r'^c/', include('contests.urls', namespace='contests')),
	url(r'^$', views.index, name='index'),
]