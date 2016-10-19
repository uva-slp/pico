from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^u/', include('users.urls', namespace='users')),
	url(r'^c/', include('contests.urls', namespace='contests')),
	url(r'^$', views.index, name='index'),
]