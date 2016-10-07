from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('main.urls', namespace='main')),
    url(r'^admin/', admin.site.urls),
]