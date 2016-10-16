from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', views.index, name='home'),
	url(r'^users/', include('users.urls', namespace="users"), name='users'),
]