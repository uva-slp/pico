from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^', include('users.urls', namespace='users')),
	url(r'^teams/', include('teams.urls', namespace='teams')),
	url(r'^organizations/', include('organizations.urls', namespace='organizations')),
	url(r'^contests/', include('contests.urls', namespace='contests')),
	url(r'^$', views.index, name='index'),
	url(r'^home$', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

