from django.conf.urls import include, url
from django.contrib import admin

from pccs.views import *
from submissions import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^users/', include('users.urls', namespace='users')),
	url(r'^contests/', include('contests.urls', namespace='contests')),
        url(r'^submissions/', include('submissions.urls')), 
	url(r'^$', views.index, name='index'),
]
